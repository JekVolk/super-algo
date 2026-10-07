import subprocess
import sys
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Тести: масив з 5 чисел: 1 2 1 3 2
# Запити:
# 1 5 -> 3 різних (1, 2, 3)
# 1 3 -> 2 різних (1, 2)
# 2 4 -> 3 різних (2, 1, 3)
# 4 5 -> 2 різних (3, 2)
# 1 1 -> 1 різний (1)
TESTS = [
    ("5\n1 2 1 3 2\n5\n1 5\n1 3\n2 4\n4 5\n1 1\n", "3\n2\n3\n2\n1\n"),
    ("4\n5 5 5 5\n2\n1 4\n2 3\n", "1\n1\n"),
    ("3\n10 20 30\n1\n1 3\n", "3\n"),
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

    print(f"\n✅ Всі {passed} тести для задачі F (Standard6: Різні на відрізках) успішно пройдено!")

if __name__ == "__main__":
    main()
