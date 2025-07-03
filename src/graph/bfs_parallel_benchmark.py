from mpi4py import MPI
import math
import time

# グローバル変数
COMM = MPI.COMM_WORLD # 全てのプロセスで共有されるコミュニケータ
rank = COMM.Get_rank() # 自プロセスのランク番号
LEADER_RANK = 0 # リーダーの rank 番号
SIZE = COMM.Get_size() # 並列度（厳密にはそのコミュニケータに所属するプロセスの総数）
START_VERTEX = 0 # 開始頂点
UNVISITED_DIST = -1 # 訪問できない頂点までの距離は -1 とする
INPUT_FILE_PATH_LIST = [
    "input_data/path_1000_999.txt",
    "input_data/tree_1000_999.txt",
    "input_data/random_graph_1000_2000.txt",
    "input_data/random_graph_1000_20000.txt",
    "input_data/random_graph_1000_200000.txt",
    "input_data/complete_graph_1000_499500.txt",
]
GET_OUTPUT_FILE_PATH = {
    "input_data/path_1000_999.txt": "result/path/",
    "input_data/tree_1000_999.txt": "result/tree/",
    "input_data/random_graph_1000_2000.txt": "result/random_graph/",
    "input_data/random_graph_1000_20000.txt": "result/random_graph/",
    "input_data/random_graph_1000_200000.txt": "result/random_graph/",
    "input_data/complete_graph_1000_499500.txt": "result/complete_graph/",
}


# 小数点以下を切り上げたミリ秒単位の実行時間（実時間）を返す
def get_total_time_ms_ceil(start_time):
    end_time = time.perf_counter() # 現在の時間を取得
    total_time_second = end_time - start_time # 経過時間を計算
    total_time_ms = 1000 * total_time_second # 秒からミリ秒に変換
    total_time_ms_ceil = math.ceil(total_time_ms) # 小数点以下を切り上げ
    return total_time_ms_ceil

def main():
    for INPUT_FILE_PATH in INPUT_FILE_PATH_LIST:
        n = m = graph = None

        # 入力を受け取る
        if rank == LEADER_RANK:
            # ファイルからグラフの情報を読み込む
            with open(INPUT_FILE_PATH, "r") as file:
                lines = file.readlines()
                n, m = map(int, lines[0].split())
                edges = [list(map(int, line.split())) for line in lines[1:m + 1]]

            # 時間計測開始
            start_time = time.perf_counter()

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

        # 計算結果をテキストファイルに出力
        pc_name = "super" # 本プログラムを実行した PC の名前
        output_file_path = f"{GET_OUTPUT_FILE_PATH[INPUT_FILE_PATH]}{pc_name}_{n}_{m}_parallel_{SIZE}.txt"
        if rank == LEADER_RANK:
            total_time_ms_ceil = get_total_time_ms_ceil(start_time)
            with open(output_file_path, mode = "w") as file:
                dist_str_info = " ".join(map(str, dist[1:])) # 距離の配列をスペース区切りの文字列に変換
                file.write(f"{SIZE}\n") # 並列度
                file.write(f"{dist_str_info}\n") # 距離
                file.write(f"{total_time_ms_ceil}\n") # 実行時間（ミリ秒）


# エントリポイント
if __name__ == "__main__":
    main()
