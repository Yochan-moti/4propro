from djitellopy import Tello
import cv2, math, time

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

while True:
    img = frame_read.frame
    cv2.imshow("drone", img)

    key = cv2.waitKey(1) & 0xff
    if key == 27: # ESC
        break

    elif key == ord('t'):
        tello.takeoff()
    elif key == ord('l'):
        tello.land()
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('m'):
        tello.move_up(20)
        tello.move_down(20)
        tello.move_up(20)
        tello.move_down(20)


tello.land()
