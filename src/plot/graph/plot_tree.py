import matplotlib.pyplot as plt
import japanize_matplotlib # 図の中で日本語が使えるようにする
import glob

# グラフを作成する関数（引数は x 軸の上限値）
# x 軸：並列度
# y 軸：実行時間（ミリ秒）
# 実験データは木の結果を使用
def plot_tree(cpu_size_limit = None):
    super_x_process_size = []
    super_y_time = []
    m2_x_process_size = []
    m2_y_time = []

    # 実験データの読み込み
    files = glob.glob("./../../graph/result/tree/*.txt")
    for file_path in files:
        file_name = file_path.split("/")[-1]
        cpu_size = int(file_name.split("_")[-1].replace(".txt", ""))

        # 逐次処理のファイル名の末尾（数値）は並列度を表していないので、その並列度を 1 にしておく
        if cpu_size == 999:
            cpu_size = 1 # 逐次処理の並列度は 1

        # 特定の並列度以下のグラフを作成する場合
        if cpu_size_limit is not None and cpu_size > cpu_size_limit:
            continue

        # ファイル名が "super" で始まる場合はスーパーコンピュータのデータ
        # ファイル名が "m2_max_mac" で始まる場合は M2 Max Mac のデータ
        # そのため、ファイル名の先頭を見て処理を分ける
        if file_name.startswith("super"):
            with open(file_path, "r") as file:
                lines = file.readlines()
                assert int(lines[0].strip()) == cpu_size, "エラー：ファイルの先頭にある並列度とファイル名の並列度が不一致です"
                _ans = list(map(int, lines[1].strip().split())) # 距離（今回は使わない）
                time = int(lines[2].strip()) # 実行時間（ミリ秒）
                super_x_process_size.append(cpu_size)
                super_y_time.append(time)
        elif file_name.startswith("m2_max_mac"):
            with open(file_path, "r") as file:
                lines = file.readlines()
                _ans = list(map(int, lines[0].strip().split())) # 距離（今回は使わない）
                time = int(lines[1].strip()) # 実行時間（ミリ秒）
                m2_x_process_size.append(cpu_size)
                m2_y_time.append(time)

    # グラフの描画
    plt.scatter(super_x_process_size, super_y_time, color = "red", label = "supercomputer") # 横軸, 縦軸, 点の色, ラベル
    plt.scatter(m2_x_process_size, m2_y_time, color = "blue", label = "M2 Max Mac") # 横軸, 縦軸, 点の色, ラベル
    plt.xticks(super_x_process_size + m2_x_process_size) # x 軸の目盛りを設定
    REPEAT_SIZE = 10
    repeat = max(super_y_time + m2_y_time) // REPEAT_SIZE + 1 # y 軸の目盛りの間隔
    plt.yticks(range(0, repeat * (REPEAT_SIZE + 3), repeat)) # y 軸の目盛りを設定
    plt.grid() # グリッド線を表示
    plt.legend(loc = "upper left") # 凡例を左上に表示
    plt.title(f"1000 頂点 999 辺の木に対する実験結果")
    plt.xlabel("並列度")
    plt.ylabel("実行時間 [ms]")
    plt.tight_layout() # レイアウトの調整

    # グラフの保存
    save_path = "plot_tree.png"
    if cpu_size_limit is not None:
        save_path = f"plot_tree_limit_{cpu_size_limit}.png"
    plt.savefig(save_path) # 作成したグラフの保存先
    plt.close()
    return save_path


def main():
    path1 = plot_tree() # 全ての並列度に対するグラフを作成
    path2 = plot_tree(cpu_size_limit = 100) # 特定の並列度以下のグラフを作成
    print("グラフを作成しました", path1, path2)


# エントリポイント
if __name__ == "__main__":
    main()
