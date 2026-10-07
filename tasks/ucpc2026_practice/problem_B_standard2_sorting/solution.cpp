#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (cin >> n) {
        vector<long long> a(n);
        for (int i = 0; i < n; ++i) {
            cin >> a[i];
        }
        sort(a.begin(), a.end());
        for (int i = 0; i < n; ++i) {
            cout << a[i] << (i + 1 == n ? "" : " ");
        }
        cout << "\n";
    }
    return 0;
}
