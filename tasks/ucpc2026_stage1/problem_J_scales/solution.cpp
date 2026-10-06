#include <iostream>
#include <string>

using namespace std;

string query(unsigned long long x, unsigned long long y) {
    cout << "? " << x << " " << y << "\n";
    cout.flush();
    string resp;
    if (!(cin >> resp)) {
        exit(0);
    }
    return resp;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    if (!(cin >> n)) return 0;
    
    unsigned long long A = 0;
    unsigned long long B = 0;
    string c = query(0, 0);
    
    for (int j = n - 1; j >= 0; --j) {
        unsigned long long bit = (1ULL << j);
        if (c == "=") {
            string r = query(A ^ bit, B);
            if (r == "<") {
                A |= bit;
                B |= bit;
            }
        } else {
            if (j == 0) {
                if (c == ">") {
                    A |= bit;
                } else {
                    B |= bit;
                }
                break;
            }
            
            string r1 = query(A ^ bit, B);
            string r2 = query(A, B ^ bit);
            if (r1 == r2) {
                if (c == ">") {
                    A |= bit;
                } else {
                    B |= bit;
                }
                c = r1;
            } else {
                if (r1 == "<") {
                    A |= bit;
                    B |= bit;
                }
            }
        }
    }
    
    cout << "! " << A << " " << B << "\n";
    cout.flush();
    return 0;
}
