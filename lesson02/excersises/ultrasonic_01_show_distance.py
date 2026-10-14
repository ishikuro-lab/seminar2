# 超音波練習1：距離と単位を1回表示してください。
# 穴埋めは1か所。文字は引用符で囲みます。ヒント："cm"。
# 【使い方】___ を埋めて保存してから実行してください。
# read_distance()：距離を cm で測る。print()：画面に表示。sleep()：待つ。
# 配線：VCC=5 V、GND=GND、TRIG=GPIO23、ECHO=分圧後のGPIO24。
# ECHOは直接GPIOにつながず、lesson02/README.md の配線を先生と確認します。
# センサは班で共有し、実行は1人ずつ交代してください。
# None は「測れない」の意味です。None と数字は比較しません。
# 最初は import の下に dry_run() と書くと、模擬距離20 cmで確認できます。
# 実機で動かすときは dry_run() の行を外します。Thonnyでは実行環境も再起動します。

from lesson_tools import read_distance, dry_run

unit = ___

distance = read_distance()
print(distance, unit)
