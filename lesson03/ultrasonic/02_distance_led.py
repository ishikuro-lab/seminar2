# 距離を10回測り、10cm未満ならLEDを点ける。
import lgpio
import time
from hcsr04 import setup_gpio, read_distance, close_gpio

led_pin = 12  # BCM12（物理32）。LEDに直列330Ω
h = setup_gpio(led_pin)  # センサとLEDを準備する
try:
    for i in range(10):
        distance = read_distance(h)  # 定義はhcsr04.py。戻り値はcmかNone
        if distance is None:
            lgpio.gpio_write(h, led_pin, 0)
            print("測れません")
        elif distance < 10:
            lgpio.gpio_write(h, led_pin, 1)
            print(distance, "cm：点灯")
        else:
            lgpio.gpio_write(h, led_pin, 0)
            print(distance, "cm：消灯")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("中断しました")
finally:
    close_gpio(h, led_pin)  # LEDを消し、センサとGPIOを片付ける
