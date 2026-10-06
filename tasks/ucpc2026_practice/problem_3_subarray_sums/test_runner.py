import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_tests():
    folder = Path(__file__).parent
    inputs = sorted(folder.glob("input*.txt"))
    if not inputs:
        print("Тестові файли не знайдено!")
        sys.exit(1)

    all_passed = True
    for inp in inputs:
        idx = inp.stem.replace("input", "")
        out = folder / f"output{idx}.txt"
        if not out.exists():
            continue

        with open(inp, "r", encoding="utf-8") as f:
            in_data = f.read()
        with open(out, "r", encoding="utf-8") as f:
            expected = f.read().strip()

        res = subprocess.run([sys.executable, str(folder / "solution.py")], input=in_data, text=True, capture_output=True)
        actual = res.stdout.strip()

        if actual == expected:
            print(f"Тест #{idx}: PASSED")
        else:
            all_passed = False
            print(f"❌ Тест #{idx}: FAILED")
            print(f"   Очікувалось:\n{expected}")
            print(f"   Отримано:\n{actual}")

    if all_passed:
        print("Всі тести для задачі 3 пройшли успішно!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
