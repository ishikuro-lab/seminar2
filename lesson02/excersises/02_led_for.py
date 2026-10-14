# 練習02【LED・for】LEDを3回点滅させてください。
# 穴は1か所。for は決まった回数の繰り返しです。
# range(3) なら3回。i には0、1、2の順に数字が入ります。
# ___ を埋めて保存します。字下げは半角スペース4個です。
# LED：GPIO12 → 抵抗330 Ω → LED → GND。電源を切って配線してください。
# led_on(12)：点ける。led_off(12)：消す。sleep(数字)：その秒数だけ待つ。
# 模擬実行：import の下に dry_run() を追加します。
# 実機で試すときはその行を外し、Thonnyの実行環境も再起動します。

from lesson_tools import led_on, led_off, sleep, dry_run

count = ___

for i in range(count):
    led_on(12)
    sleep(0.5)
    led_off(12)
    sleep(0.5)
