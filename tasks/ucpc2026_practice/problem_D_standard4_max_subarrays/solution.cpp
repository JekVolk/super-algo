#include <iostream>
#include <vector>
#include <stack>

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

        // L[i]: індекс першого строго більшого елемента ліворуч (або -1)
        vector<int> L(n);
        stack<int> st;
        for (int i = 0; i < n; ++i) {
            while (!st.empty() && a[st.top()] <= a[i]) {
                st.pop();
            }
            L[i] = st.empty() ? -1 : st.top();
            st.push(i);
        }

        // R[i]: індекс першого більшого або рівного елемента праворуч (або n)
        // Використовуємо строго більший з одного боку і >= з іншого для уникнення подвійного рахунку дублікатів
        vector<int> R(n);
        while (!st.empty()) st.pop();
        for (int i = n - 1; i >= 0; --i) {
            while (!st.empty() && a[st.top()] < a[i]) {
                st.pop();
            }
            R[i] = st.empty() ? n : st.top();
            st.push(i);
        }

        long long total_sum = 0;
        for (int i = 0; i < n; ++i) {
            long long left_count = i - L[i];
            long long right_count = R[i] - i;
            total_sum += a[i] * left_count * right_count;
        }

        cout << total_sum << "\n";
    }
    return 0;
}
