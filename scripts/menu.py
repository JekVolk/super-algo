#!/usr/bin/env python3
"""
Interactive Command Center & Dashboard for Super-Algo.
Provides a quick unified interface for coaches and contest participants.
"""

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print("=" * 68)
    print("  🚀 SUPER-ALGO: ОЛІМПІАДНИЙ КОМАНДНИЙ ЦЕНТР (UCPC / ICPC)")
    print("=" * 68)

def open_skill_tree():
    html_file = (ROOT_DIR / "web" / "index.html").resolve().as_uri()
    print(f"\n[*] Відкриваємо Дерево Навичок у браузері: {html_file}")
    webbrowser.open(html_file)

def open_animator():
    html_file = (ROOT_DIR / "web" / "ucpc_animator.html").resolve().as_uri()
    print(f"\n[*] Відкриваємо Інтерактивний Аніматор у браузері: {html_file}")
    webbrowser.open(html_file)

def run_all_tests():
    print("\n[*] Запуск повного тестувального комплексу для всіх задач...")
    script1 = ROOT_DIR / "tasks" / "test_all_stage1.py"
    script2 = ROOT_DIR / "tasks" / "test_all_practice.py"
    if script1.exists():
        print("\n--- Запуск UCPC Stage 1 тестів ---")
        subprocess.run([sys.executable, str(script1)], cwd=ROOT_DIR / "tasks")
    if script2.exists():
        print("\n--- Запуск UCPC Practice тестів ---")
        subprocess.run([sys.executable, str(script2)], cwd=ROOT_DIR / "tasks")

def run_stress_test_wizard():
    print("\n=== 🧪 Майстер запуску стрес-тесту ===")
    gen = input("Шлях до генератора (напр. gen.py або Enter для виходу): ").strip()
    if not gen:
        return
    fast = input("Шлях до швидкого розв'язку (напр. solution.cpp або solution.py): ").strip()
    naive = input("Шлях до наївного розв'язку (напр. naive.py): ").strip()
    tests = input("Кількість тестів [за замовчуванням 500]: ").strip()
    tests = tests if tests else "500"
    
    script = ROOT_DIR / "scripts" / "stress_tester.py"
    subprocess.run([sys.executable, str(script), gen, fast, naive, tests])

def test_generators():
    print("\n[*] Демонстрація генератора дерев та графів (test_gen_lib.py)...")
    script = ROOT_DIR / "scripts" / "test_gen_lib.py"
    subprocess.run([sys.executable, str(script)])

def start_listener():
    script = ROOT_DIR / "scripts" / "companion_listener.py"
    print(f"\n[*] Запуск Competitive Companion Listener (порт 10043)...")
    subprocess.run([sys.executable, str(script)])

def scrape_eolymp():
    url = input("\nВведіть URL задачі з Eolymp (Enter для стандартного тестового туру): ").strip()
    if not url:
        url = "https://ucpc.eolymp.space/uk/compete/ucpc2026practice/problem/1"
    cookie = input("Введіть Cookie (необов'язково, якщо сесія відкрита): ").strip()
    script = ROOT_DIR / "scripts" / "eolymp_scraper.py"
    cmd = [sys.executable, str(script), url]
    if cookie:
        cmd.extend(["--cookie", cookie])
    subprocess.run(cmd)

def main():
    while True:
        clear_screen()
        print_banner()
        print(" [1] 🌳 Відкрити Дерево Навичок та 5-Рівневий Навігатор")
        print(" [2] 🎬 Відкрити Інтерактивний Аніматор Задач UCPC")
        print(" [3] 🧪 Запустити тести всіх розібраних задач")
        print(" [4] ⚡ Запустити стрес-тест (C++ / Python)")
        print(" [5] 🎲 Тест бібліотеки генерації дерев/графів (test_gen_lib)")
        print(" [6] 🔌 Запустити слухач Competitive Companion (порт 10043)")
        print(" [7] 🕷️ Скрапити задачу з Eolymp за посиланням")
        print(" [0] 🚪 Вихід")
        print("=" * 68)

        choice = input("Оберіть дію [0-7]: ").strip()
        if choice == "1":
            open_skill_tree()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "2":
            open_animator()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "3":
            run_all_tests()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "4":
            run_stress_test_wizard()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "5":
            test_generators()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "6":
            start_listener()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "7":
            scrape_eolymp()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "0":
            print("\nДо зустрічі на контестах!")
            break
        else:
            print("\nНевірна опція. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
