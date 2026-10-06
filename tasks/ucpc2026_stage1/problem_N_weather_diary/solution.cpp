#include <iostream>
#include <cmath>

using namespace std;

string solve_n(long long n, long long u, long long v, long long e, long long g) {
    if (u + v + 1 + e + g != n) return "NO";
    if (abs(u - v) > 1) return "NO";
    if (u == 0 && v == 0 && e > 0 && g > 0) return "NO";
    return "YES";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    long long n, u, v, e, g;
    while (cin >> n >> u >> v >> e >> g) {
        cout << solve_n(n, u, v, e, g) << "\n";
    }
    return 0;
}
