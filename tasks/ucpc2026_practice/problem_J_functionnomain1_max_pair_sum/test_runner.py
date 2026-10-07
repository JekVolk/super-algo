import subprocess
import sys
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Тести
# 4 елементи: 3 1 4 2 -> два найбільших це 4 і 3 -> сума 7
# 2 елементи: -5 -10 -> -15
# 5 елементів: 10 10 5 1 2 -> 20 (два однакових максимуми)
TESTS = [
    ("4\n3 1 4 2\n", "7\n"),
    ("2\n-5 -10\n", "-15\n"),
    ("5\n10 10 5 1 2\n", "20\n"),
    ("3\n100 200 50\n", "300\n"),
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

    print(f"\n✅ Всі {passed} тести для задачі J (FunctionNoMain1: Максимальна сума пари) успішно пройдено!")

if __name__ == "__main__":
    main()
