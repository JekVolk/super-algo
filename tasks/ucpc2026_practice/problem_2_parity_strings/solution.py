import sys
from collections import Counter

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    counts = Counter(s)
    odd = sum(1 for c in counts.values() if c % 2 != 0)
    print("YES" if odd <= 1 else "NO")

if __name__ == "__main__":
    solve()
