from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time

# Speed of the drone
# ドローンのスピード
S = 20
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
# pygameのウィンドウ表示の1秒あたりのフレーム数。入力情報は1フレームに1回処理されるため、数値が低いと入力遅延も発生します。
FPS = 120

class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations (yaw)
            - W and S: Up and down.

        Tello の表示を維持し、キーボードキーで移動します。
        終了するには、エスケープキーを押します。
        操作方法は
            - T: 離陸
            - L: 着陸
            - 矢印キー。前進、後退、左、右
            - AとD：反時計回りと時計回りの回転（ヨー）
            - WとS：上と下

    """

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

        self.honoo = pygame.image.load(gazo)
        self.honoo = pygame.transform.scale(self.honoo, (200, 200))

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
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

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
            self.screen.blit(self.honoo, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        # 終了前に必ず呼び出す。リソースの割り当てを解除すること。
        self.tello.end()

    def keydown(self, key):
        """
        Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity 前
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity　後ろ
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity　左
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity　右
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity　上昇
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity　下降
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity　反時計回り
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity　時計回り
            self.yaw_velocity = S
        elif key == pygame.K_m:
            gazo = "honoo_hi_fire.png"


    def keyup(self, key):
        """
        Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False
        elif key == pygame.K_m:
            gazo = ""



    def update(self):
        """
        Update routine. Send velocities to Tello.
        """
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)


def main():
    frontend = FrontEnd()

    frontend.run()


if __name__ == '__main__':
    main()
