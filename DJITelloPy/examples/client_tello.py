# websocketと使ったドローン操作(カメラ取得できない)

import asyncio
import websockets

from djitellopy import Tello
import cv2, math, time

# tello.takeoff()

async def hello():

    tello = Tello()
    tello.connect()

    tello.streamon()
    # frame_read = tello.get_frame_read()

    # tello.takeoff()

    fly=False

    uri = "ws://127.0.0.1:30000"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        print(f"wait....")
        while True:
            # img = frame_read.frame
            # cv2.imshow("drone", img)

            # tello.takeoff()

            greeting = await websocket.recv()

            key = cv2.waitKey(1) & 0xff
            if key == 27: # ESC
                break

            if greeting=="FLY":
                print("<<< 上昇")
                tello.takeoff()
            if greeting=="DOWN":
                print("<<< 着地")
                tello.land()
            if greeting=="RIGHT":
                print("<<< 右")
                tello.move_right(30)
            if greeting=="LEFT":
                print("<<< 左")
                tello.move_left(30)


asyncio.run(hello())
