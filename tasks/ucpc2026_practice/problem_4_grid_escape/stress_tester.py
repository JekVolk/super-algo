"""
stress_tester.py — генератор випадкових лабіринтів для задачі 4 (Grid Escape)
Порівнює швидке BFS-рішення з еталонним.

Запуск:
    python stress_tester.py
"""
import random
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SOLUTION = Path(__file__).parent / "solution.py"


def generate_maze(n: int, m: int, wall_prob: float = 0.3) -> str:
    """
    Генерує випадковий лабіринт N×M.
    wall_prob — ймовірність, що клітинка є стіною '#'.
    S та E завжди розміщуються у кутах (не можуть бути стіною).
    """
    grid = []
    for r in range(n):
        row = []
        for c in range(m):
            # Кути завжди вільні (для S та E)
            if (r, c) in [(0, 0), (n - 1, m - 1)]:
                row.append(".")
            else:
                row.append("#" if random.random() < wall_prob else ".")
        grid.append("".join(row))

    # Розміщуємо S та E у протилежних кутах
    grid[0] = "S" + grid[0][1:]
    grid[n - 1] = grid[n - 1][:-1] + "E"

    header = f"{n} {m}"
    return header + "\n" + "\n".join(grid)


def brute_force_bfs(input_str: str) -> int:
    """Еталонне BFS-рішення (довірений розв'язувач)."""
    from collections import deque

    lines = input_str.split()
    n, m = int(lines[0]), int(lines[1])
    grid = lines[2 : 2 + n]

    start = target = None
    for r in range(n):
        for c in range(m):
            if grid[r][c] == "S":
                start = (r, c)
            if grid[r][c] == "E":
                target = (r, c)

    if not start or not target:
        return -1

    dist = [[-1] * m for _ in range(n)]
    q = deque([start])
    dist[start[0]][start[1]] = 0
    dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]

    while q:
        r, c = q.popleft()
        if (r, c) == target:
            return dist[r][c]
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if (
                0 <= nr < n
                and 0 <= nc < m
                and grid[nr][nc] != "#"
                and dist[nr][nc] == -1
            ):
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return -1


def run_stress(iterations: int = 200) -> None:
    print(f"Запускаємо {iterations} стрес-тестів...")
    for i in range(iterations):
        n = random.randint(1, 15)
        m = random.randint(1, 15)
        wall_prob = random.uniform(0.1, 0.5)
        inp = generate_maze(n, m, wall_prob)

        expected = str(brute_force_bfs(inp))
        res = subprocess.run(
            [sys.executable, str(SOLUTION)],
            input=inp,
            text=True,
            capture_output=True,
        )
        actual = res.stdout.strip()

        if actual != expected:
            print(f"❌ ЗНАЙДЕНО РОЗБІЖНІСТЬ на тесті #{i + 1}!")
            print(f"Вхід:\n{inp}")
            print(f"Очікувалось: {expected}")
            print(f"Отримано:    {actual}")
            return

        if (i + 1) % 50 == 0:
            print(f"  ✓ {i + 1}/{iterations} тестів пройдено...")

    print("✅ Усі стрес-тести пройшли!")


if __name__ == "__main__":
    run_stress(200)
