#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

int solve_g(const string& s_n, const string& s_m) {
    if (s_n == s_m) return 0;
    if (s_m == "1") return -1;
    
    int c = 0;
    for (char ch : s_n) {
        if (ch == '1') c++;
    }
    
    int pop_m = 0;
    for (char ch : s_m) {
        if (ch == '1') pop_m++;
    }
    
    int tz = 0;
    for (int i = (int)s_m.length() - 1; i >= 0 && s_m[i] == '0'; --i) {
        tz++;
    }
    
    int p = pop_m - 1 + tz;
    
    if (c == p) return 1;
    if (c > p) return 2;
    return p - c + 1;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    string n, m;
    while (cin >> n >> m) {
        cout << solve_g(n, m) << "\n";
    }
    return 0;
}
