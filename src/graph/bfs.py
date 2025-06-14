from collections import deque

# BFS
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

    # キューを用意する
    queue = deque([START_VERTEX])

    # bfs
    while queue:
        v = queue.popleft()
        for nv in graph[v]:
            if dist[nv] <= dist[v] + 1:
                continue
            dist[nv] = dist[v] + 1
            queue.append(nv)

    # 訪問できない頂点の距離を -1 にする
    for i in range(n):
        if dist[i] == INF:
            dist[i] = -1
    return dist[1:]

def main():
    print("n 頂点 m 辺からなる単純グラフの頂点 0 から頂点 i へ辿るのに必要な辺数の最小値を求めます")
    print("2 以上の正整数 n と 1 以上の正整数 m を空白区切りで入力してください: ", end="")
    n, m = map(int, input().split()) # 入力を受け取って整数に変換
    if n < 2 or m < 1:
        print("入力が不正です")
        exit()

    print("次に m 行に渡って辺の情報を空白区切りで入力してください: ", end="")
    edges = []
    for _ in range(m):
        uv = list(map(int, input().split()))
        edges.append(uv)
        if not (0 <= uv[0] < uv[1] <= n - 1):
            print("入力が不正です")
            exit()

    print("頂点 0 から頂点 i へ辿るのに必要な辺数は次の通りです（辿れない場合は -1 とします）")
    dist = bfs(n, m, edges)
    print(*dist)

if __name__ == "__main__":
    main()
