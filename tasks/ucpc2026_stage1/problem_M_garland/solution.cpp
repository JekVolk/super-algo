#include <bits/stdc++.h>
using namespace std;

// Задача M: Гірлянда UCPC (UCPC 2026 Stage 1)
// Метод: Два жадібні проходи (зліва і справа) за O(N)

const int MOD = 1e9 + 7;

long long power3(long long exp) {
    long long res = 1;
    long long base = 3;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

void solve() {
    string s;
    if (!(cin >> s)) return;
    int n = s.size();

    const string target = "UCPC";

    // 1. Жадібний прохід зліва
    vector<int> L(4, -1);
    int cur = 0;
    for (int i = 0; i < n; ++i) {
        if (cur < 4 && s[i] == target[cur]) {
            L[cur] = i;
            cur++;
        }
    }

    // Якщо "UCPC" не входить узагалі — будь-яке розфарбування підходить
    if (L[3] == -1) {
        cout << power3(n) << "\n";
        return;
    }

    // 2. Жадібний прохід справа
    vector<int> R(4, -1);
    cur = 3;
    for (int i = n - 1; i >= 0; --i) {
        if (cur >= 0 && s[i] == target[cur]) {
            R[cur] = i;
            cur--;
        }
    }

    // 3. Підрахунок вільних ламп
    // Лампа i грає роль j iff s[i] == target[j] && L[j] <= i && i <= R[j]
    vector<bool> is_role(n, false);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < 4; ++j) {
            if (s[i] == target[j] && i >= L[j] && i <= R[j]) {
                is_role[i] = true;
            }
        }
    }

    int free_lamps = 0;
    for (int i = 0; i < n; ++i) {
        if (!is_role[i]) free_lamps++;
    }

    // 4. Перевірка: чи є лампа, що грає обидві ролі 2 ('C') і 4 ('C')
    // Лампа грає обидві ролі iff L[3] <= R[1]
    bool clash = (L[3] <= R[1]);

    // Якщо деяка лампа грає обидві ролі C, то c_2 = c_4, тому 3^(f+3), інакше 3^(f+4)
    long long ans;
    if (clash) {
        ans = power3(free_lamps + 3);
    } else {
        ans = power3(free_lamps + 4);
    }

    cout << ans << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t = 1;
    // Якщо декілька тестів:
    // cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}
