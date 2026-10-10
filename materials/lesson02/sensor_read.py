#!/usr/bin/env python3
"""ライントレースセンサ 1 ch を読み続ける。Ctrl+C で止める。

配線: センサ基板 OUT1 → GPIO4 (物理 7)、VCC → 3.3 V (物理 1)、GND → GND (物理 9)
      ※ 5 V にはつながない (GPIO が壊れる)
読み方: 白い床 (反射あり) = 0 (Low)、黒い線や何も無い = 1 (High)
実行: python3 sensor_read.py              (GPIO4 を 0.2 秒おきに)
      python3 sensor_read.py --pin 5     (別のチャンネル)
"""

import argparse
import time

import lgpio

SENSOR_PIN = 4


def main():
    parser = argparse.ArgumentParser(description="センサ 1 ch を読み続ける")
    parser.add_argument("--pin", type=int, default=SENSOR_PIN, help=f"センサ出力をつないだ GPIO 番号 (既定 {SENSOR_PIN})")
    parser.add_argument("--interval", type=float, default=0.2, help="読む間隔 [秒] (既定 0.2)")
    args = parser.parse_args()

    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_input(h, args.pin)        # 入力にする (電圧を読む)
    print(f"GPIO{args.pin} を読みます。0 = 白 (反射あり)、1 = 黒 (反射なし)。Ctrl+C で終了")
    try:
        while True:
            value = lgpio.gpio_read(h, args.pin)   # 0 か 1 が返る
            label = "白 (反射あり)" if value == 0 else "黒 (反射なし)"
            print(f"GPIO{args.pin} = {value}  {label}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n終了")
    finally:
        lgpio.gpio_free(h, args.pin)
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()
