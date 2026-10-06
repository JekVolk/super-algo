# Задача 4: Втеча з лабіринту (Labyrinth Escape / Grid BFS)
> **Олімпіада:** UCPC 2026 Practice (Пробний тур)  
> **Офіційне посилання:** [https://ucpc.eolymp.space/uk/compete/ucpc2026practice/problem/4](https://ucpc.eolymp.space/uk/compete/ucpc2026practice/problem/4)

---

## 1. Вдупляння (Sense-Making)
Уявіть карту гри: сітка розміром $N \times M$.
- `'S'` — точка старту (Start);
- `'E'` — вихід (Exit);
- `'.'` — вільний коридор, по якому можна ходити;
- `'#'` — непрохідна кам'яна стіна.

За 1 секунду можна перейти в 4 сусідні клітинки: вгору, вниз, вліво, вправо (якщо там немає стіни і ми не виходимо за межі карти).
**Що від нас хочуть:** знайти **мінімальну кількість секунд**, за яку можна дійти від `'S'` до `'E'`. Якщо до виходу пройти взагалі неможливо (замурований) — вивести `-1`.

---

## 2. Ручні крайові тести

1. **Тест 1 (Прямий коридор):**
   ```text
   1 3
   S.E
   ```
   *Відповідь:* `2` кроки.

2. **Тест 2 (Глухий кут / стіна):**
   ```text
   2 2
   S#
   #E
   ```
   *Відповідь:* `-1` (шляху немає, стіни блокують прохід).

3. **Тест 3 (Звивистий шлях у формі змійки):**
   ```text
   3 3
   S.#
   #.#
   #.E
   ```
   *Шлях:* $(0,0) \to (0,1) \to (1,1) \to (2,1) \to (2,2)$. Довжина: `4` кроки.

---

## 3. Аналіз лімітів і бюджет часу
- Розміри сітки: $1 \le N, M \le 1000$. Загальна кількість клітинок $V = N \times M \le 10^6$.
- Кількість переходів (ребер): з кожної клітинки не більше 4 ребер, отже $E \le 4 \cdot 10^6$.
- Ліміт часу: 1.0 сек (дозволяє до $10^8$ операцій).
- Ліміт пам'яті: 256 MB.
- **Оцінка складності:**
  - $O(N \cdot M)$ за часом (кожна клітинка відвідується рівно один раз).
  - $O(N \cdot M)$ за пам'яттю (масив відстаней `dist` розміром $1000 \times 1000 \times 4$ байти $\approx 4$ МБ).

---

## 4. Вибір алгоритму з Mind Map
- [ALGORITHM_DECISION_TREE.md](../../docs/ALGORITHM_DECISION_TREE.md) -> 3. Графи -> Найкоротший шлях -> Всі ребра ваги 1 $\implies$ **BFS на черзі `std::queue` / `collections.deque` за $O(V + E)$**.

---

## 5. Доведення та Інваріант

### Чому не DFS?
Рекурсивний DFS знаходить довільний шлях, а не найкоротший! Щоб знайти найкоротший через DFS, доведеться перебирати експоненційну кількість траєкторій $O(4^{N \cdot M})$, що дасть катастрофічний `TLE` уже при $N, M \ge 15$, а також `SIGSEGV` (переповнення стеку викликів при глибині $10^6$).

### Математичний інваріант BFS
Черга `queue` у будь-який момент часу підтримує **монотонність відстаней**:
$$\text{dist}[v_1] \le \text{dist}[v_2] \le \dots \le \text{dist}[v_k]$$
Різниця відстаней між першим та останнім елементом у черзі ніколи не перевищує 1:
$$\text{dist}[\text{tail}] - \text{dist}[\text{head}] \le 1$$
Коли ми вперше дістаємо вершину `'E'` з черги, знайдена відстань **гарантовано є мінімально можливою**.

---

## 6. Двомовний код

### Python 3.12 (Еталонне олімпіадне рішення)
```python
import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])
    grid = input_data[2:2 + n]

    start = None
    target = None

    for r in range(n):
        for c in range(m):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                target = (r, c)

    if not start or not target:
        print(-1)
        return

    # BFS
    dist = [[-1] * m for _ in range(n)]
    q = deque([start])
    dist[start[0]][start[1]] = 0

    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    while q:
        r, c = q.popleft()
        if (r, c) == target:
            print(dist[r][c])
            return

        cur_d = dist[r][c]
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#':
                if dist[nr][nc] == -1:
                    dist[nr][nc] = cur_d + 1
                    q.append((nr, nc))

    print(-1)

if __name__ == "__main__":
    solve()
```

### C++20 (Швидке олімпіадне рішення)
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <queue>

using namespace std;

struct Cell {
    int r, c;
};

const int dr[4] = {-1, 1, 0, 0};
const int dc[4] = {0, 0, -1, 1};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<string> grid(n);
    Cell start{-1, -1}, target{-1, -1};

    for (int r = 0; r < n; ++r) {
        cin >> grid[r];
        for (int c = 0; c < m; ++c) {
            if (grid[r][c] == 'S') start = {r, c};
            if (grid[r][c] == 'E') target = {r, c};
        }
    }

    if (start.r == -1 || target.r == -1) {
        cout << -1 << "\n";
        return 0;
    }

    vector<vector<int>> dist(n, vector<int>(m, -1));
    queue<Cell> q;

    dist[start.r][start.c] = 0;
    q.push(start);

    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();

        if (r == target.r && c == target.c) {
            cout << dist[r][c] << "\n";
            return 0;
        }

        for (int i = 0; i < 4; ++i) {
            int nr = r + dr[i];
            int nc = c + dc[i];

            if (nr >= 0 && nr < n && nc >= 0 && nc < m && grid[nr][nc] != '#') {
                if (dist[nr][nc] == -1) {
                    dist[nr][nc] = dist[r][c] + 1;
                    q.push({nr, nc});
                }
            }
        }
    }

    cout << -1 << "\n";
    return 0;
}
```

---

## 7. Аудит граблів та людських помилок
1. **Помилка позначення відвіданих (Visited Trap):**
   - *Помилка:* позначати `dist[nr][nc]` не під час додавання в чергу `q.push()`, а тільки під час вилучення `q.pop()`.
   - *Наслідок:* одна й та сама клітинка додається в чергу 4 рази від усіх своїх сусідів, черга розростається до розміру $4^{N \cdot M} \implies$ **MLE або жорсткий TLE**.
   - *Правило:* позначай відвіданою `dist[nr][nc] = cur_d + 1` **ОДРАЗУ перед push**!
2. **Змішування координат `(r, c)` та `(x, y)`:**
   - У матриці $N$ — це рядки (`r`, від $0$ до $N-1$), а $M$ — це стовпці (`c`, від $0$ до $M-1$). Переплутати $N$ та $M$ — гарантований `Out of bounds (SIGSEGV)` на прямокутних полях $10 \times 1000$.

---

## 8. Стрес-тест та командна стратегія
- **Синхронізація з Eolymp:**
  Щоб підтягнути тести конкретного приватного туру:
  ```bash
  python scripts/eolymp_scraper.py https://ucpc.eolymp.space/uk/compete/ucpc2026practice/problem/4 --cookie "ВАШ_EOLYMP_COOKIE"
  ```
  Або запустіть фоновий слухач:
  ```bash
  python scripts/companion_listener.py
  ```
- **ICPC Командний розподіл:**
  - Графовий спеціаліст кодить BFS за 3 хвилини.
  - Другий учасник тим часом малює на чернетці ручні тести з лабіринтами без виходу або зі стартом одразу біля фінішу.
  - Третій готує структуру для наступного етапу.
