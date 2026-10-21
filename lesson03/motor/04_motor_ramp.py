# 少しずつ加速・減速。必ず車輪を浮かせて実行する。
import time
from motor_gpio import setup_gpio, set_speed, close_gpio

in1 = 17  # A側（右）。B側（左）を使うときは22
in2 = 18  # A側（右）。B側（左）を使うときは19
max_speed = 80  # 最大の速さ：0〜100%、10刻み
wait = 0.1  # 1段階の秒数。全体を10秒以内にする
if max_speed not in range(0, 101, 10):
    raise ValueError("max_speedは0〜100の10刻みにしてください")
pins = [in1, in2]
h = setup_gpio(pins)
try:
    for speed in range(0, max_speed + 1, 10):  # 加速：0, 10, …, 80
        print(speed, "%")
        set_speed(h, in1, in2, speed)
        time.sleep(wait)
    for speed in range(max_speed, -1, -10):  # 減速：80, 70, …, 0
        print(speed, "%")
        set_speed(h, in1, in2, speed)
        time.sleep(wait)
except KeyboardInterrupt:
    print("中断しました")
finally:
    close_gpio(h, pins)  # PWM停止・全ピンLow・GPIO解放
