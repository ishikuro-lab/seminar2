# センサ8 chを読む。電源は3.3 V。Ctrl+C で終了。
from lesson_gpio import read_sensor, sleep

sensor_pins = [4, 5, 6, 16, 20, 21, 23, 24]  # OUT1〜8

while True:
    values = []
    for pin in sensor_pins:
        value = read_sensor(pin)
        values.append(value)
    print(values)
    sleep(0.2)
