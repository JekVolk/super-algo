"""
test_runner.py — Задача C: Танок залишків (UCPC 2026 Stage 1)
Inline-тести: min(n,m,k) доведено алгебраїчно, тут верифікуємо крайові випадки.
"""
import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Формат: (input_str "n m k", expected_output)
TEST_CASES = [
    # 1. n=m=k=1 → єдина трійка (1,1,1): 1%1=0 → відповідь 1
    ("1 1 1", "1"),
    # 2. n=3, m=5, k=4 → min=3 (лише (x,x,x) для x=1,2,3)
    ("3 5 4", "3"),
    # 3. n=2, m=3, k=5 → min=2
    ("2 3 5", "2"),
    # 4. n=1000000000, m=1000000000, k=1000000000 → min=10^9
    ("1000000000 1000000000 1000000000", "1000000000"),
    # 5. n=3, m=3, k=3 → min=3 (три трійки: (1,1,1),(2,2,2),(3,3,3))
    ("3 3 3", "3"),
    # 6. Мінімум на k
    ("100 200 7", "7"),
    # 7. Мінімум на n
    ("5 999 888", "5"),
]

def test_py():
    print("=== Тестування Python-розв'язку: Задача C (Танок залишків) ===")
    cwd = os.path.dirname(os.path.abspath(__file__))
    passed = 0
    failed = 0
    for i, (inp, expected) in enumerate(TEST_CASES, 1):
        p = subprocess.run(
            [sys.executable, "solution.py"],
            input=inp,
            text=True,
            capture_output=True,
            cwd=cwd
        )
        got = p.stdout.strip()
        if got == expected:
            print(f"  ✅ Тест #{i}: PASSED  ({inp} → {expected})")
            passed += 1
        else:
            print(f"  ❌ Тест #{i}: FAILED — вхід '{inp}', очікувалось '{expected}', отримано '{got}'")
            if p.stderr:
                print(f"     stderr: {p.stderr.strip()[:200]}")
            failed += 1
    print(f"\nРезультат: {passed}/{len(TEST_CASES)} тестів пройдено.")
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    test_py()
