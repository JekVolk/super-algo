import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])
    a = [int(x) for x in input_data[2:2 + n]]

    cur_sum = sum(a[:k])
    max_sum = cur_sum

    for i in range(k, n):
        cur_sum += a[i] - a[i - k]
        if cur_sum > max_sum:
            max_sum = cur_sum

    print(max_sum)

if __name__ == "__main__":
    solve()
