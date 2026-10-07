import subprocess
import sys
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TESTS = [
    ("5\n3 1 4 1 5\n", "1 1 3 4 5\n"),
    ("1\n42\n", "42\n"),
    ("6\n-5 0 10 -20 3 0\n", "-20 -5 0 0 3 10\n"),
    ("4\n1 2 3 4\n", "1 2 3 4\n"),
    ("4\n4 3 2 1\n", "1 2 3 4\n"),
    ("5\n-1000000000 1000000000 0 -5 5\n", "-1000000000 -5 0 5 1000000000\n"),
]

def main():
    prob_dir = Path(__file__).parent
    sol_py = prob_dir / "solution.py"

    passed = 0
    for idx, (inp, expected) in enumerate(TESTS, 1):
        proc = subprocess.run(
            [sys.executable, str(sol_py)],
            input=inp,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        out = proc.stdout.strip()
        exp = expected.strip()
        if out == exp:
            passed += 1
            print(f"Тест #{idx}: PASSED")
        else:
            print(f"Тест #{idx}: FAILED! Отримано: {out!r}, Очікувалось: {exp!r}")
            sys.exit(1)

    print(f"\n✅ Всі {passed} тести для задачі B (Standard2: Сортування) успішно пройдено!")

if __name__ == "__main__":
    main()
