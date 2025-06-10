from mpi4py import MPI
import time

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
            base = n // (size - 1)
            comm.send([base * (i - 1), min(n, base * i)], dest = i, tag = i)
    else:
        left, right = comm.recv(source = 0, tag = rank)
        print(f"わたしはスタッフ {rank} で、{left} 以上 {right - 1} 以下の素数を数えますね！")
        count = 0
        for i in range(left, right):
            count += is_prime(i) # Python では True の場合 1, False の場合 0 として扱われる
        comm.send(count, dest = 0, tag = rank)

    if rank == 0:
        time.sleep(0.5) # 他のスタッフが計算を終えるのを待つためにわざと待機
        total_count = 0
        for i in range(1, size):
            total_count += comm.recv(source = i, tag = i)
        print(f"1 から {n} までの素数の個数は {total_count} です")

if __name__ == "__main__":
    main()
