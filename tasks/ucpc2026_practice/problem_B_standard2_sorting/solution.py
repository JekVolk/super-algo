import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:n+1]]
    a.sort()
    sys.stdout.write(" ".join(map(str, a)) + "\n")

if __name__ == "__main__":
    main()
