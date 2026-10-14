# HC-SR04 で距離を測る。配線は README を確認。
from lesson_gpio import read_distance, sleep

while True:
    distance = read_distance()
    if distance is None:
        print("測れません")
    else:
        print(distance, "cm")
    sleep(0.2)
