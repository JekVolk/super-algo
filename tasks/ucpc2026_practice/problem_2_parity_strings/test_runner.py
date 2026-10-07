import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Inline test cases: (input_str, expected_output)
# Рядок можна скласти у паліндром ↔ не більше однієї літери з непарною кількістю
TESTS = [
    # Один символ — завжди YES (1 непарна, ≤1)
    ("a",        "YES"),
    ("z",        "YES"),
    # Парні кількості всіх символів → YES
    ("aabb",     "YES"),
    ("aabbcc",   "YES"),
    # Один символ із непарною кількістю → YES (паліндром непарної довжини)
    ("aab",      "YES"),
    ("aaabb",    "YES"),
    # Два+ символи з непарними кількостями → NO
    ("abc",      "NO"),
    ("aabbc",    "YES"),
    # Рядок із однакових символів парної довжини
    ("aaaa",     "YES"),
    # Рядок з усіма різними символами (3 непарних) → NO
    ("abc",      "NO"),
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
        print("✅ Всі тести для задачі 2 пройшли успішно!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
