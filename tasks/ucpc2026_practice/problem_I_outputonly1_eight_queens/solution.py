import sys

BOARD = [
    "Q . . . . . . .",
    ". . . . Q . . .",
    ". . . . . . . Q",
    ". . . . . Q . .",
    ". . Q . . . . .",
    ". . . . . . Q .",
    ". Q . . . . . .",
    ". . . Q . . . ."
]

def main():
    for row in BOARD:
        sys.stdout.write(row + "\n")

if __name__ == "__main__":
    main()
