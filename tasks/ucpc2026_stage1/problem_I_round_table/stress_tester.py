"""
stress_tester.py — стрес-тест для Problem I: Круглий стіл (Round Table)
Порівнює швидкий розв'язок на двійковому підйомі (Binary Lifting O(M log M))
з повним експоненційним пошуком найбільшої множини неперетинних дуг на колі O(2^M).
"""
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def arc_cells(l: int, r: int, n: int) -> set:
    if l <= r:
        return set(range(l, r + 1))
    else:
        return set(range(l, n + 1)) | set(range(1, r + 1))

def brute_force_round_table(n: int, m: int, segments: list) -> int:
    arc_sets = [arc_cells(l, r, n) for l, r in segments]
    best = 0
    # Перебір усіх 2^m підмножин
    for mask in range(1 << m):
        chosen = [i for i in range(m) if (mask & (1 << i))]
        if len(chosen) <= best:
            continue
        # Перевірка на попарний неперетин
        valid = True
        occupied = set()
        for idx in chosen:
            if occupied & arc_sets[idx]:
                valid = False
                break
            occupied |= arc_sets[idx]
        if valid:
            best = len(chosen)
    return best

def run_stress(iterations: int = 40):
    print(f"Запуск {iterations} стрес-тестів для Problem I...")
    for it in range(iterations):
        n = random.randint(3, 10)
        m = random.randint(1, 8)
        segments = []
        for _ in range(m):
            l = random.randint(1, n)
            r = random.randint(1, n)
            # Дуга не повинна покривати все коло (довжина < n)
            if l == (r % n + 1):
                # Повне коло, зсунемо r
                r = (r % n) + 1
            segments.append((l, r))
            
        expected = str(brute_force_round_table(n, m, segments))
        inp = f"{n} {m}\n" + "\n".join(f"{l} {r}" for l, r in segments)
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        actual = res.stdout.strip()
        
        if actual != expected:
            print(f"❌ FAIL на тесті #{it+1}!")
            print(f"Вхід:\n{inp}")
            print(f"Очікувалось: {expected}, отримано: {actual}")
            sys.exit(1)
            
    print("✅ Усі 40 стрес-тестів для Problem I пройдено!")

if __name__ == "__main__":
    run_stress(40)
