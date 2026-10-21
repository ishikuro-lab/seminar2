# PWMで速さを変える。必ず車輪を浮かせて実行する。
import time
from motor_gpio import setup_gpio, set_speed, close_gpio

in1 = 17  # A側（右）。B側（左）を使うときは22
in2 = 18  # A側（右）。B側（左）を使うときは19
speed = 50  # 0〜100%。40以下だと回らないことがある
seconds = 2  # 回す秒数。10秒より長くしない
pins = [in1, in2]
h = setup_gpio(pins)
try:
    set_speed(h, in1, in2, speed)  # 引数speedで速さを指定する
    time.sleep(seconds)
except KeyboardInterrupt:
    print("中断しました")
finally:
    close_gpio(h, pins)  # PWM停止・全ピンLow・GPIO解放
