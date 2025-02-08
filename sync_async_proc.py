import queue
import threading
import concurrent.futures
import time


class SyncAsyncRspProcessor:
    """ 同步异步响应处理器
    * 如果任务在规定时间内完成，则直接返回结果
    * 如果任务在规定时间内未完成，则在 get_result_timeout 时间结束后，返回None
       * 如果在 fail_timeout 时间内完成，则调用回调函数 complete_cb
       * 如果在 fail_timeout 时间内未完成，则在 fail_timeout 时间结束后，杀掉处理线程，并回调 fail_cb
    """

    def __init__(self, task, timeout, complete_cb=None, fail_timeout=None, fail_cb=None):
        """
        :param task: 任务函数，需要有返回
        :param timeout: 获取结果的超时时间，单位为秒
        :param complete_cb: 任务完成后的回调函数，如果为None，则不设置回调
        :param fail_timeout: 任务失败的超时时间，如果为None，则不设置超时
        :param fail_cb: 任务失败后的回调函数，如果为None，则不设置回调
        """
        self.q = queue.Queue(maxsize=1)
        self.timeout = timeout
        self.task = task
        self.complete_cb = complete_cb
        self.fail_timeout = fail_timeout
        self.fail_cb = fail_cb

        if self.fail_timeout and self.fail_timeout < self.timeout:
            raise ValueError("fail_timeout should be greater than timeout")

        self.timeout_event = threading.Event()
        self.timeout_event.clear()
        self.lock = threading.Lock()

    def get_result(self):
        thread = threading.Thread(target=self.worker_, args=(), daemon=True)
        thread.start()

        try:
            return self.q.get(timeout=self.timeout)
        except queue.Empty:
            self.timeout_event.set()
            return None

    def worker_(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.task)
            try:
                result = future.result(timeout=self.fail_timeout)
                # FIXME 这里有先进入Empty而未设置timeout event的情况，可能导致被推送的Queue没有处理
                if not self.timeout_event.is_set():
                    self.q.put(result)
                    return
                elif self.complete_cb:
                    self.complete_cb(result)
            except concurrent.futures.TimeoutError:
                if self.fail_cb:
                    self.fail_cb()


def main():
    def task():  # 模拟一个耗时较长的操作
        time.sleep(1.5)
        return "Result from tt"

    def cb(result):
        print("cb", result, time.time())

    print("start", time.time())
    ret = SyncAsyncRspProcessor(task, cb, 2, 4).get_result()
    print("finish", ret, time.time())
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
