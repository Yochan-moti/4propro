import websocket

from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time

class Test:
    def on_message(self, wsapp, message):
        print(message)

if __name__ == "__main__":
    test = Test()
    wsapp = websocket.WebSocketApp("ws://127.0.0.1:30000", on_message=test.on_message)
    wsapp.run_forever()
