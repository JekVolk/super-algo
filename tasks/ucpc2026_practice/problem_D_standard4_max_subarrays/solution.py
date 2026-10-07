import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:n+1]]

    # L[i]: перший індекс зліва, де a[idx] > a[i]
    L = [-1] * n
    stack = []
    for i in range(n):
        while stack and a[stack[-1]] <= a[i]:
            stack.pop()
        L[i] = stack[-1] if stack else -1
        stack.append(i)

    # R[i]: перший індекс справа, де a[idx] >= a[i] (для суворих пар без дублікатів)
    R = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] < a[i]:
            stack.pop()
        R[i] = stack[-1] if stack else n
        stack.append(i)

    total_sum = 0
    for i in range(n):
        left_count = i - L[i]
        right_count = R[i] - i
        total_sum += a[i] * left_count * right_count

    sys.stdout.write(f"{total_sum}\n")

if __name__ == "__main__":
    main()
