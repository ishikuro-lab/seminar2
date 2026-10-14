# LEDを3秒点灯。GPIO12 → 抵抗330 Ω → LED → GND。
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
    lgpio.gpio_write(h, led_pin, 1)  # 1はHigh：点灯
    time.sleep(3)                   # 3秒待つ
    lgpio.gpio_write(h, led_pin, 0)  # 0はLow：消灯
except KeyboardInterrupt:
    print("中断しました")
finally:
    try:
        lgpio.gpio_write(h, led_pin, 0)  # 消灯
    finally:
        lgpio.gpiochip_close(h)         # ピンを解放
