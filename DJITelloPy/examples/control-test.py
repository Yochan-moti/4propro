# サンプルプログラムとただカウントするだけプログラムのマルチスレッド
import threading

from djitellopy import Tello
import cv2, math, time


class ope(threading.Thread):
    def __init__(self, tello):
        super(ope, self).__init__()
        self.tello = Tello()

    def run(self):
        self.tello.connect()

        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        # self.tello.takeoff()

        while True:
            img = frame_read.frame
            cv2.imshow("drone", img)

            key = cv2.waitKey(1) & 0xff
            if key == 27: # ESC
                break
            elif key == ord('t'):
                self.tello.takeoff()
            elif key == ord('w'):
                self.tello.move_forward(30)
            elif key == ord('s'):
                self.tello.move_back(30)
            elif key == ord('a'):
                self.tello.move_left(30)
            elif key == ord('d'):
                self.tello.move_right(30)
            elif key == ord('e'):
                self.tello.rotate_clockwise(30)
            elif key == ord('q'):
                self.tello.rotate_counter_clockwise(30)
            elif key == ord('r'):
                self.tello.move_up(30)
            elif key == ord('f'):
                self.tello.move_down(30)

        self.tello.land()

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


t1 = ope("t1")
t2 = MyThread2("t2")

t1.start()
t2.start()
