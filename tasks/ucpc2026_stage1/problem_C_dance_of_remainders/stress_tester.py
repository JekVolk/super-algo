"""
stress_tester.py — стрес-тест для Problem C: Танок залишків (Dance of Remainders)
Порівнює математичну відповідь min(n, m, k) з наївним перебором O(N * M * K)
для перевірки гіпотези, що a % b == b % c == c % a тільки при a == b == c.
"""
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def brute_force_triplets(n: int, m: int, k: int) -> int:
    cnt = 0
    for a in range(1, n + 1):
        for b in range(1, m + 1):
            for c in range(1, k + 1):
                if (a % b == b % c) and (b % c == c % a):
                    cnt += 1
    return cnt

def run_stress(iterations: int = 50):
    print(f"Запуск {iterations} стрес-тестів для Problem C...")
    for it in range(iterations):
        n = random.randint(1, 20)
        m = random.randint(1, 20)
        k = random.randint(1, 20)
        
        expected = str(brute_force_triplets(n, m, k))
        inp = f"{n} {m} {k}"
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        actual = res.stdout.strip()
        
        if actual != expected:
            print(f"❌ FAIL на тесті #{it+1} ({n}, {m}, {k})!")
            print(f"Очікувалось: {expected}, отримано: {actual}")
            sys.exit(1)
            
    print("✅ Усі 50 стрес-тестів для Problem C пройдено! Інваріант a=b=c повністю підтверджено.")

if __name__ == "__main__":
    run_stress(50)
