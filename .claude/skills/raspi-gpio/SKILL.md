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
4. `SIGHUP` / `SIGTERM` を受けたら `SystemExit` にして `finally` を通す(SSH 切断対策)。教材では `signal.default_int_handler` を直接登録し、新たな関数は作らない。
5. 実行手順を README に書く: dry-run → 車輪を浮かせて → 床に置いて前を空ける。

## 公開中の教材

第2回の LED・センサ教材は `lesson02/` にある。GPIO の準備・測定・終了処理も各教材内に書く。独自の補助関数・共通ファイルは追加せず、`lgpio` と `time` の関数を直接使う。

モーターの完成版サンプルは開発用リポジトリに保持しており、この公開リポジトリには置かない。存在しないサンプルを import するコードは作らない。

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
