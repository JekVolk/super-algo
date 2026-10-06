import sys

# Precompute pairs for small m < 10000
def digit_sum(n: int) -> int:
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    return s

def is_harshad(n: int) -> bool:
    return n % digit_sum(n) == 0

# Precompute small Harshad pairs
SMALL_PAIRS = []
for x in range(1, 20005):
    if is_harshad(x) and is_harshad(x + 1):
        SMALL_PAIRS.append(x)

def solve_one(s_m: str) -> str:
    s_m = s_m.strip()
    if not s_m:
        return ""
    
    # If m fits in small range
    if len(s_m) < 5:
        m = int(s_m)
        for x in SMALL_PAIRS:
            if x >= m:
                if x + 1 <= 2 * m:
                    return str(x)
                else:
                    return "-1"
        return "-1"
    
    # Large m: length L >= 5
    L = len(s_m)
    B = L - 2 # B >= 3
    p = int(s_m[:2])
    
    if 10 <= p <= 16:
        c = 17
    elif 17 <= p <= 25:
        c = 26
    elif 26 <= p <= 34:
        c = 35
    elif 35 <= p <= 61:
        c = 62
    else: # 62 <= p <= 99
        c = 107
        
    return str(c) + ("0" * B)

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    # First token might be T or single test
    # If first token is integer T and matches count of remaining items
    try:
        t = int(input_data[0])
        if len(input_data) == t + 1:
            tests = input_data[1:]
        else:
            tests = input_data
    except ValueError:
        tests = input_data
        
    for item in tests:
        print(solve_one(item))

if __name__ == "__main__":
    main()
