#include <bits/stdc++.h>
using namespace std;

// Задача A: Антивірус (UCPC 2026 Stage 1)
// Складність: O(N + K) за часом, O(N) за пам'яттю

void solve() {
    int n, k;
    if (!(cin >> n >> k)) return;

    // a[v] — номер батьківської папки для папки v (для v = 2..n)
    // Гарантується a[v] < v
    vector<int> a(n + 1, 0);
    for (int v = 2; v <= n; ++v) {
        cin >> a[v];
    }

    // b[v] — максимальна залишкова глибина сканування у папці v
    // Якщо b[v] >= 0, то папка v перевірена
    vector<int> b(n + 1, -1);
    for (int i = 0; i < k; ++i) {
        int c, d;
        cin >> c >> d;
        b[c] = max(b[c], d);
    }

    // Оскільки a[v] < v, порядок 1, 2, ..., n вже є топологічним сортуванням!
    // Жоден DFS не потрібен: папка v отримує залишок сили від батька a[v]
    for (int v = 1; v <= n; ++v) {
        int parent = a[v];
        if (parent > 0 && b[parent] > 0) {
            b[v] = max(b[v], b[parent] - 1);
        }
    }

    // Підрахунок перевірених папок
    int checked_count = 0;
    for (int v = 1; v <= n; ++v) {
        if (b[v] >= 0) {
            checked_count++;
        }
    }

    cout << checked_count << "\n";
}

int main() {
    // Прискорення олімпіадного введення/виведення
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t = 1;
    // cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}
