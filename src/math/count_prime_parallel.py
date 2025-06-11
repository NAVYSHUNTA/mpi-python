from mpi4py import MPI
import time
import math

# 素数判定
def is_prime(target):
    if target < 2:
        return False
    for i in range(2, target):
        if target % i == 0:
            return False
    return True

# 1 から n までの素数の個数を数え上げ
def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    n = 20000 # 今後、ユーザーからの入力に変更する？（TODO）

    if rank == 0:
        for i in range(1, size):
            base = math.ceil(n / (size - 1) ** 2)
            one_step_base = base * (size - 1)
            for j in range(1, size):
                s = (i - 1) * one_step_base
                comm.send([s + base * (j - 1) + 1, min(n + 1, s + base * j + 1)], dest = j, tag = i)
    else:
        for i in range(1, size):
            left, right = comm.recv(source = 0, tag = i)
            count = 0
            if left >= right:
                comm.send(count, dest = 0, tag = i)
                continue

            print(f"わたしはスタッフ {rank} で、{left} 以上 {right - 1} 以下の素数を数えますね！")
            for num in range(left, right):
                count += is_prime(num) # Python では True の場合 1, False の場合 0 として扱われる
            comm.send(count, dest = 0, tag = i)

    if rank == 0:
        time.sleep(0.5) # 他のスタッフが計算を終えるのを待つためにわざと待機
        total_count = 0
        for i in range(1, size):
            for j in range(1, size):
                total_count += comm.recv(source = i, tag = j)
        print(f"1 から {n} までの素数の個数は {total_count} です")

if __name__ == "__main__":
    main()
