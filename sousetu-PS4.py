import RPi.GPIO as GPIO
import time
from pygame.locals import *
import pygame
import sys

pygame.init()# Pygameを初期化
screen = pygame.display.set_mode((400, 330))# 画面を作成
pygame.display.set_caption("PS4 event")# タイトルを作成

# モータードライバーを接続したGPIOピンの定義(1:GPIO 2:GPIO 3:GND)
pin11, pin12, pin13 = 33, 35, 34
pin21, pin22, pin23 = 8, 10, 9

# いろんな変数の定義
Input1, Input2, Input3 = 0, 0, 0
V1, V2 = 0, 0
Record1, Record2 = 0, 0
Phase1, Phase2 = 0, 0

# ピンの設定 例)出力、入力
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin11, GPIO.OUT)#黄色い線-正転・反転用(電流を送ると反転)
GPIO.output(pin11, GPIO.LOW)
GPIO.setup(pin12, GPIO.OUT)#白い線-pwm用(出力をそのまま変更)
GPIO.output(pin12, GPIO.LOW)
GPIO.setup(pin21, GPIO.OUT)#黄色い線-正転・反転用(電流を送ると反転)
GPIO.output(pin21, GPIO.LOW)
GPIO.setup(pin22, GPIO.OUT)#白い線-pwm用(出力をそのまま変更)
GPIO.output(pin22, GPIO.LOW)
#LEDを接続したGPIOピンの定義
GPIO.setup(11, GPIO.OUT)#オレンジ色の線-チカチカ用
GPIO.setup(12, GPIO.OUT)#オレンジ色の線-チカチカ用

pwm1 = GPIO.PWM(pin12, 1000)#pin12, 1000Hzのpwm
pwm2 = GPIO.PWM(pin22, 1000)#pin22, 1000Hzのpwm

pwm1.start(0)#開始,初期出力0
pwm2.start(0)#開始,初期出力0

#　pwmの式(回転速度の変化をなめらかにする)
def pwmOutput(start, stop, step, sleep, pwm):
    if step == 0: return#速度を変えないときエラーが出ないようにする
    for i in range(start, stop + (1 if step > 0 else -1), int(step)):
        pwm.ChangeDutyCycle(i)
        time.sleep(sleep)

# programスタート
print("いってらっしゃい！\n気をつけてね！")

try:
    while PS4.getButtonClick(PS) != 1:#9でない場合繰り替えす→9になると終了
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
   
                if PS4.getButtonPress(UP) == 1:
                    Input1 = 1
                    Phase1 += 1
                    print("straight")
                if PS4.getButtonPress(DOWN) == 1:
                    Input1 = 2
                    Phase1 += 1
                    print("back")
                        
                if PS4.getButtonPress(L1) == 1:
                    Input2 = 1
                    Phase2 += 1
                    print("左回り")
                        
                if PS4.getButtonPress(R1) == 1:
                    Input2 = 2
                    Phase2 += 1
                    print("右回り")
                    
                if PS4.getButtonPress(LEFT) == 1:
                    print("左ライトon")
                    GPIO.output(11, True)

                if PS4.getButtonPress(CIRCLE) == 1:
                    GPIO.output(12, True)
                    print("右ライトon")
                
                if PS4.getButtonPress(UP) == 0:
                    Input1 = 0
                    Phase1 -= 1
                    print("straight")
                if PS4.getButtonPress(DOWN) == 0:
                    Input1 = 0
                    Phase1 -= 1
                    print("back")
                        
                if PS4.getButtonPress(L1) == 0:
                    Input2 = 0
                    Phase2 -= 1
                    print("左回り")
                        
                if PS4.getButtonPress(R1) == 0:
                    Input2 = 0
                    Phase2 -= 1
                    print("右回り")
                    
                if PS4.getButtonPress(LEFT) == 0:
                    print("左ライトon")
                    GPIO.output(11, False)

                if PS4.getButtonPress(CIRCLE) == 0:
                    GPIO.output(12, False)
                    print("右ライトon")
                    
            """pygame.display.update()
        if InputM == 0 or InputM == 9:#停止させる
            pwmOutput(VM, 0, -VM / 25, 0.02, pwmM)#pwm制御をする
            #VM/25(回転していたら100/25で4)ずつ速度を落とす
            VM, RecordM = 0, 0#現在の速度・回転方向を代入
        if InputM == 1:#正転させる
            if RecordM == 2:#反転中の場合一度停止させてから正転させるために
                pwmOutput(VM, 0, -VM / 25, 0.02, pwmM)#停止させる
                VM = 0#このあとの制御のため速度を更新
            GPIO.output(pinM1, GPIO.LOW)#正転させる
            pwmOutput(VM, 100, (100 - VM) / 25, 0.02, pwmM)
            #(100-VM)/25{(100-0)/25=4}ずつ速度を上げる
            VM, RecordM = 100, 1
        if InputM == 2:#反転させる
            if RecordM == 1:#正転中の場合
                pwmOutput(VM, 0, -VM / 25, 0.02, pwmM)
                VM = 0
            GPIO.output(pinM1, GPIO.HIGH)#反転
            pwmOutput(VM, 100, (100 - VM) / 25, 0.02, pwmM)
            VM, RecordM = 100, 2"""
                    
            pygame.display.update()
# 1
        if Input1 == 0 or Input1 == 9:#停止させる
            pwmOutput(V1, 0, -V1 / 1, 0.02, pwm1)#pwm制御をする
            #V1/25(回転していたら100/25で4)ずつ速度を落とす
            V1, Record1 = 0, 0#現在の速度・回転方向を代入
        if Input1 == 1:#正転させる
            if Record1 == 2:#反転中の場合一度停止させてから正転させるために
                pwmOutput(V1, 0, -V1 / 1, 0.02, pwm1)#停止させる
                V1 = 0#このあとの制御のため速度を更新
            GPIO.output(pin11, GPIO.LOW)#正転させる
            pwmOutput(V1, 40, (40 - V1) / 1, 0.02, pwm1)
            #(100-V1)/25{(100-0)/25=4}ずつ速度を上げる
            V1, Record1 = 40, 1
        if Input1 == 2:#反転させる
            if Record1 == 1:#正転中の場合
                pwmOutput(V1, 0, -V1 / 1, 0.02, pwm1)
                V1 = 0
            GPIO.output(pin11, GPIO.HIGH)#反転
            pwmOutput(V1, 40, (40 - V1) / 1, 0.02, pwm1)
            V1, Record1 = 40, 2
            
# 2
        if Input2 == 0 or Input2 == 9:#停止させる
            pwmOutput(V2, 0, -V2 / 1, 0.02, pwm2)#pwm制御をする
            #V2/25(回転していたら100/25で4)ずつ速度を落とす
            V2, Record2 = 0, 0#現在の速度・回転方向を代入
        if Input2 == 1:#正転させる
            if Record2 == 2:#反転中の場合一度停止させてから正転させるために
                pwmOutput(V2, 0, -V2 / 1, 0.02, pwm2)#停止させる
                V2 = 0#このあとの制御のため速度を更新
            GPIO.output(pin21, GPIO.LOW)#正転させる
            pwmOutput(V2, 100, (100 - V2) / 1, 0.02, pwm2)
            #(100-V2)/25{(100-0)/25=4}ずつ速度を上げる
            V2, Record2 = 100, 1
        if Input2 == 2:#反転させる
            if Record2 == 1:#正転中の場合
                pwmOutput(V2, 0, -V2 / 1, 0.02, pwm2)
                V2 = 0
            GPIO.output(pin21, GPIO.HIGH)#反転
            pwmOutput(V2, 100, (100 - V2) / 1, 0.02, pwm2)
            V2, Record2 = 100, 2
        
    if PS4.getButtonClick(PS) == 1:
        print("おかえり！\n無事でよかった！")
# プログラム強制終了時にモーターを止める                        
except:
    pass
finally:
    pwm1.stop()
    GPIO.output(pin11, GPIO.LOW)
    pwm2.stop()
    GPIO.output(pin21, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()