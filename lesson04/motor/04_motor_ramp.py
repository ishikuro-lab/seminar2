# ゆっくり加速して、ゆっくり減速する。必ず車輪を浮かせて実行する。
# 動き出す瞬間の速さ(最低速度)を観察できる。
import lgpio
import time
import signal

in1 = 17        # A側(右)のIN1。B側(左)を使うときは22
in2 = 18        # A側(右)のIN2。B側(左)を使うときは19
max_speed = 80  # いちばん速いときの速さ [%]
wait = 0.1      # 1段階あたりの秒数

# SSHが切れてもfinallyを通ってモーターを止める
signal.signal(signal.SIGHUP, signal.default_int_handler)
signal.signal(signal.SIGTERM, signal.default_int_handler)

h = lgpio.gpiochip_open(0)  # GPIOを使う準備

try:
    lgpio.gpio_claim_output(h, in1, 0)  # 最初は両方Low = 停止
    lgpio.gpio_claim_output(h, in2, 0)
    lgpio.gpio_write(h, in2, 0)         # 回したい向きの反対側はLowにする

    print("加速")
    for speed in range(0, max_speed + 1, 10):  # 0, 10, 20, ... max_speed
        print(speed, "%")
        lgpio.tx_pwm(h, in1, 1000, speed)
        time.sleep(wait)

    print("減速")
    for speed in range(max_speed, -1, -10):    # max_speed, ... 20, 10, 0
        print(speed, "%")
        lgpio.tx_pwm(h, in1, 1000, speed)
        time.sleep(wait)

    print("停止")
except KeyboardInterrupt:
    print("中断しました")
finally:
    lgpio.tx_pwm(h, in1, 1000, 0)  # PWMを止める
    lgpio.gpio_write(h, in1, 0)    # 途中で止めても必ず両方Lowに戻す
    lgpio.gpio_write(h, in2, 0)
    lgpio.gpiochip_close(h)        # ピンを解放
