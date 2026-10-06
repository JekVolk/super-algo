#!/usr/bin/env python3
"""
Competitive Companion Local Listener & Auto-Scaffolder.
Listens for HTTP POST requests from the Competitive Companion browser extension
(available free for Chrome, Firefox, Edge).
Automatically scaffolds problem folders, sample test cases, solutions (C++/Python),
and test runners.
"""

import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

DEFAULT_PORT = 10043  # Standard port for Competitive Companion (e.g. CP Editor / CPH)

def sanitize_name(name: str) -> str:
    cleaned = re.sub(r'[\\/*?:"<>| ]', '_', name.strip())
    return re.sub(r'_+', '_', cleaned)

CPP_TEMPLATE = """#include <bits/stdc++.h>
using namespace std;

void solve() {
    // Введіть розв'язок тут
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t = 1;
    // Якщо задача має декілька тестів (t > 1), розкоментуйте:
    // cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}
"""

PYTHON_TEMPLATE = """import sys

def solve():
    input = sys.stdin.readline
    # Введіть розв'язок тут
    pass

def main():
    # Якщо декілька тестів:
    # t = int(sys.stdin.readline())
    # for _ in range(t):
    #     solve()
    solve()

if __name__ == "__main__":
    main()
"""

TEST_RUNNER_TEMPLATE = """import subprocess
import sys
from pathlib import Path

def run_tests(target="solution.py"):
    folder = Path(__file__).parent
    inputs = sorted(folder.glob("input*.txt"))
    if not inputs:
        print("Тестові файли input*.txt не знайдено!")
        return

    print(f"=== Запуск тестів для {target} ===")
    all_passed = True
    for inp in inputs:
        idx = inp.stem.replace("input", "")
        out = folder / f"output{idx}.txt"
        if not out.exists():
            continue

        with open(inp, "r", encoding="utf-8") as f_in:
            in_data = f_in.read()
        with open(out, "r", encoding="utf-8") as f_out:
            expected_out = f_out.read().strip()

        if target.endswith(".py"):
            cmd = [sys.executable, str(folder / target)]
        elif target.endswith(".cpp"):
            exe = folder / "solution_exe"
            subprocess.run(["g++", "-O3", str(folder / target), "-o", str(exe)], check=True)
            cmd = [str(exe)]
        else:
            cmd = [target]

        res = subprocess.run(cmd, input=in_data, text=True, capture_output=True)
        actual_out = res.stdout.strip()

        if actual_out == expected_out:
            print(f" Тест #{idx}: PASSED")
        else:
            all_passed = False
            print(f"❌ Тест #{idx}: FAILED")
            print(f"   Вхідні дані:\\n{in_data.strip()}")
            print(f"   Очікувалось:\\n{expected_out}")
            print(f"   Отримано:\\n{actual_out}")

    if all_passed:
        print("\\n Всі приклади пройшли успішно!")
    else:
        print("\\n Знайдено розбіжності!")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "solution.py"
    run_tests(target)
"""

class CompanionHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode("utf-8"))
            self.process_problem(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            print(f"Помилка обробки: {e}", file=sys.stderr)
            self.send_response(500)
            self.end_headers()

    def process_problem(self, data: dict):
        problem_name = data.get("name", "Unknown_Problem")
        group = data.get("group", "Unknown_Group")
        url = data.get("url", "")
        tests = data.get("tests", [])
        time_limit = data.get("timeLimit", 1000)
        memory_limit = data.get("memoryLimit", 256)

        group_clean = sanitize_name(group)
        name_clean = sanitize_name(problem_name)

        base_dir = Path("tasks") / group_clean / name_clean
        base_dir.mkdir(parents=True, exist_ok=True)

        # Save metadata
        with open(base_dir / "problem.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Save sample tests
        for i, test in enumerate(tests, 1):
            with open(base_dir / f"input{i}.txt", "w", encoding="utf-8") as f:
                f.write(test.get("input", ""))
            with open(base_dir / f"output{i}.txt", "w", encoding="utf-8") as f:
                f.write(test.get("output", ""))

        # Create templates if not exist
        if not (base_dir / "solution.cpp").exists():
            with open(base_dir / "solution.cpp", "w", encoding="utf-8") as f:
                f.write(CPP_TEMPLATE)
        if not (base_dir / "solution.py").exists():
            with open(base_dir / "solution.py", "w", encoding="utf-8") as f:
                f.write(PYTHON_TEMPLATE)
        if not (base_dir / "test_runner.py").exists():
            with open(base_dir / "test_runner.py", "w", encoding="utf-8") as f:
                f.write(TEST_RUNNER_TEMPLATE)

        # Create problem summary README
        with open(base_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"# {problem_name}\\n\\n")
            f.write(f"- **Група/Турнір:** {group}\\n")
            f.write(f"- **URL:** [{url}]({url})\\n")
            f.write(f"- **Ліміт часу:** {time_limit} ms\\n")
            f.write(f"- **Ліміт пам'яті:** {memory_limit} MB\\n\\n")
            f.write(f"## Кількість тестів у прикладі: {len(tests)}\\n\\n")
            f.write("Для запуску тестів:\\n```bash\\npython test_runner.py solution.py\\n```\\n")

        print(f"\\n Задача '{problem_name}' успішно створена в: {base_dir}")
        print(f" Завантажено тестів: {len(tests)}")

def run_server(port=DEFAULT_PORT):
    server = HTTPServer(("127.0.0.1", port), CompanionHandler)
    print(f" Competitive Companion Listener активний на http://127.0.0.1:{port}")
    print("Натисніть зелену іконку '+' у браузері на сторінці задачі (Codeforces, AtCoder, LeetCode, CSES тощо) для імпорту!")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nЗупинка сервера...")
        server.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    run_server(port)
