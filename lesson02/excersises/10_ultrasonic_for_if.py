# 練習10【超音波・forとif】距離を5回測り、3種類の表示に分けます。
# 10 cm未満は「近い」、10 cm以上30 cm未満は「中くらい」、30 cm以上は「遠い」。
# 穴は3か所。count は回数、near_cm と far_cm は距離の境目です。
# ___ を埋めて保存します。字下げは半角スペース4個です。
# read_distance()：距離[cm]を測る。print()：表示。sleep()：待つ。
# None は「測れない」という意味です。測れないときは数字と比較しません。
# VCC=5 V、GND=GND、TRIG=GPIO23、ECHO=抵抗で分圧してGPIO24。
# ECHOを直接GPIOへつながず、lesson02/README.md の配線を先生と確認します。
# センサの実行は班で1人ずつ交代してください。
# 模擬実行：import の下に dry_run() を追加すると模擬距離20 cmになります。
# 実機で試すときはその行を外し、Thonnyの実行環境も再起動します。

from lesson_tools import read_distance, sleep, dry_run

count = ___
near_cm = ___
far_cm = ___

for i in range(count):
    distance = read_distance()
    if distance is None:
        print("測れません")
    elif distance < near_cm:
        print("近い")
    elif distance < far_cm:
        print("中くらい")
    else:
        print("遠い")
    sleep(0.5)
