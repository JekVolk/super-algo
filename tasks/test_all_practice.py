#!/usr/bin/env python3
"""
Master Test Runner for UCPC 2026 Practice Stage (Пробний тур).
Runs test suites across all 10 practice problems (A to J).
"""

import subprocess
import sys
import time
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROBLEMS = [
    "problem_A_standard1_sum_ab",
    "problem_B_standard2_sorting",
    "problem_C_standard3_brackets",
    "problem_D_standard4_max_subarrays",
    "problem_E_standard5_free_ticket",
    "problem_F_standard6_distinct_segments",
    "problem_G_interactive1_guess_number",
    "problem_H_multiplerun1_encode_decode",
    "problem_I_outputonly1_eight_queens",
    "problem_J_functionnomain1_max_pair_sum",
]

def main():
    root = Path(__file__).parent / "ucpc2026_practice"
    if not root.exists():
        print(f"Помилка: Папку {root} не знайдено!")
        sys.exit(1)

    print("=" * 65)
    print("🏆 ЗАПУСК ПОВНОГО ТЕСТОВОГО НАБОРУ: UCPC 2026 PRACTICE (ALL 10 A-J)")
    print("=" * 65)

    total = len(PROBLEMS)
    passed = 0
    start_time = time.time()

    for prob_name in PROBLEMS:
        runner = root / prob_name / "test_runner.py"
        if not runner.exists():
            print(f"  ❌ {prob_name}: test_runner.py НЕ ЗНАЙДЕНО!")
            continue

        print(f"\n▶ Тестування задачі: [{prob_name}]...")
        res = subprocess.run([sys.executable, str(runner)], capture_output=True, text=True, encoding="utf-8", errors="replace")

        if res.returncode == 0:
            passed += 1
            print(f"  ✅ {prob_name}: 100% Всі тести пройдено!")
        else:
            print(f"  ❌ {prob_name}: ПОМИЛКА!")
            print(res.stdout)
            print(res.stderr)

    elapsed = time.time() - start_time
    print("\n" + "=" * 65)
    print(f"📊 ПІДСУМОК: {passed}/{total} задач пройдено успішно за {elapsed:.2f} сек!")
    if passed == total:
        print("🎉 ВСІ 10 ЗАДАЧ ПРОБНОГО ТУРУ (A-J) ВЕРИФІКОВАНО НА 100%!")
    print("=" * 65)

    if passed != total:
        sys.exit(1)

if __name__ == "__main__":
    main()
