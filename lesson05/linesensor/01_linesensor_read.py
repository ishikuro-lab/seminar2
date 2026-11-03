# ラインセンサ(フォトリフレクタ 8 個)を 1 秒ごとに読んで表示する。Ctrl + C で止める。
# 白(光が反射する)で 1、黒(光を吸う)で 0。モーターは動かさない。
import lgpio
import time

# OUT1〜OUT8 をつないだ GPIO 番号(左から順に)
sensor_pins = (4, 27, 5, 6, 26, 25, 16, 20)

h = lgpio.gpiochip_open(0)  # GPIOを使う準備
claimed = []                # 準備できたピン(後片付けで手放す)
try:
    for pin in sensor_pins:
        # 入力にする。黒では電圧が決まらないので、プルダウン(何もなければ 0)で読む
        lgpio.gpio_claim_input(h, pin, lgpio.SET_PULL_DOWN)
        claimed.append(pin)
    print("Ctrl + C で止めます(白 = 1、黒 = 0)")
    seconds = 0
    while True:
        values = [lgpio.gpio_read(h, pin) for pin in sensor_pins]  # 8 本を読む
        print(f"{seconds:3d} 秒  {values}")
        seconds += 1
        time.sleep(1)
except KeyboardInterrupt:
    print("\n止めました")
finally:
    for pin in claimed:
        lgpio.gpio_free(h, pin)  # ピンを手放す
    lgpio.gpiochip_close(h)      # GPIOを閉じる
