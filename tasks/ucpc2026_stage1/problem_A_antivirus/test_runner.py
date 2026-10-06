import subprocess
import sys
from pathlib import Path

def run():
    folder = Path(__file__).parent
    inputs = sorted(folder.glob("input*.txt"))
    target = sys.argv[1] if len(sys.argv) > 1 else "solution.py"
    print(f"=== Перевірка {target} для Задачі A: Антивірус ===")
    
    passed = 0
    for inp in inputs:
        idx = inp.stem.replace("input", "")
        out = folder / f"output{idx}.txt"
        if not out.exists():
            continue
        
        with open(inp, "r", encoding="utf-8") as f:
            in_data = f.read()
        with open(out, "r", encoding="utf-8") as f:
            expected = f.read().strip()

        if target.endswith(".py"):
            cmd = [sys.executable, str(folder / target)]
        else:
            exe = folder / "sol_exe"
            subprocess.run(["g++", "-O3", str(folder / target), "-o", str(exe)], check=True)
            cmd = [str(exe)]

        res = subprocess.run(cmd, input=in_data, text=True, capture_output=True)
        actual = res.stdout.strip()

        if actual == expected:
            print(f" Тест #{idx}: PASSED")
            passed += 1
        else:
            print(f"❌ Тест #{idx}: FAILED")
            print(f"   Очікувалось: '{expected}'")
            print(f"   Отримано:    '{actual}'")

    if passed == len(inputs):
        print(f" Всі {passed} тести пройдено успішно!\n")

if __name__ == "__main__":
    run()
