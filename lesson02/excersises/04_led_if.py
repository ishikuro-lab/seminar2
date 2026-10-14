# 練習04【LED・if】mode が1なら1秒点灯、0なら消灯にしてください。
# 穴は1か所。最初は1、その後0に書き換えて動きを比べます。
# if は「もし」、else は「それ以外」。== は同じ値かの比較です。
# ___ を埋めて保存します。字下げは半角スペース4個です。
# LED：GPIO12 → 抵抗330 Ω → LED → GND。電源を切って配線してください。
# led_on(12)：点ける。led_off(12)：消す。sleep(数字)：その秒数だけ待つ。
# 模擬実行：import の下に dry_run() を追加します。
# 実機で試すときはその行を外し、Thonnyの実行環境も再起動します。

from lesson_tools import led_on, led_off, sleep, dry_run

mode = ___

if mode == 1:
    led_on(12)
    sleep(1)
else:
    led_off(12)

led_off(12)  # 最後は必ず消す
