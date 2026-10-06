#include <iostream>
#include <vector>
#include <string>
#include <queue>

using namespace std;

struct Cell {
    int r, c;
};

const int dr[4] = {-1, 1, 0, 0};
const int dc[4] = {0, 0, -1, 1};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<string> grid(n);
    Cell start{-1, -1}, target{-1, -1};

    for (int r = 0; r < n; ++r) {
        cin >> grid[r];
        for (int c = 0; c < m; ++c) {
            if (grid[r][c] == 'S') start = {r, c};
            if (grid[r][c] == 'E') target = {r, c};
        }
    }

    if (start.r == -1 || target.r == -1) {
        cout << -1 << "\n";
        return 0;
    }

    vector<vector<int>> dist(n, vector<int>(m, -1));
    queue<Cell> q;

    dist[start.r][start.c] = 0;
    q.push(start);

    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();

        if (r == target.r && c == target.c) {
            cout << dist[r][c] << "\n";
            return 0;
        }

        for (int i = 0; i < 4; ++i) {
            int nr = r + dr[i];
            int nc = c + dc[i];

            if (nr >= 0 && nr < n && nc >= 0 && nc < m && grid[nr][nc] != '#') {
                if (dist[nr][nc] == -1) {
                    dist[nr][nc] = dist[r][c] + 1;
                    q.push({nr, nc});
                }
            }
        }
    }

    cout << -1 << "\n";
    return 0;
}
