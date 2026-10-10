#!/usr/bin/env python3
"""正転 → 停止 → 逆転 → 停止 と動かす。

IN1=High, IN2=Low が正転、IN1=Low, IN2=High が逆転。
向きを変えるときは、いったん両方 Low (停止) にしてから切り替える。
いきなり逆にすると、モーターと電池に大きな電流が流れるため。

実行: python3 motor_reverse.py --dry-run
      python3 motor_reverse.py            (A 側、各 2 秒)
      python3 motor_reverse.py --motor B --seconds 1
"""

import argparse
import time

MOTORS = {"A": (17, 18), "B": (22, 19)}
MAX_SECONDS = 10.0
STOP_SECONDS = 1.0


def set_motor(h, in1, in2, direction, dry_run):
    """direction: 'forward' (正転), 'reverse' (逆転), 'stop' (停止)"""
    table = {
        "forward": (1, 0),
        "reverse": (0, 1),
        "stop": (0, 0),
    }
    v1, v2 = table[direction]
    if dry_run:
        print(f"  (dry-run) GPIO{in1} = {v1}, GPIO{in2} = {v2}")
        return
    # 両方 High (ブレーキ) の瞬間を作らないよう、Low にする側を先に書く
    if v1 == 0:
        lgpio_write(h, in1, 0)
        lgpio_write(h, in2, v2)
    else:
        lgpio_write(h, in2, 0)
        lgpio_write(h, in1, v1)


def lgpio_write(h, pin, value):
    import lgpio

    lgpio.gpio_write(h, pin, value)


def main():
    parser = argparse.ArgumentParser(description="正転 → 停止 → 逆転 → 停止")
    parser.add_argument("--motor", choices=sorted(MOTORS), default="A", help="A (右) か B (左)")
    parser.add_argument("--seconds", type=float, default=2.0, help=f"回す秒数 (既定 2、上限 {MAX_SECONDS:g})")
    parser.add_argument("--dry-run", action="store_true", help="GPIO に触らない")
    args = parser.parse_args()
    if not 0 < args.seconds <= MAX_SECONDS:
        parser.error(f"--seconds は 0 より大きく {MAX_SECONDS:g} 以下")

    in1, in2 = MOTORS[args.motor]
    h = None
    if not args.dry_run:
        import lgpio

        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(h, in1, 0)
        lgpio.gpio_claim_output(h, in2, 0)

    def wait(sec):
        if not args.dry_run:
            time.sleep(sec)

    try:
        for direction, label in (("forward", "正転"), ("reverse", "逆転")):
            print(f"{label} {args.seconds:g} 秒")
            set_motor(h, in1, in2, direction, args.dry_run)
            wait(args.seconds)
            print(f"停止 {STOP_SECONDS:g} 秒")
            set_motor(h, in1, in2, "stop", args.dry_run)
            wait(STOP_SECONDS)
    except KeyboardInterrupt:
        print("\n中断")
    finally:
        if h is not None:
            import lgpio

            lgpio.gpio_write(h, in1, 0)
            lgpio.gpio_write(h, in2, 0)
            lgpio.gpio_free(h, in1)
            lgpio.gpio_free(h, in2)
            lgpio.gpiochip_close(h)
    print("終了")


if __name__ == "__main__":
    main()
