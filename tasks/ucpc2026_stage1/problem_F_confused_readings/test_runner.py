import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def generate_test(orig):
    n = len(orig)
    all_vals = []
    for mask in range(1, 1 << n):
        s = sum(orig[i] for i in range(n) if (mask & (1 << i)))
        o = 0
        for i in range(n):
            if mask & (1 << i):
                o |= orig[i]
        all_vals.extend([s, o])
    all_vals.sort()
    inp = f"{n}\n" + " ".join(map(str, all_vals))
    expected = " ".join(map(str, orig))
    return inp, expected

TEST_CASES = [
    generate_test([5]),
    generate_test([3, 5]),
    generate_test([2, 2]),
    generate_test([1, 4, 6])
]

def test_py():
    print("Testing Python solution for Problem F...")
    for inp, expected in TEST_CASES:
        p = subprocess.run(
            [sys.executable, "solution.py"],
            input=inp,
            text=True,
            capture_output=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        res = p.stdout.strip()
        assert res == expected, f"Failed for input: expected '{expected}', got '{res}'"
    print("Python tests PASSED for Problem F!")

if __name__ == "__main__":
    test_py()
