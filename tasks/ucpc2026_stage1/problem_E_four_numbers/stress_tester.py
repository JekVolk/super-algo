"""
stress_tester.py — стрес-тест для Problem E: Чотири числа (Four Numbers)
Порівнює алгоритм з парами O(N^2 log N) з наївним перебором O(N^4).
Знаходить максимальну суму a[i] + a[j] + a[k] + a[l] <= m (з повтореннями).
"""
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def brute_force_4sum(n: int, m: int, a: list) -> str:
    best = -float('inf')
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                for l in range(k, n):
                    s = a[i] + a[j] + a[k] + a[l]
                    if s <= m and s > best:
                        best = s
    return str(best) if best != -float('inf') else "-1"

def run_stress(iterations: int = 40):
    print(f"Запуск {iterations} стрес-тестів для Problem E...")
    for it in range(iterations):
        n = random.randint(1, 10)
        a = [random.randint(-50, 50) for _ in range(n)]
        m = random.randint(-150, 150)
        
        expected = brute_force_4sum(n, m, a)
        inp = f"{n} {m}\n" + " ".join(map(str, a))
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        actual = res.stdout.strip()
        
        if actual != expected:
            print(f"❌ FAIL на тесті #{it+1}!")
            print(f"Вхід: n={n}, m={m}, a={a}")
            print(f"Очікувалось: {expected}, отримано: {actual}")
            sys.exit(1)
            
    print("✅ Усі 40 стрес-тестів для Problem E пройдено!")

if __name__ == "__main__":
    run_stress(40)
