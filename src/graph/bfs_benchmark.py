from collections import deque
import math
import time

# グローバル変数
START_VERTEX = 0 # 開始頂点
UNVISITED_DIST = -1 # 訪問できない頂点までの距離は -1 とする
INPUT_FILE_PATH_LIST = [
    "input_data/line_graph_1000_999.txt",
    "input_data/tree_1000_999.txt",
    "input_data/random_graph_1000_2000.txt",
    "input_data/random_graph_1000_20000.txt",
    "input_data/random_graph_1000_200000.txt",
    "input_data/complete_graph_1000_499500.txt",
]
GET_OUTPUT_FILE_PATH = {
    "input_data/line_graph_1000_999.txt": "result/line_graph/",
    "input_data/tree_1000_999.txt": "result/tree/",
    "input_data/random_graph_1000_2000.txt": "result/random_graph/",
    "input_data/random_graph_1000_20000.txt": "result/random_graph/",
    "input_data/random_graph_1000_200000.txt": "result/random_graph/",
    "input_data/complete_graph_1000_499500.txt": "result/complete_graph/",
}


def bfs(n, m, edges):
    # グラフを用意する
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 開始頂点からの距離を配列で管理
    INF = m + 1 # 訪問できるのであれば開始頂点からの距離は m 以下なので m + 1 を無限大として扱える
    dist = [INF] * n # 長さが n で、初期値が無限大の配列を用意する
    dist[START_VERTEX] = 0 # 開始頂点から開始頂点までの距離は 0

    # BFS を行うために queue を用意する（Python では deque の方が高速なので敢えて deque を使っている）
    # deque と queue の対応は以下の通り
    # deque の popleft() は queue の pop() に相当する
    # deque の append() は queue の append() に相当する
    queue = deque([START_VERTEX])

    # BFS
    while queue: # queue が空になるまで繰り返す
        v = queue.popleft() # queue の先頭から頂点を取り出す
        for nv in graph[v]: # v に隣接している頂点の集合が graph[v]
            if dist[nv] <= dist[v] + 1:
                continue # 距離が更新されない場合はスキップする
            dist[nv] = dist[v] + 1
            queue.append(nv) # queue の末尾に距離が更新された頂点を追加する

    # 訪問できない頂点の距離を INF から UNVISITED_DIST に変更する
    for v in range(n):
        if dist[v] == INF:
            dist[v] = UNVISITED_DIST
    return dist[1:] # 開始頂点以外の距離を返す


# 小数点以下を切り上げたミリ秒単位の実行時間（実時間）を返す
def get_total_time_ms_ceil(start_time):
    end_time = time.perf_counter()
    total_time_second = end_time - start_time
    total_time_ms = 1000 * total_time_second # 秒からミリ秒に変換
    total_time_ms_ceil = math.ceil(total_time_ms) # 小数点以下を切り上げ
    return total_time_ms_ceil


def main():
    for INPUT_FILE_PATH in INPUT_FILE_PATH_LIST:
        n = m = edges = None
        # 入力を受け取る
        # ファイルからグラフの情報を読み込む
        with open(INPUT_FILE_PATH) as file:
            lines = file.readlines()
            n, m = map(int, lines[0].split())
            edges = [list(map(int, line.split())) for line in lines[1:m + 1]]

        # 時間計測開始
        start_time = time.perf_counter()

        # BFS を実行
        dist = bfs(n, m, edges)
        total_time_ms_ceil = get_total_time_ms_ceil(start_time)

        # 計算結果をテキストファイルに出力
        pc_name = "m2_max_mac" # 本プログラムを実行した PC の名前
        output_file_path = f"{GET_OUTPUT_FILE_PATH[INPUT_FILE_PATH]}{pc_name}_{n}_{m}.txt"
        with open(output_file_path, mode = "w") as file:
            dist_str_info = " ".join(map(str, dist)) # 距離の配列をスペース区切りの文字列に変換
            file.write(f"{dist_str_info}\n") # 距離
            file.write(f"{total_time_ms_ceil}\n") # 実行時間（ミリ秒）


# エントリポイント
if __name__ == "__main__":
    main()
