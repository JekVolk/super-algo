import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Inline test cases: (input_str, expected_output)
# Формат: "N M\nрядок_1\nрядок_2\n..."
TESTS = [
    # Тест 1: прямий коридор → 2 кроки
    ("1 3\nS.E",             "2"),
    # Тест 2: замурований вихід → -1
    ("2 2\nS#\n#E",          "-1"),
    # Тест 3: змійкоподібний шлях → 4 кроки
    ("3 3\nS.#\n#.#\n#.E",   "4"),
    # Тест 4: сітка 1×1 (без E) → -1
    ("1 1\nS",               "-1"),
    # Тест 5: S одразу поруч з E (1 крок)
    ("1 2\nSE",              "1"),
    # Тест 6: E повністю замурований стінами
    ("3 3\n..S\n###\nE..",   "-1"),
    # Тест 7: великий відкритий коридор → 4 кроки
    ("1 5\nS...E",           "4"),
    # Тест 8: S та E розділені лише одним .
    ("3 1\nS\n.\nE",         "2"),
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
            print(f"   Вхід:\n{inp}")
            print(f"   Очікувалось: {expected!r}")
            print(f"   Отримано:    {actual!r}")
            if res.stderr:
                print(f"   STDERR: {res.stderr.strip()}")

    print()
    if all_passed:
        print("✅ Всі тести для задачі 4 пройшли успішно!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
