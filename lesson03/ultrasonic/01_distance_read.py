# 距離を10回測る。測定の仕組みは同じフォルダのhcsr04.pyへ。
import time
from hcsr04 import setup_gpio, read_distance, close_gpio

h = setup_gpio()  # GPIOの準備。戻り値をhに入れる
try:
    for i in range(10):
        distance = read_distance(h)  # hを渡して測る。戻り値はcmかNone
        if distance is None:
            print("測れません")
        else:
            print(distance, "cm")
        time.sleep(0.5)  # 測れないときも待つ
except KeyboardInterrupt:
    print("中断しました")
finally:
    close_gpio(h)  # 終了・エラー・Ctrl+Cの後片付け
