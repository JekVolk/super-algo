import subprocess
import sys
import os
import math

TEST_CASES = [
    1.0,
    2.0,
    -2.0,
    2.5,
    0.0,
    0.5,
    -1.5,
    100.0
]

def test_py():
    print("Testing Python solution for Problem K...")
    for s in TEST_CASES:
        p = subprocess.run(
            [sys.executable, "solution.py"],
            input=str(s),
            text=True,
            capture_output=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        lines = p.stdout.strip().splitlines()
        n = int(lines[0])
        vals = [float(x) for x in lines[1].split()]
        assert len(vals) == n, f"Expected {n} values, got {len(vals)}"
        val_sum = sum(vals)
        val_prod = math.prod(vals)
        assert abs(val_sum - s) < 1e-7, f"Sum mismatch for s={s}: expected {s}, got {val_sum}"
        assert abs(val_prod - 1.0) < 1e-7, f"Prod mismatch for s={s}: expected 1.0, got {val_prod}"
    print("Python tests PASSED for Problem K!")

if __name__ == "__main__":
    test_py()
