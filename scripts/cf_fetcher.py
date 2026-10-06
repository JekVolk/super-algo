#!/usr/bin/env python3
"""
Codeforces API Problem Fetcher and Scaffolder for Super-Algo.
Fetches problem statements, constraints, and tests via official Codeforces API and creates standard structure.
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

# Force UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def fetch_cf_problem(contest_id: int, problem_index: str, output_dir: Path):
    problem_index = problem_index.upper()
    api_url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}&from=1&count=1"
    
    print(f"[*] Запит до Codeforces API для Контесту #{contest_id}, Задача {problem_index}...")
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "Super-Algo/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"⚠️ Не вдалося отримати дані через API ({e}). Створюємо стандартний шаблон...")
        payload = {"status": "FAILED"}

    problem_name = f"Problem_{problem_index}"
    tags = []
    
    if payload.get("status") == "OK":
        problems = payload.get("result", {}).get("problems", [])
        for p in problems:
            if p.get("index") == problem_index:
                problem_name = f"{problem_index}_{p.get('name', 'Unknown')}"
                tags = p.get("tags", [])
                break

    clean_name = re.sub(r'[\\/*?:"<>| ]', '_', problem_name)
    target_path = output_dir / f"cf_{contest_id}_{clean_name}"
    target_path.mkdir(parents=True, exist_ok=True)

    # 1. Create solution.cpp
    cpp_file = target_path / "solution.cpp"
    if not cpp_file.exists():
        cpp_file.write_text("""#include <bits/stdc++.h>
using namespace std;

void solve() {
    // Введіть рішення тут
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t = 1;
    // cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}
""", encoding="utf-8")

    # 2. Create solution.py
    py_file = target_path / "solution.py"
    if not py_file.exists():
        py_file.write_text("""import sys

def solve():
    input = sys.stdin.readline
    # Введіть рішення тут
    pass

def main():
    solve()

if __name__ == "__main__":
    main()
""", encoding="utf-8")

    # 3. Create test_runner.py
    runner_file = target_path / "test_runner.py"
    if not runner_file.exists():
        runner_file.write_text("""import subprocess, sys
from pathlib import Path

def run():
    folder = Path(__file__).parent
    inputs = sorted(folder.glob("input*.txt"))
    if not inputs:
        print("Тестів input*.txt не знайдено!")
        return
    for inp in inputs:
        out = folder / inp.name.replace("input", "output")
        if not out.exists(): continue
        res = subprocess.run([sys.executable, str(folder / "solution.py")], input=inp.read_text(), text=True, capture_output=True)
        if res.stdout.strip() == out.read_text().strip():
            print(f"✅ {inp.name}: PASSED")
        else:
            print(f"❌ {inp.name}: FAILED\\nОчікувано:\\n{out.read_text()}\\nОтримано:\\n{res.stdout}")

if __name__ == "__main__": run()
""", encoding="utf-8")

    # 4. Generate README.md
    readme_file = target_path / "README.md"
    readme_file.write_text(f"""# 🏆 Codeforces {contest_id}{problem_index}: {problem_name}

- **URL:** [https://codeforces.com/contest/{contest_id}/problem/{problem_index}](https://codeforces.com/contest/{contest_id}/problem/{problem_index})
- **Теги:** {', '.join(tags) if tags else 'Ad-hoc'}
- **Тестування:** `python test_runner.py`

## ⚡ Розбір задачі
Скористайтеся 8-кроковим стандартом Super-Algo або згенеруйте повний аналіз.
""", encoding="utf-8")

    print(f"✅ Створено директорію задачі Codeforces: {target_path}")

def main():
    parser = argparse.ArgumentParser(description="Fetch and scaffold Codeforces problem")
    parser.add_argument("contest_id", type=int, help="ID контесту Codeforces (напр. 1950)")
    parser.add_argument("problem_index", type=str, help="Індекс задачі (A, B, C, D...)")
    parser.add_argument("--out", default="tasks", help="Цільова папка (за замовчуванням tasks)")
    args = parser.parse_args()

    fetch_cf_problem(args.contest_id, args.problem_index, Path(args.out))

if __name__ == "__main__":
    main()
