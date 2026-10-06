import subprocess
import sys
import os

TEST_CASES = [
    ("1\n1 10 50", "50"),
    ("3\n1 5 10\n1 5 20\n1 5 30", "60"),
    ("4\n1 5 10\n1 5 20\n1 5 30\n1 5 40", "90"),
    ("4\n1 3 10\n3 5 20\n1 5 25\n2 4 5", "55")
]

def test_py():
    print("Testing Python solution for Problem L...")
    for inp, expected in TEST_CASES:
        p = subprocess.run(
            [sys.executable, "solution.py"],
            input=inp,
            text=True,
            capture_output=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        res = p.stdout.strip()
        assert res == expected, f"Failed for input:\n{inp}\nExpected: {expected}, Got: {res}"
    print("Python tests PASSED for Problem L!")

if __name__ == "__main__":
    test_py()
