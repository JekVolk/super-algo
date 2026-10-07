#include <iostream>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) {
        n = 1000000;
    }

    long long low = 1, high = n;
    while (low <= high) {
        long long mid = low + (high - low) / 2;
        cout << "? " << mid << endl; // endl guarantees flush

        string resp;
        if (!(cin >> resp)) break;

        if (resp == "=" || resp == "CORRECT") {
            cout << "! " << mid << endl;
            break;
        } else if (resp == "<" || resp == "LESS") {
            // Загадане число менше за mid
            high = mid - 1;
        } else if (resp == ">" || resp == "GREATER") {
            // Загадане число більше за mid
            low = mid + 1;
        }
    }

    return 0;
}
