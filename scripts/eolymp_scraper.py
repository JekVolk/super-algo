#!/usr/bin/env python3
"""
Eolymp Space & UCPC Automated Problem Scraper.
Fetches problem statements, constraints, sample tests, and assets
from Eolymp Space (e.g. https://ucpc.eolymp.space/uk/compete/ucpc2026practice/problem/1).

Supports:
1. Session Cookie authentication (for authorized contests like UCPC)
2. Next.js RSC payload & inline JSON parsing
3. Extraction of base64 encoded input/output test cases
4. Local HTML file ingestion (drag & drop or saved page)
5. Export to tasks/<contest>/<problem>/ directory with C++ and Python templates
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

CPP_TEMPLATE = """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void solve() {
    // Введіть розв'язок задачі
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t = 1;
    // cin >> t; // розкоментуйте при multi-test
    while (t--) {
        solve();
    }
    return 0;
}
"""

PYTHON_TEMPLATE = """import sys

def solve():
    # Введіть розв'язок задачі
    pass

def main():
    solve()

if __name__ == "__main__":
    main()
"""

TEST_RUNNER_TEMPLATE = """import subprocess
import sys
from pathlib import Path

def run_tests():
    folder = Path(__file__).parent
    inputs = sorted(folder.glob("input*.txt"))
    if not inputs:
        print("Вхідні тести input*.txt не знайдено!")
        return

    print("=== Запуск тестів ===")
    all_passed = True
    for inp in inputs:
        idx = inp.stem.replace("input", "")
        out = folder / f"output{idx}.txt"
        if not out.exists():
            continue

        with open(inp, "r", encoding="utf-8") as f:
            in_data = f.read()
        with open(out, "r", encoding="utf-8") as f:
            expected = f.read().strip()

        res = subprocess.run([sys.executable, str(folder / "solution.py")], input=in_data, text=True, capture_output=True)
        actual = res.stdout.strip()

        if actual == expected:
            print(f"✅ Тест #{idx}: PASSED")
        else:
            all_passed = False
            print(f"❌ Тест #{idx}: FAILED")
            print(f"   Очікувалось:\\n{expected}")
            print(f"   Отримано:\\n{actual}")

    if all_passed:
        print("\\n🎉 Всі приклади пройшли успішно!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
"""

def sanitize_slug(text: str) -> str:
    cleaned = re.sub(r'[\\/*?:"<>| ]', '_', text.strip())
    return re.sub(r'_+', '_', cleaned)

class EolympScraper:
    def __init__(self, cookie: str = ""):
        self.cookie = cookie

    def fetch_url(self, url: str) -> str:
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        if self.cookie:
            headers["Cookie"] = self.cookie

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")

    def parse_html_content(self, html: str, source_url: str = "") -> dict:
        # Check if redirected to login
        if ("/signin" in html or "SigninForm" in html) and ("Standard" not in html and "problem" not in html):
            if not self.cookie:
                print("\n⚠️ УВАГА: Контест UCPC на Eolymp вимагає авторизації!")
                print("Для отримання доступу передайте кукі вашої сесії браузера:")
                print("python scripts/eolymp_scraper.py <url> --cookie \"eolymp_session=...\"")
                print("Або збережіть сторінку в html і вкажіть шлях до локального файлу:")
                print("python scripts/eolymp_scraper.py path/to/page.html")

        # 1. Пошук Next.js ContestStudio даних задачі
        title = "Problem"
        time_limit = "1.0s"
        memory_limit = "256 MB"
        statement_text = ""
        samples = []

        # Спроба витягти заголовок з title
        title_match = re.search(r'<title>(.*?)</title>', html)
        if title_match:
            title = title_match.group(1).replace("Ukrainian Collegiate Programming Contest", "").strip(" -|")

        # Спроба витягти специфічну назву (наприклад Standard1: A+B)
        spec_title = re.search(r'"title":"((?:Standard|Interactive|MultipleRun|OutputOnly|FunctionNoMain)[^"]+)"', html)
        if spec_title:
            title = spec_title.group(1)

        # Спроба витягти ліміти
        tl_match = re.search(r'"time-limit-max":"(\d+)"', html)
        if tl_match:
            time_limit = f"{int(tl_match.group(1)) / 1000.0:.1f}s"
        else:
            tl_text = re.search(r'(\d+(?:\.\d+)?)\s*(?:сек|sec|s)', html, re.IGNORECASE)
            if tl_text:
                time_limit = tl_text.group(0)

        ml_match = re.search(r'"memory-limit-max":"(\d+)"', html)
        if ml_match:
            memory_limit = f"{int(ml_match.group(1)) // (1024 * 1024)} MB"
        else:
            ml_text = re.search(r'(\d+)\s*(?:МБ|MB|MiB)', html, re.IGNORECASE)
            if ml_text:
                memory_limit = ml_text.group(0)

        # Спроба витягти base64 зразки тестів
        # Приклад: {"type":"problem-example-hint","attr":{"index":"1","input-ref":"data:text/plain;base64,MiAzCg==","output-ref":"data:text/plain;base64,NQo="}}
        b64_matches = re.findall(r'input-ref":"data:text/plain;base64,([^"]+)".*?output-ref":"data:text/plain;base64,([^"]+)"', html)
        for inp_b64, out_b64 in b64_matches:
            try:
                inp = base64.b64decode(inp_b64).decode("utf-8")
                out = base64.b64decode(out_b64).decode("utf-8")
                samples.append({"input": inp.strip(), "output": out.strip()})
            except Exception:
                pass

        # Якщо base64 немає, шукаємо в pre тегах
        if not samples:
            pre_blocks = re.findall(r'<pre[^>]*>(.*?)</pre>', html, re.DOTALL)
            if len(pre_blocks) >= 2:
                for i in range(0, len(pre_blocks) - 1, 2):
                    inp = re.sub(r'<[^>]+>', '', pre_blocks[i]).strip()
                    out = re.sub(r'<[^>]+>', '', pre_blocks[i+1]).strip()
                    if inp and out:
                        samples.append({"input": inp, "output": out})

        return {
            "title": title,
            "url": source_url,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "samples": samples
        }

    def save_problem(self, prob_data: dict, contest_name: str = "ucpc2026practice"):
        title_slug = sanitize_slug(prob_data["title"])
        folder = Path("tasks") / contest_name / title_slug
        folder.mkdir(parents=True, exist_ok=True)

        # Save metadata
        with open(folder / "problem.json", "w", encoding="utf-8") as f:
            json.dump(prob_data, f, indent=2, ensure_ascii=False)

        # Save sample tests
        samples = prob_data.get("samples", [])
        for idx, s in enumerate(samples, 1):
            with open(folder / f"input{idx}.txt", "w", encoding="utf-8") as f:
                f.write(s["input"] + "\n")
            with open(folder / f"output{idx}.txt", "w", encoding="utf-8") as f:
                f.write(s["output"] + "\n")

        # Create boilerplate files if missing
        if not (folder / "solution.cpp").exists():
            with open(folder / "solution.cpp", "w", encoding="utf-8") as f:
                f.write(CPP_TEMPLATE)

        if not (folder / "solution.py").exists():
            with open(folder / "solution.py", "w", encoding="utf-8") as f:
                f.write(PYTHON_TEMPLATE)

        if not (folder / "test_runner.py").exists():
            with open(folder / "test_runner.py", "w", encoding="utf-8") as f:
                f.write(TEST_RUNNER_TEMPLATE)

        # Create README template
        if not (folder / "README.md").exists():
            with open(folder / "README.md", "w", encoding="utf-8") as f:
                f.write(f"# {prob_data['title']}\n\n")
                f.write(f"- **URL:** [{prob_data['url']}]({prob_data['url']})\n")
                f.write(f"- **Ліміт часу:** {prob_data['time_limit']}\n")
                f.write(f"- **Ліміт пам'яті:** {prob_data['memory_limit']}\n")
                f.write(f"- **Зразків тестів:** {len(samples)}\n\n")
                f.write("## ⚡ 8-Кроковий Розбір (Sense-Making to Verification)\n")
                f.write("1. **Вдупляння (Sense-Making):** ...\n")
                f.write("2. **Ручні крайові тести:** ...\n")
                f.write("3. **Аналіз лімітів і бюджет часу:** ...\n")
                f.write("4. **Вибір алгоритму з Mind Map:** ...\n")
                f.write("5. **Доведення та Інваріант:** ...\n")
                f.write("6. **Двомовний код (C++20 та Python 3.12):** ...\n")
                f.write("7. **Аудит граблів та людських помилок:** ...\n")
                f.write("8. **Стрес-тест та командна стратегія:** ...\n")

        print(f"\n✅ Задача збережена у папку: {folder}")
        print(f"  Збережено тестів: {len(samples)}")
        print(f"  Згенеровано шаблони: solution.cpp, solution.py, test_runner.py, README.md")

def main():
    parser = argparse.ArgumentParser(description="Eolymp / UCPC Automated Problem Scraper & Extractor")
    parser.add_argument("source", nargs="?", default="", help="URL задачі на Eolymp АБО шлях до локального .html файлу")
    parser.add_argument("--cookie", default="", help="Cookie авторизації з браузера")
    parser.add_argument("--contest", default="ucpc2026practice", help="Назва турніру для папки")
    args = parser.parse_args()

    scraper = EolympScraper(cookie=args.cookie)

    if not args.source:
        print("Використання:")
        print("  1. Через URL:  python scripts/eolymp_scraper.py https://ucpc.eolymp.space/... --cookie \"...\"")
        print("  2. Через файл: python scripts/eolymp_scraper.py page.html --contest ucpc2026_stage1")
        return

    # Перевірка чи source є локальним файлом
    path = Path(args.source)
    if path.exists() and path.is_file():
        print(f"[*] Зчитування локального HTML файлу: {path}")
        html = path.read_text(encoding="utf-8", errors="replace")
        data = scraper.parse_html_content(html, source_url=str(path))
        scraper.save_problem(data, contest_name=args.contest)
    else:
        # Зчитування через HTTP URL
        print(f"[*] Завантаження з мережі: {args.source}")
        try:
            html = scraper.fetch_url(args.source)
            data = scraper.parse_html_content(html, source_url=args.source)
            scraper.save_problem(data, contest_name=args.contest)
        except Exception as e:
            print(f"❌ Помилка завантаження: {e}")

if __name__ == "__main__":
    main()
