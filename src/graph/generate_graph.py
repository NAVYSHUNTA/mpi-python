import sys
import random

# グラフの名称と頂点数、辺数をコマンドライン引数から取得
graph_name, n, m = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

# 制約違反のチェック
assert 2 <= n <= 10 ** 4, "頂点数が制約に違反しています"
assert 1 <= m <= n * (n - 1) // 2, "辺数が制約に違反しています"
assert graph_name in ["tree", "line", "complete", "random"], "グラフの名称が不正です"


# グラフの生成
def generate_graph(graph_name, n, m):
    if graph_name == "tree":
        assert n - 1 >= m, "木は m が n - 1 以下である必要があります"
        # 木を生成
        edges = []
        exist_edge_set = set() # 既存の辺を管理する集合
        exist_vertex_set = {0} # 既存の頂点を管理する集合
        exist_vertex = [0] # 既存の頂点を管理する配列（ランダム選択用）
        while len(edges) < m:
            # 始点をランダムに選ぶ
            v = random.choice(exist_vertex)
            if v == n - 1:
                continue

            # 終点をランダムに選ぶ
            nv = random.randint(v + 1, n - 1)

            # 既存の辺と重複しないようにチェック
            new_edge = (v, nv)
            if new_edge in exist_edge_set:
                continue
            exist_edge_set.add(new_edge)
            edges.append(new_edge)
            exist_vertex_set.add(nv)
            exist_vertex.append(nv)
        return edges

    elif graph_name == "line":
        assert n - 1 >= m, "単純道は m が n - 1 以下である必要があります"
        # 単純道を生成
        edges = [(i, i + 1) for i in range(m)]
        return edges

    elif graph_name == "complete":
        assert m == n * (n - 1) // 2, "完全グラフは m が n(n - 1) / 2 である必要があります"
        # 完全グラフを生成
        edges = []
        for v in range(n):
            for nv in range(v + 1, n):
                edges.append([v, nv])
        return edges

    elif graph_name == "random":
        # ランダムグラフを生成
        edges = []
        exist_edge_set = set()
        while len(edges) < m:
            v = random.randint(0, n - 2)
            nv = random.randint(v + 1, n - 1)
            new_edge = (v, nv)
            if new_edge in exist_edge_set:
                continue
            exist_edge_set.add(new_edge)
            edges.append(new_edge)
        return edges


def main():
    # グラフを生成
    edges = generate_graph(graph_name, n, m)

    # 生成したグラフの情報をテキストファイルに出力
    with open(f"input_data/{graph_name}_graph.txt", "w") as file:
        file.write(f"{n} {m}\n")
        for u, v in edges:
            file.write(f"{u} {v}\n")
            assert 0 <= u < v <= n - 1, "辺の頂点番号が制約に違反しています"


# エントリポイント
if __name__ == "__main__":
    main()
    print(f"{graph_name} グラフを生成しました: {n} 頂点, {m} 辺")
    print(f"出力ファイル: input_data/{graph_name}_graph.txt")
