"""
stress_tester.py — стрес-тест для Problem 1: Sum A + B
Перевіряє швидкий розв'язок проти наївного додавання на випадкових даних великої розмірності.
"""
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def run_stress(iterations: int = 100):
    print(f"Запуск {iterations} стрес-тестів для Problem 1...")
    for i in range(iterations):
        a = random.randint(-10**18, 10**18)
        b = random.randint(-10**18, 10**18)
        expected = str(a + b)
        inp = f"{a} {b}"
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        actual = res.stdout.strip()
        if actual != expected:
            print(f"❌ FAIL на тесті #{i+1}: {a} + {b}")
            print(f"Очікувалось: {expected}, отримано: {actual}")
            sys.exit(1)
    print("✅ Усі 100 стрес-тестів для Problem 1 пройдено!")

if __name__ == "__main__":
    run_stress(100)
