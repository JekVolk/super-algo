"""
stress_tester.py — стрес-тест для Problem 2: Parity Strings (Palindrome Permutation)
Порівнює розв'язок із наївною перевіркою парності лічильників символів.
"""
import random
import string
import subprocess
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def naive_check(s: str) -> str:
    cnt = Counter(s)
    odd = sum(1 for c in cnt.values() if c % 2 != 0)
    return "YES" if odd <= 1 else "NO"

def run_stress(iterations: int = 100):
    print(f"Запуск {iterations} стрес-тестів для Problem 2...")
    for i in range(iterations):
        length = random.randint(1, 100)
        # Випадковий рядок з літер 'a'-'e' для кращого шансу парностей
        s = "".join(random.choice("abcde") for _ in range(length))
        expected = naive_check(s)
        res = subprocess.run([sys.executable, str(SOLUTION)], input=s, text=True, capture_output=True)
        actual = res.stdout.strip()
        if actual != expected:
            print(f"❌ FAIL на тесті #{i+1}: {s}")
            print(f"Очікувалось: {expected}, отримано: {actual}")
            sys.exit(1)
    print("✅ Усі 100 стрес-тестів для Problem 2 пройдено!")

if __name__ == "__main__":
    run_stress(100)
