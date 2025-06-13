from mpi4py import MPI
import time
import math

# グローバル変数
COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
LEADER_RANK = 0 # リーダーの rank 番号
ALL_MEMBER_SIZE = COMM.Get_size()
WORK_MEMBER_SIZE = ALL_MEMBER_SIZE - 1 # 並列度（メンバーに指示を出すリーダー自身を除く）

# 素数判定
def is_prime(target):
    if target < 2:
        return False
    for div in range(2, target):
        if target % div == 0:
            return False
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

            print(f"わたしはメンバー {rank} で、{left} 以上 {right - 1} 以下の素数を数えますね！") # TODO: この行はスパコンで時間計測する前に削除する
            for num in range(left, right):
                count += is_prime(num) # Python では True の場合 1, False の場合 0 として扱われる
            COMM.send(count, dest = LEADER_RANK, tag = repeat)

def main():
    # ユーザーから受け取った入力をもとにリーダーがメンバーへ計算を指示する
    if rank == LEADER_RANK:
        n = int(input()) # 入力を受け取って整数に変換
        calc_order(n) # メンバーに計算の指示を出す

    # 各メンバーが計算を行う
    count_prime()

    # リーダーが計算結果を集計する
    if rank == LEADER_RANK:
        time.sleep(0.5) # 他のメンバーが計算を終えるのを待つためにわざと待機（TODO: この行はスパコンで時間計測する前に削除する）
        total_prime_count = 0
        for member in range(1, ALL_MEMBER_SIZE):
            for repeat in range(1, ALL_MEMBER_SIZE):
                total_prime_count += COMM.recv(source = member, tag = repeat)
        print(n, total_prime_count)

if __name__ == "__main__":
    main()
