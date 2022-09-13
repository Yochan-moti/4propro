# import websocket
#
from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time

S = 60
FPS = 120

class FrontEnd(object):
    def __init__(self):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        # Telloドローンと対話するためのTelloオブジェクトを初期化する。
        self.tello = Tello()

        # Drone velocities between -100~100
        # ドローンの速度：-100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        # create update timer
        # アップロードタイマーを作成
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

    def run(self):

        self.tello.connect()
        self.tello.set_speed(self.speed)

        # In case streaming is on. This happens when we quit this program without the escape key.
        # ストリーミングがオンになっている場合。エスケープキーを使わずにこのプログラムを終了すると、この現象が発生します。
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        should_stop = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                #     else:
                #         self.keydown(event.key)
                # elif event.type == pygame.KEYUP:
                #     self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            # battery n. 电池
            text = "Battery: {}%".format(self.tello.get_battery())
            cv2.putText(frame, text, (5, 720 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        # 終了前に必ず呼び出す。リソースの割り当てを解除すること。
        self.tello.end()


    def update(self):
        """
        Update routine. Send velocities to Tello.
        """
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)

    # def on_message(self,wsapp, message):
    #     print(message)

def main():
    frontend = FrontEnd()
    # wsapp = websocket.WebSocketApp("ws://127.0.0.1:30000", on_message=FrontEnd().on_message)
    # wsapp.run_forever()

    frontend.run()


if __name__ == '__main__':
    main()
