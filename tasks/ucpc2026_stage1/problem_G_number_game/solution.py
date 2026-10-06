import sys

def solve_g(s_n: str, s_m: str) -> int:
    s_n = s_n.strip()
    s_m = s_m.strip()
    
    if s_n == s_m:
        return 0
    if s_m == "1":
        return -1
        
    c = s_n.count("1")
    pop_m = s_m.count("1")
    tz = len(s_m) - len(s_m.rstrip("0"))
    p = pop_m - 1 + tz
    
    if c == p:
        return 1
    elif c > p:
        return 2
    else:
        return p - c + 1

def main():
    lines = sys.stdin.read().split()
    if not lines:
        return
    idx = 0
    while idx < len(lines):
        s_n = lines[idx]
        s_m = lines[idx + 1]
        idx += 2
        print(solve_g(s_n, s_m))

if __name__ == "__main__":
    main()
