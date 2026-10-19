# PWMでモーターの速さを変える。必ず車輪を浮かせて実行する。
# 第2回のLEDの明るさと同じ仕組み。デューティ比が大きいほど速い。
import lgpio
import time
import signal

in1 = 17     # A側(右)のIN1。B側(左)を使うときは22
in2 = 18     # A側(右)のIN2。B側(左)を使うときは19
speed = 50   # 速さ 0〜100 [%]。40以下だと回らないことがある
seconds = 2  # 回す秒数。10秒より長くしない

# SSHが切れてもfinallyを通ってモーターを止める
signal.signal(signal.SIGHUP, signal.default_int_handler)
signal.signal(signal.SIGTERM, signal.default_int_handler)

h = lgpio.gpiochip_open(0)  # GPIOを使う準備

try:
    lgpio.gpio_claim_output(h, in1, 0)  # 最初は両方Low = 停止
    lgpio.gpio_claim_output(h, in2, 0)
    print("速さ", speed, "% で", seconds, "秒")
    lgpio.gpio_write(h, in2, 0)                # 回したい向きの反対側はLowにする
    lgpio.tx_pwm(h, in1, 1000, speed)          # 1000 Hz、デューティ比 speed %
    time.sleep(seconds)
    print("停止")
except KeyboardInterrupt:
    print("中断しました")
finally:
    lgpio.tx_pwm(h, in1, 1000, 0)  # PWMを止める
    lgpio.gpio_write(h, in1, 0)    # 途中で止めても必ず両方Lowに戻す
    lgpio.gpio_write(h, in2, 0)
    lgpio.gpiochip_close(h)        # ピンを解放
