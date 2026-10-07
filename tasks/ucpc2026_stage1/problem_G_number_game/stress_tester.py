"""
stress_tester.py — стрес-тест для Problem G: Числова гра (Number Game)
Порівнює аналітичну формулу з BFS-пошуком найкоротшого шляху на графі переходів по кількості одиниць.
"""
import random
import subprocess
import sys
from collections import deque
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def bfs_min_moves(n_str: str, m_str: str) -> str:
    if n_str == m_str:
        return "0"
    m_val = int(m_str, 2)
    if m_val == 1:
        return "-1"
    
    c = n_str.count('1')
    p = bin(m_val - 1).count('1')
    
    # BFS від c до p
    # Зі стану u можна перейти до будь-якого v у [1, u + 1] за 1 крок
    # Потім з p до m — рівно 1 крок
    dist = {}
    q = deque([c])
    dist[c] = 0
    while q:
        u = q.popleft()
        if u == p:
            return str(dist[u] + 1)
        for v in range(1, u + 2):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return "-1"

def run_stress(iterations: int = 50):
    print(f"Запуск {iterations} стрес-тестів для Problem G...")
    for it in range(iterations):
        val_n = random.randint(1, 1000)
        val_m = random.randint(1, 1000)
        n_str = bin(val_n)[2:]
        m_str = bin(val_m)[2:]
        
        expected = bfs_min_moves(n_str, m_str)
        inp = f"{n_str} {m_str}"
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        actual = res.stdout.strip()
        
        if actual != expected:
            print(f"❌ FAIL на тесті #{it+1}: {n_str} -> {m_str}")
            print(f"Очікувалось: {expected}, отримано: {actual}")
            sys.exit(1)
            
    print("✅ Усі 50 стрес-тестів для Problem G пройдено!")

if __name__ == "__main__":
    run_stress(50)
