import sys

def main():
    line = sys.stdin.readline().strip()
    if not line:
        return
    n = int(line)

    low = 1
    high = n

    while low <= high:
        mid = (low + high) // 2
        sys.stdout.write(f"? {mid}\n")
        sys.stdout.flush()

        resp = sys.stdin.readline().strip()
        if not resp:
            break

        if resp in ("=", "CORRECT"):
            sys.stdout.write(f"! {mid}\n")
            sys.stdout.flush()
            break
        elif resp in ("<", "LESS"):
            high = mid - 1
        elif resp in (">", "GREATER"):
            low = mid + 1

if __name__ == "__main__":
    main()
