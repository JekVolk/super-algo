#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;

void solve_k(double s) {
    if (abs(s - 1.0) < 1e-12) {
        cout << 1 << "\n";
        cout << fixed << setprecision(15) << 1.0 << "\n";
        return;
    }
    if (abs(s) >= 2.0 - 1e-12) {
        double D = max(0.0, s * s - 4.0);
        double sign = (s >= 0) ? 1.0 : -1.0;
        double y = sign * (abs(s) + sqrt(D)) / 2.0;
        cout << 2 << "\n";
        cout << fixed << setprecision(15) << y << " " << (1.0 / y) << "\n";
        return;
    }
    double D = (s + 1.0) * (s + 1.0) + 4.0;
    double y = ((s + 1.0) + sqrt(D)) / 2.0;
    double z = ((s + 1.0) - sqrt(D)) / 2.0;
    cout << 3 << "\n";
    cout << fixed << setprecision(15) << -1.0 << " " << y << " " << z << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    double s;
    while (cin >> s) {
        solve_k(s);
    }
    return 0;
}
