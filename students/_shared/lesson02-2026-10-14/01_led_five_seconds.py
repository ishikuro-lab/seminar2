# 練習01【LED・順番に実行】
# GPIO12のLEDを5秒間点けてから消すプログラムを書いてください。
#
# 【作業の指示】
# このコメントの下に、自分でコードを書いてください。
# 字下げには半角スペース4個を使います。
# lgpio.gpio_writeで点灯・消灯し、time.sleepで待ち時間を指定します。
# LEDはGPIO12に接続し、抵抗330 Ωを必ず入れてください。
# プログラムの最後にはLEDを消してください。
# LEDは終了時に消灯し、最後にlgpio.gpiochip_closeでGPIOを解放してください。

import lgpio
import time
import signal

signal.signal(signal.SIGHUP, signal.default_int_handler)
signal.signal(signal.SIGTERM, signal.default_int_handler)

led_pin = 12
h = lgpio.gpiochip_open(0)

try:
    lgpio.gpio.claim_output(h, led_pin, 0)
    lgpio.gpio_write(h, led_pin, 1)
    time.sleep(5)
    lgpio.gpio_write(h, led_pin, 0)
except KeyboardInterrupt:
    print("KeybordInterrupt")
finally:
    try:
        lgpio.gpio_write(h, led_pin, 0)
    finally:
        lgpio.gpiochip_close(h)
        
