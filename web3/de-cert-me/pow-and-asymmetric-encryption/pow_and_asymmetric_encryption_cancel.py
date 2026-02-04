import hashlib
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class POWSolver:
    def __init__(self, nickname):
        self.nickname = nickname
        self.found_event = threading.Event()  # 用于通知找到结果的事件
        self.result = None
        self.result_lock = threading.Lock()
        self.total_tried = 0
        self.counter_lock = threading.Lock()

    def find_hash(self, leading_zeros, num_threads=8, batch_size=10000):
        """
        使用线程池寻找满足条件的哈希值

        Args:
            leading_zeros: 要求的前导0数量
            num_threads: 线程数
            batch_size: 每个任务批处理的nonce数量
        """
        print(f"\n开始寻找 {leading_zeros} 个前导0的哈希值...")
        print(f"昵称: {self.nickname}, 线程数: {num_threads}")
        print("-" * 60)

        # 重置状态
        self.found_event.clear()
        self.result = None
        self.total_tried = 0

        start_time = time.time()
        target_prefix = '0' * leading_zeros

        # 创建线程池
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # 提交初始任务
            futures = []
            for i in range(num_threads):
                # 每个线程处理不同的nonce范围，避免重复
                start_nonce = i * 1000000
                future = executor.submit(
                    self._worker_task,
                    start_nonce, target_prefix, batch_size
                )
                futures.append(future)

            # 等待任意一个任务完成或找到结果
            done, not_done = [], futures
            while not self.found_event.is_set() and not_done:
                # 检查已完成的任务
                done_now, not_done = [], []
                for future in not_done:
                    if future.done():
                        done_now.append(future)
                    else:
                        not_done.append(future)

                # 处理已完成的任务
                for future in done_now:
                    if future.result():  # 如果任务返回了有效结果
                        break

                # 如果还没找到，等待一小段时间
                if not self.found_event.is_set() and not_done:
                    time.sleep(0.01)

            # 如果找到结果，取消所有未完成的任务
            if self.found_event.is_set():
                for future in not_done:
                    future.cancel()

        end_time = time.time()
        elapsed = end_time - start_time

        if self.result:
            nonce, data, hash_result = self.result
            print(f"\n找到符合条件的哈希！")
            print(f"花费时间: {elapsed:.4f} 秒")
            print(f"尝试次数: {self.total_tried:,} 次")
            print(f"原始数据: '{data}'")
            print(f"SHA256哈希: {hash_result}")
            print(f"哈希前{leading_zeros}位: {hash_result[:leading_zeros]}")

            # 显示进度信息
            hashes_per_sec = self.total_tried / elapsed if elapsed > 0 else 0
            print(f"哈希速度: {hashes_per_sec:,.0f} 次/秒")

            return elapsed, nonce, data, hash_result

        return None

    def _worker_task(self, start_nonce, target_prefix, batch_size):
        """工作线程任务"""
        nonce = start_nonce

        while not self.found_event.is_set():
            # 处理一批nonce
            for i in range(batch_size):
                if self.found_event.is_set():
                    return False

                data = f"{self.nickname}{nonce + i}"
                hash_result = hashlib.sha256(data.encode()).hexdigest()

                # 检查是否满足条件
                if hash_result.startswith(target_prefix):
                    # 使用锁确保只有一个线程设置结果
                    with self.result_lock:
                        if not self.result:  # 双重检查
                            self.result = (nonce + i, data, hash_result)
                            self.found_event.set()  # 通知所有线程
                            return True

                # 更新计数器（定期更新，避免锁竞争）
                if (nonce + i) % 100 == 0:  # 每100次更新一次
                    with self.counter_lock:
                        self.total_tried += 100

            # 更新计数器（处理完一批后）
            with self.counter_lock:
                self.total_tried += batch_size

            nonce += batch_size

            # 定期打印进度
            if nonce % (batch_size * 100) == 0:
                with self.counter_lock:
                    print(f"已尝试 {self.total_tried:,} 次...", end='\r')

        return False


class AdvancedPOWSolver(POWSolver):
    """更高级的POW求解器，支持动态任务分配"""

    def find_hash_advanced(self, leading_zeros, num_threads=8):
        """使用动态任务分配的高级版本"""
        print(f"\n[高级模式] 寻找 {leading_zeros} 个前导0的哈希值...")
        print(f"昵称: {self.nickname}, 线程数: {num_threads}")
        print("-" * 60)

        self.found_event.clear()
        self.result = None
        self.total_tried = 0

        start_time = time.time()
        target_prefix = '0' * leading_zeros

        # 使用更智能的任务分配
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # 使用future列表和任务队列
            futures = []
            next_nonce = 0

            # 提交初始任务
            for _ in range(num_threads * 2):  # 两倍的任务，保持队列饱满
                if self.found_event.is_set():
                    break

                future = executor.submit(
                    self._smart_worker_task,
                    next_nonce, target_prefix
                )
                futures.append(future)
                next_nonce += 10000  # 每个任务处理10000个nonce

            # 等待结果
            try:
                # 使用as_completed，等待第一个完成的任务
                for future in as_completed(futures, timeout=None):
                    if self.found_event.is_set() or future.result():
                        break

                    # 如果任务完成但没有找到结果，添加新任务
                    if not self.found_event.is_set():
                        new_future = executor.submit(
                            self._smart_worker_task,
                            next_nonce, target_prefix
                        )
                        futures.append(new_future)
                        next_nonce += 10000
            finally:
                # 找到结果后取消所有任务
                self.found_event.set()
                for f in futures:
                    f.cancel()

        end_time = time.time()
        elapsed = end_time - start_time

        if self.result:
            nonce, data, hash_result = self.result
            print(f"\n找到符合条件的哈希！")
            print(f"花费时间: {elapsed:.4f} 秒")
            print(f"尝试次数: {self.total_tried:,} 次")
            print(f"原始数据: '{data}'")
            print(f"SHA256哈希: {hash_result}")
            print(f"哈希前{leading_zeros}位: {hash_result[:leading_zeros]}")

            # 计算概率
            probability = 1 / (16 ** leading_zeros)
            expected_tries = 1 / probability
            print(f"理论概率: 1/{16 ** leading_zeros:,} ≈ {probability:.2e}")
            print(f"期望尝试次数: {expected_tries:,.0f}")
            print(f"实际效率: {self.total_tried / expected_tries:.2%}")

            return elapsed, nonce, data, hash_result

        return None

    def _smart_worker_task(self, start_nonce, target_prefix):
        """智能工作线程任务"""
        batch_size = 1000
        nonce = start_nonce

        for i in range(batch_size):
            if self.found_event.is_set():
                return False

            data = f"{self.nickname}{nonce + i}"
            hash_result = hashlib.sha256(data.encode()).hexdigest()

            if hash_result.startswith(target_prefix):
                with self.result_lock:
                    if not self.result:
                        self.result = (nonce + i, data, hash_result)
                        self.found_event.set()
                        return True

            # 更新计数器
            if (nonce + i) % 10 == 0:
                with self.counter_lock:
                    self.total_tried += 10

        with self.counter_lock:
            self.total_tried += batch_size

        # 定期报告进度
        if start_nonce % 100000 == 0:
            with self.counter_lock:
                print(f"已尝试 {self.total_tried:,} 次...", end='\r')

        return False


def benchmark_solvers():
    """对比不同求解器的性能"""
    nickname = "DeepSeek"

    print("=" * 60)
    print("POW求解器性能对比")
    print("=" * 60)

    # 测试不同前导0数量的求解时间
    for zeros in [3, 4, 5, 6]:
        print(f"\n\n测试 {zeros} 个前导0:")
        print("-" * 40)

        # 基本求解器
        solver1 = POWSolver(nickname)
        start = time.time()
        result1 = solver1.find_hash(zeros, num_threads=4)
        time1 = time.time() - start

        # 高级求解器
        solver2 = AdvancedPOWSolver(nickname)
        start = time.time()
        result2 = solver2.find_hash_advanced(zeros, num_threads=4)
        time2 = time.time() - start

        print(f"\n性能对比:")
        print(f"基本求解器: {time1:.4f} 秒")
        print(f"高级求解器: {time2:.4f} 秒")
        print(f"速度提升: {time1 / time2:.2f}x")


def main():
    """主函数"""
    nickname = "gaogzhen"

    print("=" * 60)
    print("优化的POW求解器（线程池 + 即时终止）")
    print("=" * 60)

    # 使用高级求解器
    solver = AdvancedPOWSolver(nickname)

    # 寻找4个前导0的哈希值
    print("\n" + "=" * 60)
    result_4 = solver.find_hash_advanced(4, num_threads=8)

    # 寻找5个前导0的哈希值
    print("\n" + "=" * 60)
    result_5 = solver.find_hash_advanced(5, num_threads=8)

    if result_4 and result_5:
        time_4, nonce_4, data_4, hash_4 = result_4
        time_5, nonce_5, data_5, hash_5 = result_5

        print("\n" + "=" * 60)
        print("最终结果对比:")
        print("=" * 60)
        print(f"4个0前导: {time_4:.4f} 秒, 尝试 {solver.total_tried:,} 次")
        print(f"5个0前导: {time_5:.4f} 秒, 尝试 {solver.total_tried:,} 次")

        # 计算难度增加比例
        difficulty_4 = 16 ** 4  # 4个0的概率
        difficulty_5 = 16 ** 5  # 5个0的概率
        expected_ratio = difficulty_5 / difficulty_4  # 期望的时间比例

        print(f"\n理论难度对比:")
        print(f"4个0难度: 1/{difficulty_4:,} ≈ {1 / difficulty_4:.2e}")
        print(f"5个0难度: 1/{difficulty_5:,} ≈ {1 / difficulty_5:.2e}")
        print(f"难度增加倍数: {expected_ratio:.1f}x (理论)")
        print(f"实际时间倍数: {time_5 / time_4:.1f}x")


if __name__ == "__main__":
    # 运行主程序
    main()

    # 如果需要性能对比，可以取消下面的注释
    benchmark_solvers()