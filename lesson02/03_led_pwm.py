# LED の明るさを変える。
from lesson_gpio import brightness, led_off, sleep

brightness(12, 50)  # 明るさの指定は0〜100 [%]
sleep(5)
led_off(12)
