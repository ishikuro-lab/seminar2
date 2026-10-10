#!/usr/bin/env python3
"""PWM で LED の明るさを決める。

PWM = High と Low を高速に切り替え、High の割合 (デューティ比) で明るさを変える。
配線: led_on.py と同じ
実行: python3 led_pwm.py --duty 25     (25 % の明るさで 5 秒)
      python3 led_pwm.py --duty 100    (全点灯)
"""

import argparse
import time

import lgpio

LED_PIN = 12
PWM_HZ = 1000  # 1 秒に 1000 回切り替える。目には点滅が見えない


def main():
    parser = argparse.ArgumentParser(description="PWM で LED の明るさを決める")
    parser.add_argument("--pin", type=int, default=LED_PIN, help=f"GPIO 番号 (既定 {LED_PIN})")
    parser.add_argument("--duty", type=float, default=50, help="デューティ比 0〜100 [%%] (既定 50)")
    parser.add_argument("--seconds", type=float, default=5.0, help="点けておく秒数 (既定 5)")
    args = parser.parse_args()
    if not 0 <= args.duty <= 100:
        parser.error("--duty は 0 から 100 の間で指定してください")

    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, args.pin, 0)
    try:
        print(f"GPIO{args.pin} に {PWM_HZ} Hz、デューティ比 {args.duty:g} % の PWM を出します")
        lgpio.tx_pwm(h, args.pin, PWM_HZ, args.duty)   # ここから PWM が出続ける
        time.sleep(args.seconds)
    finally:
        lgpio.tx_pwm(h, args.pin, PWM_HZ, 0)            # PWM を止める (デューティ 0 %)
        lgpio.gpio_write(h, args.pin, 0)
        lgpio.gpio_free(h, args.pin)
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()
