import subprocess
import sys
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def verify_board(lines):
    queens = []
    for r, line in enumerate(lines):
        tokens = line.strip().split()
        assert len(tokens) == 8, f"Рядок {r} має {len(tokens)} клітинок замість 8"
        for c, ch in enumerate(tokens):
            if ch == "Q":
                queens.append((r, c))

    assert len(queens) == 8, f"Знайдено {len(queens)} ферзів замість 8"

    # Перевірка на взаємні атаки
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            r1, c1 = queens[i]
            r2, c2 = queens[j]
            assert r1 != r2, f"Ферзі на одному рядку {r1}"
            assert c1 != c2, f"Ферзі на одному стовпчику {c1}"
            assert abs(r1 - r2) != abs(c1 - c2), f"Ферзі б'ють один одного по діагоналі: ({r1},{c1}) та ({r2},{c2})"
    return True

def main():
    prob_dir = Path(__file__).parent
    sol_py = prob_dir / "solution.py"

    proc = subprocess.run(
        [sys.executable, str(sol_py)],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    lines = [l for l in proc.stdout.strip().split("\n") if l.strip()]

    try:
        verify_board(lines)
        print("✅ Дошку 8x8 верифіковано: рівно 8 ферзів, жодної атаки по вертикалі, горизонталі чи діагоналях!")
    except AssertionError as e:
        print(f"❌ ПОМИЛКА ВЕРИФІКАЦІЇ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
