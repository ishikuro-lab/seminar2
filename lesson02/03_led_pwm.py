# PWMでLEDの明るさを指定。配線は01_led_on.pyと同じ。
import lgpio
import time
import signal

# SSH切断や終了要求も、中断として後片付けする。
signal.signal(signal.SIGHUP, signal.default_int_handler)
signal.signal(signal.SIGTERM, signal.default_int_handler)

duty = 50  # 点灯する時間の割合[%]。0〜100で変更する
if not 0 <= duty <= 100:
    raise ValueError("dutyは0〜100で指定してください")

led_pin = 12
h = lgpio.gpiochip_open(0)  # GPIOを使う準備

try:
    lgpio.gpio_claim_output(h, led_pin, 0)  # 出力に設定。最初は消灯
    if duty == 0:
        lgpio.gpio_write(h, led_pin, 0)
    elif duty == 100:
        lgpio.gpio_write(h, led_pin, 1)
    else:
        lgpio.tx_pwm(h, led_pin, 1000, duty)  # 1000 Hz、指定した割合のPWM
    time.sleep(5)
except KeyboardInterrupt:
    print("中断しました")
finally:
    try:
        lgpio.tx_pwm(h, led_pin, 1000, 0)  # PWMを停止
        lgpio.gpio_write(h, led_pin, 0)   # 消灯
    finally:
        lgpio.gpiochip_close(h)           # ピンを解放
