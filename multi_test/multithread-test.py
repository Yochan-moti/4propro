
import threading

import websockets
import asyncio


from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time

def boil_udon():
  print("hello")
  tello = Tello()
  tello.connect()
  tello.streamon()
  frame_read = tello.get_frame_read()
  # tello.takeoff()
  while True:
      img = frame_read.frame
      cv2.imshow("drone", img)

      key = cv2.waitKey(1) & 0xff
      if key == 27: # ESC
          break
      elif key == ord('w'):
          tello.move_forward(30)
      elif key == ord('s'):
          tello.move_back(30)
      elif key == ord('a'):
          tello.move_left(30)
      elif key == ord('d'):
          tello.move_right(30)
      elif key == ord('e'):
          tello.rotate_clockwise(30)
      elif key == ord('q'):
          tello.rotate_counter_clockwise(30)
      elif key == ord('r'):
          tello.move_up(30)
      elif key == ord('f'):
          tello.move_down(30)

      elif key == ord('b'):
          tello.flip_back()

      elif key == ord('c'):
          tello.flip_back()
          tello.flip_forward()
          tello.flip_left()
          tello.flip_right()

  tello.land()

async def make_tuyu():
    print("hello,hello")
    uri = "ws://127.0.0.1:30000"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        print(f"wait....")
        while True:
            print(f"wait....")
            while True:
                greeting = websocket.recv()
                print(greeting)
# run()を書き直す
# def make_tuyu():
#     asyncio.run(hello())

print('うどんを作ります。')
thread1 = threading.Thread(target=boil_udon)
thread2 = threading.Thread(target=make_tuyu)
thread1.start()
thread2.start()
# asyncio.run(make_tuyu())
thread1.join()
thread2.join()
print('盛り付けます。')
print('うどんができました。')
