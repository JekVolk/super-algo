#include <bits/stdc++.h>
using namespace std;

// Задача E: Чотири числа (UCPC 2026 Stage 1)
// Метод: Meet-in-the-Middle + Два Вказівники за O(N^2 log N) або O(N^2)

void solve() {
    int n;
    long long m;
    if (!(cin >> n >> m)) return;

    vector<long long> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    // 1. Формуємо всі попарні суми P[x, y] = a[x] + a[y] для x <= y
    vector<long long> p;
    p.reserve(n * (n + 1) / 2);
    for (int i = 0; i < n; ++i) {
        for (int j = i; j < n; ++j) {
            p.push_back(a[i] + a[j]);
        }
    }

    // 2. Сортуємо попарні суми
    sort(p.begin(), p.end());

    // 3. Шукаємо максимум p[l] + p[r] <= m двома вказівниками
    long long best_sum = LLONG_MIN;
    bool found = false;

    int l = 0, r = (int)p.size() - 1;
    while (l <= r) {
        long long current_sum = p[l] + p[r];
        if (current_sum <= m) {
            if (!found || current_sum > best_sum) {
                best_sum = current_sum;
                found = true;
            }
            l++;
        } else {
            r--;
        }
    }

    if (found) {
        cout << best_sum << "\n";
    } else {
        cout << -1 << "\n";
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t = 1;
    while (t--) {
        solve();
    }
    return 0;
}
