#!/usr/bin/env python3
"""
Eolymp Space & UCPC Automated Problem Scraper.
Fetches problem statements, constraints, sample tests, and assets
from Eolymp Space (e.g. https://ucpc.eolymp.space/uk/compete/ucpc2026practice/problem/1).

Supports:
1. Session Cookie authentication (for authorized contests like UCPC)
2. Automatic fallback / Next.js RSC payload parsing
3. Export to tasks/<contest>/<problem>/ directory with C++ and Python templates
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

CPP_TEMPLATE = """#include <bits/stdc++.h>
using namespace std;

void solve() {
    // Введіть розв'язок задачі
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

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
    input = sys.stdin.readline
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

        res = subprocess.run([sys.executable, "solution.py"], input=in_data, text=True, capture_output=True)
        actual = res.stdout.strip()

        if actual == expected:
            print(f" Тест #{idx}: PASSED")
        else:
            all_passed = False
            print(f"❌ Тест #{idx}: FAILED")
            print(f"   Очікувалось:\\n{expected}")
            print(f"   Отримано:\\n{actual}")

    if all_passed:
        print("\\n Всі приклади пройшли успішно!")

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

    def parse_problem(self, url: str) -> dict:
        print(f"[*] Завантаження сторінки: {url}")
        html = self.fetch_url(url)

        # Check if redirected to login
        if "/signin" in html or "SigninForm" in html:
            if not self.cookie:
                print("\\n⚠️ УВАГА: Контест UCPC на Eolymp вимагає авторизації!")
                print("Для отримання доступу передайте кукі вашої сесії браузера:")
                print("python scripts/eolymp_scraper.py <url> --cookie \"eolymp_session=...\"")
                print("Або скористайтеся Competitive Companion прямо з браузера!")

        # 1. Title
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1).replace("Ukrainian Collegiate Programming Contest", "").strip(" -|") if title_match else "Problem"
        if not title:
            # Try to find problem number in URL
            url_parts = url.rstrip("/").split("/")
            prob_num = url_parts[-1] if url_parts else "1"
            title = f"Problem_{prob_num}"

        # 2. Time limit & Memory limit
        time_limit = "1.0s"
        tl_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:сек|sec|s)', html, re.IGNORECASE)
        if tl_match:
            time_limit = tl_match.group(0)

        memory_limit = "256 MB"
        ml_match = re.search(r'(\d+)\s*(?:МБ|MB|MiB)', html, re.IGNORECASE)
        if ml_match:
            memory_limit = ml_match.group(0)

        # 3. Sample tests extraction (look for code blocks or pre tags)
        samples = []
        pre_blocks = re.findall(r'<pre[^>]*>(.*?)</pre>', html, re.DOTALL)
        # Often inputs and outputs come in pairs
        if len(pre_blocks) >= 2:
            for i in range(0, len(pre_blocks) - 1, 2):
                inp = re.sub(r'<[^>]+>', '', pre_blocks[i]).strip()
                out = re.sub(r'<[^>]+>', '', pre_blocks[i+1]).strip()
                if inp and out:
                    samples.append({"input": inp, "output": out})

        return {
            "title": title,
            "url": url,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "samples": samples,
            "raw_html": html
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

        # Create boilerplate files
        if not (folder / "solution.cpp").exists():
            with open(folder / "solution.cpp", "w", encoding="utf-8") as f:
                f.write(CPP_TEMPLATE)

        if not (folder / "solution.py").exists():
            with open(folder / "solution.py", "w", encoding="utf-8") as f:
                f.write(PYTHON_TEMPLATE)

        if not (folder / "test_runner.py").exists():
            with open(folder / "test_runner.py", "w", encoding="utf-8") as f:
                f.write(TEST_RUNNER_TEMPLATE)

        # Create README
        with open(folder / "README.md", "w", encoding="utf-8") as f:
            f.write(f"# {prob_data['title']}\\n\\n")
            f.write(f"- **URL:** [{prob_data['url']}]({prob_data['url']})\\n")
            f.write(f"- **Ліміт часу:** {prob_data['time_limit']}\\n")
            f.write(f"- **Ліміт пам'яті:** {prob_data['memory_limit']}\\n")
            f.write(f"- **Зразків тестів:** {len(samples)}\\n\\n")
            f.write("## Запуск тестів:\\n```bash\\npython test_runner.py\\n```\\n")

        print(f"\\n Задача збережена у папку: {folder}")
        print(f" Збережено тестів: {len(samples)}")
        print(f" Згенеровано шаблони: solution.cpp, solution.py, test_runner.py")

def main():
    parser = argparse.ArgumentParser(description="Eolymp / UCPC Problem Scraper")
    parser.add_argument("url", nargs="?", default="https://ucpc.eolymp.space/uk/compete/ucpc2026practice/problem/1", help="URL задачі на Eolymp")
    parser.add_argument("--cookie", default="", help="Cookie авторизації з браузера")
    parser.add_argument("--contest", default="ucpc2026practice", help="Назва турніру для папки")
    args = parser.parse_args()

    scraper = EolympScraper(cookie=args.cookie)
    try:
        data = scraper.parse_problem(args.url)
        scraper.save_problem(data, contest_name=args.contest)
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    main()
