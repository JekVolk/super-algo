import sys
import math

def solve_k(s: float) -> list[float]:
    if abs(s - 1.0) < 1e-12:
        return [1.0]
    if abs(s) >= 2.0 - 1e-12:
        D = max(0.0, s * s - 4.0)
        sign = 1.0 if s >= 0 else -1.0
        y = sign * (abs(s) + math.sqrt(D)) / 2.0
        return [y, 1.0 / y]
    else:
        D = (s + 1.0) ** 2 + 4.0
        y = ((s + 1.0) + math.sqrt(D)) / 2.0
        z = ((s + 1.0) - math.sqrt(D)) / 2.0
        return [-1.0, y, z]

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    for item in input_data:
        s = float(item)
        res = solve_k(s)
        print(len(res))
        print(*(f"{x:.15f}" for x in res))

if __name__ == "__main__":
    main()
