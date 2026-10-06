#!/usr/bin/env python3
"""
Stress Testing & Fuzzing Engine for Competitive Programming.
Compares a fast solution against a naive/brute-force solution
using randomly generated test cases until a discrepancy is found.
"""

import subprocess
import sys
import random
from pathlib import Path

def run_stress_test(generator_script, fast_solution, naive_solution, max_tests=1000):
    print(f"=== Запуск стрес-тестування: {fast_solution} проти {naive_solution} ===")
    print(f"Генератор: {generator_script}, Максимум тестів: {max_tests}\\n")

    for test_idx in range(1, max_tests + 1):
        # 1. Генерація тесту
        gen_res = subprocess.run([sys.executable, generator_script], capture_output=True, text=True, check=True)
        test_input = gen_res.stdout

        # 2. Запуск наївного розв'язку (еталон)
        naive_res = subprocess.run([sys.executable, naive_solution], input=test_input, capture_output=True, text=True)
        if naive_res.returncode != 0:
            print(f"❌ Помилка виконання в наївному розв'язку на тесті #{test_idx}:")
            print(naive_res.stderr)
            return

        # 3. Запуск оптимізованого розв'язку
        fast_res = subprocess.run([sys.executable, fast_solution], input=test_input, capture_output=True, text=True)
        if fast_res.returncode != 0:
            print(f"❌ Crash/RE в оптимізованому розв'язку на тесті #{test_idx}:")
            print("Вхідні дані:")
            print(test_input)
            print("Stderr:")
            print(fast_res.stderr)
            return

        expected = naive_res.stdout.strip()
        actual = fast_res.stdout.strip()

        if expected != actual:
            print(f"❌ ЗНАЙДЕНО ПОМИЛКУ (WA) на тесті #{test_idx}!")
            print("----------------------------------------")
            print("ВХІДНІ ДАНІ:")
            print(test_input.strip())
            print("----------------------------------------")
            print(f"ОЧІКУВАЛОСЯ (Еталон):\\n{expected}")
            print("----------------------------------------")
            print(f"ОТРИМАНО (Оптимізований):\\n{actual}")
            print("----------------------------------------")
            
            # Збереження контрприкладу
            with open("failing_test.txt", "w", encoding="utf-8") as f:
                f.write(test_input)
            print(" Контрприклад збережено у 'failing_test.txt'")
            return

        if test_idx % 50 == 0:
            print(f" Пройдено {test_idx}/{max_tests} тестів...")

    print(f"\\n УСПІХ! Всі {max_tests} випадкових тестів збіглися бездоганно!")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Використання: python stress_tester.py <generator.py> <fast.py> <naive.py> [max_tests]")
        sys.exit(1)
    
    gen = sys.argv[1]
    fast = sys.argv[2]
    naive = sys.argv[3]
    num_tests = int(sys.argv[4]) if len(sys.argv) > 4 else 500
    run_stress_test(gen, fast, naive, num_tests)
