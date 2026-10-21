# 正転→停止→逆転。必ず車輪を浮かせて実行する。
import time
from motor_gpio import setup_gpio, set_speed, stop_motor, close_gpio

in1 = 17  # A側（右）。B側（左）を使うときは22
in2 = 18  # A側（右）。B側（左）を使うときは19
seconds = 2  # 片方向の秒数。往復の合計を10秒以内にする
stop_seconds = 1  # 逆転前は必ず一度止める
pins = [in1, in2]
h = setup_gpio(pins)
try:
    set_speed(h, in1, in2, 100)  # 正転
    time.sleep(seconds)
    stop_motor(h, pins)
    time.sleep(stop_seconds)
    set_speed(h, in2, in1, 100)  # 2本の順番を入れ替えると逆転
    time.sleep(seconds)
except KeyboardInterrupt:
    print("中断しました")
finally:
    close_gpio(h, pins)  # PWM停止・全ピンLow・GPIO解放
