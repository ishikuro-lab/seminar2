#!/usr/bin/env python3
"""LED をゆっくり明るく → 暗く、を繰り返す。Ctrl+C で止める。

配線: led_on.py と同じ
実行: python3 led_fade.py                    (0〜100 % を 5 % 刻み、50 ms ごと)
      python3 led_fade.py --step 1 --wait 0.02   (なめらかに)
"""

import argparse
import time

import lgpio

LED_PIN = 12
PWM_HZ = 1000


def main():
    parser = argparse.ArgumentParser(description="LED をゆっくり明るく→暗く")
    parser.add_argument("--pin", type=int, default=LED_PIN, help=f"GPIO 番号 (既定 {LED_PIN})")
    parser.add_argument("--step", type=float, default=5, help="1 回に変える量 [%%] (既定 5)")
    parser.add_argument("--wait", type=float, default=0.05, help="1 段階ごとの待ち時間 [秒] (既定 0.05)")
    args = parser.parse_args()

    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, args.pin, 0)
    print("止めるときは Ctrl+C")
    try:
        while True:
            # 明るくする: 0, 5, 10, ... , 100
            duty = 0.0
            while duty <= 100:
                lgpio.tx_pwm(h, args.pin, PWM_HZ, duty)
                time.sleep(args.wait)
                duty += args.step
            # 暗くする: 100, 95, ... , 0
            duty = 100.0
            while duty >= 0:
                lgpio.tx_pwm(h, args.pin, PWM_HZ, duty)
                time.sleep(args.wait)
                duty -= args.step
    except KeyboardInterrupt:
        print("\n止めました")
    finally:
        lgpio.tx_pwm(h, args.pin, PWM_HZ, 0)
        lgpio.gpio_write(h, args.pin, 0)
        lgpio.gpio_free(h, args.pin)
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()
