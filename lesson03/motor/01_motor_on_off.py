# A側のモーターを2秒だけ正転させて止める。必ず車輪を浮かせて実行する。
import lgpio
import time
import signal

in1 = 17     # A側(右)のIN1。B側(左)を使うときは22
in2 = 18     # A側(右)のIN2。B側(左)を使うときは19
seconds = 2  # 回す秒数。10秒より長くしない

# SSHが切れてもfinallyを通ってモーターを止める
signal.signal(signal.SIGHUP, signal.default_int_handler)
signal.signal(signal.SIGTERM, signal.default_int_handler)

h = lgpio.gpiochip_open(0)  # GPIOを使う準備

try:
    lgpio.gpio_claim_output(h, in1, 0)  # 最初は両方Low = 停止
    lgpio.gpio_claim_output(h, in2, 0)
    print("正転", seconds, "秒")
    lgpio.gpio_write(h, in1, 1)         # IN1をHigh、IN2をLowにすると正転
    lgpio.gpio_write(h, in2, 0)
    time.sleep(seconds)
    print("停止")
except KeyboardInterrupt:
    print("中断しました")
finally:
    lgpio.gpio_write(h, in1, 0)  # 途中で止めても必ず両方Lowに戻す
    lgpio.gpio_write(h, in2, 0)
    lgpio.gpiochip_close(h)      # ピンを解放
