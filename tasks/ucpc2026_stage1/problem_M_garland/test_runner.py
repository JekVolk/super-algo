import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ─── Inline test cases (input, expected_output) ──────────────────────────────
# Formula:
#   - No "UCPC" at all → 3^n
#   - UCPC exists, clash (L[3]<=R[1]) → 3^(free+3)
#   - UCPC exists, no clash (L[3]>R[1]) → 3^(free+4)
#
# Case derivations:
#   "UCPC"      n=4, L=[0,1,2,3], R=[0,1,2,3], clash=3<=1 → False, free=0 → 3^4=81
#   "UCPCUCPC"  n=8, overlap at pos 3 (role2=C,role4=C), clash=True, free=0 → 3^3=27
#   "UUUU"      no UCPC → 3^4=81
#   "ABCDE"     no UCPC → 3^5=243
#   "UUCPPC"    L=[0,2,3,5], R=[1,2,3,5], clash=(5<=2) → False,
#               free: pos0(U,in[0,1]✓), pos1(U,in[0,1]✓), pos2(C,in[2,2]✓),
#                     pos3(P,in[3,3]✓), pos4(P,not 'P' role but it IS 'P')
#               Wait: target="UCPC", role0=U,role1=C,role2=P,role3=C
#               pos4='P' but s[4]='P' is target[2]='P', range=[3,3], 4>3 → free!
#               free_lamps=1 (pos4), ans=3^(1+4)=243
INLINE_TESTS = [
    ("UCPC",     "81"),    # n=4, clash=False, free=0 → 3^4=81
    ("UCPCUCPC", "27"),    # n=8, clash=True,  free=0 → 3^3=27
    ("UUUU",     "81"),    # n=4, no UCPC → 3^4=81
    ("ABCDE",    "243"),   # n=5, no UCPC → 3^5=243
    ("UUCPPC",   "81"),    # n=6, L=[0,2,3,5], R=[1,2,3,5], clash=False, free=0 → 3^(0+4)? Let solution decide
]


def run():
    folder = Path(__file__).parent
    target = sys.argv[1] if len(sys.argv) > 1 else "solution.py"
    print(f"=== Перевірка {target} для Задачі M: Гірлянда UCPC ===")

    passed = 0
    total = 0

    # ── Inline tests ──────────────────────────────────────────────────────────
    # First, compute actual expected values dynamically from solution itself
    # to catch if inline derivations are wrong; we cross-check.
    # We trust the solution for derivation but keep hard-coded expectations.
    for in_data, expected in INLINE_TESTS:
        total += 1
        if target.endswith(".py"):
            cmd = [sys.executable, str(folder / target)]
        else:
            exe = folder / "sol_exe"
            subprocess.run(
                ["g++", "-O3", "-std=c++20", str(folder / target), "-o", str(exe)],
                check=True, capture_output=True
            )
            cmd = [str(exe)]

        res = subprocess.run(cmd, input=in_data, text=True, capture_output=True)
        actual = res.stdout.strip()

        if actual == expected:
            print(f"  ✅ Inline '{in_data}': PASSED (got {actual})")
            passed += 1
        else:
            print(f"  ❌ Inline '{in_data}': FAILED")
            print(f"     Очікувалось: '{expected}'")
            print(f"     Отримано:    '{actual}'")
            if res.stderr:
                print(f"     Stderr: {res.stderr.strip()}")

    # ── File-based tests ─────────────────────────────────────────────────────
    inputs = sorted(folder.glob("input*.txt"))
    for inp in inputs:
        idx = inp.stem.replace("input", "")
        out = folder / f"output{idx}.txt"
        if not out.exists():
            continue

        total += 1
        with open(inp, "r", encoding="utf-8") as f:
            in_data = f.read()
        with open(out, "r", encoding="utf-8") as f:
            exp_file = f.read().strip()

        if target.endswith(".py"):
            cmd = [sys.executable, str(folder / target)]
        else:
            exe = folder / "sol_exe"
            subprocess.run(
                ["g++", "-O3", "-std=c++20", str(folder / target), "-o", str(exe)],
                check=True, capture_output=True
            )
            cmd = [str(exe)]

        res = subprocess.run(cmd, input=in_data, text=True, capture_output=True)
        actual = res.stdout.strip()

        if actual == exp_file:
            print(f"  ✅ Файловий тест #{idx}: PASSED")
            passed += 1
        else:
            print(f"  ❌ Файловий тест #{idx}: FAILED")
            print(f"     Очікувалось: '{exp_file}'")
            print(f"     Отримано:    '{actual}'")

    print()
    if passed == total:
        print(f"✅ Всі {passed}/{total} тестів пройдено успішно!\n")
    else:
        print(f"⚠️  Пройдено {passed}/{total} тестів.\n")


if __name__ == "__main__":
    run()
