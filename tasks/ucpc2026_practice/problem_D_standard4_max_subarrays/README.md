# Problem D: Standard4: Сума максимумів підвідрізків (Sum of Subarray Maximums)
**Турнір:** UCPC 2026. Practice Session (Пробний тур Eolymp)  
**Теги:** `monotonic-stack` `data-structures` `combinatorics` `contribution-technique` `O(N)`  
**Складність:** Medium (Олімпіадна класика)  

---

## ⚡ 8-Кроковий Золотий Стандарт Розбору

### 1. Вдупляння (Sense-Making)
Дано масив із $n$ цілих чисел $a_1, a_2, \dots, a_n$.
Розглядаються всі можливі неперервні підвідрізки $[l, r]$ ($1 \le l \le r \le n$). Для кожного такого підвідрізка обчислюється його максимум: $\max(a[l..r])$.
Необхідно порахувати суму цих максимумів за всіма підвідрізками:
$$\sum_{1 \le l \le r \le n} \max_{l \le k \le r} a_k$$

**Ключовий інсайт:** Замість того, щоб перебирати підвідрізки і шукати максимум, порахуємо **внесок кожного елемента $a_i$** — тобто в скількох підвідрізках елемент $a_i$ є максимальним.

---

### 2. Ручні крайові тести
1. **$n = 3$, $a = [1, 3, 2]$:**  
   Підвідрізки та їх максимуми:
   - $[1] \to 1$, $[1, 3] \to 3$, $[1, 3, 2] \to 3$
   - $[3] \to 3$, $[3, 2] \to 3$
   - $[2] \to 2$  
   Сума: $1 + 3 + 3 + 3 + 3 + 2 = 15$.
2. **Дублікати $a = [2, 2]$:**  
   - $[2] \to 2$, $[2, 2] \to 2$, $[2] \to 2$. Сума: $2 + 2 + 2 = 6$.  
   *Увага на дублікати:* щоб не порахувати один і той самий підвідрізок двічі, розриваємо зв'язки: з одного боку шукаємо строго більший, з іншого — більший або рівний.

---

### 3. Аналіз лімітів і бюджет часу
- $n \le 2 \cdot 10^5$.
- Числа $a_i \in [-10^9, 10^9]$ або до $10^9$.
- Час: $1.0$ секунда.
- Наївний перебір усіх $\frac{n(n+1)}{2}$ підвідрізків — $O(n^2)$ $\implies \approx 2 \cdot 10^{10}$ операцій $\implies$ **TLE**!
- Необхідний час: **$O(n)$** за допомогою монотонного стека.
- Значення підсумкової суми може сягати $O(n^2 \cdot \max a_i) \approx 4 \cdot 10^{19}$, тому обов'язково використовуємо 64-бітний `long long` у C++ та довгу арифметику в Python.

---

### 4. Вибір алгоритму з Mind Map
- [docs/ALGORITHM_DECISION_TREE.md](../../docs/ALGORITHM_DECISION_TREE.md) $\to$ **Data Structures** $\to$ **Monotonic Stack (Contribution Technique)**:
  - Знаходимо $L[i]$ — перший індекс зліва від $i$, де $a[L[i]] > a[i]$ (строго більше).
  - Знаходимо $R[i]$ — перший індекс справа від $i$, де $a[R[i]] \ge a[i]$ (більше або рівне).
  - Кількість підвідрізків, де $a_i$ є максимальним: $(i - L[i]) \times (R[i] - i)$.

---

### 5. Доведення та Інваріант
Елемент $a_i$ є максимальним на відрізку $[l, r]$ тоді й лише тоді, коли:
$$L[i] < l \le i \quad \text{та} \quad i \le r < R[i]$$
За правилом добутку комбінаторики кількість таких пар $(l, r)$ дорівнює $(i - L[i]) \cdot (R[i] - i)$.
Оскільки монотонний стек кожен індекс додає і видаляє не більше одного разу, сумарна кількість операцій становить $2n$ додань і $\le 2n$ видалень $\implies$ суворо $O(n)$ час.

---

### 6. Двомовний код (C++20 та Python 3.12)

#### C++20 (`solution.cpp`):
```cpp
#include <iostream>
#include <vector>
#include <stack>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (cin >> n) {
        vector<long long> a(n);
        for (int i = 0; i < n; ++i) {
            cin >> a[i];
        }

        // L[i]: індекс першого строго більшого зліва (-1 якщо немає)
        vector<int> L(n);
        stack<int> st;
        for (int i = 0; i < n; ++i) {
            while (!st.empty() && a[st.top()] <= a[i]) {
                st.pop();
            }
            L[i] = st.empty() ? -1 : st.top();
            st.push(i);
        }

        // R[i]: індекс першого більшого або рівного справа (n якщо немає)
        vector<int> R(n);
        while (!st.empty()) st.pop();
        for (int i = n - 1; i >= 0; --i) {
            while (!st.empty() && a[st.top()] < a[i]) {
                st.pop();
            }
            R[i] = st.empty() ? n : st.top();
            st.push(i);
        }

        long long total_sum = 0;
        for (int i = 0; i < n; ++i) {
            long long left_count = i - L[i];
            long long right_count = R[i] - i;
            total_sum += a[i] * left_count * right_count;
        }

        cout << total_sum << "\n";
    }
    return 0;
}
```

#### Python 3.12 (`solution.py`):
```python
import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:n+1]]

    L = [-1] * n
    stack = []
    for i in range(n):
        while stack and a[stack[-1]] <= a[i]:
            stack.pop()
        L[i] = stack[-1] if stack else -1
        stack.append(i)

    R = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] < a[i]:
            stack.pop()
        R[i] = stack[-1] if stack else n
        stack.append(i)

    total_sum = 0
    for i in range(n):
        left_count = i - L[i]
        right_count = R[i] - i
        total_sum += a[i] * left_count * right_count

    sys.stdout.write(f"{total_sum}\n")

if __name__ == "__main__":
    main()
```

---

### 7. Аудит граблів та людських помилок
1. **Переповнення 32-бітного типу:** Множення `left_count * right_count` або додавання до `total_sum` переповнює `int`. Потрібно обов'язково використовувати `long long` у C++.
2. **Подвійний підрахунок при однакових значеннях:** Якщо з обох боків брати `<=` або `>=`, однаковий максимум у масиві (наприклад $[2, 2]$) буде пораховано кілька разів. Слід брати строго більше (`<=`) з одного боку і нестрого (`<`) з іншого.

---

### 8. Стрес-тест та командна стратегія
- **Наївний алгоритм:** подвійний цикл $O(n^2)$ з підтриманням `current_max = max(current_max, a[r])`.
- **Роль на ICPC:** Класична задача на монотонний стек середнього рівня. Зазвичай кодується основним алгоритмістом команди за 5-7 хвилин.
