# 練習05【LED・forとif】
# for文を使ってLEDを6回光らせてください。
# if文を使い、最初の3回は0.2秒、残りの3回は1秒点灯させます。
# 点灯と点灯の間は、0.5秒消灯してください。
#
# 【作業の指示】
# このコメントの下に、自分でコードを書いてください。
# 字下げには半角スペース4個を使います。
# lgpio.gpio_writeで点灯・消灯し、time.sleepで待ち時間を指定します。
# LEDはGPIO12に接続し、抵抗330 Ωを必ず入れてください。
# プログラムの最後にはLEDを消してください。
# LEDは終了時に消灯し、最後にlgpio.gpiochip_closeでGPIOを解放してください。
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
    for i in range(3):
        lgpio.gpio_write(h, led_pin, 1)
        time.sleep(0.2)
        lgpio.gpio_write(h, led_pin, 0)
        time.sleep(0.5)
    for i in range(3):
        lgpio.gpio_write(h, led_pin, 1)
        time.sleep(1)
        lgpio.gpio_write(h, led_pin, 0)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("中断しました")
finally:
    try:
        lgpio.gpio_write(h, led_pin, 0)  # 消灯
    finally:
        lgpio.gpiochip_close(h)         # ピンを解放