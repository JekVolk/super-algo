import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]

    if mode == "ENCODE":
        n = int(tokens[1])
        vals = tokens[2:2+n]
        sys.stdout.write(",".join(vals) + "\n")
    elif mode == "DECODE":
        encoded = tokens[1]
        vals = encoded.split(",")
        sys.stdout.write(" ".join(vals) + "\n")

if __name__ == "__main__":
    main()
