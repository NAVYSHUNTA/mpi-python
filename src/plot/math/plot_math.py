import matplotlib.pyplot as plt
import japanize_matplotlib # 図の中で日本語が使えるようにする
import glob

# ファイル名から CPU 名を取得するための辞書
get_cpu_name_by_file_name = {
    "m2_max_mac.txt": "M2 Max Mac",
    "m4_mac.txt": "M4 Mac",
    "super.txt": "スーパーコンピュータ"
}


# グラフを作成する関数（引数は x 軸の下限値）
# x 軸：入力値
# y 軸：実行時間（ミリ秒）
# 実験データは逐次処理の実験結果を使用
def plot_math(input_size_lower_limit = None):
    # 実験データの読み込み
    files = glob.glob("./../../math/result/*.txt")
    for file_path in files:
        file_name = file_path.split("/")[-1]

        # 逐次処理のファイルのみを対象とする
        if file_name not in ["super.txt", "m2_max_mac.txt", "m4_mac.txt"]:
            continue

        with open(file_path, "r") as file:
            x_input_size = [] # x 軸のデータ
            y_time = [] # y 軸のデータ
            lines = file.readlines()
            for line in lines:
                # 入力値, 答え, 実行時間（ミリ秒）
                n, _ans, time = map(int, line.strip().split())

                # 特定の入力値以上のグラフを作成する場合
                if input_size_lower_limit is not None and n < input_size_lower_limit:
                    continue

                x_input_size.append(n)
                y_time.append(time)

            cpu_name = get_cpu_name_by_file_name[file_name]
            plt.plot(x_input_size, y_time, marker = "o", linestyle = "dotted", label = cpu_name) # 横軸, 縦軸, 点の種類, 線の種類, ラベル

    # グラフの描画
    plt.xscale("log") # x 軸は対数スケール
    plt.yscale("log") # y 軸は対数スケール
    plt.grid() # グリッド線を表示
    plt.legend(loc = "upper left") # 凡例を左上に表示
    plt.title("素数の数え上げに対する逐次処理の実験結果")
    plt.xlabel("入力値")
    plt.ylabel("実行時間 [ms]")
    plt.tight_layout() # レイアウトの調整

    # グラフの保存
    save_path = "plot_math.png"
    if input_size_lower_limit is not None:
        save_path = f"plot_math_limit_{input_size_lower_limit}.png"
    plt.savefig(save_path) # 作成したグラフの保存先
    plt.close()
    return save_path


def main():
    path1 = plot_math() # 全ての入力値に対するグラフを作成
    path2 = plot_math(input_size_lower_limit = 10 ** 4) # 特定の入力値に対するグラフを作成
    print("グラフを作成しました", path1, path2)


# エントリポイント
if __name__ == "__main__":
    main()
