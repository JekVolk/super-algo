from typing import List

def max_pair_sum(a: List[int]) -> int:
    """Знаходить максимальну суму двох різних елементів масиву за O(N)."""
    if len(a) < 2:
        return 0

    max1 = float('-inf')
    max2 = float('-inf')

    for x in a:
        if x > max1:
            max2 = max1
            max1 = x
        elif x > max2:
            max2 = x

    return int(max1 + max2)

if __name__ == "__main__":
    import sys
    tokens = sys.stdin.read().split()
    if tokens:
        n = int(tokens[0])
        nums = [int(x) for x in tokens[1:n+1]]
        print(max_pair_sum(nums))
