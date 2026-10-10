# 第 3 回 — モーターを動かす

今回は **ロボット基板**(Raspberry Pi Zero 2 W を載せる基板。モータードライバ DRV8833 付き)を使って、DC モーターを回します。

| 順番 | 内容 | スクリプト |
|---|---|---|
| 1 | モーターを回す・止める(ON/OFF) | `motor_on_off.py` |
| 2 | 逆向きに回す | `motor_reverse.py` |
| 3 | PWM で速さを変える | `motor_pwm.py`、`motor_ramp.py` |
| 4 | 演習 | [exercises.md](exercises.md) |

## 安全のルール(必ず守る)

1. **車輪を浮かせてから** 実行する(机の上で走り出すと落ちます)。
2. 新しいコードは **`--dry-run`** で試してから本番(GPIO に触らず、出す値を表示するだけ)。
3. 走らせる時間には **上限** を付ける(教材のスクリプトは最大 10 秒)。
4. 止めるときは `Ctrl + C`。プログラムは終わるときに必ず全ピンを Low にする。
5. 基板のモーター電源スイッチは、配線が済むまで OFF。

## 準備

```
cd ~/seminar2
git pull
cp -r materials/lesson03 work/lesson03
cd work/lesson03
```

## なぜモータードライバが要るのか

GPIO が出せる電流は数 mA で、電圧も 3.3 V です。モーターは数百 mA 流れ、電源も 5 V 以上が要るので、GPIO で直接は回せません。**モータードライバ**(DRV8833)は、GPIO の小さな信号を受けて、モーター用の大きな電流を流す「スイッチの集まり」です。

```
GPIO ──(小さな信号)──> DRV8833 ──(大きな電流)──> モーター
                         ↑
                    モーター電源 (電池)
```

## 配線(ロボット基板)

基板上で配線済みです。ラズパイを基板のソケットに差し、モーターをコネクタに差すだけです。

| 側 | コネクタ | IN1 | IN2 | 車輪 |
|---|---|---|---|---|
| A | J4 | GPIO17(物理 11) | GPIO18(物理 12) | 右 |
| B | J5 | GPIO22(物理 15) | GPIO19(物理 35) | 左 |

- モーターの 2 本の線は、どちらをどちらに差しても壊れません。逆に回るだけです。
- DRV8833 の有効化ピン(nSLEEP)は基板上で 3.3 V につながっているので、プログラムで触る必要はありません。

## IN1 と IN2 の組み合わせ

DRV8833 は 1 つのモーターを 2 本の入力(IN1、IN2)で制御します。

| IN1 | IN2 | モーター | この授業での呼び方 |
|---|---|---|---|
| Low | Low | 止まる(惰性で回る) | 停止 |
| High | Low | 回る | 正転 |
| Low | High | 逆に回る | 逆転 |
| High | High | 止まる(ブレーキ、急停止) | ブレーキ |

速さを変えたいときは、High にする側を PWM にします(デューティ比が大きいほど速い)。

## プログラムの基本形

```python
import lgpio

IN1, IN2 = 17, 18                        # A 側 (右)

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, IN1, 0)       # 最初は両方 Low = 停止
lgpio.gpio_claim_output(h, IN2, 0)
try:
    lgpio.gpio_write(h, IN1, 1)          # 正転
    lgpio.gpio_write(h, IN2, 0)
    time.sleep(2)
finally:
    lgpio.gpio_write(h, IN1, 0)          # 必ず止める
    lgpio.gpio_write(h, IN2, 0)
    lgpio.gpiochip_close(h)
```

第 2 回の LED と同じ形です。違いは「ピンが 2 本」と「終了時に必ず止める」ことの重みです。

## 実行のしかた

```
python3 motor_on_off.py --dry-run       # まず GPIO に触らずに確認
python3 motor_on_off.py                 # A 側を 2 秒回す (車輪を浮かせて)
python3 motor_on_off.py --motor B       # B 側
python3 motor_pwm.py --speed 0.5        # 50 % の速さ
python3 motor_on_off.py --help          # 引数の一覧
```

## 各スクリプト

| ファイル | やること | 学ぶこと |
|---|---|---|
| `motor_on_off.py` | 2 秒回して止める | IN1/IN2、try/finally、`--dry-run` |
| `motor_reverse.py` | 正転 → 停止 → 逆転 → 停止 | 向きの切り替え、間に停止を挟む理由 |
| `motor_pwm.py` | 指定した速さで回す | PWM による速度制御 |
| `motor_ramp.py` | ゆっくり加速 → 減速 | `for` ループで PWM を変える |

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| 回らない、うなるだけ | モーター電源スイッチ、電池。`--speed 0.6` 以上にする(低すぎると回らない) |
| 正転のはずが逆に回る | モーター線の差し込みを逆にする。またはコードの IN1/IN2 を入れ替える |
| `GPIO busy` | 前のプログラムが残っている。`ps aux \| grep python` → `kill 番号` |
| 止まらない | `Ctrl + C`。それでもだめなら電源スイッチ OFF。原因は `finally` が無いか、ループに上限が無いこと |
| 両方 High にしてしまった | ブレーキ状態(壊れない)。片方を Low にする |

## 完成版の紹介

`motor/motor_test.py` と `motor/straight.py` は、今回の内容を関数にまとめて、SSH が切れても止まるようにした完成版です。第 4 回以降の走行プログラムはこれを `import` して作ります。
