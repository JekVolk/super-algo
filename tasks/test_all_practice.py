#!/usr/bin/env python3
"""
Master Test Runner for UCPC 2026 Practice Stage (Пробний тур).
Runs test suites across all 4 practice problems.
"""

import subprocess
import sys
import time
from pathlib import Path

# Safe utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    root = Path(__file__).parent / "ucpc2026_practice"
    if not root.exists():
        print(f"Помилка: Папку {root} не знайдено!")
        sys.exit(1)

    runners = sorted(root.glob("*/test_runner.py"))
    if not runners:
        print("Жодного test_runner.py не знайдено!")
        sys.exit(1)

    print("=" * 60)
    print("🏆 ЗАПУСК ПОВНОГО ТЕСТОВОГО НАБОРУ: UCPC 2026 PRACTICE")
    print("=" * 60)

    total = len(runners)
    passed = 0
    start_time = time.time()

    for r in runners:
        prob_name = r.parent.name
        print(f"\n▶ Тестування задачі: [{prob_name}]...")
        res = subprocess.run([sys.executable, str(r)], capture_output=True, text=True, encoding="utf-8", errors="replace")
        
        if res.returncode == 0:
            passed += 1
            print(f"  ✅ {prob_name}: 100% Всі тести пройдено!")
        else:
            print(f"  ❌ {prob_name}: ПОМИЛКА!")
            print(res.stdout)
            print(res.stderr)

    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"📊 ПІДСУМОК: {passed}/{total} задач пройдено успішно за {elapsed:.2f} сек!")
    if passed == total:
        print("🎉 Всі задачі пробного туру UCPC 2026 мають верифіковані 100% рішення!")
    print("=" * 60)

    if passed != total:
        sys.exit(1)

if __name__ == "__main__":
    main()
