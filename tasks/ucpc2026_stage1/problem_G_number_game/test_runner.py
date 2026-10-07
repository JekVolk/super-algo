import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TEST_CASES = [
    ("10 11", "1"),
    ("1 1", "0"),
    ("10 1", "-1"),
    ("111 100", "2"),
    ("1 1111", "3"),
    ("1000 1", "-1"),
    ("10101 10101", "0"),
    ("11 110", "1"),
    ("11 1000", "2"),
]

def test_py():
    print("Testing Python solution for Problem G...")
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
    print("Python tests PASSED for Problem G!")

if __name__ == "__main__":
    test_py()
