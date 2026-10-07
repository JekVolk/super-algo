"""
stress_tester.py — стрес-тест для Problem H: Візерунок (Pattern)
Перевіряє рекурентність unbordered words через повний перебір усіх слів k^n.
Слово має бордер, якщо є префікс довжини 1 <= l < n, який збігається з суфіксом.
"""
import itertools
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def has_border(s: tuple) -> bool:
    n = len(s)
    for l in range(1, n):
        if s[:l] == s[n - l:]:
            return True
    return False

def count_unbordered(n: int, k: int) -> int:
    cnt = 0
    for w in itertools.product(range(k), repeat=n):
        if not has_border(w):
            cnt += 1
    return cnt

def run_stress():
    print("Запуск стрес-тестів для Problem H (Unbordered words)...")
    for k in [2, 3]:
        for n in range(1, 8):
            expected = str(count_unbordered(n, k))
            inp = f"{n} {k}"
            res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
            actual = res.stdout.strip()
            if actual != expected:
                print(f"❌ FAIL: n={n}, k={k} — очікувалось {expected}, отримано {actual}")
                sys.exit(1)
            else:
                print(f"  ✓ n={n}, k={k}: {expected} (OK)")
    print("✅ Усі стрес-тести для Problem H пройдено! Рекурентність доведена.")

if __name__ == "__main__":
    run_stress()
