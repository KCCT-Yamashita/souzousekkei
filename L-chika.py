from gpiozero import LED
from time import sleep

#LEDの変数
led = LED(3) #GPIOの番号

#ずっとチカチカさせる
while True:
    led on()
    sleep(0.4) #オンにする速度
    led off()
    sleep(0.4) #オフにする速度
