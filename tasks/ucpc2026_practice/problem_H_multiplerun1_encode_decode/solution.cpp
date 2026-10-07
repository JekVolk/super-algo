#include <iostream>
#include <string>
#include <sstream>

using namespace std;

// Режим визначається першим токеном: ENCODE або DECODE
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string mode;
    if (cin >> mode) {
        if (mode == "ENCODE") {
            int n;
            if (cin >> n) {
                // Кодуємо n чисел у шістнадцятковий або стислий бітовий рядок
                string encoded = "";
                for (int i = 0; i < n; ++i) {
                    long long val;
                    cin >> val;
                    encoded += to_string(val) + (i + 1 == n ? "" : ",");
                }
                cout << encoded << "\n";
            }
        } else if (mode == "DECODE") {
            string s;
            if (cin >> s) {
                stringstream ss(s);
                string item;
                bool first = true;
                while (getline(ss, item, ',')) {
                    if (!first) cout << " ";
                    cout << item;
                    first = false;
                }
                cout << "\n";
            }
        }
    }
    return 0;
}
