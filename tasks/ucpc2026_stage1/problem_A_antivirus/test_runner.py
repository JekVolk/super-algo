"""
test_runner.py — Задача A: Антивірус (UCPC 2026 Stage 1)
Inline-тести: мінімум 5 значущих випадків.
"""
import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Формат: (input_str, expected_output)
# Рядок вводу: перший рядок "n k", потім n-1 батьків (для v=2..n), потім k пар (c d)
TEST_CASES = [
    # 1. n=1, k=0 — лише корінь, жодного запуску => 0 папок
    (
        "1 0",
        "0"
    ),
    # 2. n=1, k=1 — корінь сканується з глибиною 0 => 1 папка (сама себе)
    (
        "1 1\n1 0",
        "1"
    ),
    # 3. Ланцюг 1->2->3->4, запуски (1,1) та (2,2) => всі 4 папки
    (
        "4 2\n1 2 3\n1 1\n2 2",
        "4"
    ),
    # 4. Ланцюг 1->2->3->4, запуск лише (1,10) з великою глибиною => всі 4
    (
        "4 1\n1 2 3\n1 10",
        "4"
    ),
    # 5. Два запуски на одному вузлі: (2,5) та (2,1) — має взятися max=5
    #    Дерево: 1->2->3->4->5. Запуск (2,5) покриває {2,3,4,5}, (2,1) покриває {2,3}.
    #    Вузол 1 не покритий. Відповідь: 4
    (
        "5 2\n1 2 3 4\n2 5\n2 1",
        "4"
    ),
    # 6. Запуск з глибиною 0 — сканується лише стартова папка
    #    Дерево: 1->2->3. Запуск (2,0) => тільки {2}. Відповідь: 1
    (
        "3 1\n1 2\n2 0",
        "1"
    ),
    # 7. Перекриття: дерево-зірка (1 — батько для 2,3,4,5).
    #    Запуск (1,1) — покриває {1,2,3,4,5}. Відповідь: 5
    (
        "5 1\n1 1 1 1\n1 1",
        "5"
    ),
]

def test_py():
    print("=== Тестування Python-розв'язку: Задача A (Антивірус) ===")
    cwd = os.path.dirname(os.path.abspath(__file__))
    passed = 0
    failed = 0
    for i, (inp, expected) in enumerate(TEST_CASES, 1):
        p = subprocess.run(
            [sys.executable, "solution.py"],
            input=inp,
            text=True,
            capture_output=True,
            cwd=cwd
        )
        got = p.stdout.strip()
        if got == expected:
            print(f"  ✅ Тест #{i}: PASSED")
            passed += 1
        else:
            print(f"  ❌ Тест #{i}: FAILED — очікувалось '{expected}', отримано '{got}'")
            if p.stderr:
                print(f"     stderr: {p.stderr.strip()[:200]}")
            failed += 1
    print(f"\nРезультат: {passed}/{len(TEST_CASES)} тестів пройдено.")
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    test_py()
