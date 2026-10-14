# 練習03【LED・while】LEDを5回点滅させてください。
# 穴は1か所。while は条件が成り立つ間の繰り返しです。
# done = done + 1 は回数を1増やす命令です。この行は消さないでください。
# ___ を埋めて保存します。字下げは半角スペース4個です。
# LED：GPIO12 → 抵抗330 Ω → LED → GND。電源を切って配線してください。
# led_on(12)：点ける。led_off(12)：消す。sleep(数字)：その秒数だけ待つ。
# 模擬実行：import の下に dry_run() を追加します。
# 実機で試すときはその行を外し、Thonnyの実行環境も再起動します。

from lesson_tools import led_on, led_off, sleep, dry_run

count = ___
done = 0

while done < count:
    led_on(12)
    sleep(0.5)
    led_off(12)
    sleep(0.5)
    done = done + 1
