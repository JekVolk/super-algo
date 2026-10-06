import subprocess
import sys
import os

TEST_CASES = [
    ("1", "1"),
    ("10", "-1"),
    ("21", "-1"),
    ("41", "80"),
    ("100", "110"),
    ("12345", "17000"),
    ("99999", "107000")
]

def test_py():
    print("Testing Python solution for Problem B...")
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
    print("Python tests PASSED!")

if __name__ == "__main__":
    test_py()
