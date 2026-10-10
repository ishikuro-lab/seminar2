#!/usr/bin/env python3
"""両輪を同時に回して直進させる。指定した時間が過ぎたら自動で止まる。

床に置き、前方を空けてから実行すること。
"""

import argparse
import time

from motor_test import MOTORS, Gpio, drive, install_stop_signals

MAX_SECONDS = 10.0

# 前進になる向き。+1 は正転 (IN1 に PWM)、-1 は逆転。実機で確かめて決める。
FORWARD = {"A": +1, "B": +1}


def main():
    parser = argparse.ArgumentParser(description="両輪を同時に回して直進させる")
    parser.add_argument("--speed", type=float, default=0.7, help="出力 0〜1 (既定 0.7)")
    parser.add_argument(
        "--seconds", type=float, default=1.0, help=f"走らせる時間 [秒] (既定 1、上限 {MAX_SECONDS:g})"
    )
    parser.add_argument(
        "--flip",
        choices=sorted(MOTORS),
        action="append",
        default=[],
        help="その側の向きを反転する (向きを確かめるとき用)",
    )
    parser.add_argument("--dry-run", action="store_true", help="GPIO に触らず、出す値を表示するだけ")
    args = parser.parse_args()
    if not 0.0 < args.speed <= 1.0:
        parser.error("--speed は 0 より大きく 1 以下で指定してください")
    if not 0.0 < args.seconds <= MAX_SECONDS:
        parser.error(f"--seconds は 0 より大きく {MAX_SECONDS:g} 以下で指定してください")

    speeds = {}
    for name in sorted(MOTORS):
        sign = -FORWARD[name] if name in args.flip else FORWARD[name]
        speeds[name] = sign * args.speed

    install_stop_signals()

    gpio = None if args.dry_run else Gpio()
    interrupted = False
    try:
        summary = ", ".join(
            f"{name} 側 {'正転' if speed > 0 else '逆転'}" for name, speed in speeds.items()
        )
        print(f"直進 {args.speed:.0%} ({summary}) ... {args.seconds:g} 秒", flush=True)
        for name, speed in speeds.items():
            drive(gpio, name, speed)
        if not args.dry_run:
            time.sleep(args.seconds)
    except KeyboardInterrupt:
        interrupted = True
    finally:
        if gpio is not None:
            gpio.close()

    if args.dry_run:
        print("終了。dry-run のため GPIO には触っていません。")
    elif interrupted:
        print("中断しました。全ピンを Low にしました。")
    else:
        print("停止。全ピンを Low にしました。")


if __name__ == "__main__":
    main()
