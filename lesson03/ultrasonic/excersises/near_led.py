# 練習：近づいたらLEDを点ける
# 02_distance_led.pyを参考に、この下に自分でコードを書きましょう。
# 1. hcsr04.pyの関数を読み込み、GPIOの準備・測定・終了に使います。
# 2. while文で5回測り、20 cm未満なら点灯、20 cm以上なら消灯します。
# 3. 戻り値がNoneなら「測れません」と表示して消灯します。
#    失敗も1回に数え、毎回0.5秒待ちます。
# 4. finallyでclose_gpio(h, led_pin)を呼び、Ctrl+Cでも片付けます。
#
# 配線：TRIG BCM23、ECHOは1kΩ/1.5kΩで分圧してBCM24へ。
# LED BCM12に直列330Ω。VCC 5V・GND共通。lesson03/README.md参照。
# 実行は班で1人ずつ。自分のstudentsフォルダで編集します。
