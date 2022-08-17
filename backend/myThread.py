import threading, time

# 定义一个MyThread.py线程类 用于多线程返回结果
class MyThread(threading.Thread):

    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            # print(traceback.print_exc())
            return "threading error"


# 获取多线程return返回值的测试方法
def admin(number):
    uiu = number
    for i in range(10):
        uiu = uiu + i
    return uiu


if __name__ == "__main__":
    # 创建四个线程
    more_th1 = MyThread(admin, (5,))
    more_th2 = MyThread(admin, (10,))
        # 启动线程
    more_th1.start()
    more_th2.start()
    # 线程等待
    more_th1.join()
    a=more_th1.get_result()
    print(a)
    more_th2.join()
    print(more_th2.get_result())
