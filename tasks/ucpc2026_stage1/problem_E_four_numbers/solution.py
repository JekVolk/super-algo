import sys

# Задача E: Чотири числа (UCPC 2026 Stage 1)
# Метод: Meet-in-the-Middle + Два Вказівники за O(N^2 log N)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])
    a = [int(x) for x in input_data[2:2 + n]]

    # 1. Попарні суми
    p = []
    for i in range(n):
        for j in range(i, n):
            p.append(a[i] + a[j])

    # 2. Сортування
    p.sort()

    # 3. Два вказівники
    best_sum = None
    l = 0
    r = len(p) - 1

    while l <= r:
        cur = p[l] + p[r]
        if cur <= m:
            if best_sum is None or cur > best_sum:
                best_sum = cur
            l += 1
        else:
            r -= 1

    if best_sum is not None:
        print(best_sum)
    else:
        print(-1)

if __name__ == "__main__":
    solve()
