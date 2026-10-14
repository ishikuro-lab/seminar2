# 練習09【超音波・whileとif】5回測り、20 cmより近いときLEDを点けます。
# 穴は2か所。count は回数、near_cm はLEDが点く距離の境目です。
# 測れないときは消灯します。LEDには抵抗330 Ωを入れます。
# ___ を埋めて保存します。字下げは半角スペース4個です。
# read_distance()：距離[cm]を測る。print()：表示。sleep()：待つ。
# None は「測れない」という意味です。測れないときは数字と比較しません。
# VCC=5 V、GND=GND、TRIG=GPIO23、ECHO=抵抗で分圧してGPIO24。
# ECHOを直接GPIOへつながず、lesson02/README.md の配線を先生と確認します。
# センサの実行は班で1人ずつ交代してください。
# 模擬実行：import の下に dry_run() を追加すると模擬距離20 cmになります。
# 実機で試すときはその行を外し、Thonnyの実行環境も再起動します。

from lesson_tools import read_distance, led_on, led_off, sleep, dry_run

count = ___
near_cm = ___
done = 0

while done < count:
    distance = read_distance()
    if distance is None:
        led_off(12)
    elif distance < near_cm:
        led_on(12)
    else:
        led_off(12)
    sleep(0.5)
    done = done + 1

led_off(12)  # 終わったら消す
