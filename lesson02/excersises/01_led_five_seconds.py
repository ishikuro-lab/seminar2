# 練習01【LED・順番に実行】5秒点けてから消してください。
# 穴は1か所。seconds は待つ秒数です。
# ___ を埋めて保存します。字下げは半角スペース4個です。
# LED：GPIO12 → 抵抗330 Ω → LED → GND。電源を切って配線してください。
# led_on(12)：点ける。led_off(12)：消す。sleep(数字)：その秒数だけ待つ。
# 模擬実行：import の下に dry_run() を追加します。
# 実機で試すときはその行を外し、Thonnyの実行環境も再起動します。

from lesson_tools import led_on, led_off, sleep, dry_run

seconds = ___

led_on(12)
sleep(seconds)
led_off(12)
