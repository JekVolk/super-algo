import subprocess
import sys
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TESTS = [
    ("3\n1 3 2\n", "15\n"),
    ("1\n10\n", "10\n"),
    ("2\n2 2\n", "6\n"),
    ("4\n1 2 3 4\n", "30\n"),
    ("4\n4 3 2 1\n", "30\n"),
    ("5\n2 1 4 3 5\n", "57\n"),
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

    print(f"\n✅ Всі {passed} тести для задачі D (Standard4: Сума максимумів підвідрізків) успішно пройдено!")

if __name__ == "__main__":
    main()
