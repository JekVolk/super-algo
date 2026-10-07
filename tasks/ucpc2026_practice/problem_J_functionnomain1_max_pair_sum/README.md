# Problem J: FunctionNoMain1: Максимальна сума пари (Maximum Pair Sum)
**Турнір:** UCPC 2026. Practice Session (Пробний тур Eolymp)  
**Теги:** `grader` `function-only` `implementation` `greedy` `O(N)`  
**Складність:** Easy  

---

## ⚡ 8-Кроковий Золотий Стандарт Розбору

### 1. Вдупляння (Sense-Making)
У форматі **Function Without Main** вам не потрібно писати `int main()` або зчитувати вхідні дані через `cin` чи `sys.stdin`. Тестувальна система підключає власний прихований модуль (grader/чекер) і викликає вашу функцію:
- У C++: `long long maxPairSum(const std::vector<int>& a);`
- У Python: `def max_pair_sum(a: list[int]) -> int:`

**Що треба знайти:**  
Максимальну суму двох різних елементів (за різними індексами $i \ne j$) масиву: $\max_{i \ne j} (a_i + a_j)$.

---

### 2. Ручні крайові тести
1. **$n = 2$ елементи:**  
   $a = [-5, -10] \implies$ Вихід: $-15$. Коректна робота з від'ємними числами (не можна ініціалізувати нулями!).
2. **Дублікати найбільших:**  
   $a = [10, 10, 5, 1] \implies$ Вихід: $20$ (два різних індекси з однаковим значенням 10).
3. **Строго різні значення:**  
   $a = [3, 1, 4, 2] \implies$ Найбільші 4 і 3 $\implies$ Сума: $7$.

---

### 3. Аналіз лімітів і бюджет часу
- $n \le 10^5$.
- Елементи $a_i \in [-10^9, 10^9]$.
- Час: $0.5$ секунд.
- Повний сортування $O(n \log n)$ теж проходить, але лінійний пошук двох максимумів за один прохід працює за **$O(n)$** часу та $O(1)$ додаткової пам'яті.

---

### 4. Вибір алгоритму з Mind Map
- [docs/ALGORITHM_DECISION_TREE.md](../../docs/ALGORITHM_DECISION_TREE.md) $\to$ **Basic Implementations & Greedy** $\to$ **Single-Pass Two Maximums**:
  - Змінні `max1` та `max2`, ініціалізовані мінімальним можливим числом (`LLONG_MIN` / `-inf`).
  - Оновлення при кожному новому $x$.

---

### 5. Доведення та Інваріант
**Інваріант двох найбільших:**  
Після обробки префікса $a[0..k]$ значення `max1` містить $\max_{0 \le i \le k} a_i$, а `max2` містить другий за величиною елемент серед $a[0..k]$.  
Сума `max1 + max2` є максимально можливою сумою пари на префіксі. Кожен елемент перевіряється рівно один раз $\implies O(n)$ операцій.

---

### 6. Двомовний код (C++20 та Python 3.12)

#### C++20 (`solution.cpp`):
```cpp
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

long long maxPairSum(const vector<int>& a) {
    if (a.size() < 2) return 0;

    long long max1 = LLONG_MIN;
    long long max2 = LLONG_MIN;

    for (int x : a) {
        if (x > max1) {
            max2 = max1;
            max1 = x;
        } else if (x > max2) {
            max2 = x;
        }
    }

    return max1 + max2;
}

#ifndef ONLINE_JUDGE
#include <iostream>
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (cin >> n) {
        vector<int> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        cout << maxPairSum(a) << "\n";
    }
    return 0;
}
#endif
```

#### Python 3.12 (`solution.py`):
```python
from typing import List

def max_pair_sum(a: List[int]) -> int:
    """Знаходить максимальну суму двох елементів за різними індексами за O(N)."""
    if len(a) < 2:
        return 0

    max1 = float('-inf')
    max2 = float('-inf')

    for x in a:
        if x > max1:
            max2 = max1
            max1 = x
        elif x > max2:
            max2 = x

    return int(max1 + max2)

if __name__ == "__main__":
    import sys
    tokens = sys.stdin.read().split()
    if tokens:
        n = int(tokens[0])
        nums = [int(x) for x in tokens[1:n+1]]
        print(max_pair_sum(nums))
```

---

### 7. Аудит граблів та людських помилок
1. **Ініціалізація нулями:** Якщо всі числа в масиві від'ємні (наприклад $[-5, -10]$), ініціалізація `max1 = 0, max2 = 0` видасть хибну відповідь `0`. Обов'язково ініціалізуйте `-inf` або `LLONG_MIN`.
2. **Наявність функції `main()` на сервері:** Якщо сервер компілює код разом зі своїм grader, два визначення `int main()` призведуть до помилки лінкування `multiple definition of 'main'`. Використовуйте директиву `#ifndef ONLINE_JUDGE` для локальних тестів.

---

### 8. Стрес-тест та командна стратегія
- Тестер `test_runner.py` перевіряє поведінку функції на від'ємних числах, однакових числах та граничних значеннях.
