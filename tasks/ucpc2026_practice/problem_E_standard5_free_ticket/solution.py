import sys
import heapq

INF = 10**18

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    m = int(input_data[1])

    adj = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        w = int(input_data[idx+2])
        idx += 3
        adj[u].append((v, w))
        adj[v].append((u, w))

    # dist[u][0] - без квитка, dist[u][1] - з використанням 1 безкоштовного квитка
    dist = [[INF, INF] for _ in range(n + 1)]
    dist[1][0] = 0

    # heap містить кортежі (d, u, used)
    pq = [(0, 1, 0)]

    while pq:
        d, u, used = heapq.heappop(pq)
        if d > dist[u][used]:
            continue

        for v, w in adj[u]:
            # Звичайний проїзд
            if d + w < dist[v][used]:
                dist[v][used] = d + w
                heapq.heappush(pq, (d + w, v, used))

            # Використання безкоштовного квитка
            if used == 0 and d < dist[v][1]:
                dist[v][1] = d
                heapq.heappush(pq, (d, v, 1))

    ans = min(dist[n][0], dist[n][1])
    sys.stdout.write(f"{-1 if ans >= INF else ans}\n")

if __name__ == "__main__":
    main()
