#include <iostream>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    if (!(cin >> s)) return 0;

    int mask = 0;
    for (char c : s) {
        mask ^= (1 << (c - 'a'));
    }

    if ((mask & (mask - 1)) == 0) {
        cout << "YES\n";
    } else {
        cout << "NO\n";
    }
    return 0;
}
