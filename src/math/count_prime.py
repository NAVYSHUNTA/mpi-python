# import time # 時間計測用のライブラリ

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
    n = int(input()) # 入力を受け取って整数に変換
    print(n, count_prime(n)) # (入力値, 答え, 実行時間) の形式にする（TODO）

if __name__ == "__main__":
    main()
