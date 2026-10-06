#include <bits/stdc++.h>
using namespace std;

// Задача C: Танок залишків (UCPC 2026 Stage 1)
// Складність: O(1) на тест

void solve() {
    long long n, m, k;
    if (!(cin >> n >> m >> k)) return;

    // Всі три залишки a%b == b%c == c%a можуть бути рівними
    // тоді й тільки тоді, коли a == b == c == x.
    // Оскільки 1 <= x <= n, 1 <= x <= m, 1 <= x <= k,
    // відповідь дорівнює мінімуму з трьох чисел.
    long long ans = min({n, m, k});
    cout << ans << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t = 1;
    // Якщо у задачі декілька тестів, наприклад cin >> t:
    // cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}
