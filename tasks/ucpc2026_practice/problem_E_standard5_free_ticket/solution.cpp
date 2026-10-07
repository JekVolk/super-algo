#include <iostream>
#include <vector>
#include <queue>
#include <tuple>

using namespace std;

const long long INF = 1e18;

struct Edge {
    int to;
    long long weight;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (cin >> n >> m) {
        vector<vector<Edge>> adj(n + 1);
        for (int i = 0; i < m; ++i) {
            int u, v;
            long long w;
            cin >> u >> v >> w;
            adj[u].push_back({v, w});
            adj[v].push_back({u, w}); // неорієнтований граф
        }

        // dist[u][0]: найкоротша відстань до u без використання квитка
        // dist[u][1]: найкоротша відстань до u з використанням 1 безкоштовного квитка
        vector<vector<long long>> dist(n + 1, vector<long long>(2, INF));
        priority_queue<tuple<long long, int, int>, vector<tuple<long long, int, int>>, greater<>> pq;

        dist[1][0] = 0;
        pq.push({0, 1, 0});

        while (!pq.empty()) {
            auto [d, u, used] = pq.top();
            pq.pop();

            if (d > dist[u][used]) continue;

            for (const auto& edge : adj[u]) {
                int v = edge.to;
                long long w = edge.weight;

                // Перехід 1: звичайний проїзд
                if (dist[u][used] + w < dist[v][used]) {
                    dist[v][used] = dist[u][used] + w;
                    pq.push({dist[v][used], v, used});
                }

                // Перехід 2: використання безкоштовного квитка (якщо ще не використано)
                if (used == 0 && dist[u][0] < dist[v][1]) {
                    dist[v][1] = dist[u][0];
                    pq.push({dist[v][1], v, 1});
                }
            }
        }

        long long ans = min(dist[n][0], dist[n][1]);
        cout << (ans >= INF ? -1 : ans) << "\n";
    }
    return 0;
}
