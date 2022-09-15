import asyncio
import websockets
import pyautogui
import cv2, math, time

async def hello():

    uri = "ws://127.0.0.1:30000"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        print(f"wait....")
        while True:
            greeting = await websocket.recv()

            pyautogui.moveTo(600, 500)
            pyautogui.click()

            key = cv2.waitKey(1) & 0xff
            if key == 27: # ESC
                break

            if greeting=="FLY":
                print("<<< 上昇")
                pyautogui.keyDown("t")
                pyautogui.keyUp("t")
            if greeting=="LAND":
                print("<<< 着地")
                pyautogui.keyDown("l")
                pyautogui.keyUp("l")
            if greeting=="RIGHT":
                print("<<< 右")
                pyautogui.keyDown("right")
                pyautogui.keyUp("right")
                # tello.move_right(30)
            if greeting=="LEFT":
                print("<<< 左")
                pyautogui.keyDown("left")
                pyautogui.keyUp("left")
                # tello.move_left(30)


asyncio.run(hello())
