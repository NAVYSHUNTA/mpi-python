import matplotlib.pyplot as plt
import japanize_matplotlib # 図の中で日本語が使えるようにする

CPU_NAME = "m2_max_mac"
INPUT_DATA_PATH = f"./../../math/result/{CPU_NAME}.txt"

x_input_size = [] # x 軸のデータ
y_time = [] # y 軸のデータ

# ファイルの内容を読み込んで作図する
with open(INPUT_DATA_PATH, "r") as file:
    lines = file.readlines()
    for line in lines:
        # 入力値, 答え, 実行時間（ミリ秒）
        n, _ans, time = map(int, line.strip().split())
        x_input_size.append(n)
        y_time.append(time)

plt.plot(x_input_size, y_time, marker = "o", linestyle = "dotted") # 横軸, 縦軸, 点の種類, 線の種類
plt.xscale("log") # x 軸は対数スケール
plt.yscale("log") # y 軸は対数スケール
plt.title(f"{CPU_NAME} での実験結果")
plt.xlabel("入力値")
plt.ylabel("実行時間 [ms]")
plt.savefig(f"plot_math_{CPU_NAME}.png") # 作成したグラフの保存先
