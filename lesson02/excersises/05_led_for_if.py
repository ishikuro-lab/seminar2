# 練習05【LED・forとif】6回光らせてください。
# 最初の3回は0.2秒、残りの3回は1秒点灯します。穴は1か所。
# i は0から始まるので、i < 3 は最初の3回です。
# ___ を埋めて保存します。字下げは半角スペース4個です。
# LED：GPIO12 → 抵抗330 Ω → LED → GND。電源を切って配線してください。
# led_on(12)：点ける。led_off(12)：消す。sleep(数字)：その秒数だけ待つ。
# 模擬実行：import の下に dry_run() を追加します。
# 実機で試すときはその行を外し、Thonnyの実行環境も再起動します。

from lesson_tools import led_on, led_off, sleep, dry_run

count = ___

for i in range(count):
    led_on(12)
    if i < 3:
        sleep(0.2)
    else:
        sleep(1)
    led_off(12)
    sleep(0.5)
