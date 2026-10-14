# 練習08【超音波・if】20 cmより近ければ「近い」、それ以外は「遠い」と表示します。
# 穴は1か所。if は「もし」、elif は「そうでなく、もし」、else は「それ以外」。
# distance is None は測れなかった場合の確認です。その行はそのまま使います。
# ___ を埋めて保存します。字下げは半角スペース4個です。
# read_distance()：距離[cm]を測る。print()：表示。sleep()：待つ。
# None は「測れない」という意味です。測れないときは数字と比較しません。
# VCC=5 V、GND=GND、TRIG=GPIO23、ECHO=抵抗で分圧してGPIO24。
# ECHOを直接GPIOへつながず、lesson02/README.md の配線を先生と確認します。
# センサの実行は班で1人ずつ交代してください。
# 模擬実行：import の下に dry_run() を追加すると模擬距離20 cmになります。
# 実機で試すときはその行を外し、Thonnyの実行環境も再起動します。

from lesson_tools import read_distance, dry_run

near_cm = ___

distance = read_distance()
if distance is None:
    print("測れません")
elif distance < near_cm:
    print("近い")
else:
    print("遠い")
