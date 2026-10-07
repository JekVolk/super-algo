"""
stress_tester.py — стрес-тест для Problem L: Три комп'ютери (Three Computers)
Порівнює швидкий потік мінімальної вартості (MCMF O(N log N)) 
з точним експоненційним перебором O(4^N) призначення задач 3 комп'ютерам.
"""
import itertools
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def is_compatible(tasks):
    tasks_sorted = sorted(tasks, key=lambda x: x[0])
    for i in range(len(tasks_sorted) - 1):
        if tasks_sorted[i][1] >= tasks_sorted[i + 1][0]:
            return False
    return True

def brute_force_three_computers(n, tasks):
    best = 0
    # Кожна задача призначається на 0, 1, 2, 3 (0 = не беремо)
    for assign in itertools.product(range(4), repeat=n):
        c1 = [tasks[i] for i in range(n) if assign[i] == 1]
        c2 = [tasks[i] for i in range(n) if assign[i] == 2]
        c3 = [tasks[i] for i in range(n) if assign[i] == 3]
        if is_compatible(c1) and is_compatible(c2) and is_compatible(c3):
            total_w = sum(tasks[i][2] for i in range(n) if assign[i] > 0)
            if total_w > best:
                best = total_w
    return best

def run_stress(count: int = 30):
    print(f"Запуск {count} стрес-тестів для Problem L...")
    for it in range(count):
        n = random.randint(1, 6)
        tasks = []
        for _ in range(n):
            l = random.randint(1, 10)
            r = random.randint(l, 15)
            w = random.randint(1, 100)
            tasks.append((l, r, w))
            
        expected = str(brute_force_three_computers(n, tasks))
        inp = f"{n}\n" + "\n".join(f"{l} {r} {w}" for l, r, w in tasks)
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        actual = res.stdout.strip()
        
        if actual != expected:
            print(f"❌ FAIL на тесті #{it+1}!")
            print(f"Вхід:\n{inp}")
            print(f"Очікувалось: {expected}, отримано: {actual}")
            sys.exit(1)
            
    print("✅ Усі 30 стрес-тестів для Problem L пройдено! MCMF верифіковано.")

if __name__ == "__main__":
    run_stress(30)
