# simple example demonstrating how to control a Tello using your keyboard.
# For a more fully featured example see manual-control-pygame.py
#
# Use W, A, S, D for moving, E, Q for rotating and R, F for going up and down.
# When starting the script the Tello will takeoff, pressing ESC makes it land
#  and the script exit.

# キーボードを使用して Tello を操作する方法を示す簡単な例です。
# より高度な機能を持つサンプルは manual-control-pygame.py を参照してください。
# 移動には W, A, S, D を、回転には E, Q を、上下移動には R, F を使用します。
# スクリプトを起動するとTelloは離陸し、ESCキーを押すと着陸してスクリプトが終了します。

from djitellopy import Tello
import cv2, math, time

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

# tello.takeoff()

while True:
    # In reality you want to display frames in a seperate thread. Otherwise
    #  they will freeze while the drone moves.
    # 実際には、フレームを別のスレッドに表示したい。そうしないと、ドローンが動いている間にフリーズしてしまいます。
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
        tello.move_up(10)
        tello.move_down(10)
        tello.move_up(10)
        tello.move_down(10)


tello.land()
