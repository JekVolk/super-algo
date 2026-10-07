"""
test_runner.py — Задача E: Чотири числа (UCPC 2026 Stage 1)
Inline-тести: min 5 значущих.
Формат вводу: перший рядок "n m", другий рядок — n чисел.
"""
import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Формат: (input_str, expected_output)
TEST_CASES = [
    # 1. n=1, a=[5], m=20 → 4*5=20 ≤ 20, відповідь 20
    ("1 20\n5", "20"),
    # 2. n=1, a=[5], m=19 → 4*5=20 > 19, відповідь -1
    ("1 19\n5", "-1"),
    # 3. Від'ємні числа: a=[-10, 2], m=-5 → best -16 ≤ -5 (але -4 > -5, тому max ≤-5 = -16? 
    #    Перевіримо: -10+-10+2+2=-16 ≤-5 ✓; -10+2+2+2=-4 > -5.
    #    Відповідь: -16? Ні — ще -10-10-10+2=-28. Всі пари: 
    #    p = {-20,-10,-10,-8,4} sorted: -20,-10,-10,-8,4
    #    Two-ptr знайде макс пару сум ≤-5:
    #    -20+4=-16 ≤-5 ✓, -10+4=-6 ≤-5 ✓, -8+4=-4 > -5, -10-8=-18≤-5...
    #    Найкраще: -10+4=-6? Ні, -8+(-10)=-18. 
    #    Пари: -10,-10,-10,-8,4 — wait n=2: indices i≤j:
    #    (0,0):-20, (0,1):-8, (1,1):4 → sorted: -20,-8,4
    #    ptr l=0,r=2: -20+4=-16≤-5 → best=-16, l=1
    #    l=1,r=2: -8+4=-4>-5 → r=1
    #    l=1,r=1: -8+(-8)=-16≤-5 → best=-16, l=2 → stop
    #    Answer: -16... but wait can we get -6? -8+4=-4>-5. -8+(-8)=-16 ✓
    #    Actually best satisfying ≤-5 is max of {-16,-16}=-16 
    #    Hmm, but -8+(-10)? Only n=2 elements: a[-10,2], pairs: a[0]+a[0]=-20, a[0]+a[1]=-8, a[1]+a[1]=4
    #    So four-number sums: p_l+p_r: (-20,-20)=-40, (-20,-8)=-28, (-20,4)=-16, (-8,-8)=-16, (-8,4)=-4, (4,4)=8
    #    Max sum ≤ -5: -4>-5, so -16. Answer: -16
    ("2 -5\n-10 2", "-16"),
    # 4. Всі нулі, m=0 → 0+0+0+0=0 ≤ 0, відповідь 0
    ("3 0\n0 0 0", "0"),
    # 5. Два від'ємних числа, m=-10: a=[-3,-4], m=-10
    #    Pairs: -6,-7,-8. Two-ptr: -8+(-8)=-16≤-10✓,-8+(-7)=-15≤-10✓,-8+(-6)=-14≤-10✓,-7+(-6)=-13≤-10✓,-6+(-6)=-12≤-10✓,-7+(-7)=-14≤-10,-6+(-7)...
    #    Actually sorted pairs: [-8,-7,-7,-6,-6] (a0+a0=-8, a0+a1=-7 twice? No, i≤j)
    #    (0,0):-8, (0,1):-7, (1,1):-6 → sorted: -8,-7,-6
    #    l=0,r=2: -8+(-6)=-14≤-10✓, l=1; l=1,r=2:-7+(-6)=-13≤-10✓,l=2; l=2,r=2:-6+(-6)=-12≤-10✓,l=3→stop
    #    Best=-12. Answer: -12
    ("2 -10\n-3 -4", "-12"),
    # 6. Файлові тести з умови: з input1.txt (стандартний тест)
    #    n=3, a=[1,2,3], m=10 → пари:{2,3,4,4,5,6} max≤10: 6+4=10 → 10
    ("3 10\n1 2 3", "10"),
    # 7. n=2, a=[1000000000, 1000000000], m=4000000000 → 4*10^9 ≤ 4*10^9 → 4000000000
    ("2 4000000000\n1000000000 1000000000", "4000000000"),
]

def test_py():
    print("=== Тестування Python-розв'язку: Задача E (Чотири числа) ===")
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
            print(f"  ✅ Тест #{i}: PASSED")
            passed += 1
        else:
            print(f"  ❌ Тест #{i}: FAILED — очікувалось '{expected}', отримано '{got}'")
            if p.stderr:
                print(f"     stderr: {p.stderr.strip()[:200]}")
            failed += 1
    print(f"\nРезультат: {passed}/{len(TEST_CASES)} тестів пройдено.")
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    test_py()
