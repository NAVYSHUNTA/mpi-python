from mpi4py import MPI

# グローバル変数
COMM = MPI.COMM_WORLD # 全てのプロセスで共有されるコミュニケータ
rank = COMM.Get_rank() # 自プロセスのランク番号
LEADER_RANK = 0 # リーダーの rank 番号
SIZE = COMM.Get_size() # 並列度（厳密にはそのコミュニケータに所属するプロセスの総数）
START_VERTEX = 0 # 開始頂点

def main():
    n = m = graph = None

    # 入力を受け取る
    if rank == LEADER_RANK:
        n, m = map(int, input().split())
        edges = []
        for _ in range(m):
            uv = list(map(int, input().split()))
            edges.append(uv)

        # グラフを用意する
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

    # 入力で受け取った情報を全メンバーに配布
    n = COMM.bcast(n, root = LEADER_RANK)
    m = COMM.bcast(m, root = LEADER_RANK)
    graph = COMM.bcast(graph, root = LEADER_RANK)

    COMM.Barrier() # 全メンバーがグラフを受け取るまで待機

    # 頂点 0 からの距離を配列で管理
    INF = m + 1
    dist = [INF] * n
    dist[START_VERTEX] = 0

    dist_level = 0
    cur_vertex_set = set([START_VERTEX])
    while True:
        local_next_vertex_set = set()
        target_vertex = list(cur_vertex_set)

        local_target_vertex = [] # 自分が担当する頂点のリスト
        for i, vertex in enumerate(target_vertex):
            if i % SIZE == rank:
                local_target_vertex.append(vertex)

        for v in local_target_vertex:
            for nv in graph[v]:
                if dist[nv] <= dist_level + 1:
                    continue
                dist[nv] = dist_level + 1
                local_next_vertex_set.add(nv)
        all_next_vertex_list = COMM.allgather(list(local_next_vertex_set))

        next_vertex_set = set()
        for next_vertex_list in all_next_vertex_list:
            next_vertex_set.update(next_vertex_list)

        for next_vertex in next_vertex_set:
            dist[next_vertex] = dist_level + 1

        if not next_vertex_set:
            break

        cur_vertex_set = next_vertex_set
        dist_level += 1

        COMM.Barrier()

    # 訪問できない頂点の距離を -1 とする
    for i in range(n):
        if dist[i] == INF:
            dist[i] = -1

    # 計算結果の出力
    if rank == LEADER_RANK:
        print(*dist[1:])

# エントリポイント
if __name__ == "__main__":
    main()
