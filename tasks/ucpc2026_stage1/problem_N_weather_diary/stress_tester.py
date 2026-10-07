"""
stress_tester.py — стрес-тест для Problem N: Щоденник погоди (Weather Diary)
Генерує випадкові послідовності 'S' та 'R' різної довжини n, рахує переходи u, v, e, g
і перевіряє, що розв'язок видає "YES" для реальних щоденників та "NO" при спотворенні лічильників.
"""
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def count_transitions(seq: str):
    u = v = e = g = 0
    for i in range(len(seq) - 1):
        pair = seq[i:i+2]
        if pair == "SR": u += 1
        elif pair == "RS": v += 1
        elif pair == "SS": e += 1
        elif pair == "RR": g += 1
    return u, v, e, g

def run_stress(count: int = 50):
    print(f"Запуск {count} стрес-тестів для Problem N...")
    for it in range(count):
        n = random.randint(1, 30)
        seq = "".join(random.choice("SR") for _ in range(n))
        u, v, e, g = count_transitions(seq)
        
        # 1. Справжній щоденник має давати YES
        inp_valid = f"{n} {u} {v} {e} {g}"
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp_valid, text=True, capture_output=True)
        if res.stdout.strip() != "YES":
            print(f"❌ FAIL: Справжня послідовність {seq} дала NO!")
            print(f"Вхід: {inp_valid}")
            sys.exit(1)
            
        # 2. Неможливий щоденник: збільшимо u на 2
        inp_invalid = f"{n} {u + 2} {v} {e} {g}"
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp_invalid, text=True, capture_output=True)
        if res.stdout.strip() != "NO":
            print(f"❌ FAIL: Неможливий вхід {inp_invalid} дав YES!")
            sys.exit(1)
            
    print("✅ Усі 50 стрес-тестів для Problem N пройдено!")

if __name__ == "__main__":
    run_stress(50)
