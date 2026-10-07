#include <iostream>

using namespace std;

// Еталонна розстановка 8 ферзів без взаємних атак
const char* BOARD[8] = {
    "Q . . . . . . .",
    ". . . . Q . . .",
    ". . . . . . . Q",
    ". . . . . Q . .",
    ". . Q . . . . .",
    ". . . . . . Q .",
    ". Q . . . . . .",
    ". . . Q . . . ."
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    for (int i = 0; i < 8; ++i) {
        cout << BOARD[i] << "\n";
    }
    return 0;
}
