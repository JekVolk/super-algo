import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])
    grid = input_data[2:2 + n]

    start = None
    target = None

    for r in range(n):
        for c in range(m):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                target = (r, c)

    if not start or not target:
        print(-1)
        return

    dist = [[-1] * m for _ in range(n)]
    q = deque([start])
    dist[start[0]][start[1]] = 0

    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    while q:
        r, c = q.popleft()
        if (r, c) == target:
            print(dist[r][c])
            return

        cur_d = dist[r][c]
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#':
                if dist[nr][nc] == -1:
                    dist[nr][nc] = cur_d + 1
                    q.append((nr, nc))

    print(-1)

if __name__ == "__main__":
    solve()
