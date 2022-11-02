import asyncio
import websockets
import pyautogui
import cv2, math, time

async def hello():

    uri = "ws://127.0.0.1:30000"
    data = [0]*2
    async with websockets.connect(uri, ping_interval=None) as websocket:
        print(f"wait....")

        while True:
            greeting = await websocket.recv()

            data[0] = data[1]
            data[1] = greeting

            pyautogui.moveTo(600, 500)
            pyautogui.click()

            key = cv2.waitKey(1) & 0xff
            if key == 27: # ESC
                break

            if data[0] != data[1]:
                if data[0]=="YURA":
                    print("<<< ゆらゆら終わり")
                    pyautogui.keyUp("m")
                if data[0]=="RIGHT":
                    print("<<< 右終わり")
                    pyautogui.keyUp("right")
                    pyautogui.keyUp("up")
                if data[0]=="LEFT":
                    print("<<< 左終わり")
                    pyautogui.keyUp("left")
                    pyautogui.keyUp("up")
                if data[0]=="R_ROTATE":
                    print("<<< 右回転終わり")
                    pyautogui.keyUp("d")
                if data[0]=="L_ROTATE":
                    print("<<< 左回転終わり")
                    pyautogui.keyUp("a")
                if data[0]=="GO":
                    print("<<< 直進終わり")
                    pyautogui.keyUp("up")


                if data[1]=="FLY":
                    print("<<< 離陸")
                    pyautogui.keyDown("t")
                    pyautogui.keyUp("t")
                if data[1]=="LAND":
                    print("<<< 着地")
                    pyautogui.keyDown("l")
                    pyautogui.keyUp("l")


                if data[1]=="YURA":
                    print("<<< ゆらゆら")
                    pyautogui.keyDown("m")
                if data[1]=="RIGHT":
                    print("<<< 右")
                    pyautogui.keyDown("right")
                    pyautogui.keyDown("up")
                if data[1]=="LEFT":
                    print("<<< 左")
                    pyautogui.keyDown("left")
                    pyautogui.keyDown("up")
                if data[1]=="R_ROTATE":
                    print("<<< 右回転")
                    pyautogui.keyDown("d")
                if data[1]=="L_ROTATE":
                    print("<<< 左回転")
                    pyautogui.keyDown("a")
                if data[1]=="GO":
                    print("<<< 直進")
                    pyautogui.keyDown("up")


                if data[1]=="kurage":
                    print("<<< クラゲモードON")
                    pyautogui.keyDown("k")
                    pyautogui.keyUp("k")
                if data[1]=="tori":
                    print("<<< 鳥モードON")
                    pyautogui.keyDown("b")
                    pyautogui.keyUp("b")



asyncio.run(hello())
