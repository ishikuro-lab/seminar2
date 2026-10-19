# HC-SR04の距離とECHO（応答信号）の異常を10回確認する。
# 実行: python3 ultrasonic_check.py
# 注意: ECHOの5Vを直接つながず、抵抗で3.3V以下に下げてGPIO24へ接続する。
import lgpio
import time
import signal

# SSH切断・終了要求でもfinallyで後片付けする。
signal.signal(signal.SIGHUP, signal.default_int_handler)
signal.signal(signal.SIGTERM, signal.default_int_handler)

TRIG = 23
ECHO = 24
TIMEOUT = 0.03

h = lgpio.gpiochip_open(0)
trig_claimed = False
echo_claimed = False

try:
    lgpio.gpio_claim_output(h, TRIG, 0)
    trig_claimed = True
    lgpio.gpio_claim_input(h, ECHO)
    echo_claimed = True

    for i in range(10):
        print(f"\n測定 {i+1}")

        initial = lgpio.gpio_read(h, ECHO)
        print("送信前 ECHO:", initial)

        if initial == 1:
            print("異常: ECHOが最初からHIGH")
            time.sleep(0.5)
            continue

        lgpio.gpio_write(h, TRIG, 0)
        time.sleep(0.00001)

        lgpio.gpio_write(h, TRIG, 1)
        time.sleep(0.00001)
        lgpio.gpio_write(h, TRIG, 0)

        deadline = time.monotonic() + TIMEOUT

        while lgpio.gpio_read(h, ECHO) == 0:
            if time.monotonic() >= deadline:
                print("異常: ECHOがHIGHにならない")
                break
        else:
            start = time.monotonic()
            deadline = start + TIMEOUT

            while lgpio.gpio_read(h, ECHO) == 1:
                if time.monotonic() >= deadline:
                    print("異常: ECHOがLOWに戻らない")
                    break
            else:
                end = time.monotonic()
                distance = (end - start) * 34300 / 2
                print(f"距離: {distance:.1f} cm")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("中断しました")
finally:
    # ECHOは入力なので書き込まず、確保したピンを解放する。
    try:
        if trig_claimed:
            lgpio.gpio_write(h, TRIG, 0)
    finally:
        try:
            if trig_claimed:
                lgpio.gpio_free(h, TRIG)
        finally:
            try:
                if echo_claimed:
                    lgpio.gpio_free(h, ECHO)
            finally:
                lgpio.gpiochip_close(h)
