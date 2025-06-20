from mpi4py import MPI

# グローバル変数
COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
SIZE = COMM.Get_size()

def main():
    print(f"こんにちは！並列度は {SIZE} で、私はランク {rank} を担当しています！")

# エントリポイント
if __name__ == "__main__":
    main()
