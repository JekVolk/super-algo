import sys

# Задача C: Танок залишків (UCPC 2026 Stage 1)
# Складність: O(1) на тест

def solve():
    input = sys.stdin.read
    lines = input().split()
    if not lines:
        return
    n = int(lines[0])
    m = int(lines[1])
    k = int(lines[2])
    print(min(n, m, k))

if __name__ == "__main__":
    solve()
