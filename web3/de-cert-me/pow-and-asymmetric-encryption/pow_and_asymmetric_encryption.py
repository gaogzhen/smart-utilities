import hashlib
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


def find_hash_mt(nickname, leading_zeros, num_threads=4):
    """
    多线程版本的工作量证明

    Args:
        nickname: 用户昵称
        leading_zeros: 要求的前导0数量
        num_threads: 线程数
    """
    print(f"\n开始多线程寻找 {leading_zeros} 个前导0的哈希值...")
    print(f"昵称: {nickname}, 线程数: {num_threads}")
    print("-" * 60)

    start_time = time.time()
    found = False
    result = None
    lock = threading.Lock()
    counter = 0

    target_prefix = '0' * leading_zeros

    def worker(thread_id, start_nonce, batch_size=10000):
        nonlocal found, result, counter
        nonce = start_nonce

        while not found:
            for i in range(batch_size):
                if found:
                    return None

                data = f"{nickname}{nonce + i}"
                hash_result = hashlib.sha256(data.encode()).hexdigest()

                if hash_result.startswith(target_prefix):
                    with lock:
                        if not found:  # 双重检查，防止多个线程同时找到
                            found = True
                            result = (nonce + i, data, hash_result)
                            return result

            with lock:
                counter += batch_size
                if counter % 100000 == 0:
                    print(f"已尝试 {counter:,} 次...", end='\r')

            nonce += batch_size

    # 创建并启动线程
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i, i * 1000000))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed = end_time - start_time

    if result:
        nonce, data, hash_result = result
        print(f"\n找到符合条件的哈希！")
        print(f"花费时间: {elapsed:.4f} 秒")
        print(f"尝试次数: {counter:,} 次（约）")
        print(f"原始数据: '{data}'")
        print(f"SHA256哈希: {hash_result}")
        print(f"哈希前{leading_zeros}位: {hash_result[:leading_zeros]}")

        return elapsed, nonce, data, hash_result

    return None


def main_mt():
    """多线程版本的主函数"""
    nickname = "goagzhen"

    print("=" * 60)
    print("多线程工作量证明（POW）")
    print("=" * 60)

    # 寻找4个前导0的哈希值
    time_4zeros, nonce_4, data_4, hash_4 = find_hash_mt(nickname, 4, num_threads=8)

    # 寻找5个前导0的哈希值
    time_5zeros, nonce_5, data_5, hash_5 = find_hash_mt(nickname, 5, num_threads=8)

    print("\n" + "=" * 60)
    print("结果对比:")
    print("=" * 60)
    print(f"4个0前导: {time_4zeros:.4f} 秒")
    print(f"5个0前导: {time_5zeros:.4f} 秒")
    print(f"难度增加比例: {time_5zeros / time_4zeros:.2f} 倍")


# 运行多线程版本
if __name__ == "__main__":
    main_mt()