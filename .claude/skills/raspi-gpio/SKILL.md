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
- 両方 High はブレーキ。切り替えのときは Low にする側を先に下げる。

## 安全手順(コードに必ず組み込む)

1. 第2回教材は模擬GPIO環境で動作確認し、GPIOに触れず検証する。
2. 走行時間に上限(例 10 秒)。`time.sleep` で待ち、ループで回し続けない。
3. `try/finally` で終了時に全ピン Low、`gpio_free`、`gpiochip_close`。
4. モーターを回すコードでは `SIGHUP` / `SIGTERM` を受けたら `finally` を通す(SSH 切断対策)。`signal.default_int_handler` を直接登録し、新たな関数は作らない。LED・センサ教材(`lesson02/` の LED と `lesson03/ultrasonic/` の超音波)は初学者向けに簡単さを優先し、`signal` は入れない(`try / except KeyboardInterrupt / finally` のみ)。
5. 実行手順を README に書く: コードを読んでどのピンが何秒 High になるか確かめる → 車輪を浮かせて → 床に置いて前を空ける。教材は `argparse` を使わないので `--dry-run` は無い。秒数はファイル先頭の変数にし、上限(10 秒)を書き添える。

## 公開中の教材

第2回の LED 教材は `lesson02/`、第3回は `lesson03/ultrasonic/`(超音波 `01_distance_read.py`・`02_distance_led.py`)、第4回は `lesson04/motor/`(`01_motor_on_off.py`〜`04_motor_ramp.py`)にある。演習は各フォルダの `excersises/` に1問ずつ。モーター教材も `argparse` を使わず、ピン・速さ・秒数を先頭の変数にする(`signal` の2行だけは入れる)。GPIO の準備・測定・終了処理も各教材内に書く。独自の補助関数・共通ファイルは追加せず、`lgpio` と `time` の関数を直接使う。

モーターの完成版サンプルは開発用リポジトリに保持しており、この公開リポジトリには置かない。存在しないサンプルを import するコードは作らない。

## lgpio の要点

- `import lgpio`、`h = lgpio.gpiochip_open(0)`、`lgpio.gpio_claim_output(h, pin, 0)`。
- PWM: `lgpio.tx_pwm(h, pin, 1000, duty_percent)`。モーターでは 0% と 100% を `gpio_write` のデジタル出力に切り替える(100% の PWM は High に張り付かないことがある)。`lesson02/` の LED 教材は簡単さを優先して `tx_pwm` だけを使う。
- `tx_pwm(h, pin, 1000, 0)` は PWM を止めない(0% の PWM が動き続け、そのピンを Low に書き戻す)。止めるときは周波数 0 の `tx_pwm(h, pin, 0, 0)`。PWM を使ったピンを `gpio_write` で High にするときは、先に周波数 0 で止める。2026-10-27 に関数版 `motor_gpio.py` の 100% で回らなかった原因。
- 入力(センサ・スイッチ): `lgpio.gpio_claim_input(h, pin, lgpio.SET_PULL_UP)`、`lgpio.gpio_read(h, pin)`。
- 後片付け: `gpio_free` → `gpiochip_close`。
- `lgpio` は Raspberry Pi OS に入っている。無ければ `sudo apt install python3-lgpio`(先生に依頼)。

## よくある間違い

- ピン番号を物理番号で書いてしまう(GPIO17 ≠ 物理 17)。
- `while True:` でモーターを回し、止め忘れる。
- 例外で落ちてピンが High のまま → `finally` を書く。
- 2 つのプログラムが同じピンを使い `GPIO busy` → 前のプロセスを `kill`。
