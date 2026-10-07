import sys

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i: int, delta: int):
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [0] + [int(x) for x in input_data[1:n+1]]

    idx = n + 1
    if idx >= len(input_data):
        return
    q = int(input_data[idx])
    idx += 1

    queries = []
    for qid in range(q):
        l = int(input_data[idx])
        r = int(input_data[idx+1])
        idx += 2
        queries.append((l, r, qid))

    queries.sort(key=lambda item: item[1])

    ft = Fenwick(n)
    last_pos = {}
    ans = [0] * q

    cur_r = 1
    for l, r, qid in queries:
        while cur_r <= r:
            val = a[cur_r]
            if val in last_pos:
                ft.add(last_pos[val], -1)
            ft.add(cur_r, 1)
            last_pos[val] = cur_r
            cur_r += 1
        ans[qid] = ft.query(r) - ft.query(l - 1)

    sys.stdout.write("\n".join(map(str, ans)) + "\n")

if __name__ == "__main__":
    main()
