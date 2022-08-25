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
