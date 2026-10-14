# LEDを10回点滅。配線は01_led_on.pyと同じ。
import lgpio
import time
import signal

# SSH切断や終了要求も、中断として後片付けする。
signal.signal(signal.SIGHUP, signal.default_int_handler)
signal.signal(signal.SIGTERM, signal.default_int_handler)

led_pin = 12
h = lgpio.gpiochip_open(0)  # GPIOを使う準備

try:
    lgpio.gpio_claim_output(h, led_pin, 0)  # 出力に設定。最初は消灯
    for i in range(10):
        lgpio.gpio_write(h, led_pin, 1)
        time.sleep(0.5)
        lgpio.gpio_write(h, led_pin, 0)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("中断しました")
finally:
    try:
        lgpio.gpio_write(h, led_pin, 0)  # 消灯
    finally:
        lgpio.gpiochip_close(h)         # ピンを解放
