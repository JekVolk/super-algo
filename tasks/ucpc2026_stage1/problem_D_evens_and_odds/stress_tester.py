"""
stress_tester.py — стрес-тест для Problem D: Evens and Odds
Порівнює швидкий розв'язок (solution.py) із brute-force перевіркою та перевіркою збалансованості.
"""
import random
import subprocess
import sys
import os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def check_balanced(s: str) -> bool:
    """Перевіряємо, чи рядок s є збалансованим."""
    s_rev = s[::-1]
    contrib = 0
    for pos, ch in enumerate(s_rev):
        d = int(ch)
        if pos % 2 == 0:
            if d % 2 == 1:
                contrib += d
        else:
            if d % 2 == 0:
                contrib -= d
    return contrib == 0

def brute_force(N: str) -> str:
    """
    Brute-force: знаходимо мінімальний збалансований M >= N
    шляхом послідовного перебору рядків.
    """
    for k in range(8):
        if k == 0:
            if check_balanced(N):
                return N
        else:
            from itertools import product
            for digits in product("0123456789", repeat=k):
                candidate = N + "".join(digits)
                if check_balanced(candidate):
                    return candidate
    return N

def run_stress(n_tests: int = 50):
    print(f"Запуск {n_tests} стрес-тестів для Problem D...")
    for i in range(n_tests):
        length = random.randint(1, 4)
        first = random.randint(1, 9)
        rest = [random.randint(0, 9) for _ in range(length - 1)]
        N = str(first) + "".join(map(str, rest))
        
        expected = brute_force(N)
        res = subprocess.run([sys.executable, str(SOLUTION)], input=N, text=True, capture_output=True)
        got = res.stdout.strip()
        
        if got != expected:
            print(f"❌ FAIL: N={N}: очікувалось={expected}, отримано={got}")
            sys.exit(1)
        if not check_balanced(got):
            print(f"❌ FAIL: N={N}: відповідь {got} не збалансована!")
            sys.exit(1)
            
    print("✅ Усі 50 стрес-тестів для Problem D пройдено!")

if __name__ == "__main__":
    run_stress(50)
