#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_map>

using namespace std;

struct Fenwick {
    int n;
    vector<int> tree;
    Fenwick(int n) : n(n), tree(n + 1, 0) {}

    void add(int i, int delta) {
        for (; i <= n; i += i & -i) {
            tree[i] += delta;
        }
    }

    int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) {
            sum += tree[i];
        }
        return sum;
    }
};

struct Query {
    int l, r, id;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (cin >> n) {
        vector<int> a(n + 1);
        for (int i = 1; i <= n; ++i) {
            cin >> a[i];
        }

        int q;
        if (!(cin >> q)) return 0;

        vector<Query> queries(q);
        for (int i = 0; i < q; ++i) {
            cin >> queries[i].l >> queries[i].r;
            queries[i].id = i;
        }

        // Сортуємо запити за правою межею r
        sort(queries.begin(), queries.end(), [](const Query& a, const Query& b) {
            return a.r < b.r;
        });

        Fenwick ft(n);
        unordered_map<int, int> last_pos;
        vector<int> ans(q);

        int cur_r = 1;
        for (const auto& qry : queries) {
            while (cur_r <= qry.r) {
                int val = a[cur_r];
                if (last_pos.count(val)) {
                    ft.add(last_pos[val], -1);
                }
                ft.add(cur_r, 1);
                last_pos[val] = cur_r;
                cur_r++;
            }
            ans[qry.id] = ft.query(qry.r) - ft.query(qry.l - 1);
        }

        for (int i = 0; i < q; ++i) {
            cout << ans[i] << "\n";
        }
    }
    return 0;
}
