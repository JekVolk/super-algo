import sys

def solve_n(n: int, u: int, v: int, e: int, g: int) -> str:
    if u + v + 1 + e + g != n:
        return "NO"
    if abs(u - v) > 1:
        return "NO"
    if u == 0 and v == 0 and e > 0 and g > 0:
        return "NO"
    return "YES"

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    idx = 0
    while idx < len(input_data):
        n = int(input_data[idx])
        u = int(input_data[idx + 1])
        v = int(input_data[idx + 2])
        e = int(input_data[idx + 3])
        g = int(input_data[idx + 4])
        idx += 5
        print(solve_n(n, u, v, e, g))

if __name__ == "__main__":
    main()
