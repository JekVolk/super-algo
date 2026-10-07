import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TEST_CASES = [
    ("1 2", "2"),
    ("2 2", "2"),
    ("3 2", "4"),
    ("4 2", "6"),
    ("5 3", "144")
]

def test_py():
    print("Testing Python solution for Problem H...")
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
    print("Python tests PASSED for Problem H!")

if __name__ == "__main__":
    test_py()
