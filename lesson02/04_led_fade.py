# LEDを徐々に明るく・暗くする。3往復して終了。
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
    for cycle in range(3):
        for duty in range(0, 101, 5):
            lgpio.tx_pwm(h, led_pin, 1000, 0)
            if duty == 0:
                lgpio.gpio_write(h, led_pin, 0)
            elif duty == 100:
                lgpio.gpio_write(h, led_pin, 1)
            else:
                lgpio.tx_pwm(h, led_pin, 1000, duty)
            time.sleep(0.05)
        for duty in range(100, -1, -5):
            lgpio.tx_pwm(h, led_pin, 1000, 0)
            if duty == 0:
                lgpio.gpio_write(h, led_pin, 0)
            elif duty == 100:
                lgpio.gpio_write(h, led_pin, 1)
            else:
                lgpio.tx_pwm(h, led_pin, 1000, duty)
            time.sleep(0.05)
except KeyboardInterrupt:
    print("中断しました")
finally:
    try:
        lgpio.tx_pwm(h, led_pin, 1000, 0)  # PWMを停止
        lgpio.gpio_write(h, led_pin, 0)   # 消灯
    finally:
        lgpio.gpiochip_close(h)           # ピンを解放
