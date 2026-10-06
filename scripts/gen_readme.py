#!/usr/bin/env python3
"""
Standard 8-Step Problem README Scaffold Generator for Super-Algo.
Generates an Olympic Pedagogical README.md with all 8 mandatory steps.
"""

import argparse
import sys
from pathlib import Path

# Force UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

README_TEMPLATE = """# 🏆 Задача: {title}

> **Джерело / Платформа:** {source}  
> **Обмеження:** Час: `{time_limit}`, Пам'ять: `{memory_limit}`

---

## ⚡ 1. Вдупляння (Sense-Making)
- **Об'єкти задачі:** {objects}
- **Дозволені операції:** {operations}
- **Що насправді просять:** {core_goal}

---

## 🧪 2. Ручні Крайові Тести (Edge Cases)
1. **Тест $N = 1$ (Мінімальні розміри):**
   - Вхід: `{test1_in}`
   - Очікувано: `{test1_out}`
   - *Чому саме так:* {test1_why}
2. **Тест на максимум / граничні значення ($10^9$ або від'ємні):**
   - Вхід: `{test2_in}`
   - Очікувано: `{test2_out}`
3. **Хитрий контр-приклад (Пастка для наївного алгоритму):**
   - Вхід: `{test3_in}`
   - Очікувано: `{test3_out}`
   - *Пастка:* Наївний алгоритм робить неправильний вибір або падає за TLE.

---

## ⏱️ 3. Аналіз Лімітів та Бюджет Часу
- **Розмір $N$:** `{n_bound}`
- **Допустима часова складність:** `$O({time_complexity})$`
- **Допустима просторова складність:** `$O({space_complexity})$`
- **Бюджет операцій:** ~{ops_count} операцій, що гарантовано вкладається в ліміт {time_limit}.

---

## 🌳 4. Позиція в Дереві Рішень (Algorithm Decision Tree)
- **Макро-розділ:** `{macro_domain}`
- **Алгоритм:** `{algorithm_name}`
- **Шлях у дереві:** `{decision_path}`

---

## 📐 5. Доведення та Математичний Інваріант
- **Чому наївний підхід падає:** Наївний підхід вимагає $O({naive_complexity})$, що при $N = {n_bound}$ дає $> 10^{{12}}$ операцій $\\to$ гарантований **TLE**.
- **Математичний інваріант оптимального рішення:**
  > {invariant_text}
- **Переходи / Формула:**
  $${formula_latex}$$

---

## 💻 6. Двомовний Код (C++20 та Python 3.12)
- C++ реалізація: [solution.cpp](solution.cpp)
- Python реалізація: [solution.py](solution.py)
- Тестувальник: `python test_runner.py solution.py` або `python test_runner.py solution.cpp`

---

## ⚠️ 7. Каталог Граблів та Людських Помилок
1. **[WA]** `{trap_1}`
2. **[TLE]** `{trap_2}`
3. **[UB/Overflow]** `{trap_3}`

---

## 🎯 8. Стрес-Тест та Командна Тактика (ICPC)
- **Генератор тестів:** `python ../../scripts/test_gen_lib.py`
- **Команда стрес-тесту:**
  ```bash
  python ../../scripts/stress_tester.py gen.py solution.cpp naive.py 500
  ```
- **Ролі в трійці:**
  - *Кодер:* друкує структуру та швидкий I/O.
  - *Математик:* перевіряє інваріант формули на папері.
  - *Тестер:* пише наївний перебір та контролює крайові випадки.
"""

def generate_readme(folder_path: Path, title: str, source: str = "Competitive Programming"):
    folder_path.mkdir(parents=True, exist_ok=True)
    readme_file = folder_path / "README.md"
    
    content = README_TEMPLATE.format(
        title=title,
        source=source,
        time_limit="1.0s",
        memory_limit="256MB",
        objects="Масив чисел / граф з вершинами",
        operations="Запити суми або оновлення елементів",
        core_goal="Знайти екстремум або порахувати кількість валідних конфігурацій",
        test1_in="1\\n5",
        test1_out="5",
        test1_why="Мінімальний розмір вхідних даних",
        test2_in="2\\n1000000000 1000000000",
        test2_out="2000000000",
        test3_in="3\\n-1 0 1",
        test3_out="0",
        n_bound="2 * 10^5",
        time_complexity="N \\log N",
        space_complexity="N",
        ops_count="~4 * 10^6",
        macro_domain="Структури даних / ДП",
        algorithm_name="Segment Tree / Two Pointers",
        decision_path="Відрізки -> Монотонність -> Два вказівники O(N)",
        naive_complexity="N^2",
        invariant_text="На кожному кроці підтримується вірність префіксу або черги станів.",
        formula_latex="dp[i] = \\max(dp[i-1], dp[i-2] + a_i)",
        trap_1="Забутий 64-бітний long long при додаванні великих чисел",
        trap_2="std::endl замість '\\n' у циклах виводу",
        trap_3="1 << k замість 1LL << k при бітових зсувах"
    )
    
    readme_file.write_text(content, encoding="utf-8")
    print(f"✅ Створено еталонний 8-кроковий README: {readme_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate 8-step Olympic README scaffold")
    parser.add_argument("folder", help="Шлях до папки задачі")
    parser.add_argument("--title", default="Нова олімпіадна задача", help="Назва задачі")
    parser.add_argument("--source", default="Codeforces / UCPC", help="Джерело задачі")
    args = parser.parse_args()

    generate_readme(Path(args.folder), args.title, args.source)

if __name__ == "__main__":
    main()
