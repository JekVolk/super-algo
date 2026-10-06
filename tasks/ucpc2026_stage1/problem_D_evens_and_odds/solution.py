import sys

def check_balanced(s: str) -> int:
    s_rev = s[::-1]
    contrib = 0
    for pos, ch in enumerate(s_rev):
        d = int(ch)
        if pos % 2 == 0:
            if d % 2 == 1:
                contrib += d
        else:
            if d % 2 == 0:
                contrib -= d
    return contrib

def can_solve(rem_e: int, rem_o: int, T: int) -> bool:
    p = T % 2
    if p == 0:
        E_p = rem_e if rem_e % 2 == 0 else rem_e - 1
    else:
        E_p = rem_e if rem_e % 2 == 1 else rem_e - 1
        
    if E_p < p:
        if p == 1 or rem_e < 0:
            return False
            
    low_x = p
    high_x = 9 * E_p
    low_req = max(T, low_x)
    high_req = min(T + 8 * rem_o, high_x)
    return low_req <= high_req

def solve_d(N: str) -> str:
    N = N.strip()
    if not N:
        return ""
        
    N_rev = N[::-1]
    d0 = 0
    d1 = 0
    for pos, ch in enumerate(N_rev):
        d = int(ch)
        if pos % 2 == 0:
            if d % 2 == 1: d0 += d
        else:
            if d % 2 == 0: d0 -= d
            
        if (pos + 1) % 2 == 0:
            if d % 2 == 1: d1 += d
        else:
            if d % 2 == 0: d1 -= d
            
    if d0 == 0:
        return N
        
    max_k = len(N) + 120
    for k in range(1, max_k):
        shift_parity = k % 2
        T = -d0 if shift_parity == 0 else -d1
        e = (k + 1) // 2
        o = k // 2
        if can_solve(e, o, T):
            block = []
            curr_T = T
            cur_e = e
            cur_o = o
            for pos in range(k - 1, -1, -1):
                is_even = (pos % 2 == 0)
                next_e = cur_e - (1 if is_even else 0)
                next_o = cur_o - (1 if not is_even else 0)
                
                for d in range(10):
                    if is_even:
                        add = d if d % 2 == 1 else 0
                        nxt_T = curr_T - add
                    else:
                        sub = d if d % 2 == 0 else 0
                        nxt_T = curr_T + sub
                    if can_solve(next_e, next_o, nxt_T):
                        block.append(str(d))
                        curr_T = nxt_T
                        cur_e = next_e
                        cur_o = next_o
                        break
            return N + "".join(block)
    return N

def main():
    lines = sys.stdin.read().split()
    for token in lines:
        print(solve_d(token))

if __name__ == "__main__":
    main()
