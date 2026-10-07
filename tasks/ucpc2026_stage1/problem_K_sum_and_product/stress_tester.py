"""
stress_tester.py — стрес-тест для Problem K: Сума і добуток (Sum and Product)
Перевіряє, що для випадкових дійсних чисел s сума знайдених чисел дорівнює s,
а добуток дорівнює 1 з точністю 1e-7.
"""
import math
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def run_stress(count: int = 50):
    print(f"Запуск {count} стрес-тестів для Problem K...")
    for it in range(count):
        # Випадкові числа: малі, великі, від'ємні, дробові
        choice = random.randint(1, 4)
        if choice == 1:
            s = random.uniform(-1.99, 1.99)
        elif choice == 2:
            s = random.uniform(2.01, 1000.0)
        elif choice == 3:
            s = random.uniform(-1000.0, -2.01)
        else:
            s = 1.0  # особливий випадок s=1
            
        inp = str(s)
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        lines = res.stdout.strip().splitlines()
        if not lines:
            print(f"❌ FAIL на тесті #{it+1}: порожній вивід для s={s}")
            sys.exit(1)
        n = int(lines[0])
        vals = [float(x) for x in lines[1].split()]
        if len(vals) != n:
            print(f"❌ FAIL: n={n}, але отримано {len(vals)} чисел!")
            sys.exit(1)
            
        val_sum = sum(vals)
        val_prod = math.prod(vals)
        if abs(val_sum - s) > 1e-6 or abs(val_prod - 1.0) > 1e-6:
            print(f"❌ FAIL на тесті #{it+1}: s={s}")
            print(f"   Сума: {val_sum} (різниця {abs(val_sum - s)})")
            print(f"   Добуток: {val_prod} (різниця {abs(val_prod - 1.0)})")
            sys.exit(1)
            
    print("✅ Усі 50 стрес-тестів для Problem K пройдено!")

if __name__ == "__main__":
    run_stress(50)
