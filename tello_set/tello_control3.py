from djitellopy import Tello
import cv2

from pygame.locals import *
import pygame
import sys

import numpy as np
import time

# Speed of the drone
# ドローンのスピード
S = 20
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
# pygameのウィンドウ表示の1秒あたりのフレーム数。入力情報は1フレームに1回処理されるため、数値が低いと入力遅延も発生します。
FPS = 120


############################
### スプライトクラス継承
############################
class MySprite(pygame.sprite.Sprite):

    ############################
    ### 初期化メソッド(ファイル名,X軸,Y軸,X軸移動,Y軸移動)
    ############################
    def __init__(self, name, x, y, mv_x, mv_y):
        pygame.sprite.Sprite.__init__(self)

        ### 透過変換でファイル読み込み
        self.image = pygame.image.load(name).convert_alpha()

        ### 画像サイズ変更
        self.image = pygame.transform.scale(self.image, (200, 200))

        ### 画像サイズ取得
        width  = self.image.get_width()
        height = self.image.get_height()

        ### 四角形オブジェクト生成
        self.rect = Rect(x, y, width, height)

        ### 移動位置設定
        self.mv_x = mv_x
        self.mv_y = mv_y

    ############################
    ### 画面更新
    ############################
    def update(self):

        ### 移動描写
        self.rect.move_ip(self.mv_x, self.mv_y)

        ### 画面の範囲外ならオブジェクト移動位置を反転
        if self.rect.left < 0 or self.rect.right  > 960:
            self.mv_x = -self.mv_x
        if self.rect.top  < 0 or self.rect.bottom > 720:
            self.mv_y = -self.mv_y

        ### 画面内に収める
        self.rect = self.rect.clamp(Rect(0,0,960,720))

    ############################
    ### オブジェクト描画
    ############################
    def draw(self, surface):
        surface.blit(self.image, self.rect)




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

        self.fontS = pygame.font.Font("font/JKG-L_3.ttf", 20)

        self.mode_text = ""

        # Creat pygame window
        pygame.display.set_caption("あにまるドローン")
        self.screen = pygame.display.set_mode([960, 720])

        # ドラゴンエフェクト
        self.img1 = MySprite("honoo.png",   0,   0, 8, 2)
        self.img2 = MySprite("honoo.png", 100, 100, 6, 4)
        self.img3 = MySprite("honoo.png", 200, 200, 4, 6)
        self.img4 = MySprite("honoo.png", 300, 300, 2, 8)
        self.cry_sound = pygame.mixer.Sound("dragon.mp3")

        # クラゲエフェクト
        self.img_k1 = MySprite("kaminari.png",   0,   0, 8, 2)
        self.img_k2 = MySprite("kaminari.png", 100, 100, 6, 4)
        self.img_k3 = MySprite("kaminari.png", 200, 200, 4, 6)
        self.img_k4 = MySprite("kaminari.png", 300, 300, 2, 8)
        self.cry_sound_kurage = pygame.mixer.Sound("kaminari.mp3")
        # self.kurage_BGM = pygame.mixer.Sound("kurage_BGM.mp3")
        self.bg = pygame.image.load("haikei.png").convert_alpha()


        # 鳥エフェクト
        self.img_t1 = MySprite("kaze.png",   0,   0, 8, 2)
        self.img_t2 = MySprite("kaze.png", 100, 100, 6, 4)
        self.img_t3 = MySprite("kaze.png", 200, 200, 4, 6)
        self.img_t4 = MySprite("kaze.png", 300, 300, 2, 8)
        self.cry_sound_tori = pygame.mixer.Sound("tori.mp3")



        ### グループ設定
        self.img_grp = pygame.sprite.Group()
        self.img_grp_haikei = pygame.sprite.Group()

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
            cv2.putText(frame, self.mode_text, (5, 720 - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))

            self.screen.blit(self.bg, (0, 0))

            ### スプライトを更新
            self.img_grp.update()
            ### スプライトを描画
            self.img_grp.draw(self.screen)

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

        elif key == pygame.K_m:  # ドラゴンエフェクト＆効果音
            self.img_grp = pygame.sprite.Group(self.img1, self.img2, self.img3, self.img4)
            self.cry_sound.play()
        elif key == pygame.K_k:  #　クラゲエフェクト＆効果音
            self.img_grp = pygame.sprite.Group(self.img_k1, self.img_k2, self.img_k3, self.img_k4)
            self.cry_sound_kurage.play()
        elif key == pygame.K_b:  #　鳥エフェクト＆効果音
            self.img_grp = pygame.sprite.Group(self.img_t1, self.img_t2, self.img_t3, self.img_t4)
            self.cry_sound_tori.play()

        elif key == pygame.K_r:
            self.mode_text = "JellyFish mode"
        #     self.screen.blit(self.bg, (0, 0))
        #     pygame.display.update()
        #     self.kurage_BGM.play(-1)


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
            self.img_grp = pygame.sprite.Group()
        elif key == pygame.K_k:
            self.img_grp = pygame.sprite.Group()
        elif key == pygame.K_b:
            self.img_grp = pygame.sprite.Group()

        # elif key == pygame.K_r:
        #     self.screen.blit(self.bg, (0, 0))


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
