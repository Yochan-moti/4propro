import asyncio
import websockets
import pyautogui
import cv2, math, time

async def hello():

    uri = "ws://127.0.0.1:30000"
    data = [0]*2
    async with websockets.connect(uri, ping_interval=None) as websocket:
        print(f"wait....")
        pyautogui.moveTo(600, 500)
        pyautogui.click()

        while True:
            greeting = await websocket.recv()

            data[0] = data[1]
            data[1] = greeting

            pyautogui.moveTo(600, 500)
            pyautogui.click()

            key = cv2.waitKey(1) & 0xff
            if key == 27: # ESC
                break

            if data[0] != data[1]:       # 受信内容が切り替わらない限り押しっぱなし
                if data[0]=="RIGHT":
                    print("<<< 右終わり")
                    pyautogui.keyUp("right")
                    pyautogui.keyUp("d")
                if data[0]=="LEFT":
                    print("<<< 左終わり")
                    pyautogui.keyUp("left")
                    pyautogui.keyUp("a")

                if data[1]=="FLY":
                    print("<<< 離陸")
                    pyautogui.keyDown("t")
                    pyautogui.keyUp("t")
                if data[1]=="LAND":
                    print("<<< 着地")
                    pyautogui.keyDown("l")
                    pyautogui.keyUp("l")
                if data[1]=="RIGHT":
                    print("<<< 右")
                    pyautogui.keyDown("right")
                    pyautogui.keyDown("d")
                if data[1]=="LEFT":
                    print("<<< 左")
                    pyautogui.keyDown("left")
                    pyautogui.keyDown("a")


asyncio.run(hello())
