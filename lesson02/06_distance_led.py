# 距離を10回測り、10 cm未満ならLED点灯。ECHOは分圧する。
import lgpio
import time
import signal

# SSH切断や終了要求も、中断として後片付けする。
signal.signal(signal.SIGHUP, signal.default_int_handler)
signal.signal(signal.SIGTERM, signal.default_int_handler)

led_pin = 12

trig_pin = 23
echo_pin = 24
timeout = 0.03  # 応答を待つ上限[秒]
h = lgpio.gpiochip_open(0)

try:
    lgpio.gpio_claim_output(h, trig_pin, 0)
    lgpio.gpio_claim_input(h, echo_pin)
    lgpio.gpio_claim_output(h, led_pin, 0)
    for i in range(10):
        distance = None  # 測れなかった場合の値

        # ECHOが前回のHighを保っていれば、今回は測らず次へ進む。
        if lgpio.gpio_read(h, echo_pin) == 0:
            # TRIGへ10 µsのHighを出し、超音波を送信する。
            lgpio.gpio_write(h, trig_pin, 0)
            time.sleep(0.000002)
            lgpio.gpio_write(h, trig_pin, 1)
            time.sleep(0.00001)
            lgpio.gpio_write(h, trig_pin, 0)

            # ECHOがHighになるまで待つ。上限時間を過ぎたら抜ける。
            deadline = time.monotonic() + timeout
            while lgpio.gpio_read(h, echo_pin) == 0:
                if time.monotonic() >= deadline:
                    break

            if time.monotonic() < deadline:
                start = time.monotonic()
                deadline = start + timeout
                # ECHOがLowになるまでの時間を測る。
                while lgpio.gpio_read(h, echo_pin) == 1:
                    if time.monotonic() >= deadline:
                        break
                end = time.monotonic()
                if end < deadline:
                    # 音速34300 cm/s × 往復時間 ÷ 2
                    distance = round((end - start) * 34300 / 2, 1)

        if distance is None:
            lgpio.gpio_write(h, led_pin, 0)
            print("測れません")
        elif distance < 10:
            lgpio.gpio_write(h, led_pin, 1)
            print(distance, "cm：点灯")
        else:
            lgpio.gpio_write(h, led_pin, 0)
            print(distance, "cm：消灯")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("中断しました")
finally:
    try:
        lgpio.gpio_write(h, led_pin, 0)
        lgpio.gpio_write(h, trig_pin, 0)
    finally:
        lgpio.gpiochip_close(h)
