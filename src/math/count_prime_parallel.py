from mpi4py import MPI
import time
import math

# グローバル変数
COMM = MPI.COMM_WORLD # 全てのプロセスで共有されるコミュニケータ
rank = COMM.Get_rank() # 自プロセスのランク番号
LEADER_RANK = 0 # リーダーの rank 番号
SIZE = COMM.Get_size() # 並列度（厳密にはそのコミュニケータに所属するプロセスの総数）

# 素数判定
# 入力値を N としたとき、この素数判定アルゴリズムの時間計算量は O(N)
# 時間計算量が O(√N) の素数判定アルゴリズムもあるが今回は簡潔さを重視して O(N) の方を採用した
def is_prime(target):
    if target < 2:
        return False # 2 未満は素数ではないので False を返す
    for div in range(2, target):
        if target % div == 0:
            return False # 割り切れる場合は素数ではないので False を返す
    return True

# 1 から n までの整数に含まれる素数の個数を数え上げる
def count_prime(n):
    one_step_range = math.ceil(n / min(n, SIZE ** 2)) # 各プロセスが調査する整数の範囲の幅
    count_prime_self = 0 # 自プロセスがカウントした素数の個数

    # 素数の個数を数え上げる
    for i in range(SIZE ** 2):
        if i % SIZE != rank:
            continue # 他のプロセスの担当箇所は無視する
        start_num = one_step_range * i + 1
        end_num = min(n, one_step_range * (i + 1))

        if start_num > n:
            break # どのプロセスでも n より大きい整数は扱わないので終了する

        # 自プロセスは start_num 以上 end_num 以下の整数に含まれる素数の個数を数える
        print(f"わたしはメンバー {rank} で、{start_num} 以上 {end_num} 以下の整数に含まれる素数の個数を数えますね！", flush = True) # TODO: この行はスパコンで時間計測する前に削除する
        for num in range(start_num, end_num + 1):
            count_prime_self += is_prime(num)

    # 各プロセスが数え上げた素数の個数の総和をリーダーに渡す
    total_count_prime = COMM.reduce(count_prime_self, op = MPI.SUM, root = LEADER_RANK)
    return total_count_prime

# 小数点以下を切り捨てたミリ秒単位の実行時間（実時間）を返す
def get_total_time_ms_floor(start_time):
    end_time = time.perf_counter()
    total_time_second = end_time - start_time
    total_time_ms = 1000 * total_time_second # 秒からミリ秒に変換
    total_time_ms_floor = int(total_time_ms) # 小数点以下を切り捨て
    return total_time_ms_floor

def main():
    n = None
    start_time = None
    if rank == LEADER_RANK:
        n = int(input()) # 入力を受け取って整数に変換
        start_time = time.perf_counter()

    n = COMM.bcast(n, root = LEADER_RANK) # 全てのメンバーに n を配布する
    total_count_prime = count_prime(n) # 素数の個数を数える

    # 計算結果の出力
    if rank == LEADER_RANK:
        total_time_ms_floor = get_total_time_ms_floor(start_time)
        print(n, total_count_prime, total_time_ms_floor) # 入力値, 1 から n までの素数の個数, 実行時間（ミリ秒）

# エントリポイント
if __name__ == "__main__":
    main()
