import sys

# Задача A: Антивірус (UCPC 2026 Stage 1)
# Складність: O(N + K) за часом, O(N) за пам'яттю

def solve():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return

    n = int(data[0])
    k = int(data[1])

    idx = 2
    # a[v] — батько для папки v (v = 2..n)
    # Зберігаємо 1-indexed масив
    a = [0] * (n + 1)
    for v in range(2, n + 1):
        a[v] = int(data[idx])
        idx += 1

    # b[v] — залишкова сила сканування (-1 якщо не сканується)
    b = [-1] * (n + 1)
    for _ in range(k):
        c = int(data[idx])
        d = int(data[idx + 1])
        idx += 2
        if d > b[c]:
            b[c] = d

    # Однопрохідний спуск по дереву зверху вниз (оскільки a[v] < v)
    for v in range(1, n + 1):
        parent = a[v]
        if parent > 0 and b[parent] > 0:
            remaining = b[parent] - 1
            if remaining > b[v]:
                b[v] = remaining

    # Кількість перевірених папок (де b[v] >= 0)
    ans = sum(1 for v in range(1, n + 1) if b[v] >= 0)
    print(ans)

if __name__ == "__main__":
    solve()
