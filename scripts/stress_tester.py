#!/usr/bin/env python3
"""
Stress Testing & Fuzzing Engine for Competitive Programming.
Supports Python (.py), C++ (.cpp), and compiled executables (.exe / binary).
Compares a fast solution against a naive/brute-force solution
using randomly generated test cases until a discrepancy is found.
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

def prepare_executable(target: str) -> list[str]:
    """Prepares and compiles (if necessary) target script or source file. Returns command list to execute."""
    p = Path(target)
    if not p.exists():
        raise FileNotFoundError(f"Файл {target} не знайдено!")

    if p.suffix.lower() == ".py":
        return [sys.executable, str(p.resolve())]
    
    if p.suffix.lower() in [".cpp", ".cc", ".cxx"]:
        exe_path = p.with_suffix(".exe" if os.name == "nt" else "")
        # Compile if executable does not exist or source is newer
        if not exe_path.exists() or p.stat().st_mtime > exe_path.stat().st_mtime:
            print(f"🔨 Компіляція {p.name} -> {exe_path.name} (g++ -O3 -std=c++20)...")
            compile_cmd = ["g++", "-O3", "-std=c++20", str(p.resolve()), "-o", str(exe_path.resolve())]
            res = subprocess.run(compile_cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"❌ Помилка компіляції {p.name}:")
                print(res.stderr)
                sys.exit(1)
            print(f" Компіляція {exe_path.name} успішна.")
        return [str(exe_path.resolve())]

    # Already an executable binary
    return [str(p.resolve())]

def run_stress_test(generator_target, fast_target, naive_target, max_tests=1000):
    print(f"=== 🚀 Запуск стрес-тестування: {fast_target} проти {naive_target} ===")
    print(f"🎲 Генератор: {generator_target}, Максимум тестів: {max_tests}\n")

    try:
        gen_cmd = prepare_executable(generator_target)
        fast_cmd = prepare_executable(fast_target)
        naive_cmd = prepare_executable(naive_target)
    except Exception as e:
        print(f"❌ Помилка ініціалізації: {e}")
        return

    start_time = time.time()
    for test_idx in range(1, max_tests + 1):
        # 1. Генерація тесту
        try:
            gen_res = subprocess.run(gen_cmd, capture_output=True, text=True, check=True)
            test_input = gen_res.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ Помилка виконання генератора на тесті #{test_idx}:")
            print(e.stderr)
            return

        # 2. Запуск наївного розв'язку (еталон)
        try:
            naive_res = subprocess.run(naive_cmd, input=test_input, capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            print(f"❌ TLE (Timeout 5s) в наївному розв'язку на тесті #{test_idx}!")
            return

        if naive_res.returncode != 0:
            print(f"❌ Crash/RE в наївному розв'язку на тесті #{test_idx}:")
            print(naive_res.stderr)
            return

        # 3. Запуск оптимізованого розв'язку
        try:
            fast_res = subprocess.run(fast_cmd, input=test_input, capture_output=True, text=True, timeout=3)
        except subprocess.TimeoutExpired:
            print(f"❌ TLE (Timeout 3s) в оптимізованому розв'язку на тесті #{test_idx}!")
            with open("failing_test.txt", "w", encoding="utf-8") as f:
                f.write(test_input)
            print(" Контрприклад збережено у 'failing_test.txt'")
            return

        if fast_res.returncode != 0:
            print(f"❌ Crash/RE в оптимізованому розв'язку на тесті #{test_idx}:")
            print("Вхідні дані:")
            print(test_input)
            print("Stderr:")
            print(fast_res.stderr)
            with open("failing_test.txt", "w", encoding="utf-8") as f:
                f.write(test_input)
            print(" Контрприклад збережено у 'failing_test.txt'")
            return

        expected = naive_res.stdout.strip()
        actual = fast_res.stdout.strip()

        if expected != actual:
            print(f"❌ ЗНАЙДЕНО ПОМИЛКУ (WA) на тесті #{test_idx}!")
            print("----------------------------------------")
            print("ВХІДНІ ДАНІ:")
            print(test_input.strip())
            print("----------------------------------------")
            print(f"ОЧІКУВАЛОСЯ (Еталон):\n{expected}")
            print("----------------------------------------")
            print(f"ОТРИМАНО (Оптимізований):\n{actual}")
            print("----------------------------------------")
            
            # Збереження контрприкладу
            with open("failing_test.txt", "w", encoding="utf-8") as f:
                f.write(test_input)
            print(" Контрприклад збережено у 'failing_test.txt'")
            return

        if test_idx % 50 == 0:
            elapsed = time.time() - start_time
            print(f" Пройдено {test_idx}/{max_tests} тестів... ({elapsed:.1f}с)")

    elapsed = time.time() - start_time
    print(f"\n УСПІХ! Всі {max_tests} випадкових тестів збіглися бездоганно! ({elapsed:.1f}с)")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Використання: python stress_tester.py <generator.py> <fast.py|fast.cpp> <naive.py|naive.cpp> [max_tests]")
        sys.exit(1)
    
    gen = sys.argv[1]
    fast = sys.argv[2]
    naive = sys.argv[3]
    num_tests = int(sys.argv[4]) if len(sys.argv) > 4 else 500
    run_stress_test(gen, fast, naive, num_tests)
