#include <iostream>
#include <vector>

using namespace std;

const long long MOD = 1000000007;

long long solve_h(int n, long long k) {
    if (n <= 0) return 0;
    k %= MOD;
    vector<long long> u(n + 1, 0);
    u[1] = k;
    for (int i = 2; i <= n; ++i) {
        if (i % 2 == 1) {
            u[i] = (k * u[i - 1]) % MOD;
        } else {
            int m = i / 2;
            u[i] = ((k * u[i - 1] - u[m]) % MOD + MOD) % MOD;
        }
    }
    return u[n];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    long long k;
    while (cin >> n >> k) {
        cout << solve_h(n, k) << "\n";
    }
    return 0;
}
