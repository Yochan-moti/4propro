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
                print("<<< 離陸")
                pyautogui.keyDown("t")
                pyautogui.keyUp("t")
            if greeting=="FLY1":
                print("<<< ゆらゆら")
                pyautogui.keyDown("m")
                pyautogui.keyUp("m")
                sleep(3)
                print("sleep,3")
            if greeting=="LAND":
                print("<<< 着地")
                pyautogui.keyDown("l")
                pyautogui.keyUp("l")
            if greeting=="RIGHT":
                print("<<< 右")
                pyautogui.keyDown("d")
                pyautogui.keyUp("d")
            if greeting=="LEFT":
                print("<<< 左")
                pyautogui.keyDown("a")
                pyautogui.keyUp("a")


asyncio.run(hello())
