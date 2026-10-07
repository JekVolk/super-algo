"""
stress_tester.py — стрес-тест для Problem A: Антивірус (Antivirus)
Порівнює лінійне динамічне програмування b[v] = max(b[v], b[a[v]] - 1) 
з наївним BFS/DFS розповсюдженням від кожного запуску.
"""
import random
import subprocess
import sys
from collections import deque
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"

def naive_antivirus(n, k, a_list, queries):
    adj = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        p = a_list[v - 2]
        adj[p].append(v)
    
    visited = [False] * (n + 1)
    for c, d in queries:
        q = deque([(c, d)])
        visited[c] = True
        while q:
            u, cur_d = q.popleft()
            if cur_d > 0:
                for nxt in adj[u]:
                    visited[nxt] = True
                    q.append((nxt, cur_d - 1))
    return sum(visited[1:])

def run_stress(iterations: int = 50):
    print(f"Запуск {iterations} стрес-тестів для Problem A...")
    for it in range(iterations):
        n = random.randint(1, 30)
        a_list = [random.randint(1, v - 1) for v in range(2, n + 1)]
        k = random.randint(0, 10)
        queries = []
        for _ in range(k):
            c = random.randint(1, n)
            d = random.randint(0, 10)
            queries.append((c, d))
        
        expected = str(naive_antivirus(n, k, a_list, queries))
        
        lines = [f"{n} {k}"]
        if n > 1:
            lines.append(" ".join(map(str, a_list)))
        for c, d in queries:
            lines.append(f"{c} {d}")
        inp = "\n".join(lines)
        
        res = subprocess.run([sys.executable, str(SOLUTION)], input=inp, text=True, capture_output=True)
        actual = res.stdout.strip()
        if actual != expected:
            print(f"❌ FAIL на тесті #{it+1}!")
            print(f"Вхід:\n{inp}")
            print(f"Очікувалось: {expected}, отримано: {actual}")
            sys.exit(1)
    print("✅ Усі 50 стрес-тестів для Problem A пройдено!")

if __name__ == "__main__":
    run_stress(50)
