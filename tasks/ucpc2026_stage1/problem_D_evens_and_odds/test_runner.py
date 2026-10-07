import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TEST_CASES = [
    ("4", "4"),
    ("12", "12"),
    ("5", "50"),
    ("135", "13560"),
    ("2468", "2468309")
]

def check_balanced(s: str) -> int:
    s_rev = s[::-1]
    contrib = 0
    for pos, ch in enumerate(s_rev):
        d = int(ch)
        if pos % 2 == 0:
            if d % 2 == 1:
                contrib += d
        else:
            if d % 2 == 0:
                contrib -= d
    return contrib

def test_py():
    print("Testing Python solution for Problem D...")
    for inp, expected in TEST_CASES:
        p = subprocess.run(
            [sys.executable, "solution.py"],
            input=inp,
            text=True,
            capture_output=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        res = p.stdout.strip()
        assert res == expected, f"Failed for {inp}: expected {expected}, got {res}"
        assert check_balanced(res) == 0, f"Result {res} is not balanced!"
    print("Python tests PASSED for Problem D!")

if __name__ == "__main__":
    test_py()
