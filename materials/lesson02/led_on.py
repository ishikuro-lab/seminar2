#!/usr/bin/env python3
"""LED を 3 秒点けて消す。

配線: GPIO12 (物理 32) → 抵抗 330Ω → LED (長い足) → LED (短い足) → GND (物理 34)
実行: python3 led_on.py            (GPIO12)
      python3 led_on.py --pin 21   (別のピンを使うとき)
"""

import argparse
import time

import lgpio

LED_PIN = 12  # 最初はこの番号を使う。配線を変えたら --pin で指定できる


def main():
    parser = argparse.ArgumentParser(description="LED を 3 秒点けて消す")
    parser.add_argument("--pin", type=int, default=LED_PIN, help=f"LED をつないだ GPIO 番号 (既定 {LED_PIN})")
    parser.add_argument("--seconds", type=float, default=3.0, help="点けておく秒数 (既定 3)")
    args = parser.parse_args()

    h = lgpio.gpiochip_open(0)                 # GPIO を使う準備
    lgpio.gpio_claim_output(h, args.pin, 0)    # 出力にする。最初は Low (消灯)
    try:
        print(f"GPIO{args.pin} を High にします (点灯)")
        lgpio.gpio_write(h, args.pin, 1)       # 1 = High = 3.3 V
        time.sleep(args.seconds)               # 待つ (この間 LED は点いたまま)
        print("Low にします (消灯)")
        lgpio.gpio_write(h, args.pin, 0)       # 0 = Low = 0 V
    finally:
        # エラーや Ctrl+C でもここは必ず通る。消灯して後片付け。
        lgpio.gpio_write(h, args.pin, 0)
        lgpio.gpio_free(h, args.pin)
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()
