import subprocess
import sys
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TESTS = [
    # 3 вершини, 2 ребра: 1-2 вага 10, 2-3 вага 20 -> квиток на 2-3 дає 10
    ("3 2\n1 2 10\n2 3 20\n", "10\n"),
    # Пряме важке ребро 1-3 вага 50, обхідне 1-2 (5), 2-3 (5) -> квиток на пряме дає 0!
    ("3 3\n1 3 50\n1 2 5\n2 3 5\n", "0\n"),
    # Граф незв'язний
    ("3 1\n1 2 10\n", "-1\n"),
    # 4 вершини
    ("4 4\n1 2 10\n2 4 10\n1 3 100\n3 4 10\n", "10\n"),
]

def main():
    prob_dir = Path(__file__).parent
    sol_py = prob_dir / "solution.py"

    passed = 0
    for idx, (inp, expected) in enumerate(TESTS, 1):
        proc = subprocess.run(
            [sys.executable, str(sol_py)],
            input=inp,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        out = proc.stdout.strip()
        exp = expected.strip()
        if out == exp:
            passed += 1
            print(f"Тест #{idx}: PASSED")
        else:
            print(f"Тест #{idx}: FAILED! Отримано: {out!r}, Очікувалось: {exp!r}")
            sys.exit(1)

    print(f"\n✅ Всі {passed} тести для задачі E (Standard5: Один безкоштовний квиток) успішно пройдено!")

if __name__ == "__main__":
    main()
