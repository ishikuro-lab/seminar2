#!/usr/bin/env python3
"""ゆっくり加速して、ゆっくり減速する。

0 % → 最大 → 0 % とデューティ比を少しずつ変える。急に動かすより、
車体や電池にやさしく、動き出す瞬間の速さ (最低速度) も観察できる。

実行: python3 motor_ramp.py --dry-run
      python3 motor_ramp.py                       (A 側、最大 80 %、全体で 4 秒)
      python3 motor_ramp.py --max 1.0 --seconds 6
"""

import argparse
import time

MOTORS = {"A": (17, 18), "B": (22, 19)}
MAX_SECONDS = 10.0
PWM_HZ = 1000
STEPS = 20  # 加速・減速をそれぞれ何段階に分けるか


def main():
    parser = argparse.ArgumentParser(description="ゆっくり加速 → 減速")
    parser.add_argument("--motor", choices=sorted(MOTORS), default="A", help="A (右) か B (左)")
    parser.add_argument("--max", type=float, default=0.8, help="最大の速さ 0〜1 (既定 0.8)")
    parser.add_argument("--seconds", type=float, default=4.0, help=f"全体の秒数 (既定 4、上限 {MAX_SECONDS:g})")
    parser.add_argument("--dry-run", action="store_true", help="GPIO に触らない")
    args = parser.parse_args()
    if not 0 < args.max <= 1:
        parser.error("--max は 0 より大きく 1 以下")
    if not 0 < args.seconds <= MAX_SECONDS:
        parser.error(f"--seconds は 0 より大きく {MAX_SECONDS:g} 以下")

    in1, in2 = MOTORS[args.motor]
    wait = args.seconds / (2 * STEPS)  # 1 段階あたりの時間
    # 加速: 0, 1/20, 2/20, ..., 1 倍。減速はその逆順
    up = [args.max * i / STEPS for i in range(STEPS + 1)]
    down = up[::-1]

    h = None
    if not args.dry_run:
        import lgpio

        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(h, in1, 0)
        lgpio.gpio_claim_output(h, in2, 0)

    try:
        for label, speeds in (("加速", up), ("減速", down)):
            print(label)
            for speed in speeds:
                duty = speed * 100
                if args.dry_run:
                    print(f"  (dry-run) GPIO{in1} デューティ {duty:5.1f} %")
                else:
                    import lgpio

                    lgpio.tx_pwm(h, in1, PWM_HZ, duty)
                    time.sleep(wait)
    except KeyboardInterrupt:
        print("\n中断")
    finally:
        if h is not None:
            import lgpio

            lgpio.tx_pwm(h, in1, PWM_HZ, 0)
            lgpio.gpio_write(h, in1, 0)
            lgpio.gpio_write(h, in2, 0)
            lgpio.gpio_free(h, in1)
            lgpio.gpio_free(h, in2)
            lgpio.gpiochip_close(h)
    print("終了")


if __name__ == "__main__":
    main()
