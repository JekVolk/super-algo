import sys
import heapq

def solve_l(n: int, tasks: list[tuple[int, int, int]]) -> int:
    if n == 0:
        return 0
    coords = set()
    for l, r, w in tasks:
        coords.add(l)
        coords.add(r + 1)
    sorted_coords = sorted(coords)
    coord_to_idx = {x: i for i, x in enumerate(sorted_coords)}
    V = len(sorted_coords)
    
    adj = [[] for _ in range(V)]
    
    def add_edge(u, v, cap, cost):
        idx_u = len(adj[u])
        idx_v = len(adj[v])
        adj[u].append({'to': v, 'cap': cap, 'cost': cost, 'rev': idx_v})
        adj[v].append({'to': u, 'cap': 0, 'cost': -cost, 'rev': idx_u})
        
    for j in range(V - 1):
        add_edge(j, j + 1, 3, 0)
        
    for l, r, w in tasks:
        u = coord_to_idx[l]
        v = coord_to_idx[r + 1]
        add_edge(u, v, 1, -w)
        
    INF = 10**18
    phi = [INF] * V
    phi[0] = 0
    for u in range(V):
        if phi[u] == INF:
            continue
        for e in adj[u]:
            if e['cap'] > 0 and e['to'] > u:
                v = e['to']
                if phi[u] + e['cost'] < phi[v]:
                    phi[v] = phi[u] + e['cost']
                    
    for i in range(V):
        if phi[i] == INF:
            phi[i] = 0
            
    total_cost = 0
    for _ in range(3):
        dist = [INF] * V
        prev_v = [-1] * V
        prev_e = [-1] * V
        dist[0] = 0
        pq = [(0, 0)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for i, e in enumerate(adj[u]):
                if e['cap'] > 0:
                    v = e['to']
                    red_cost = e['cost'] + phi[u] - phi[v]
                    if dist[u] + red_cost < dist[v]:
                        dist[v] = dist[u] + red_cost
                        prev_v[v] = u
                        prev_e[v] = i
                        heapq.heappush(pq, (dist[v], v))
                        
        if dist[V - 1] == INF:
            break
            
        for v in range(V):
            if dist[v] < INF:
                phi[v] += dist[v]
                
        curr = V - 1
        while curr != 0:
            p = prev_v[curr]
            e_idx = prev_e[curr]
            e = adj[p][e_idx]
            rev_e = adj[curr][e['rev']]
            e['cap'] -= 1
            rev_e['cap'] += 1
            total_cost += e['cost']
            curr = p
            
    return -total_cost

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    idx = 0
    while idx < len(input_data):
        n = int(input_data[idx])
        idx += 1
        tasks = []
        for _ in range(n):
            l = int(input_data[idx])
            r = int(input_data[idx + 1])
            w = int(input_data[idx + 2])
            idx += 3
            tasks.append((l, r, w))
        print(solve_l(n, tasks))

if __name__ == "__main__":
    main()
