from collections import deque

def bfs(n, m, edges):
    # グラフを用意する
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 頂点 0 からの距離を配列で管理
    START_VERTEX = 0
    INF = m + 1
    dist = [INF] * n
    dist[START_VERTEX] = 0

    # BFS を行うためにキューを用意する
    queue = deque([START_VERTEX])

    # BFS
    while queue:
        v = queue.popleft()
        for nv in graph[v]:
            if dist[nv] <= dist[v] + 1:
                continue
            dist[nv] = dist[v] + 1
            queue.append(nv)

    # 訪問できない頂点の距離を -1 とする
    for i in range(n):
        if dist[i] == INF:
            dist[i] = -1
    return dist[1:]

def main():
    # 入力を受け取る
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        uv = list(map(int, input().split()))
        edges.append(uv)

    # 計算結果の出力
    dist = bfs(n, m, edges)
    print(*dist)

# エントリポイント
if __name__ == "__main__":
    main()
