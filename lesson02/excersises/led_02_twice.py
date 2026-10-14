# LED練習2：1秒点灯・1秒消灯・1秒点灯・消灯にしてください。
# 穴埋めは2か所。最後は必ず消します。
# 【使い方】___ を数字に置き換え、保存してから実行してください。
# ___ を残したままでは動きません。
# LED：GPIO12 → 抵抗330 Ω → LED → GND。電源を切って配線します。
# led_on(12)：点ける。led_off(12)：消す。sleep(数字)：その秒数だけ待つ。
# 最初は import の下に dry_run() と書くと、GPIOに触れず確認できます。
# 実機で動かすときは dry_run() の行を外します。Thonnyでは実行環境も再起動します。

from lesson_tools import led_on, led_off, sleep, dry_run

on_seconds = ___
off_seconds = ___

led_on(12)
sleep(on_seconds)
led_off(12)
sleep(off_seconds)
led_on(12)
sleep(on_seconds)
led_off(12)
