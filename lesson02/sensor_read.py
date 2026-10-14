# センサ OUT1 → GPIO4。電源は3.3 V。5 Vは禁止。
from lesson_gpio import read_sensor, sleep

while True:
    value = read_sensor(4)
    print(value)  # 0 = 白、1 = 黒・反射なし
    sleep(0.2)
