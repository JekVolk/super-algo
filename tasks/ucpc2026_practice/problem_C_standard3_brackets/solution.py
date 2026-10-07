import sys

def is_balanced(s: str) -> bool:
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in matching.values():
            stack.append(ch)
        elif ch in matching:
            if not stack or stack[-1] != matching[ch]:
                return False
            stack.pop()
    return len(stack) == 0

def main():
    lines = sys.stdin.read().split()
    for s in lines:
        if is_balanced(s):
            sys.stdout.write("YES\n")
        else:
            sys.stdout.write("NO\n")

if __name__ == "__main__":
    main()
