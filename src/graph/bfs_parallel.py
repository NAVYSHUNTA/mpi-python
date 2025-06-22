from mpi4py import MPI

# グローバル変数
COMM = MPI.COMM_WORLD # 全てのプロセスで共有されるコミュニケータ
rank = COMM.Get_rank() # 自プロセスのランク番号
LEADER_RANK = 0 # リーダーの rank 番号
SIZE = COMM.Get_size() # 並列度（厳密にはそのコミュニケータに所属するプロセスの総数）
START_VERTEX = 0 # 開始頂点
UNVISITED_DIST = -1 # 訪問できない頂点までの距離は -1 とする

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

    # 入力で受け取ったグラフの情報を全メンバーに配布
    n = COMM.bcast(n, root = LEADER_RANK)
    m = COMM.bcast(m, root = LEADER_RANK)
    graph = COMM.bcast(graph, root = LEADER_RANK)

    COMM.Barrier() # 全メンバーがグラフを受け取るまで待機

    # 開始頂点からの距離を配列で管理
    INF = m + 1 # 訪問できるのであれば開始頂点からの距離は m 以下なので m + 1 を無限大として扱える
    dist = [INF] * n # 長さが n で、初期値が無限大の配列を用意する
    dist[START_VERTEX] = 0 # 開始頂点から開始頂点までの距離は 0

    dist_level = 1 # 現在の距離レベル（開始頂点からの距離）
    cur_vertex_set = set([START_VERTEX]) # 探索対象の頂点を格納する集合（初期状態では開始頂点のみ）

    while True:
        target_vertex = list(cur_vertex_set) # 探索対象の頂点が格納された配列
        target_vertex_self = [] # 自プロセスが担当する頂点が格納された配列

        # 各プロセスが担当する頂点を決定する
        for i, vertex in enumerate(target_vertex):
            if i % SIZE == rank:
                target_vertex_self.append(vertex)

        # 各プロセスが、担当する頂点の距離を必要に応じて更新する
        next_vertex_set_self = set() # 距離が更新された頂点を格納する集合（次のステップでの探索対象となる）
        for v in target_vertex_self:
            for nv in graph[v]: # v に隣接している頂点の集合が graph[v]
                if dist[nv] <= dist_level: # 距離が更新されない場合はスキップする
                    continue
                dist[nv] = dist_level
                next_vertex_set_self.add(nv) # 距離が更新された頂点を追加する

        all_next_vertex_list = COMM.allgather(next_vertex_set_self) # 返り値は set ではなく list であることに注意
        next_vertex_set = set() # 次のステップの探索対象となる頂点の集合
        for next_vertex_list in all_next_vertex_list:
            next_vertex_set.update(next_vertex_list)

        # 次のステップの探索対象となる頂点の距離を更新する
        for next_vertex in next_vertex_set:
            dist[next_vertex] = dist_level

        # 次のステップの探索対象となる頂点が存在しない場合は終了
        if not next_vertex_set:
            break

        # 次のステップの探索対象となる頂点の集合を更新
        cur_vertex_set = next_vertex_set

        # 全プロセスが同一ステップでの探索を完了するまで待機
        COMM.Barrier()

        # 距離レベルを更新
        dist_level += 1

    # 訪問できない頂点の距離を INF から UNVISITED_DIST に変更する
    for v in range(n):
        if dist[v] == INF:
            dist[v] = UNVISITED_DIST

    # 計算結果の出力
    if rank == LEADER_RANK:
        print(*dist[1:])

# エントリポイント
if __name__ == "__main__":
    main()
