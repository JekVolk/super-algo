#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

void solve_one(int n, vector<long long>& b) {
    sort(b.begin(), b.end());
    
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    vector<long long> a;
    vector<long long> subsets_sum = {0};
    vector<long long> subsets_or = {0};
    
    for (long long val : b) {
        if (!pq.empty() && pq.top() == val) {
            pq.pop();
        } else {
            long long x = val;
            a.push_back(x);
            if ((int)a.size() == n) {
                break;
            }
            
            size_t m = subsets_sum.size();
            vector<long long> new_sums(m);
            vector<long long> new_ors(m);
            for (size_t i = 0; i < m; ++i) {
                long long ns = subsets_sum[i] + x;
                long long no = subsets_or[i] | x;
                new_sums[i] = ns;
                new_ors[i] = no;
                pq.push(ns);
                pq.push(no);
            }
            // Pop one copy of x corresponding to the current element
            pq.pop();
            
            for (size_t i = 0; i < m; ++i) {
                subsets_sum.push_back(new_sums[i]);
                subsets_or.push_back(new_ors[i]);
            }
        }
    }
    
    for (size_t i = 0; i < a.size(); ++i) {
        cout << a[i] << (i + 1 == a.size() ? "" : " ");
    }
    cout << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    while (cin >> n) {
        int m = 2 * ((1 << n) - 1);
        vector<long long> b(m);
        for (int i = 0; i < m; ++i) {
            cin >> b[i];
        }
        solve_one(n, b);
    }
    return 0;
}
