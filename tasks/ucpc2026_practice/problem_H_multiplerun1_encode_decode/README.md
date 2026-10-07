# Problem H: MultipleRun1: Закодуй і розкодуй (Encode and Decode)
**Турнір:** UCPC 2026. Practice Session (Пробний тур Eolymp)  
**Теги:** `communication` `multiple-run` `encoding` `serialization` `O(N)`  
**Складність:** Medium  

---

## ⚡ 8-Кроковий Золотий Стандарт Розбору

### 1. Вдупляння (Sense-Making)
У змаганнях типу ICPC/IOI формат **Multiple Run** (задачі на комунікацію) передбачає запуск вашої програми двічі:
1. **Перший запуск (Encoder):** Програма отримує на вхід початкові дані (наприклад, масив чисел $a$) і повинна вивести компактне повідомлення (рядок $S$).
2. **Другий запуск (Decoder):** Програма отримує виключно повідомлення $S$, не маючи доступу до початкових вхідних даних, і повинна відновити початковий масив $a$.

**Що треба зробити:**  
Розробити узгоджений протокол серіалізації/десеріалізації між двома запусками.

---

### 2. Ручні крайові тести
1. **Масив з одного елемента:**  
   $a = [42] \implies$ Encoder виводить `42` $\implies$ Decoder повертає $[42]$.
2. **Від'ємні числа та нулі:**  
   $a = [-10, 0, 100] \implies$ правильна обробка знака мінус при конвертації.
3. **Великі числа:**  
   $a_i \approx 10^9 \implies$ збереження точності 64-бітних цілих.

---

### 3. Аналіз лімітів і бюджет часу
- $n \le 10^5$.
- Числа в діапазоні $[-10^9, 10^9]$.
- Ліміт пам'яті повідомлення: $|S| \le 2 \cdot 10^6$ символів.
- Ліміт часу: $1.0$ секунда на кожен запуск.
- Складність: **$O(n)$** лінійно за часом та пам'яттю.

---

### 4. Вибір алгоритму з Mind Map
- [docs/ALGORITHM_DECISION_TREE.md](../../docs/ALGORITHM_DECISION_TREE.md) $\to$ **Communication & Protocols** $\to$ **Two-Phase Serialization**:
  - Розпізнавання режиму за першим аргументом або форматом потоку.
  - Encoder: генерація роздільника (кома або пробіл).
  - Decoder: парсинг токенів та вивід відновлених чисел.

---

### 5. Доведення та Інваріант
**Інваріант бієкції кодування:**  
Відображення $f: \mathbb{Z}^n \to \Sigma^*$ є ін'єктивним. Оскільки кожен елемент кодується однозначним рядком, а роздільники не перетинаються з алфавітом цифр і знака мінус, відновлення $f^{-1}(S)$ гарантовано дає вихідну послідовність $a$ без втрати інформації.

---

### 6. Двомовний код (C++20 та Python 3.12)

#### C++20 (`solution.cpp`):
```cpp
#include <iostream>
#include <string>
#include <sstream>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string mode;
    if (cin >> mode) {
        if (mode == "ENCODE") {
            int n;
            if (cin >> n) {
                string encoded = "";
                for (int i = 0; i < n; ++i) {
                    long long val;
                    cin >> val;
                    encoded += to_string(val) + (i + 1 == n ? "" : ",");
                }
                cout << encoded << "\n";
            }
        } else if (mode == "DECODE") {
            string s;
            if (cin >> s) {
                stringstream ss(s);
                string item;
                bool first = true;
                while (getline(ss, item, ',')) {
                    if (!first) cout << " ";
                    cout << item;
                    first = false;
                }
                cout << "\n";
            }
        }
    }
    return 0;
}
```

#### Python 3.12 (`solution.py`):
```python
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]

    if mode == "ENCODE":
        n = int(tokens[1])
        vals = tokens[2:2+n]
        sys.stdout.write(",".join(vals) + "\n")
    elif mode == "DECODE":
        encoded = tokens[1]
        vals = encoded.split(",")
        sys.stdout.write(" ".join(vals) + "\n")

if __name__ == "__main__":
    main()
```

---

### 7. Аудит граблів та людських помилок
1. **Вивід зайвих даних або налагоджувальних повідомлень:** Будь-який `cerr` чи зайвий пробіл у каналі зв'язку зламає десеріалізацію на другому етапі.
2. **Спільний стан між запусками:** Пам'ятайте, що між запуском 1 і запуском 2 глобальні змінні **не зберігаються**, оскільки це окремі процеси ОС. Єдиний спосіб передачі даних — виведений рядок.

---

### 8. Стрес-тест та командна стратегія
- Тестер `test_runner.py` запускає пайплайн у два кроки через підпроцеси ОС, емулюючи роботу чекера Eolymp.
