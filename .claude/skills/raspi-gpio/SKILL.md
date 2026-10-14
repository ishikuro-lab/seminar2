---
name: raspi-gpio
description: Raspberry Pi Zero 2 W + DRV8833 でモーターや GPIO を安全に扱うコードを書く。配線表、lgpio の使い方、安全手順、テンプレ。モーター・GPIO・センサのコードを書くときや配線を確認するときに使う。
---

# raspi-gpio — モーターと GPIO のコードを書く

## 配線(矢上祭 2026 ロボット基板、DRV8833)

| 側 | コネクタ | IN1 | IN2 | 既定の車輪 |
|---|---|---|---|---|
| A | J4 | GPIO17(物理 11) | GPIO18(物理 12) | 右 |
| B | J5 | GPIO22(物理 15) | GPIO19(物理 35) | 左 |

- 番号は BCM(GPIO 番号)。物理ピン番号と混同しない。
- DRV8833 の有効化(nSLEEP)は基板上で 3.3V 固定。GPIO で操作しない。
- 片方のピンに PWM(1000 Hz)、もう片方を Low で回る。IN1 に PWM = 正転。
- 両方 High はブレーキ。切り替えのときは Low にする側を先に下げる(`motor/motor_test.py` の `drive()`)。

## 安全手順(コードに必ず組み込む)

1. `--dry-run` オプションを付け、GPIO に触らずに出す値を表示できるようにする。
2. 走行時間に上限(例 10 秒)。`time.sleep` で待ち、ループで回し続けない。
3. `try/finally` で終了時に全ピン Low、`gpio_free`、`gpiochip_close`。
4. `SIGHUP` / `SIGTERM` を受けたら `SystemExit` にして `finally` を通す(SSH 切断対策)。`motor_test.py` の `install_stop_signals()` を再利用する。
5. 実行手順を README に書く: dry-run → 車輪を浮かせて → 床に置いて前を空ける。

## 手本

- `motor/motor_test.py`: `Gpio` クラス(claim、PWM、close)、`drive(gpio, name, speed)`、信号処理。新しいコードはここから `import` する。
- `motor/straight.py`: 両輪を同時に回し、時間で止める。`FORWARD` で前進方向を定義。

## テンプレ(lesson02/work/ に置く新しい走行プログラム)

```python
#!/usr/bin/env python3
"""説明を 1 行で。車輪を浮かせてから実行すること。"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "motor"))
from motor_test import MOTORS, Gpio, drive, install_stop_signals  # noqa: E402

MAX_SECONDS = 10.0


def main():
    p = argparse.ArgumentParser(description="説明")
    p.add_argument("--speed", type=float, default=0.5, help="出力 0〜1")
    p.add_argument("--seconds", type=float, default=1.0, help=f"時間 [秒]、上限 {MAX_SECONDS:g}")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    if not 0.0 < a.speed <= 1.0 or not 0.0 < a.seconds <= MAX_SECONDS:
        p.error("--speed は 0〜1、--seconds は 0 より大きく上限以下")

    install_stop_signals()
    gpio = None if a.dry_run else Gpio()
    try:
        drive(gpio, "A", a.speed)      # 右輪 正転
        drive(gpio, "B", -a.speed)     # 左輪 逆転(その場で回る例)
        if not a.dry_run:
            time.sleep(a.seconds)
    except KeyboardInterrupt:
        print("中断")
    finally:
        if gpio is not None:
            gpio.close()
    print("停止。全ピンを Low にしました。")


if __name__ == "__main__":
    main()
```

## lgpio の要点

- `import lgpio`、`h = lgpio.gpiochip_open(0)`、`lgpio.gpio_claim_output(h, pin, 0)`。
- PWM: `lgpio.tx_pwm(h, pin, 1000, duty_percent)`。0% と 100% は `gpio_write` のデジタル出力に切り替える(100% の PWM は High に張り付かないことがある)。
- 入力(センサ・スイッチ): `lgpio.gpio_claim_input(h, pin, lgpio.SET_PULL_UP)`、`lgpio.gpio_read(h, pin)`。
- 後片付け: `gpio_free` → `gpiochip_close`。
- `lgpio` は Raspberry Pi OS に入っている。無ければ `sudo apt install python3-lgpio`(先生に依頼)。

## よくある間違い

- ピン番号を物理番号で書いてしまう(GPIO17 ≠ 物理 17)。
- `while True:` でモーターを回し、止め忘れる。
- 例外で落ちてピンが High のまま → `finally` を書く。
- 2 つのプログラムが同じピンを使い `GPIO busy` → 前のプロセスを `kill`。
