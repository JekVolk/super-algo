import sys

MOD = 10**9 + 7

def solve_h(n: int, k: int) -> int:
    if n <= 0:
        return 0
    k %= MOD
    u = [0] * (n + 1)
    u[1] = k
    for i in range(2, n + 1):
        if i % 2 == 1:
            u[i] = (k * u[i - 1]) % MOD
        else:
            m = i // 2
            u[i] = (k * u[i - 1] - u[m]) % MOD
    return u[n]

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    idx = 0
    while idx < len(input_data):
        n = int(input_data[idx])
        k = int(input_data[idx + 1])
        idx += 2
        print(solve_h(n, k))

if __name__ == "__main__":
    main()
