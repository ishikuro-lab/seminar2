#!/usr/bin/env python3
"""PWM でモーターの速さを変える。

IN1 に PWM (1000 Hz)、IN2 を Low にすると、デューティ比に応じた速さで正転する。
第 2 回の LED の明るさと同じ仕組み。

実行: python3 motor_pwm.py --dry-run
      python3 motor_pwm.py --speed 0.5      (50 % で 2 秒、A 側)
      python3 motor_pwm.py --speed 0.8 --motor B --seconds 1
"""

import argparse
import time

MOTORS = {"A": (17, 18), "B": (22, 19)}
MAX_SECONDS = 10.0
PWM_HZ = 1000


def main():
    parser = argparse.ArgumentParser(description="PWM でモーターの速さを変える")
    parser.add_argument("--motor", choices=sorted(MOTORS), default="A", help="A (右) か B (左)")
    parser.add_argument("--speed", type=float, default=0.5, help="速さ 0〜1 (既定 0.5)。0.4 以下だと回らないことがある")
    parser.add_argument("--seconds", type=float, default=2.0, help=f"回す秒数 (既定 2、上限 {MAX_SECONDS:g})")
    parser.add_argument("--dry-run", action="store_true", help="GPIO に触らない")
    args = parser.parse_args()
    if not 0 <= args.speed <= 1:
        parser.error("--speed は 0 から 1")
    if not 0 < args.seconds <= MAX_SECONDS:
        parser.error(f"--seconds は 0 より大きく {MAX_SECONDS:g} 以下")

    in1, in2 = MOTORS[args.motor]
    duty = args.speed * 100  # tx_pwm のデューティ比は 0〜100 [%]
    print(f"{args.motor} 側: GPIO{in1} に {PWM_HZ} Hz デューティ {duty:.0f} %、GPIO{in2} = Low、{args.seconds:g} 秒")
    if args.dry_run:
        print("(dry-run) GPIO には触っていません")
        return

    import lgpio

    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, in1, 0)
    lgpio.gpio_claim_output(h, in2, 0)
    try:
        lgpio.gpio_write(h, in2, 0)
        lgpio.tx_pwm(h, in1, PWM_HZ, duty)     # ここから PWM が出続ける
        time.sleep(args.seconds)
        print("停止")
    except KeyboardInterrupt:
        print("\n中断")
    finally:
        lgpio.tx_pwm(h, in1, PWM_HZ, 0)        # PWM を止める
        lgpio.gpio_write(h, in1, 0)
        lgpio.gpio_write(h, in2, 0)
        lgpio.gpio_free(h, in1)
        lgpio.gpio_free(h, in2)
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()
