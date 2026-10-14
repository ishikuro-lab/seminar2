# LED を徐々に明るく・暗くする。Ctrl+C で終了。
from lesson_gpio import brightness, sleep

while True:
    for duty in range(0, 101, 5):    # 明るくする
        brightness(12, duty)
        sleep(0.05)
    for duty in range(100, -1, -5):  # 暗くする
        brightness(12, duty)
        sleep(0.05)
