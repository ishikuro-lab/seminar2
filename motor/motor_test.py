#!/usr/bin/env python3
"""DRV8833 につないだ DC モーターの動作確認。

A 側 → B 側の順に「正転 → 停止 → 逆転 → 停止」と動かす。
車輪を浮かせてから実行すること。
"""

import argparse
import signal
import time

PWM_HZ = 1000
STOP_SECONDS = 1.0

# (IN1, IN2) の GPIO 番号 (BCM)。基板のシルクと同じ。
MOTORS = {
    "A": (17, 18),  # J4
    "B": (22, 19),  # J5
}


class Gpio:
    def __init__(self):
        import lgpio

        self._lgpio = lgpio
        self._handle = lgpio.gpiochip_open(0)
        self._pins = [pin for pins in MOTORS.values() for pin in pins]
        try:
            for pin in self._pins:
                lgpio.gpio_claim_output(self._handle, pin, 0)
        except Exception:
            lgpio.gpiochip_close(self._handle)
            raise

    def set_pin(self, pin, duty):
        # 100% の tx_pwm は High に張り付かないことがあるので、0% と 100% は
        # デジタル出力にして、その間だけ PWM を使う。
        if duty <= 0.0:
            self._lgpio.tx_pwm(self._handle, pin, PWM_HZ, 0.0)
            self._lgpio.gpio_write(self._handle, pin, 0)
        elif duty >= 1.0:
            self._lgpio.tx_pwm(self._handle, pin, PWM_HZ, 0.0)
            self._lgpio.gpio_write(self._handle, pin, 1)
        else:
            self._lgpio.tx_pwm(self._handle, pin, PWM_HZ, duty * 100.0)

    def close(self):
        for pin in self._pins:
            self.set_pin(pin, 0.0)
        for pin in self._pins:
            self._lgpio.gpio_free(self._handle, pin)
        self._lgpio.gpiochip_close(self._handle)


def drive(gpio, name, speed):
    """speed が正なら IN1 に PWM (正転)、負なら IN2 に PWM (逆転)、0 で停止。"""
    in1, in2 = MOTORS[name]
    if speed >= 0:
        low_pin, pwm_pin, duty = in2, in1, speed
    else:
        low_pin, pwm_pin, duty = in1, in2, -speed
    if gpio is None:
        print(f"    (dry-run) GPIO{pwm_pin} = {duty:.0%}, GPIO{low_pin} = Low")
        return
    # 両方 High (ブレーキ) の瞬間を作らないよう、Low にする側を先に切り替える。
    gpio.set_pin(low_pin, 0.0)
    gpio.set_pin(pwm_pin, duty)


def _exit_on_signal(signum, frame):
    raise SystemExit(128 + signum)


def install_stop_signals():
    """SSH が切れたとき (SIGHUP) や kill されたときも finally を通して止める。"""
    for name in ("SIGTERM", "SIGHUP"):
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), _exit_on_signal)


def main():
    parser = argparse.ArgumentParser(description="DRV8833 につないだ DC モーターの動作確認")
    parser.add_argument("--speed", type=float, default=0.4, help="出力 0〜1 (既定 0.4)")
    parser.add_argument("--seconds", type=float, default=2.0, help="回す時間 [秒] (既定 2)")
    parser.add_argument("--motor", choices=sorted(MOTORS), help="片側だけ試す (既定は A, B の順に両方)")
    parser.add_argument("--dry-run", action="store_true", help="GPIO に触らず、出す値を表示するだけ")
    args = parser.parse_args()
    if not 0.0 < args.speed <= 1.0:
        parser.error("--speed は 0 より大きく 1 以下で指定してください")
    if args.seconds <= 0.0:
        parser.error("--seconds は 0 より大きい値を指定してください")

    install_stop_signals()

    def wait(seconds):
        if not args.dry_run:
            time.sleep(seconds)

    names = [args.motor] if args.motor else sorted(MOTORS)
    gpio = None if args.dry_run else Gpio()
    interrupted = False
    try:
        for name in names:
            in1, in2 = MOTORS[name]
            for label, speed in (("正転", args.speed), ("逆転", -args.speed)):
                print(
                    f"{name} 側 (GPIO{in1}/{in2}) {label} {args.speed:.0%} ... {args.seconds:g} 秒",
                    flush=True,
                )
                drive(gpio, name, speed)
                wait(args.seconds)
                print(f"停止 ... {STOP_SECONDS:g} 秒", flush=True)
                drive(gpio, name, 0.0)
                wait(STOP_SECONDS)
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
        print("終了。全ピンを Low にしました。")


if __name__ == "__main__":
    main()
