import time # 時間計測用のライブラリ

# 素数判定
def is_prime(target):
    if target < 2:
        return False
    for div in range(2, target):
        if target % div == 0:
            return False
    return True

# 1 から n までの素数の個数を数え上げ
def count_prime(n):
    count = 0
    for num in range(1, n + 1):
        count += is_prime(num) # Python では True の場合 1, False の場合 0 として扱われる
    return count

def main():
    n = int(input()) # 
    start = time.time() # 開始時間を記録
    answer = count_prime(n) # 素数の個数を数える
    end = time.time() # 終了時間を記録
    total_time = end - start #実行時間を計算
    print(n, answer, total_time) # (入力値, 答え, 実行時間) の形式にする（TODO）

if __name__ == "__main__":
    main()
