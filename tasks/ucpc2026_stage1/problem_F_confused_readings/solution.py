import sys
import heapq

def solve_f(n: int, b: list[int]) -> list[int]:
    b.sort()
    heap = []
    a = []
    subsets_sum = [0]
    subsets_or = [0]
    
    for val in b:
        if heap and heap[0] == val:
            heapq.heappop(heap)
        else:
            x = val
            a.append(x)
            if len(a) == n:
                break
                
            new_sums = []
            new_ors = []
            for s, o in zip(subsets_sum, subsets_or):
                ns = s + x
                no = o | x
                new_sums.append(ns)
                new_ors.append(no)
                heapq.heappush(heap, ns)
                heapq.heappush(heap, no)
                
            # Pop one copy of x which corresponds to the current val
            heapq.heappop(heap)
            
            subsets_sum.extend(new_sums)
            subsets_or.extend(new_ors)
            
    return a

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    idx = 0
    while idx < len(input_data):
        n = int(input_data[idx])
        idx += 1
        num_elements = 2 * ((1 << n) - 1)
        b = [int(input_data[idx + i]) for i in range(num_elements)]
        idx += num_elements
        res = solve_f(n, b)
        print(*(res))

if __name__ == "__main__":
    main()
