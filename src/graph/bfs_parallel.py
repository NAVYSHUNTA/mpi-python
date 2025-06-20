from mpi4py import MPI

# グローバル変数
COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
LEADER_RANK = 0 # リーダーの rank 番号
ALL_MEMBER_SIZE = COMM.Get_size()
WORK_MEMBER_SIZE = ALL_MEMBER_SIZE - 1 # 並列度（メンバーに指示を出すリーダー自身を除く）
START_VERTEX = 0

# 並列 BFS（計算の指示）
def calc_order(graph, all_dist):
    pass

def main():
    # ユーザーから受け取った入力をもとにリーダーがメンバーへ計算を指示する
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

        # 全員にグラフを配布
        COMM.Bcast(graph, root = LEADER_RANK)

    COMM.Barrier() # 全員がグラフを受け取るまで待機

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
            if i % ALL_MEMBER_SIZE == rank:
                local_target_vertex.append(vertex)

        for v in local_target_vertex:
            for nv in graph[v]:
                if dist[nv] <= dist_level + 1:
                    continue
                dist[nv] = dist_level + 1
                local_next_vertex_set.add(nv)
        all_next_vertex_list = COMM.Allgather(list(local_next_vertex_set))

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

    if rank == LEADER_RANK:
        print(*dist)

if __name__ == "__main__":
    main()
