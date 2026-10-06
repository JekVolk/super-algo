#!/usr/bin/env python3
"""
scripts/verify_integrity.py
Автоматичний контролер якості (Quality Gate & Anti-Hallucination Guard).

Перевіряє:
1. Повноту 14 задач I етапу UCPC 2026 (README.md, solution.cpp, solution.py, test_runner.py).
2. Наявність усіх 8 розділів у кожному README.md.
3. Проходження всіх 14 тестів (test_runner.py).
4. Відсутність спотворених символів OCR (, =v, −j, TODO, тощо).
5. Наявність KaTeX у веб-інтерфейсах (index.html, ucpc_animator.html).
"""

import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "tasks" / "ucpc2026_stage1"
WEB_DIR = ROOT / "web"

REQUIRED_SECTIONS = [
    "1. Вдупляння (Sense-Making)",
    "2. Ручні крайові тести",
    "3. Аналіз лімітів і бюджет часу",
    "4. Вибір алгоритму з Mind Map",
    "5. Доведення та Інваріант",
    "6. Двомовний код",
    "7. Аудит граблів та людських помилок",
    "8. Стрес-тест та командна стратегія"
]

FORBIDDEN_OCR_PATTERNS = [
    "\ue020",      # Unicode glyph for \neq from broken OCR
    "b =v max",
    "v=c",
    "TODO",
    "див. далі"
]

def check_web_katex():
    print("🔍 [1/4] Перевірка підключення KaTeX у веб-візуалізаторах...")
    for html_name in ["index.html", "ucpc_animator.html"]:
        path = WEB_DIR / html_name
        if not path.exists():
            print(f"❌ Файл {html_name} не знайдено!")
            return False
        content = path.read_text(encoding="utf-8")
        if "katex" not in content.lower():
            print(f"❌ KaTeX не знайдено у {html_name}!")
            return False
    print("✅ KaTeX успішно підключено у всіх веб-інтерфейсах.")
    return True

def check_task_completeness():
    print("\n🔍 [2/4] Перевірка структури та 8 розділів у задачах I етапу...")
    problems = sorted([p for p in TASKS_DIR.iterdir() if p.is_dir()])
    if len(problems) < 14:
        print(f"❌ Знайдено лише {len(problems)} задач замість 14!")
        return False

    all_passed = True
    for prob in problems:
        readme = prob / "README.md"
        cpp = prob / "solution.cpp"
        py = prob / "solution.py"
        runner = prob / "test_runner.py"

        for f in [readme, cpp, py, runner]:
            if not f.exists():
                print(f"❌ {prob.name}: відсутній обов'язковий файл {f.name}")
                all_passed = False

        if readme.exists():
            text = readme.read_text(encoding="utf-8")
            for sec in REQUIRED_SECTIONS:
                # Шукаємо номер розділу (наприклад "1. Вдупляння")
                sec_num = sec.split(".")[0] + "."
                if sec_num not in text:
                    print(f"❌ {prob.name}: у README.md відсутній розділ: {sec}")
                    all_passed = False

            for bad_pat in FORBIDDEN_OCR_PATTERNS:
                if bad_pat in text:
                    print(f"❌ {prob.name}: знайдено артефакт сирого OCR: '{bad_pat}'")
                    all_passed = False

    if all_passed:
        print(f"✅ Усі 14 задач мають повний комплект файлів та 8 розділів без артефактів OCR.")
    return all_passed

def run_all_test_runners():
    print("\n🔍 [3/4] Запуск верифікації коду через test_runner.py для всіх 14 задач...")
    problems = sorted([p for p in TASKS_DIR.iterdir() if p.is_dir()])
    all_ok = True
    for prob in problems:
        runner = prob / "test_runner.py"
        res = subprocess.run([sys.executable, str(runner)], cwd=str(ROOT), capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ {prob.name}: test_runner.py провалився! Помилка:\n{res.stderr}\n{res.stdout}")
            all_ok = False
        else:
            print(f"   ✓ {prob.name}: тест пройдено успішно.")

    if all_ok:
        print("✅ Усі 14 розв'язків пройшли верифікацію на тестах.")
    return all_ok

def check_practice_tasks():
    print("\n🔍 [4/4] Перевірка та запуск тестів для задач Пробного Туру (4 задачі)...")
    practice_dir = ROOT / "tasks" / "ucpc2026_practice"
    if not practice_dir.exists():
        print("❌ Папку пробного туру не знайдено!")
        return False
    probs = sorted([p for p in practice_dir.iterdir() if p.is_dir()])
    if len(probs) < 4:
        print(f"❌ Знайдено лише {len(probs)} задач пробного туру замість 4!")
        return False

    all_ok = True
    for prob in probs:
        runner = prob / "test_runner.py"
        if not runner.exists():
            print(f"❌ {prob.name}: відсутній test_runner.py")
            all_ok = False
            continue
        res = subprocess.run([sys.executable, str(runner)], cwd=str(ROOT), capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ {prob.name}: тест провалився:\n{res.stderr}\n{res.stdout}")
            all_ok = False
        else:
            print(f"   ✓ {prob.name}: тест пройдено успішно.")

    if all_ok:
        print("✅ Усі 4 задачі пробного туру успішно верифіковано.")
    return all_ok

def main():
    print("=" * 60)
    print("🛡️ SUPER-ALGO: ПОВНА ПЕРЕВІРКА ЦІЛІСНОСТІ ТА ЯКОСТІ")
    print("=" * 60)

    ok1 = check_web_katex()
    ok2 = check_task_completeness()
    ok3 = run_all_test_runners()
    ok4 = check_practice_tasks()

    print("\n" + "=" * 60)
    if ok1 and ok2 and ok3 and ok4:
        print("🎉 ВСІ 18 ЗАДАЧ ТА ВЕБ-СИСТЕМА ПРОЙШЛИ ПЕРЕВІРКУ НА 100%!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("🚨 ВИЯВЛЕНО ПОМИЛКИ В ЦІЛІСНОСТІ СИСТЕМИ!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
