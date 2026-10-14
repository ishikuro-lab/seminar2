# LED練習5：自分で決めた長さで3回光らせ、友達に見せてください。
# 穴埋めは3か所。それぞれ0.1〜3秒で選びます。正解は1つではありません。
# 【使い方】___ を数字に置き換え、保存してから実行してください。
# ___ を残したままでは動きません。
# LED：GPIO12 → 抵抗330 Ω → LED → GND。電源を切って配線します。
# led_on(12)：点ける。led_off(12)：消す。sleep(数字)：その秒数だけ待つ。
# 最初は import の下に dry_run() と書くと、GPIOに触れず確認できます。
# 実機で動かすときは dry_run() の行を外します。Thonnyでは実行環境も再起動します。

from lesson_tools import led_on, led_off, sleep, dry_run

first_seconds = ___
second_seconds = ___
third_seconds = ___

led_on(12)
sleep(first_seconds)
led_off(12)
sleep(1)
led_on(12)
sleep(second_seconds)
led_off(12)
sleep(1)
led_on(12)
sleep(third_seconds)
led_off(12)
