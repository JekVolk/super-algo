import sys

def query(x: int, y: int) -> str:
    print(f"? {x} {y}", flush=True)
    resp = sys.stdin.readline().strip()
    if not resp:
        sys.exit(0)
    return resp

def solve_j(n: int) -> tuple[int, int]:
    A = 0
    B = 0
    c = query(0, 0)
    
    for j in range(n - 1, -1, -1):
        bit = 1 << j
        if c == "=":
            r = query(A ^ bit, B)
            if r == "<":
                A |= bit
                B |= bit
        else:
            if j == 0:
                if c == ">":
                    A |= bit
                else:
                    B |= bit
                break
                
            r1 = query(A ^ bit, B)
            r2 = query(A, B ^ bit)
            if r1 == r2:
                if c == ">":
                    A |= bit
                else:
                    B |= bit
                c = r1
            else:
                if r1 == "<":
                    A |= bit
                    B |= bit
                    
    return A, B

def main():
    line = sys.stdin.readline().strip()
    if not line:
        return
    n = int(line)
    A, B = solve_j(n)
    print(f"! {A} {B}", flush=True)

if __name__ == "__main__":
    main()
