#!/usr/bin/env python3
"""モーターを 2 秒回して止める (ON/OFF)。

配線: ロボット基板。A 側 (右) = GPIO17/18、B 側 (左) = GPIO22/19
実行: python3 motor_on_off.py --dry-run    (まず GPIO に触らず確認)
      python3 motor_on_off.py              (A 側を 2 秒、車輪を浮かせて)
      python3 motor_on_off.py --motor B
"""

import argparse
import time

MOTORS = {
    "A": (17, 18),  # (IN1, IN2) 右
    "B": (22, 19),  # (IN1, IN2) 左
}
MAX_SECONDS = 10.0  # これより長くは回さない


def main():
    parser = argparse.ArgumentParser(description="モーターを回して止める")
    parser.add_argument("--motor", choices=sorted(MOTORS), default="A", help="A (右) か B (左)。既定 A")
    parser.add_argument("--seconds", type=float, default=2.0, help=f"回す秒数 (既定 2、上限 {MAX_SECONDS:g})")
    parser.add_argument("--dry-run", action="store_true", help="GPIO に触らず、出す値を表示するだけ")
    args = parser.parse_args()
    if not 0 < args.seconds <= MAX_SECONDS:
        parser.error(f"--seconds は 0 より大きく {MAX_SECONDS:g} 以下にしてください")

    in1, in2 = MOTORS[args.motor]
    print(f"{args.motor} 側: IN1 = GPIO{in1}, IN2 = GPIO{in2}")

    if args.dry_run:
        print(f"(dry-run) GPIO{in1} = High, GPIO{in2} = Low で {args.seconds:g} 秒 → 両方 Low")
        return

    import lgpio  # ラズパイでだけ読み込む

    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, in1, 0)   # 最初は両方 Low (停止)
    lgpio.gpio_claim_output(h, in2, 0)
    try:
        print(f"正転 {args.seconds:g} 秒")
        lgpio.gpio_write(h, in1, 1)      # IN1 = High, IN2 = Low → 正転
        lgpio.gpio_write(h, in2, 0)
        time.sleep(args.seconds)
        print("停止")
    except KeyboardInterrupt:
        print("\n中断")
    finally:
        lgpio.gpio_write(h, in1, 0)      # 必ず両方 Low に戻す
        lgpio.gpio_write(h, in2, 0)
        lgpio.gpio_free(h, in1)
        lgpio.gpio_free(h, in2)
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()
