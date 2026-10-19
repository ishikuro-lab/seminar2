# HC-SR04で距離を10回測る。TRIGはGPIO23、ECHOは抵抗で分圧してGPIO24へ。
import lgpio
import time

trig_pin = 23
echo_pin = 24
h = lgpio.gpiochip_open(0)  # GPIOを使う準備

try:
    lgpio.gpio_claim_output(h, trig_pin, 0)  # TRIGは出力。超音波を出す合図を送る
    lgpio.gpio_claim_input(h, echo_pin)      # ECHOは入力。反射が戻るまでHighになる
    for i in range(10):
        # TRIGを10マイクロ秒だけHighにして、超音波を出す
        lgpio.gpio_write(h, trig_pin, 1)
        time.sleep(0.00001)
        lgpio.gpio_write(h, trig_pin, 0)

        while lgpio.gpio_read(h, echo_pin) == 0:
            pass                   # Highになるまで待つ
        start = time.monotonic()   # 超音波が出た時刻

        while lgpio.gpio_read(h, echo_pin) == 1:
            pass                   # Lowに戻るまで待つ
        end = time.monotonic()     # 反射が戻ってきた時刻

        # 音は1秒に34300 cm進む。往復なので2で割る
        distance = round((end - start) * 34300 / 2, 1)
        print(distance, "cm")
        time.sleep(0.5)  # 次の測定まで少し待つ
except KeyboardInterrupt:
    print("中断しました")
finally:
    lgpio.gpio_write(h, trig_pin, 0)  # TRIGをLowに戻す
    lgpio.gpiochip_close(h)           # ピンを解放
