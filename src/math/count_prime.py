import time

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
    start_time = time.time()
    total_count_prime = count_prime(n) # 素数の個数を数える
    end_time = time.time()
    total_time_second = end_time - start_time
    total_time_ms = 1000 * total_time_second # 秒からミリ秒に変換
    total_time_ms_floor = int(total_time_ms) # 小数点以下を切り捨て
    print(n, total_count_prime, total_time_ms_floor) # 入力値, 1 から n までの素数の個数, 実行時間（ミリ秒）

if __name__ == "__main__":
    main()
