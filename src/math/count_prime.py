# 素数判定
def is_prime(target):
    if target < 2:
        return False
    for i in range(2, target):
        if target % i == 0:
            return False
    return True

# 1 から n までの素数の個数を数え上げ
def count_prime(n):
    count = 0
    for i in range(1, n + 1):
        count += is_prime(i) # True の場合は 1, False の場合は 0 として扱われる
    return count

def main():
    print("1 から n までの素数を数え上げます")
    print("1 以上の正整数 n を入力してください: ", end="")
    n = int(input()) # 入力を受け取って整数に変換
    if n < 1:
        print("入力が不正です")
        print(f"{n} は 1 以上の正整数ではありません")
    else:
        print(f"1 から {n} までの素数の個数は {count_prime(n)} です")

if __name__ == "__main__":
    main()