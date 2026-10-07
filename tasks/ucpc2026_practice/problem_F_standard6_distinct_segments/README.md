# Problem F: Standard6: Різні на відрізках (Distinct Elements on Segments)
**Турнір:** UCPC 2026. Practice Session (Пробний тур Eolymp)  
**Теги:** `fenwick-tree` `bit` `offline-queries` `data-structures` `O((N+Q) log N)`  
**Складність:** Medium-Hard  

---

## ⚡ 8-Кроковий Золотий Стандарт Розбору

### 1. Вдупляння (Sense-Making)
Дано масив із $n$ цілих чисел $a_1, a_2, \dots, a_n$.
Надходить $q$ незалежних запитів: кожен запит задається парою індексів $[l, r]$. Необхідно порахувати кількість **різних значень** серед елементів $a_l, a_{l+1}, \dots, a_r$.

**Що треба знайти:**  
Для кожного запиту вивести одне число — кількість унікальних чисел на відрізку.

---

### 2. Ручні крайові тести
1. **Повтори значень:**  
   Масив $[1, 2, 1, 3, 2]$, запит $[1, 5]$.  
   Значення $\{1, 2, 3\} \implies$ Відповідь: $3$.
2. **Усі елементи однакові:**  
   Масив $[5, 5, 5, 5]$, запит $[1, 4]$.  
   Значення $\{5\} \implies$ Відповідь: $1$.
3. **Один елемент:**  
   Запит $[i, i] \implies$ Відповідь завжди $1$.

---

### 3. Аналіз лімітів і бюджет часу
- $n, q \le 2 \cdot 10^5$.
- Значення $a_i \in [1, 10^9]$.
- Час: $2.0$ секунди.
- Наївна обробка кожного запиту через `std::set` або `unordered_set` займає $O(q \cdot n) \approx 4 \cdot 10^{10}$ операцій $\implies$ **Time Limit Exceeded (TLE)**!
- Оптимальний оффлайн-підхід з деревом Фенвіка: **$O((n + q) \log n)$** $\approx 4 \cdot 10^6$ операцій, що гарантовано проходить за $< 0.3$ сек.
- Пам'ять: $O(n + q)$.

---

### 4. Вибір алгоритму з Mind Map
- [docs/ALGORITHM_DECISION_TREE.md](../../docs/ALGORITHM_DECISION_TREE.md) $\to$ **Data Structures** $\to$ **Offline Query Processing with Fenwick Tree (BIT)**:
  - Сортуємо всі запити за правою межею $r$.
  - Проходимо вказівником по масиву $r = 1 \dots n$.
  - Зберігаємо в геш-таблиці `last_pos[x]` попередню позицію входження числа $x$.
  - Якщо $x$ вже зустрічалося, віднімаємо $1$ на його старій позиції в дереві Фенвіка, і ставимо $+1$ на поточній позиції $r$.
  - Тоді для запиту $[l, r]$ відповідь — це сума на префіксі $[l, r]$ у дереві Фенвіка: $\text{query}(r) - \text{query}(l - 1)$.

---

### 5. Доведення та Інваріант
**Інваріант останнього входження:**  
У момент, коли права межа дерева Фенвіка досягає $r$, для кожного унікального значення, що зустрілося в $a[1..r]$, рівно в одній позиції (найправішій $\le r$) стоїть одиниця, а в усіх інших — нуль.  
Тоді число унікальних значень, чиє найправіше входження потрапляє у проміжок $[l, r]$, точно дорівнює кількості одиниць у цьому проміжку, що обчислюється деревом Фенвіка за $O(\log n)$.

---

### 6. Двомовний код (C++20 та Python 3.12)

#### C++20 (`solution.cpp`):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_map>

using namespace std;

struct Fenwick {
    int n;
    vector<int> tree;
    Fenwick(int n) : n(n), tree(n + 1, 0) {}

    void add(int i, int delta) {
        for (; i <= n; i += i & -i) {
            tree[i] += delta;
        }
    }

    int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) {
            sum += tree[i];
        }
        return sum;
    }
};

struct Query {
    int l, r, id;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (cin >> n) {
        vector<int> a(n + 1);
        for (int i = 1; i <= n; ++i) {
            cin >> a[i];
        }

        int q;
        if (!(cin >> q)) return 0;

        vector<Query> queries(q);
        for (int i = 0; i < q; ++i) {
            cin >> queries[i].l >> queries[i].r;
            queries[i].id = i;
        }

        sort(queries.begin(), queries.end(), [](const Query& a, const Query& b) {
            return a.r < b.r;
        });

        Fenwick ft(n);
        unordered_map<int, int> last_pos;
        vector<int> ans(q);

        int cur_r = 1;
        for (const auto& qry : queries) {
            while (cur_r <= qry.r) {
                int val = a[cur_r];
                if (last_pos.count(val)) {
                    ft.add(last_pos[val], -1);
                }
                ft.add(cur_r, 1);
                last_pos[val] = cur_r;
                cur_r++;
            }
            ans[qry.id] = ft.query(qry.r) - ft.query(qry.l - 1);
        }

        for (int i = 0; i < q; ++i) {
            cout << ans[i] << "\n";
        }
    }
    return 0;
}
```

#### Python 3.12 (`solution.py`):
```python
import sys

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i: int, delta: int):
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [0] + [int(x) for x in input_data[1:n+1]]

    idx = n + 1
    if idx >= len(input_data):
        return
    q = int(input_data[idx])
    idx += 1

    queries = []
    for qid in range(q):
        l = int(input_data[idx])
        r = int(input_data[idx+1])
        idx += 2
        queries.append((l, r, qid))

    queries.sort(key=lambda item: item[1])

    ft = Fenwick(n)
    last_pos = {}
    ans = [0] * q

    cur_r = 1
    for l, r, qid in queries:
        while cur_r <= r:
            val = a[cur_r]
            if val in last_pos:
                ft.add(last_pos[val], -1)
            ft.add(cur_r, 1)
            last_pos[val] = cur_r
            cur_r += 1
        ans[qid] = ft.query(r) - ft.query(l - 1)

    sys.stdout.write("\n".join(map(str, ans)) + "\n")

if __name__ == "__main__":
    main()
```

---

### 7. Аудит граблів та людських помилок
1. **Помилка індексації 0 vs 1:** Дерево Фенвіка строго вимагає 1-індексацію через бітовий трюк `i += i & -i`. Індексація з 0 призводить до нескінченного циклу `0 += 0`.
2. **Невідсортований вивід:** Оскільки запити сортуються за $r$, відповіді треба зберігати у вектор `ans` за початковим індексом `qid`, а не виводити безпосередньо.

---

### 8. Стрес-тест та командна стратегія
- **ICPC тактика:** Якщо онлайн-запити не вимагаються, оффлайн-підхід пишеться за 5 хвилин без складної динаміки чи персистентних дерев відрізків.
