#!/usr/bin/env python3
"""LED を点滅させる。Ctrl+C で止める。

配線: led_on.py と同じ
実行: python3 led_blink.py                  (0.5 秒おき)
      python3 led_blink.py --interval 0.1   (速く)
"""

import argparse
import time

import lgpio

LED_PIN = 12


def main():
    parser = argparse.ArgumentParser(description="LED を点滅させる")
    parser.add_argument("--pin", type=int, default=LED_PIN, help=f"GPIO 番号 (既定 {LED_PIN})")
    parser.add_argument("--interval", type=float, default=0.5, help="点灯・消灯それぞれの秒数 (既定 0.5)")
    args = parser.parse_args()

    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, args.pin, 0)
    print("点滅中。止めるときは Ctrl+C")
    count = 0
    try:
        while True:                             # 無限ループ。Ctrl+C で抜ける
            lgpio.gpio_write(h, args.pin, 1)    # 点灯
            time.sleep(args.interval)
            lgpio.gpio_write(h, args.pin, 0)    # 消灯
            time.sleep(args.interval)
            count += 1
    except KeyboardInterrupt:                   # Ctrl+C を押すとここに来る
        print(f"\n止めました ({count} 回点滅)")
    finally:
        lgpio.gpio_write(h, args.pin, 0)
        lgpio.gpio_free(h, args.pin)
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()
