#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

// Інтерфейсна функція (No main)
long long maxPairSum(const vector<int>& a) {
    if (a.size() < 2) return 0;

    long long max1 = LLONG_MIN;
    long long max2 = LLONG_MIN;

    for (int x : a) {
        if (x > max1) {
            max2 = max1;
            max1 = x;
        } else if (x > max2) {
            max2 = x;
        }
    }

    return max1 + max2;
}

#ifndef ONLINE_JUDGE
#include <iostream>
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (cin >> n) {
        vector<int> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        cout << maxPairSum(a) << "\n";
    }
    return 0;
}
#endif
