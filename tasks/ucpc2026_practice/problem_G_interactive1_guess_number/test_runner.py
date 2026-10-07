import subprocess
import sys
import threading
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_interactor(hidden_target: int, n: int):
    prob_dir = Path(__file__).parent
    sol_py = prob_dir / "solution.py"

    proc = subprocess.Popen(
        [sys.executable, str(sol_py)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    # Спочатку надсилаємо n
    proc.stdin.write(f"{n}\n")
    proc.stdin.flush()

    queries = 0
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        cmd = parts[0]
        val = int(parts[1])

        if cmd == "?":
            queries += 1
            if val == hidden_target:
                proc.stdin.write("=\n")
            elif val > hidden_target:
                proc.stdin.write("<\n")
            else:
                proc.stdin.write(">\n")
            proc.stdin.flush()
        elif cmd == "!":
            proc.wait()
            assert val == hidden_target, f"Отримано {val}, очікувалось {hidden_target}"
            return queries

    proc.wait()
    return queries

def main():
    test_cases = [
        (42, 100),
        (1, 100),
        (100, 100),
        (777, 1000000),
    ]

    for target, n in test_cases:
        q = test_interactor(target, n)
        print(f"Тест n={n}, target={target}: PASSED за {q} запитів")

    print("\n✅ Всі інтерактивні тести для задачі G успішно пройдено!")

if __name__ == "__main__":
    main()
