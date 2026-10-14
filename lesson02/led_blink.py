# LED を点滅する。Ctrl+C で終了。
from lesson_gpio import led_on, led_off, sleep

while True:
    led_on(12)
    sleep(0.5)
    led_off(12)
    sleep(0.5)
