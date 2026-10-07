"""
stress_tester.py — інтерактивний стрес-тест для Problem J: Терези (Scales)
Запускає випадкові пари (A, B) розмірності N і емулює оракул порівнянь.
"""
import subprocess
import sys
import random
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def run_interactive(n: int, a: int, b: int) -> bool:
    p = subprocess.Popen(
        [sys.executable, str(SOLUTION)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=Path(__file__).parent
    )
    p.stdin.write(f"{n}\n")
    p.stdin.flush()
    
    query_count = 0
    max_queries = 2 * n
    
    while True:
        line = p.stdout.readline()
        if not line:
            return False
        line = line.strip()
        if line.startswith("?"):
            parts = line.split()
            x = int(parts[1])
            y = int(parts[2])
            query_count += 1
            if query_count > max_queries:
                p.kill()
                return False
            va = a ^ x
            vb = b ^ y
            if va > vb:
                resp = ">\n"
            elif va < vb:
                resp = "<\n"
            else:
                resp = "=\n"
            p.stdin.write(resp)
            p.stdin.flush()
        elif line.startswith("!"):
            parts = line.split()
            found_a = int(parts[1])
            found_b = int(parts[2])
            p.terminate()
            return (found_a == a and found_b == b)

def run_stress(count: int = 40):
    print(f"Запуск {count} інтерактивних стрес-тестів для Problem J...")
    for i in range(count):
        n = random.randint(1, 20)
        max_val = (1 << n) - 1
        a = random.randint(0, max_val)
        b = random.randint(0, max_val)
        if not run_interactive(n, a, b):
            print(f"❌ FAIL: n={n}, a={a}, b={b}")
            sys.exit(1)
    print("✅ Усі 40 інтерактивних стрес-тестів для Problem J пройдено!")

if __name__ == "__main__":
    run_stress(40)
