import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_interactive_test(n, target_a, target_b):
    p = subprocess.Popen(
        [sys.executable, "solution.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    # Send n
    p.stdin.write(f"{n}\n")
    p.stdin.flush()
    
    query_count = 0
    max_queries = 2 * n
    
    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = line.strip()
        if line.startswith("?"):
            parts = line.split()
            x = int(parts[1])
            y = int(parts[2])
            query_count += 1
            va = target_a ^ x
            vb = target_b ^ y
            if va > vb:
                resp = ">\n"
            elif va < vb:
                resp = "<\n"
            else:
                resp = "=\n"
            p.stdin.write(resp)
            p.stdin.flush()
        elif line.startswith("!"):
            parts = line.split()
            found_a = int(parts[1])
            found_b = int(parts[2])
            assert found_a == target_a, f"Expected A={target_a}, got {found_a}"
            assert found_b == target_b, f"Expected B={target_b}, got {found_b}"
            assert query_count <= max_queries, f"Queries {query_count} exceeded {max_queries}"
            p.terminate()
            return query_count

def test_py():
    print("Testing Interactive Python solution for Problem J...")
    tests = [
        (4, 5, 3),
        (5, 0, 0),
        (6, 15, 15),
        (8, 100, 200),
        (10, 512, 1023)
    ]
    for n, a, b in tests:
        q = run_interactive_test(n, a, b)
        print(f"Passed n={n}, A={a}, B={b} in {q} queries (limit {2*n})")
    print("Interactive tests PASSED for Problem J!")

if __name__ == "__main__":
    test_py()
