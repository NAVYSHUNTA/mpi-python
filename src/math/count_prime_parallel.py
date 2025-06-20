from mpi4py import MPI
import time
import math

# グローバル変数
COMM = MPI.COMM_WORLD # 全てのプロセスで共有されるコミュニケータ
rank = COMM.Get_rank() # 自プロセスのランク番号
LEADER_RANK = 0 # リーダーの rank 番号
ALL_MEMBER_SIZE = COMM.Get_size() # 並列度（厳密にはそのコミュニケータに所属するプロセスの総数）
WORK_MEMBER_SIZE = ALL_MEMBER_SIZE - 1 # 並列度（メンバーに指示を出すリーダー自身を除く）

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

# 1 から n までの素数の個数を数え上げ（計算の指示）
def calc_order(n):
    if rank == LEADER_RANK:
        for repeat in range(1, ALL_MEMBER_SIZE):
            base = math.ceil(n / WORK_MEMBER_SIZE ** 2)
            one_step_base = base * WORK_MEMBER_SIZE
            for member in range(1, ALL_MEMBER_SIZE):
                s = (repeat - 1) * one_step_base
                COMM.send([s + base * (member - 1) + 1, min(n + 1, s + base * member + 1)], dest = member, tag = repeat)

# 1 から n までの素数の個数を数え上げ（指示された内容の計算）
def count_prime():
    if rank == LEADER_RANK:
        pass # nothing
    else:
        for repeat in range(1, ALL_MEMBER_SIZE):
            left, right = COMM.recv(source = LEADER_RANK, tag = repeat)

            # 無効な範囲の場合はカウントせずに終了
            count = 0
            if left >= right:
                COMM.send(count, dest = LEADER_RANK, tag = repeat)
                continue

            print(f"わたしはメンバー {rank} で、{left} 以上 {right - 1} 以下の素数を数えますね！", flush = True) # TODO: この行はスパコンで時間計測する前に削除する
            for num in range(left, right):
                count += is_prime(num) # int 型と bool 型を足したとき、Python では True, False がそれぞれ 1, 0 として扱われるのでこれを利用してカウントする
            COMM.send(count, dest = LEADER_RANK, tag = repeat)

# 小数点以下を切り捨てたミリ秒単位の実行時間（実時間）を返す
def get_total_time_ms_floor(start_time):
    end_time = time.perf_counter()
    total_time_second = end_time - start_time
    total_time_ms = 1000 * total_time_second # 秒からミリ秒に変換
    total_time_ms_floor = int(total_time_ms) # 小数点以下を切り捨て
    return total_time_ms_floor

def main():
    start_time = None
    # ユーザーから受け取った入力をもとにリーダーがメンバーへ計算を指示する
    if rank == LEADER_RANK:
        n = int(input()) # 入力を受け取って整数に変換
        start_time = time.perf_counter()
        calc_order(n) # メンバーに計算の指示を出す

    # 各メンバーが計算を行う
    count_prime()

    # リーダーが計算結果を集計する
    COMM.Barrier() # 全てのスレッドを同期させる（待機）
    if rank == LEADER_RANK:
        total_count_prime = 0
        for member in range(1, ALL_MEMBER_SIZE):
            for repeat in range(1, ALL_MEMBER_SIZE):
                total_count_prime += COMM.recv(source = member, tag = repeat)

        total_time_ms_floor = get_total_time_ms_floor(start_time)
        print(n, total_count_prime, total_time_ms_floor) # 入力値, 1 から n までの素数の個数, 実行時間（ミリ秒）

# エントリポイント
if __name__ == "__main__":
    main()
