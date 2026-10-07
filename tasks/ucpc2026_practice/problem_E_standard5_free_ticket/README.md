# Problem E: Standard5: Один безкоштовний квиток (One Free Ticket)
**Турнір:** UCPC 2026. Practice Session (Пробний тур Eolymp)  
**Теги:** `graphs` `dijkstra` `shortest-path` `state-graph` `O((N+M) log N)`  
**Складність:** Medium  

---

## ⚡ 8-Кроковий Золотий Стандарт Розбору

### 1. Вдупляння (Sense-Making)
У країні є $n$ міст і $m$ двосторонніх доріг. Кожна дорога між містами $u$ та $v$ має вартість проїзду $w$.
Ви подорожуєте з міста $1$ до міста $n$. У вас є **рівно один безкоштовний квиток**, який дозволяє обнулити вартість будь-якої однієї обраної дороги на вашому маршруті (або ви можете взагалі його не використовувати, якщо шлях безкоштовний).

**Що треба знайти:**  
Мінімальну можливу сумарну вартість дістатися з міста $1$ до міста $n$. Якщо шляху немає, вивести `-1`.

---

### 2. Ручні крайові тести
1. **Пряме ребро з безкоштовним проїздом:**  
   Міста 1 і 3 з'єднані дорогою вартістю 50. Також є шлях $1 \to 2 \to 3$ з вартостями 5 і 5.  
   Використавши квиток на дорозі $1 \to 3$, отримуємо вартість $0$!
2. **Незв'язний граф:**  
   Місто $n$ недосяжне з міста 1 $\implies$ Вихід: `-1`.
3. **Ланцюг $1 \to 2 \to 3$:**  
   Дороги $1-2$ (10) та $2-3$ (20). Вигідно взяти квиток на дорожчу дорогу (вагою 20) $\implies$ відповідь: $10 + 0 = 10$.

---

### 3. Аналіз лімітів і бюджет часу
- $n \le 10^5$, $m \le 2 \cdot 10^5$.
- Ваги $w \le 10^9$.
- Час: $1.0$ секунда.
- Простий Дейкстра в просторі станів: вершина розмножується на 2 шари (використано 0 або 1 квиток).
- Загальна кількість станів: $2n \le 2 \cdot 10^5$, перехідних ребер: $2m \le 4 \cdot 10^5$.
- Складність Дейкстри з пріоритетною чергою: **$O((n + m) \log n)$** $\approx 10^7$ операцій $\implies$ із запасом вміщується в ліміт часу.
- Пам'ять: $O(n + m)$.

---

### 4. Вибір алгоритму з Mind Map
- [docs/ALGORITHM_DECISION_TREE.md](../../docs/ALGORITHM_DECISION_TREE.md) $\to$ **Shortest Path** $\to$ **Layered Graph Dijkstra**:
  - Стан $(u, 0)$ — прибули у вершину $u$, не використавши квиток.
  - Стан $(u, 1)$ — прибули у вершину $u$, використавши 1 квиток.
  - Відстань $\text{dist}[u][used]$ оновлюється через `priority_queue` за мін-відстанню.

---

### 5. Доведення та Інваріант
**Інваріант Дейкстри:**  
Коли стан $(u, \text{used})$ витягується з вершини черги з пріоритетом, його відстань $\text{dist}[u][\text{used}]$ є гарантовано мінімально можливою через невід'ємність ваг ребер ($w \ge 0$ та $0 \ge 0$).  
Перехід зі стану $(u, 0)$ у $(v, 1)$ додає вагу $0$, що також зберігає невід'ємність. Підсумкова відповідь: $\min(\text{dist}[n][0], \text{dist}[n][1])$.

---

### 6. Двомовний код (C++20 та Python 3.12)

#### C++20 (`solution.cpp`):
```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <tuple>

using namespace std;

const long long INF = 1e18;

struct Edge {
    int to;
    long long weight;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (cin >> n >> m) {
        vector<vector<Edge>> adj(n + 1);
        for (int i = 0; i < m; ++i) {
            int u, v;
            long long w;
            cin >> u >> v >> w;
            adj[u].push_back({v, w});
            adj[v].push_back({u, w});
        }

        vector<vector<long long>> dist(n + 1, vector<long long>(2, INF));
        priority_queue<tuple<long long, int, int>, vector<tuple<long long, int, int>>, greater<>> pq;

        dist[1][0] = 0;
        pq.push({0, 1, 0});

        while (!pq.empty()) {
            auto [d, u, used] = pq.top();
            pq.pop();

            if (d > dist[u][used]) continue;

            for (const auto& edge : adj[u]) {
                int v = edge.to;
                long long w = edge.weight;

                if (dist[u][used] + w < dist[v][used]) {
                    dist[v][used] = dist[u][used] + w;
                    pq.push({dist[v][used], v, used});
                }

                if (used == 0 && dist[u][0] < dist[v][1]) {
                    dist[v][1] = dist[u][0];
                    pq.push({dist[v][1], v, 1});
                }
            }
        }

        long long ans = min(dist[n][0], dist[n][1]);
        cout << (ans >= INF ? -1 : ans) << "\n";
    }
    return 0;
}
```

#### Python 3.12 (`solution.py`):
```python
import sys
import heapq

INF = 10**18

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    m = int(input_data[1])

    adj = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        w = int(input_data[idx+2])
        idx += 3
        adj[u].append((v, w))
        adj[v].append((u, w))

    dist = [[INF, INF] for _ in range(n + 1)]
    dist[1][0] = 0
    pq = [(0, 1, 0)]

    while pq:
        d, u, used = heapq.heappop(pq)
        if d > dist[u][used]:
            continue

        for v, w in adj[u]:
            if d + w < dist[v][used]:
                dist[v][used] = d + w
                heapq.heappush(pq, (d + w, v, used))

            if used == 0 and d < dist[v][1]:
                dist[v][1] = d
                heapq.heappush(pq, (d, v, 1))

    ans = min(dist[n][0], dist[n][1])
    sys.stdout.write(f"{-1 if ans >= INF else ans}\n")

if __name__ == "__main__":
    main()
```

---

### 7. Аудит граблів та людських помилок
1. **INF занадто малий:** Сумарна вага може досягати $n \cdot \max w \approx 10^{14}$. Значення `0x3f3f3f3f` чи $2 \cdot 10^9$ переповниться. Необхідно ставити `INF = 1e18`.
2. **Орієнтованість доріг:** Уважно читайте умову — якщо дороги двосторонні, додавайте ребра в обидва боки `adj[u].push_back(v)` та `adj[v].push_back(u)`.

---

### 8. Стрес-тест та командна стратегія
- **ICPC тактика:** Графова класика 2-го рівня (Layered graph). Віддається учаснику, який спеціалізується на графах і shortest-path алгоритмах.
