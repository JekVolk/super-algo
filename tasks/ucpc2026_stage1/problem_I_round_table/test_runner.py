import subprocess
import sys
import os

TEST_CASES = [
    ("4 2\n1 2\n3 4", "2"),
    ("4 2\n1 3\n2 4", "1"),
    ("4 2\n4 1\n2 3", "2"),
    ("6 3\n1 2\n3 4\n5 6", "3"),
    ("4 1\n1 4", "1")
]

def test_py():
    print("Testing Python solution for Problem I...")
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
    print("Python tests PASSED for Problem I!")

if __name__ == "__main__":
    test_py()
