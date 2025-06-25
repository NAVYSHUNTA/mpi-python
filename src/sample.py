from mpi4py import MPI

# グローバル変数
COMM = MPI.COMM_WORLD # 全てのプロセスで共有されるコミュニケータ
rank = COMM.Get_rank() # 自プロセスのランク番号
SIZE = COMM.Get_size() # 並列度（厳密にはそのコミュニケータに所属するプロセスの総数）

def main():
    print(f"こんにちは！並列度は {SIZE} で、私はランク {rank} を担当しています！")

# エントリポイント
if __name__ == "__main__":
    main()
