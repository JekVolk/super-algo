import subprocess
import sys
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TESTS = [
    [1, 2, 3, 4, 5],
    [42],
    [-10, 0, 100, -500],
    [1000000000, 999999999],
]

def main():
    prob_dir = Path(__file__).parent
    sol_py = prob_dir / "solution.py"

    passed = 0
    for idx, original in enumerate(TESTS, 1):
        # 1. Етап кодування
        encode_inp = f"ENCODE {len(original)} " + " ".join(map(str, original)) + "\n"
        enc_proc = subprocess.run(
            [sys.executable, str(sol_py)],
            input=encode_inp,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        encoded_str = enc_proc.stdout.strip()

        # 2. Етап декодування
        decode_inp = f"DECODE {encoded_str}\n"
        dec_proc = subprocess.run(
            [sys.executable, str(sol_py)],
            input=decode_inp,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        decoded_vals = [int(x) for x in dec_proc.stdout.strip().split()]

        if decoded_vals == original:
            passed += 1
            print(f"Тест #{idx}: PASSED (Закодовано -> Декодовано успішно)")
        else:
            print(f"Тест #{idx}: FAILED! Отримано {decoded_vals}, очікувалось {original}")
            sys.exit(1)

    print(f"\n✅ Всі {passed} тести для задачі H (MultipleRun1: Закодуй і розкодуй) успішно пройдено!")

if __name__ == "__main__":
    main()
