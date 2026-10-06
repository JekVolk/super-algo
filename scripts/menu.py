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
    print("=" * 65)
    print("  🚀 SUPER-ALGO: ОЛІМПІАДНИЙ КОМАНДНИЙ ЦЕНТР (UCPC / ICPC)")
    print("=" * 65)

def open_skill_tree():
    html_file = (ROOT_DIR / "web" / "index.html").resolve().as_uri()
    print(f"\n[*] Відкриваємо Дерево Навичок у браузері: {html_file}")
    webbrowser.open(html_file)

def open_animator():
    html_file = (ROOT_DIR / "web" / "ucpc_animator.html").resolve().as_uri()
    print(f"\n[*] Відкриваємо Інтерактивний Аніматор у браузері: {html_file}")
    webbrowser.open(html_file)

def run_all_tests():
    print("\n[*] Запуск повного тестувального комплексу для всіх 14 задач...")
    script = ROOT_DIR / "tasks" / "test_all_stage1.py"
    if script.exists():
        subprocess.run([sys.executable, str(script)], cwd=ROOT_DIR / "tasks")
    else:
        runners = list((ROOT_DIR / "tasks").glob("**/test_runner.py"))
        for r in runners:
            print(f"\n--- Папка: {r.parent.name} ---")
            subprocess.run([sys.executable, str(r)], cwd=r.parent)

def start_listener():
    script = ROOT_DIR / "scripts" / "companion_listener.py"
    print(f"\n[*] Запуск Competitive Companion Listener...")
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
        print(" [4] 🔌 Запустити слухач Competitive Companion (порт 10043)")
        print(" [5] 🕷️ Скрапити задачу з Eolymp за посиланням")
        print(" [0] 🚪 Вихід")
        print("=" * 65)

        choice = input("Оберіть дію [0-5]: ").strip()
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
            start_listener()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "5":
            scrape_eolymp()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "0":
            print("\nДо зустрічі на контестах!")
            break
        else:
            print("\nНевірна опція. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
