#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int INF = 1e9;
const int LOGN = 20;

int solve_i(int n, int m, const vector<pair<int, int>>& segments) {
    vector<pair<int, int>> unrolled;
    unrolled.reserve(2 * m);
    for (const auto& seg : segments) {
        int l = seg.first;
        int r = seg.second;
        if (l <= r) {
            unrolled.push_back({l, r});
            unrolled.push_back({l + n, r + n});
        } else {
            unrolled.push_back({l, r + n});
            unrolled.push_back({l + n, r + 2 * n});
        }
    }
    
    vector<int> min_end(2 * n + 2, INF);
    for (const auto& seg : unrolled) {
        int l = seg.first;
        int r = seg.second;
        if (l <= 2 * n) {
            min_end[l] = min(min_end[l], r);
        }
    }
    
    vector<int> best_end(2 * n + 3, INF);
    for (int x = 2 * n; x >= 1; --x) {
        best_end[x] = min(best_end[x + 1], min_end[x]);
    }
    
    vector<int> nxt(2 * n + 2, 2 * n + 1);
    for (int x = 1; x <= 2 * n; ++x) {
        if (best_end[x] <= 2 * n) {
            nxt[x] = best_end[x] + 1;
        } else {
            nxt[x] = 2 * n + 1;
        }
    }
    
    vector<vector<int>> up(LOGN, vector<int>(2 * n + 2, 2 * n + 1));
    for (int x = 1; x <= 2 * n + 1; ++x) {
        up[0][x] = nxt[x];
    }
    
    for (int j = 1; j < LOGN; ++j) {
        for (int x = 1; x <= 2 * n + 1; ++x) {
            up[j][x] = up[j - 1][up[j - 1][x]];
        }
    }
    
    int ans = 0;
    for (int p = 1; p <= n; ++p) {
        int curr = p;
        int count = 0;
        int limit = p + n;
        for (int j = LOGN - 1; j >= 0; --j) {
            if (up[j][curr] <= limit) {
                count += (1 << j);
                curr = up[j][curr];
            }
        }
        ans = max(ans, count);
    }
    return ans;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, m;
    while (cin >> n >> m) {
        vector<pair<int, int>> segs(m);
        for (int i = 0; i < m; ++i) {
            cin >> segs[i].first >> segs[i].second;
        }
        cout << solve_i(n, m, segs) << "\n";
    }
    return 0;
}
