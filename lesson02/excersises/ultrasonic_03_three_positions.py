# 超音波練習3：3回距離を測り、毎回画面に表示してください。
# 穴埋めは1か所。待ち時間は3秒にして、待つ間に物の位置を変えます。
# 物を10 / 20 / 30 cmに置き、表示と定規の値を比べてください。
# 【使い方】___ を埋めて保存してから実行してください。
# read_distance()：距離を cm で測る。print()：画面に表示。sleep()：待つ。
# 配線：VCC=5 V、GND=GND、TRIG=GPIO23、ECHO=分圧後のGPIO24。
# ECHOは直接GPIOにつながず、lesson02/README.md の配線を先生と確認します。
# センサは班で共有し、実行は1人ずつ交代してください。
# None は「測れない」の意味です。None と数字は比較しません。
# 最初は import の下に dry_run() と書くと、模擬距離20 cmで確認できます。
# 実機で動かすときは dry_run() の行を外します。Thonnyでは実行環境も再起動します。

from lesson_tools import read_distance, sleep, dry_run

wait_seconds = ___

distance = read_distance()
print(distance, "cm")
sleep(wait_seconds)
distance = read_distance()
print(distance, "cm")
sleep(wait_seconds)
distance = read_distance()
print(distance, "cm")
