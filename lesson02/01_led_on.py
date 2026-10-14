# LED を3秒点ける。GPIO12 → 抵抗330Ω → LED → GND。
from lesson_gpio import led_on, led_off, sleep

led_on(12)   # 点ける
sleep(3)     # 3秒待つ
led_off(12)  # 消す
