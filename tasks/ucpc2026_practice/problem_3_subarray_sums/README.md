# Задача 3: Віконний максимум суми (Max Sliding Window Sum)

## 1. Вдупляння (Sense-Making)
Дано масив $A$ з $N$ цілих чисел та довжину підмасиву $K$ ($1 \le K \le N$). Потрібно знайти максимальну суму неперервного підмасиву довжини рівно $K$. Тобто максимізувати $\sum_{j=i}^{i+K-1} A_j$ серед усіх можливих початкових позицій $i$.

## 2. Ручні крайові тести
1. **Тест 1 ($K = N$):** Весь масив є єдиним вікном. Сума = сума всіх елементів.
2. **Тест 2 ($K = 1$):** Вікно розміром 1. Відповідь = $\max(A_i)$.
3. **Тест 3 (Всі від'ємні числа):** $A = [-5, -2, -8, -1]$, $K = 2$.
   - Вікна: $[-5, -2] \to -7$, $[-2, -8] \to -10$, $[-8, -1] \to -9$.
   - Максимум: $-7$.

## 3. Аналіз лімітів і бюджет часу
- $1 \le K \le N \le 2 \cdot 10^5$.
- $-10^9 \le A_i \le 10^9$.
- Час: 1.0 сек (до $10^8$ операцій).
- Необхідна складність: $O(N)$ часу, $O(1)$ або $O(N)$ пам'яті.

## 4. Вибір алгоритму з Mind Map
- [ALGORITHM_DECISION_TREE.md](../../docs/ALGORITHM_DECISION_TREE.md) -> 1. Робота з відрізками -> Ковзне вікно (Sliding Window / Two Pointers).

## 5. Доведення та Інваріант
Сума вікна при зміщенні на один елемент вправо змінюється за $O(1)$:
$$\text{Sum}_{i+1} = \text{Sum}_i - A_i + A_{i+K}$$
Інваріант: у будь-який момент часу змінна `current_sum` містить точну суму поточних $K$ елементів без необхідності повторного підсумовування циклом.
Максимальна сума може сягати $K \times 10^9 \approx 2 \cdot 10^{14}$, тому обов'язково використовувати 64-бітні цілі числа (`long long`).

## 6. Двомовний код

### Python 3.12
```python
import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])
    a = [int(x) for x in input_data[2:2 + n]]

    cur_sum = sum(a[:k])
    max_sum = cur_sum

    for i in range(k, n):
        cur_sum += a[i] - a[i - k]
        if cur_sum > max_sum:
            max_sum = cur_sum

    print(max_sum)

if __name__ == "__main__":
    solve()
```

### C++20
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    if (!(cin >> n >> k)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    long long cur_sum = 0;
    for (int i = 0; i < k; ++i) {
        cur_sum += a[i];
    }

    long long max_sum = cur_sum;
    for (int i = k; i < n; ++i) {
        cur_sum += a[i] - a[i - k];
        max_sum = max(max_sum, cur_sum);
    }

    cout << max_sum << "\n";
    return 0;
}
```

## 7. Аудит граблів та людських помилок
1. **Перерахунок суми з нуля на кожному кроці:** перетворює алгоритм на $O(N \cdot K)$, що при $N = 2 \cdot 10^5, K = 10^5$ дає $2 \cdot 10^{10}$ операцій $\implies$ жорсткий `TLE`.
2. **Переповнення 32-бітного `int`:** сума $2 \cdot 10^{14}$ переповнює `int`. Завжди `long long`!
3. **Ініціалізація `max_sum = 0`:** якщо всі числа від'ємні, алгоритм помилково видасть 0. Слід ініціалізувати сумою першого вікна `cur_sum` або `-INF`.

## 8. Стрес-тест та командна стратегія
- **ICPC Тактика:** Базова олімпіадна техніка "рухомого вікна". Реалізується за 2 хвилини без помилок.
