# 練習02【LED・for】
# for文を使い、LEDを3回点滅させてください。
# 1回の点滅は、0.5秒点灯・0.5秒消灯とします。
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
