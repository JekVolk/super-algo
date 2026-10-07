import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Inline test cases: (input_str, expected_output)
# Формат: перший рядок — N K, другий — N чисел
TESTS = [
    # Базовий приклад: max window [4,5] → 9
    ("5 2\n1 3 4 5 2",          "9"),
    # K = N: вся сума є єдиним вікном
    ("4 4\n1 2 3 4",            "10"),
    # K = 1: відповідь = максимальний елемент
    ("5 1\n-3 7 -1 4 -2",       "7"),
    # N = K = 1: єдиний елемент
    ("1 1\n42",                  "42"),
    # Всі від'ємні числа: max вікно [-5,-2] → -7
    ("4 2\n-5 -2 -8 -1",        "-7"),
    # Все однакове: max = K * val
    ("5 3\n2 2 2 2 2",           "6"),
    # Великі числа (перевірка 64-bit): 2 * 10^9
    ("2 2\n1000000000 1000000000", "2000000000"),
    # Від'ємні + додатні: вікно [3,5,2] → 10
    ("6 3\n-1 2 3 5 2 -4",      "10"),
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
            print(f"Тест #{idx}: PASSED  (очікувалось {expected!r})")
        else:
            all_passed = False
            print(f"❌ Тест #{idx}: FAILED")
            print(f"   Вхід:        {inp!r}")
            print(f"   Очікувалось: {expected!r}")
            print(f"   Отримано:    {actual!r}")
            if res.stderr:
                print(f"   STDERR: {res.stderr.strip()}")

    print()
    if all_passed:
        print("✅ Всі тести для задачі 3 пройшли успішно!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
