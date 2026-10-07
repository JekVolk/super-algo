"""
stress_tester.py — стрес-тест для Problem M: Гірлянда UCPC (Garland UCPC)
Порівнює швидке жадібне рішення O(N) з прямим перебором усіх 3^N розфарбувань O(3^N * N^4)
для коротких рядків n <= 8.
"""
import itertools
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def brute_force_garland(s: str) -> int:
    n = len(s)
    # Знайдемо всі четвірки індексів UCPC
    ucpc_tuples = []
    for i1 in range(n):
        if s[i1] != 'U': continue
        for i2 in range(i1 + 1, n):
            if s[i2] != 'C': continue
            for i3 in range(i2 + 1, n):
                if s[i3] != 'P': continue
                for i4 in range(i3 + 1, n):
                    if s[i4] != 'C': continue
                    ucpc_tuples.append((i1, i2, i3, i4))
                    
    # Якщо входжень немає взагалі, будь-яке розфарбування підходить
    if not ucpc_tuples:
        return 3**n
        
    valid_count = 0
    # Перебираємо всі 3^n розфарбувань
    for col in itertools.product(range(3), repeat=n):
        # Перша четвірка задає зразок
        i1, i2, i3, i4 = ucpc_tuples[0]
        pattern = (col[i1], col[i2], col[i3], col[i4])
        match = True
        for t in ucpc_tuples[1:]:
            if (col[t[0]], col[t[1]], col[t[2]], col[t[3]]) != pattern:
                match = False
                break
        if match:
            valid_count += 1
            
    return valid_count

def run_stress():
    print("Запуск стрес-тестів для Problem M (Гірлянда UCPC)...")
    # Крайові тести
    test_cases = [
        "UCPC",
        "UUUU",
        "UCPCUCPC",
        "UUCPPC",
        "UCCPC",
        "CUPC",
        "UPC",
        "UUUCPCCC"
    ]
    for s in test_cases:
        expected = str(brute_force_garland(s))
        res = subprocess.run([sys.executable, str(SOLUTION)], input=s, text=True, capture_output=True)
        actual = res.stdout.strip()
        if actual != expected:
            print(f"❌ FAIL на '{s}': очікувалось {expected}, отримано {actual}")
            sys.exit(1)
        else:
            print(f"  ✓ '{s}': {expected} (OK)")
            
    # Випадкові рядки довжини 5-7 над алфавітом {U, C, P, X}
    for it in range(15):
        length = random.randint(4, 7)
        s = "".join(random.choice("UCPX") for _ in range(length))
        expected = str(brute_force_garland(s))
        res = subprocess.run([sys.executable, str(SOLUTION)], input=s, text=True, capture_output=True)
        actual = res.stdout.strip()
        if actual != expected:
            print(f"❌ FAIL на випадковому '{s}': очікувалось {expected}, отримано {actual}")
            sys.exit(1)
            
    print("✅ Усі стрес-тести для Problem M пройдено! Інваріант і формула 3^(f+3) / 3^(f+4) верифіковані.")

if __name__ == "__main__":
    run_stress()
