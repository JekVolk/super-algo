import sys

# Задача M: Гірлянда UCPC (UCPC 2026 Stage 1)
# Метод: Два жадібні проходи за O(N)

MOD = 10**9 + 7

def power3(exp):
    return pow(3, exp, MOD)

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    n = len(s)
    target = "UCPC"

    # 1. Greedy left
    L = [-1, -1, -1, -1]
    cur = 0
    for i in range(n):
        if cur < 4 and s[i] == target[cur]:
            L[cur] = i
            cur += 1

    # Якщо "UCPC" не входить узагалі — будь-яке розфарбування підходить
    if L[3] == -1:
        print(power3(n))
        return

    # 2. Greedy right
    R = [-1, -1, -1, -1]
    cur = 3
    for i in range(n - 1, -1, -1):
        if cur >= 0 and s[i] == target[cur]:
            R[cur] = i
            cur -= 1

    # 3. Вільні лампи
    is_role = [False] * n
    for i in range(n):
        for j in range(4):
            if s[i] == target[j] and L[j] <= i <= R[j]:
                is_role[i] = True

    free_lamps = sum(1 for i in range(n) if not is_role[i])

    # 4. Перевірка на спільну лампу для ролей 2 та 4
    # Лампа грає обидві ролі 2 ('C') та 4 ('C') тоді й лише тоді, коли L[3] <= R[1]
    clash = (L[3] <= R[1])

    if clash:
        ans = power3(free_lamps + 3)
    else:
        ans = power3(free_lamps + 4)

    print(ans)

if __name__ == "__main__":
    solve()
