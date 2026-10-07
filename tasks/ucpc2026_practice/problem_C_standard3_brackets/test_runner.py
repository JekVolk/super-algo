import subprocess
import sys
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TESTS = [
    ("()\n", "YES\n"),
    ("()[]{}\n", "YES\n"),
    ("([{}])\n", "YES\n"),
    ("(\n", "NO\n"),
    (")\n", "NO\n"),
    ("([)]\n", "NO\n"),
    ("{[(])}\n", "NO\n"),
    ("(((())))\n", "YES\n"),
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

    print(f"\n✅ Всі {passed} тести для задачі C (Standard3: Дужки) успішно пройдено!")

if __name__ == "__main__":
    main()
