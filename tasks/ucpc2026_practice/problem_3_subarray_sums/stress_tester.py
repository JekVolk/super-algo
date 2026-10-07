"""
stress_tester.py — стрес-тест для Problem 3: Subarray Sums (Fixed Window Max Sum)
Порівнює ковзне вікно з наївним O(N * K) алгоритмом.
"""
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def naive_max_k_sum(a, k):
    return max(sum(a[i:i+k]) for i in range(len(a) - k + 1))

def run_stress(iterations: int = 100):
    print(f"Запуск {iterations} стрес-тестів для Problem 3...")
    for it in range(iterations):
        n = random.randint(1, 100)
        k = random.randint(1, n)
        a = [random.randint(-1000, 1000) for _ in range(n)]
        expected = str(naive_max_k_sum(a, k))
        inp = f"{n} {k}\n" + " ".join(map(str, a))
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        actual = res.stdout.strip()
        if actual != expected:
            print(f"❌ FAIL на тесті #{it+1}!")
            print(f"Вхід: n={n}, k={k}, a={a}")
            print(f"Очікувалось: {expected}, отримано: {actual}")
            sys.exit(1)
    print("✅ Усі 100 стрес-тестів для Problem 3 пройдено!")

if __name__ == "__main__":
    run_stress(100)
