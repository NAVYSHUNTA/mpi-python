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
    if rank == LEADER_RANK:
        for nv in graph[START_VERTEX]:
            all_dist[nv] = 1
            member = (nv % WORK_MEMBER_SIZE) + 1
            COMM.isend([nv, 1], dest = member, tag = 1)

    for _ in range(1, ALL_MEMBER_SIZE):
        result = COMM.irecv(source = LEADER_RANK, tag = 1)
        print(result)

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

        # 頂点 0 からの距離を配列で管理
        INF = m + 1
        all_dist = [INF] * n
        all_dist[START_VERTEX] = 0
        calc_order(graph, all_dist)
        print(*all_dist)

if __name__ == "__main__":
    main()
