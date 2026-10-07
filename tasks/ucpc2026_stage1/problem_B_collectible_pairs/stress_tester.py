"""
stress_tester.py — стрес-тест для Problem B: Колекційні пари (Collectible Pairs)
Перевіряє, що знайдене число x та x+1 дійсно є числами Харшада і потрапляють у [m, 2m].
"""
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def digit_sum(n: int) -> int:
    return sum(int(c) for c in str(n))

def is_harshad(n: int) -> bool:
    return n % digit_sum(n) == 0

def run_stress(iterations: int = 50):
    print(f"Запуск {iterations} стрес-тестів для Problem B...")
    for it in range(iterations):
        # Випадкові m різної довжини від 1 до 10^12
        digits = random.randint(1, 12)
        if digits == 1:
            m = random.randint(1, 9)
        else:
            m = random.randint(10**(digits - 1), 10**digits - 1)
        
        inp = str(m)
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        actual = res.stdout.strip()
        
        if actual == "-1":
            # Якщо сказано -1, для малих m (< 20000) перевіримо, чи дійсно немає
            if m < 2000:
                for x in range(m, 2 * m):
                    if is_harshad(x) and is_harshad(x + 1):
                        print(f"❌ FAIL на тесті #{it+1}: m={m}, рішення дало -1, але знайдено x={x}!")
                        sys.exit(1)
        else:
            x = int(actual)
            # Перевіримо властивості
            if not (m <= x and x + 1 <= 2 * m):
                print(f"❌ FAIL на тесті #{it+1}: m={m}, x={x} не вкладається в [{m}, {2*m}]!")
                sys.exit(1)
            if not (is_harshad(x) and is_harshad(x + 1)):
                print(f"❌ FAIL на тесті #{it+1}: m={m}, x={x} або x+1={x+1} не є Harshad!")
                sys.exit(1)
                
    print("✅ Усі 50 стрес-тестів для Problem B пройдено!")

if __name__ == "__main__":
    run_stress(50)
