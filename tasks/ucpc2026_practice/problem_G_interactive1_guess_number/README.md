# Problem G: Interactive1: Вгадай число (Guess the Number)
**Турнір:** UCPC 2026. Practice Session (Пробний тур Eolymp)  
**Теги:** `interactive` `binary-search` `io-flush` `O(log N)`  
**Складність:** Easy  

---

## ⚡ 8-Кроковий Золотий Стандарт Розбору

### 1. Вдупляння (Sense-Making)
Журі загадало ціле число $x \in [1, n]$.
Ваша програма може ставити запитання виду `? mid`, виводячи число в стандартний потік виведення та обов'язково скидаючи буфер (`flush`).
У відповідь тестувальна система повертає:
- `<` — загадане число строго менше за `mid`;
- `>` — загадане число строго більше за `mid`;
- `=` — ви вгадали число.

**Що треба зробити:**  
Вгадати число не більше ніж за $\lceil \log_2 n \rceil + 1$ запитів і завершити програму виводом `! x`.

---

### 2. Ручні крайові тести
1. **$n = 1$:** Запит `? 1` повертає `=` $\implies$ Відповідь `! 1` за 1 хід.
2. **Краї діапазону ($x = 1$ або $x = n$):**  
   Двійковий пошук повинен коректно звужувати межі `[low, mid - 1]` та `[mid + 1, high]` без зациклення.
3. **Парний та непарний $n$:**  
   $n = 10^6 \implies \log_2(10^6) \approx 20$ запитів, що набагато менше ліміту (зазвичай 25-30 запитів).

---

### 3. Аналіз лімітів і бюджет часу
- $n \le 10^9$ (або $10^6$).
- Ліміт запитів: $\le 30$.
- Ліміт часу: $1.0$ секунда.
- Складність: **$O(\log n)$** запитів.
- Пам'ять: $O(1)$.

---

### 4. Вибір алгоритму з Mind Map
- [docs/ALGORITHM_DECISION_TREE.md](../../docs/ALGORITHM_DECISION_TREE.md) $\to$ **Binary Search** $\to$ **Interactive Binary Search**:
  - `low = 1, high = n`.
  - `mid = low + (high - low) / 2`.
  - Обов'язковий `fflush(stdout)` або `std::endl` після кожного запиту.

---

### 5. Доведення та Інваріант
**Інваріант звуження відрізка:**  
На кожній ітерації гарантується, що загадане число $x$ лежить у поточному напівінтервалі $[low, high]$.  
Довжина відрізка на кожному кроці зменшується вдвічі:
$$L_{k+1} \le \left\lfloor \frac{L_k}{2} \right\rfloor$$
Максимальна кількість запитів: $\lfloor \log_2 n \rfloor + 1 \le 30$.

---

### 6. Двомовний код (C++20 та Python 3.12)

#### C++20 (`solution.cpp`):
```cpp
#include <iostream>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) {
        n = 1000000;
    }

    long long low = 1, high = n;
    while (low <= high) {
        long long mid = low + (high - low) / 2;
        cout << "? " << mid << endl; // endl автоматично робить flush буфера

        string resp;
        if (!(cin >> resp)) break;

        if (resp == "=" || resp == "CORRECT") {
            cout << "! " << mid << endl;
            break;
        } else if (resp == "<" || resp == "LESS") {
            high = mid - 1;
        } else if (resp == ">" || resp == "GREATER") {
            low = mid + 1;
        }
    }

    return 0;
}
```

#### Python 3.12 (`solution.py`):
```python
import sys

def main():
    line = sys.stdin.readline().strip()
    if not line:
        return
    n = int(line)

    low = 1
    high = n

    while low <= high:
        mid = (low + high) // 2
        sys.stdout.write(f"? {mid}\n")
        sys.stdout.flush()

        resp = sys.stdin.readline().strip()
        if not resp:
            break

        if resp in ("=", "CORRECT"):
            sys.stdout.write(f"! {mid}\n")
            sys.stdout.flush()
            break
        elif resp in ("<", "LESS"):
            high = mid - 1
        elif resp in (">", "GREATER"):
            low = mid + 1

if __name__ == "__main__":
    main()
```

---

### 7. Аудит граблів та людських помилок
1. **Забутий `fflush` / `flush`:** Головна причина вильоту по **Idleness Limit Exceeded** на інтерактивних задачах. Використовуйте `cout << endl;` або `sys.stdout.flush()`.
2. **Переповнення при обчисленні `mid`:** Для $n = 2 \cdot 10^9$ формула `(low + high) / 2` може переповнити 32-бітний `int`. Завжди пишіть `low + (high - low) / 2` або використовуйте `long long`.

---

### 8. Стрес-тест та командна стратегія
- **Локальний інтерактор:** скрипт `test_runner.py` емулює поведінку суддівського чекера через підпроцес, перевіряючи коректність відповіді та ліміт запитів.
