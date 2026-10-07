import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Inline test cases: (input_str, expected_output)
TESTS = [
    # Базові тести
    ("1 2",              "3"),
    ("0 0",              "0"),
    # Від'ємні числа
    ("-5 3",             "-2"),
    ("-7 -3",            "-10"),
    # Великі числа (MAX ~ 10^9)
    ("1000000000 1000000000", "2000000000"),
    ("1000000000 -1000000000", "0"),
    # Одне нульове
    ("0 42",             "42"),
    ("-1000000000 0",    "-1000000000"),
]

def run_tests():
    folder   = Path(__file__).parent
    solution = folder / "solution.py"

    all_passed = True
    for idx, (inp, expected) in enumerate(TESTS, start=1):
        res = subprocess.run(
            [sys.executable, str(solution)],
            input=inp, text=True, capture_output=True
        )
        actual = res.stdout.strip()
        if actual == expected:
            print(f"Тест #{idx}: PASSED  ({inp!r} → {actual!r})")
        else:
            all_passed = False
            print(f"❌ Тест #{idx}: FAILED  ({inp!r})")
            print(f"   Очікувалось: {expected!r}")
            print(f"   Отримано:    {actual!r}")
            if res.stderr:
                print(f"   STDERR: {res.stderr.strip()}")

    print()
    if all_passed:
        print("✅ Всі тести для задачі 1 пройшли успішно!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
