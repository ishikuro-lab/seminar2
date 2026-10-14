# LED練習1：5秒間点けてから消してください。
# 穴埋めは1か所。ヒント：待つ秒数は5です。
# 【使い方】___ を数字に置き換え、保存してから実行してください。
# ___ を残したままでは動きません。
# LED：GPIO12 → 抵抗330 Ω → LED → GND。電源を切って配線します。
# led_on(12)：点ける。led_off(12)：消す。sleep(数字)：その秒数だけ待つ。
# 最初は import の下に dry_run() と書くと、GPIOに触れず確認できます。
# 実機で動かすときは dry_run() の行を外します。Thonnyでは実行環境も再起動します。

from lesson_tools import led_on, led_off, sleep, dry_run

seconds = ___

led_on(12)
sleep(seconds)
led_off(12)
