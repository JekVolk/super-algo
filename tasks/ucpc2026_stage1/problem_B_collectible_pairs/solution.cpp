#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Digit sum
inline int digit_sum(int n) {
    int s = 0;
    while (n > 0) {
        s += n % 10;
        n /= 10;
    }
    return s;
}

inline bool is_harshad(int n) {
    return n % digit_sum(n) == 0;
}

static vector<int> small_pairs;

void precompute() {
    for (int x = 1; x <= 20005; ++x) {
        if (is_harshad(x) && is_harshad(x + 1)) {
            small_pairs.push_back(x);
        }
    }
}

string solve_one(const string& s_m) {
    if (s_m.empty()) return "";
    int L = s_m.length();
    
    if (L < 5) {
        int m = stoi(s_m);
        for (int x : small_pairs) {
            if (x >= m) {
                if (x + 1 <= 2 * m) {
                    return to_string(x);
                } else {
                    return "-1";
                }
            }
        }
        return "-1";
    }
    
    int B = L - 2; // Кількість кінцевих нулів (B >= 3, тому 10^B ділиться на 8)
    int p = stoi(s_m.substr(0, 2)); // Перші дві цифри числа m
    int c;
    // Обираємо префікс c із сумою цифр 8 так, щоб p < c < 2*p:
    // 1) x = c * 10^B має суму цифр 8 і ділиться на 8 (оскільки B >= 3 => 10^B ділиться на 1000)
    // 2) x + 1 має суму цифр 8 + 1 = 9 і ділиться на 9
    // Таким чином, обидва числа x та x+1 є числами Харшада!
    if (p >= 10 && p <= 16) c = 17;        // 1+7 = 8, 17 <= 2*10 = 20
    else if (p >= 17 && p <= 25) c = 26;   // 2+6 = 8, 26 <= 2*17 = 34
    else if (p >= 26 && p <= 34) c = 35;   // 3+5 = 8, 35 <= 2*26 = 52
    else if (p >= 35 && p <= 61) c = 62;   // 6+2 = 8, 62 <= 2*35 = 70
    else c = 107;                          // 1+0+7 = 8, 107 <= 2*62 = 124
    
    return to_string(c) + string(B, '0');
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    precompute();
    
    string s;
    if (cin >> s) {
        // Check if first token is T
        bool all_digits = true;
        for (char c : s) if (!isdigit(c)) all_digits = false;
        
        vector<string> tokens;
        tokens.push_back(s);
        string temp;
        while (cin >> temp) {
            tokens.push_back(temp);
        }
        
        if (tokens.size() > 1 && stoi(tokens[0]) == (int)tokens.size() - 1) {
            for (size_t i = 1; i < tokens.size(); ++i) {
                cout << solve_one(tokens[i]) << "\n";
            }
        } else {
            for (const auto& tok : tokens) {
                cout << solve_one(tok) << "\n";
            }
        }
    }
    return 0;
}
