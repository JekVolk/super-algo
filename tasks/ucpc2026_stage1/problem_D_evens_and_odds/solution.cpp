#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

bool can_solve(int rem_e, int rem_o, int T) {
    int p = (T % 2 + 2) % 2;
    int E_p;
    if (p == 0) {
        E_p = (rem_e % 2 == 0) ? rem_e : rem_e - 1;
    } else {
        E_p = (rem_e % 2 == 1) ? rem_e : rem_e - 1;
    }
    
    if (E_p < p) {
        if (p == 1 || rem_e < 0) return false;
    }
    
    int low_x = p;
    int high_x = 9 * E_p;
    int low_req = max(T, low_x);
    int high_req = min(T + 8 * rem_o, high_x);
    return low_req <= high_req;
}

string solve_d(const string& N) {
    if (N.empty()) return "";
    
    string N_rev = N;
    reverse(N_rev.begin(), N_rev.end());
    
    int d0 = 0, d1 = 0;
    for (size_t pos = 0; pos < N_rev.size(); ++pos) {
        int d = N_rev[pos] - '0';
        if (pos % 2 == 0) {
            if (d % 2 == 1) d0 += d;
        } else {
            if (d % 2 == 0) d0 -= d;
        }
        
        if ((pos + 1) % 2 == 0) {
            if (d % 2 == 1) d1 += d;
        } else {
            if (d % 2 == 0) d1 -= d;
        }
    }
    
    if (d0 == 0) return N;
    
    int max_k = (int)N.size() + 120;
    for (int k = 1; k < max_k; ++k) {
        int shift_parity = k % 2;
        int T = (shift_parity == 0) ? -d0 : -d1;
        int e = (k + 1) / 2;
        int o = k / 2;
        if (can_solve(e, o, T)) {
            string block = "";
            int curr_T = T;
            int cur_e = e;
            int cur_o = o;
            for (int pos = k - 1; pos >= 0; --pos) {
                bool is_even = (pos % 2 == 0);
                int next_e = cur_e - (is_even ? 1 : 0);
                int next_o = cur_o - (!is_even ? 1 : 0);
                
                for (int d = 0; d < 10; ++d) {
                    int nxt_T = curr_T;
                    if (is_even) {
                        int add = (d % 2 == 1) ? d : 0;
                        nxt_T -= add;
                    } else {
                        int sub = (d % 2 == 0) ? d : 0;
                        nxt_T += sub;
                    }
                    if (can_solve(next_e, next_o, nxt_T)) {
                        block.push_back('0' + d);
                        curr_T = nxt_T;
                        cur_e = next_e;
                        cur_o = next_o;
                        break;
                    }
                }
            }
            return N + block;
        }
    }
    return N;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    string s;
    while (cin >> s) {
        cout << solve_d(s) << "\n";
    }
    return 0;
}
