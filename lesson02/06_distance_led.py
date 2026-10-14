# 10 cm より近いと LED を点ける。Ctrl+C で終了。
from lesson_gpio import read_distance, led_on, led_off, sleep

while True:
    distance = read_distance()
    if distance is None:
        led_off(12)  # 測れないときは消す
    elif distance < 10:
        led_on(12)
    else:
        led_off(12)
    sleep(0.2)
