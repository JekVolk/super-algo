#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

const long long INF = 1e18;

struct Edge {
    int to;
    int cap;
    long long cost;
    int rev;
};

void add_edge(vector<vector<Edge>>& adj, int u, int v, int cap, long long cost) {
    int idx_u = adj[u].size();
    int idx_v = adj[v].size();
    adj[u].push_back({v, cap, cost, idx_v});
    adj[v].push_back({u, 0, -cost, idx_u});
}

long long solve_l(int n, const vector<tuple<int, int, long long>>& tasks) {
    if (n == 0) return 0;
    
    vector<int> coords;
    coords.reserve(2 * n);
    for (const auto& t : tasks) {
        coords.push_back(get<0>(t));
        coords.push_back(get<1>(t) + 1);
    }
    sort(coords.begin(), coords.end());
    coords.erase(unique(coords.begin(), coords.end()), coords.end());
    
    int V = coords.size();
    auto get_idx = [&](int x) {
        return lower_bound(coords.begin(), coords.end(), x) - coords.begin();
    };
    
    vector<vector<Edge>> adj(V);
    for (int j = 0; j < V - 1; ++j) {
        add_edge(adj, j, j + 1, 3, 0);
    }
    for (const auto& t : tasks) {
        int u = get_idx(get<0>(t));
        int v = get_idx(get<1>(t) + 1);
        long long w = get<2>(t);
        add_edge(adj, u, v, 1, -w);
    }
    
    vector<long long> phi(V, INF);
    phi[0] = 0;
    for (int u = 0; u < V; ++u) {
        if (phi[u] == INF) continue;
        for (const auto& e : adj[u]) {
            if (e.cap > 0 && e.to > u) {
                phi[e.to] = min(phi[e.to], phi[u] + e.cost);
            }
        }
    }
    for (int i = 0; i < V; ++i) {
        if (phi[i] == INF) phi[i] = 0;
    }
    
    long long total_cost = 0;
    for (int flow = 0; flow < 3; ++flow) {
        vector<long long> dist(V, INF);
        vector<int> prev_v(V, -1);
        vector<int> prev_e(V, -1);
        dist[0] = 0;
        
        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
        pq.push({0, 0});
        
        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();
            if (d > dist[u]) continue;
            
            for (size_t i = 0; i < adj[u].size(); ++i) {
                const auto& e = adj[u][i];
                if (e.cap > 0) {
                    long long red_cost = e.cost + phi[u] - phi[e.to];
                    if (dist[u] + red_cost < dist[e.to]) {
                        dist[e.to] = dist[u] + red_cost;
                        prev_v[e.to] = u;
                        prev_e[e.to] = i;
                        pq.push({dist[e.to], e.to});
                    }
                }
            }
        }
        
        if (dist[V - 1] == INF) break;
        
        for (int v = 0; v < V; ++v) {
            if (dist[v] < INF) phi[v] += dist[v];
        }
        
        int curr = V - 1;
        while (curr != 0) {
            int p = prev_v[curr];
            int e_idx = prev_e[curr];
            adj[p][e_idx].cap -= 1;
            adj[curr][adj[p][e_idx].rev].cap += 1;
            total_cost += adj[p][e_idx].cost;
            curr = p;
        }
    }
    
    return -total_cost;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    while (cin >> n) {
        vector<tuple<int, int, long long>> tasks(n);
        for (int i = 0; i < n; ++i) {
            int l, r;
            long long w;
            cin >> l >> r >> w;
            tasks[i] = {l, r, w};
        }
        cout << solve_l(n, tasks) << "\n";
    }
    return 0;
}
