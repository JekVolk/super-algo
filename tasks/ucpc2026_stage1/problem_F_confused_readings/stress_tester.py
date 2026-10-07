"""
stress_tester.py — стрес-тест для Problem F: Переплутані покази (Confused Readings)
Генерує випадковий набір чисел, рахує всі суми та побітові АБО всіх підмножин,
сортує їх і перевіряє, чи відновлює алгоритм вихідний масив.
"""
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def generate_input(n, max_val=50):
    orig = sorted(random.randint(1, max_val) for _ in range(n))
    all_vals = []
    for mask in range(1, 1 << n):
        subset = [orig[i] for i in range(n) if mask & (1 << i)]
        s = sum(subset)
        o = 0
        for v in subset:
            o |= v
        all_vals.extend([s, o])
    all_vals.sort()
    inp = f"{n}\n" + " ".join(map(str, all_vals))
    expected = " ".join(map(str, orig))
    return inp, expected

def run_stress(num_tests: int = 40):
    print(f"Запуск {num_tests} стрес-тестів для Problem F...")
    for t in range(num_tests):
        n = random.randint(1, 6)
        inp, expected = generate_input(n, max_val=40)
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        got = res.stdout.strip()
        if got != expected:
            print(f"❌ FAIL на тесті #{t+1}:")
            print(f"   Вхід: {inp}")
            print(f"   Очікувано: {expected}")
            print(f"   Отримано:  {got}")
            sys.exit(1)
    print("✅ Усі 40 стрес-тестів для Problem F пройдено!")

if __name__ == "__main__":
    run_stress(40)
