#!/usr/bin/env python3
"""ライントレースセンサ 8 ch を一行で表示する。Ctrl+C で止める。

配線: OUT1〜8 → GPIO 4, 5, 6, 16, 20, 21, 23, 24 (README の表を参照)
表示: ○ = 白 (反射あり、0)、● = 黒 (反射なし、1)
実行: python3 sensor_8ch.py
      python3 sensor_8ch.py --pins 4 5 6       (3 ch だけ使うとき)
"""

import argparse
import time

import lgpio

SENSOR_PINS = [4, 5, 6, 16, 20, 21, 23, 24]  # OUT1 から順番


def read_all(h, pins):
    """全チャンネルを読んで、0/1 のリストで返す。"""
    return [lgpio.gpio_read(h, pin) for pin in pins]


def to_marks(values):
    """[0, 1, 1, 0] → "○●●○" のような文字列にする。"""
    return "".join("●" if v == 1 else "○" for v in values)


def main():
    parser = argparse.ArgumentParser(description="センサ 8 ch を一行で表示")
    parser.add_argument("--pins", type=int, nargs="+", default=SENSOR_PINS, help="GPIO 番号を OUT1 から順に (既定 4 5 6 16 20 21 23 24)")
    parser.add_argument("--interval", type=float, default=0.2, help="読む間隔 [秒] (既定 0.2)")
    args = parser.parse_args()

    h = lgpio.gpiochip_open(0)
    for pin in args.pins:
        lgpio.gpio_claim_input(h, pin)
    print("ch:  " + " ".join(f"{i + 1}" for i in range(len(args.pins))))
    print("○ = 白、● = 黒。Ctrl+C で終了")
    try:
        while True:
            values = read_all(h, args.pins)
            print(f"\r     {to_marks(values)}   {values}", end="", flush=True)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n終了")
    finally:
        for pin in args.pins:
            lgpio.gpio_free(h, pin)
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()
