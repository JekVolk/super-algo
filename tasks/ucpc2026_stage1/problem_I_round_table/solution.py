import sys

def solve_i(n: int, m: int, segments: list[tuple[int, int]]) -> int:
    unrolled = []
    for l, r in segments:
        if l <= r:
            unrolled.append((l, r))
            unrolled.append((l + n, r + n))
        else:
            unrolled.append((l, r + n))
            unrolled.append((l + n, r + 2 * n))
            
    min_end = [10**9] * (2 * n + 2)
    for l, r in unrolled:
        if l <= 2 * n:
            if r < min_end[l]:
                min_end[l] = r
                
    best_end = [10**9] * (2 * n + 3)
    for x in range(2 * n, 0, -1):
        best_end[x] = min(best_end[x + 1], min_end[x])
        
    nxt = [2 * n + 1] * (2 * n + 2)
    for x in range(1, 2 * n + 1):
        if best_end[x] <= 2 * n:
            nxt[x] = best_end[x] + 1
        else:
            nxt[x] = 2 * n + 1
            
    LOGN = 20
    up = [[2 * n + 1] * (2 * n + 2) for _ in range(LOGN)]
    for x in range(1, 2 * n + 2):
        up[0][x] = nxt[x]
        
    for j in range(1, LOGN):
        for x in range(1, 2 * n + 2):
            up[j][x] = up[j - 1][up[j - 1][x]]
            
    ans = 0
    for p in range(1, n + 1):
        curr = p
        count = 0
        limit = p + n
        for j in range(LOGN - 1, -1, -1):
            if up[j][curr] <= limit:
                count += (1 << j)
                curr = up[j][curr]
        if count > ans:
            ans = count
            
    return ans

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    idx = 0
    while idx < len(input_data):
        n = int(input_data[idx])
        m = int(input_data[idx + 1])
        idx += 2
        segs = []
        for _ in range(m):
            l = int(input_data[idx])
            r = int(input_data[idx + 1])
            idx += 2
            segs.append((l, r))
        print(solve_i(n, m, segs))

if __name__ == "__main__":
    main()
