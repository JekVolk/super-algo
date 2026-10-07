import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TEST_CASES = [
    ("5 1 1 1 1", "YES"),
    ("4 0 0 2 1", "NO"),
    ("3 0 0 2 0", "YES"),
    ("6 2 1 1 1", "YES"),
    ("6 3 1 1 0", "NO"),
    ("1 0 0 0 0", "YES"),
    ("2 1 0 0 0", "YES"),
    ("2 0 1 0 0", "YES"),
]

def test_py():
    print("Testing Python solution for Problem N...")
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
    print("Python tests PASSED for Problem N!")

if __name__ == "__main__":
    test_py()
