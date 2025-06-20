import time

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

# 1 から n までの素数の個数を数え上げる
def count_prime(n):
    count = 0
    for num in range(1, n + 1):
        count += is_prime(num) # int 型と bool 型を足したとき、Python では True, False がそれぞれ 1, 0 として扱われるのでこれを利用してカウントする
    return count

# 小数点以下を切り捨てたミリ秒単位の実行時間（実時間）を返す
def get_total_time_ms_floor(start_time):
    end_time = time.perf_counter()
    total_time_second = end_time - start_time
    total_time_ms = 1000 * total_time_second # 秒からミリ秒に変換
    total_time_ms_floor = int(total_time_ms) # 小数点以下を切り捨て
    return total_time_ms_floor

def main():
    n = int(input()) # 入力を受け取って整数に変換
    start_time = time.perf_counter()
    total_count_prime = count_prime(n) # 素数の個数を数える
    total_time_ms_floor = get_total_time_ms_floor(start_time)

    # 計算結果の出力
    print(n, total_count_prime, total_time_ms_floor) # 入力値, 1 から n までの素数の個数, 実行時間（ミリ秒）

# エントリポイント
if __name__ == "__main__":
    main()
