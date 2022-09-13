import threading
import time


class MyThread(threading.Thread):
    def __init__(self, n):
        super(MyThread, self).__init__()
        self.n = n

    # run()を書き直す
    def run(self):
        print("task: {}".format(self.n))
        time.sleep(1)
        print('2s')
        time.sleep(1)
        print('1s')
        time.sleep(1)
        print('0s')
        time.sleep(1)

class MyThread2(threading.Thread):
    def __init__(self, n):
        super(MyThread2, self).__init__()
        self.n = n

    # run()を書き直す
    def run(self):
        print("task2: {}".format(self.n))
        time.sleep(1)
        print('2s')
        time.sleep(1)
        print('1s')
        time.sleep(1)
        print('0s')
        time.sleep(1)


t1 = MyThread("t1")
t2 = MyThread2("t2")

t1.start()
t2.start()
