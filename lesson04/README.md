# 第 4 回 — モーターを動かす

**ロボット基板**(Raspberry Pi Zero 2 W を載せる基板。モータードライバ DRV8833 付き)を使って、DC モーターを回します。
第 3 回で予定していた後半を、この回で行います。

| 順番 | 内容 | スクリプト |
|---|---|---|
| 1 | モーターを回す・止める(ON/OFF) | `motor/01_motor_on_off.py` |
| 2 | 逆向きに回す | `motor/02_motor_reverse.py` |
| 3 | PWM で速さを変える | `motor/03_motor_pwm.py`、`motor/04_motor_ramp.py` |
| 4 | 演習(モーター) | [motor/excersises/](motor/excersises/) |

教材は `motor/`、演習は `motor/excersises/` にあります。

## 準備

```
cd ~/seminar2
git pull
mkdir -p students/$USER/lesson04/motor
cp -n lesson04/motor/*.py lesson04/motor/excersises/*.py students/$USER/lesson04/motor/
cd students/$USER/lesson04/motor
```

`$USER` は自分のユーザー名(姓)に置き換わります。`lesson04/` の教材と問題は直接編集せず、自分のフォルダにコピーしたものを使います。`cp -n` は、すでにあるファイルを上書きしないので、2 回目に打っても自分の答えは消えません。

---

## 安全のルール(必ず守る)

1. **車輪を浮かせてから** 実行する(机の上で走り出すと落ちます)。
2. 実行する前に **コードを読み、どのピンが何秒 High になるか** を確かめる。初めて動かすコードは `seconds` を 1 にして、車輪を浮かせて試す。
3. 走らせる時間には **上限** を付ける(教材のスクリプトは最大 10 秒)。
4. 止めるときは `Ctrl + C`。プログラムは終わるときに必ず全ピンを Low にする。
5. 基板のモーター電源スイッチは、配線が済むまで OFF。

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

まず `01_motor_on_off.py` を読みます。第 2 回の LED と同じ形で、準備 → `try` で動かす → `finally` で必ず止める、の順に書いてあります。

```python
import lgpio
import time

in1 = 17  # A 側 (右)
in2 = 18

h = lgpio.gpiochip_open(0)
try:
    lgpio.gpio_claim_output(h, in1, 0)  # 最初は両方 Low = 停止
    lgpio.gpio_claim_output(h, in2, 0)
    lgpio.gpio_write(h, in1, 1)         # 正転
    lgpio.gpio_write(h, in2, 0)
    time.sleep(2)
finally:
    lgpio.gpio_write(h, in1, 0)         # 必ず止める
    lgpio.gpio_write(h, in2, 0)
    lgpio.gpiochip_close(h)
```

LED との違いは「ピンが 2 本」と「終了時に必ず止める」ことの重みです。

教材のスクリプトには、これに `signal` の 2 行が入っています。**SSH が切れてもモーターが止まる** ようにするためです。切れたときも `finally` を通します。ただし、切れた瞬間に必ず信号が届くとは限らないので、回す時間は短くし、異常時はモーター電源を切ってください。

## 向きと速さ

- **逆転**: `02_motor_reverse.py` は、IN1 を Low、IN2 を High にして逆に回します。**向きを変える前に両方 Low にして 1 秒止めます。** 急に逆転させるとモーターと電池に大きな電流が流れます。
- **速さ**: `03_motor_pwm.py` は、反対側を Low にしてから `lgpio.tx_pwm(h, in1, 1000, speed)` で PWM を出します。第 2 回の LED の明るさと同じ仕組みで、`speed`(0〜100 %)が大きいほど速く回ります。
- **止める**: PWM を使ったときは、`finally` で `tx_pwm(h, in1, 1000, 0)` で PWM を止めてから、両方を Low にします。

## 実行のしかた

自分のアカウントでSSH接続し、上の準備でコピーしてから実行します。Sambaでは編集し、実行はSSHの画面で行います。

```sh
source ~/venv/bin/activate
cd ~/seminar2/students/$USER/lesson04/motor
python3 01_motor_on_off.py  # A側を2秒回す。まずsecondsを1にして車輪を浮かせる
python3 03_motor_pwm.py    # 50%で2秒回す
```

速さ・秒数・使う側はファイルの先頭の変数で変えます。回す時間は合計10秒以内です。04は10 %ずつ、1段階0.1秒で加速・減速します。待ち時間を長くしすぎないでください。実行用のコマンドに引数はありません。

---

## 各スクリプト

| ファイル | やること | 学ぶこと |
|---|---|---|
| `motor/01_motor_on_off.py` | 2 秒回して止める | IN1/IN2、try/finally、`signal` |
| `motor/02_motor_reverse.py` | 正転 → 停止 → 逆転 → 停止 | 向きの切り替え、間に停止を挟む理由 |
| `motor/03_motor_pwm.py` | 指定した速さで回す | PWM による速度制御 |
| `motor/04_motor_ramp.py` | ゆっくり加速 → 減速 | `for` ループで PWM を変える |

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| 回らない、うなるだけ | モーター電源スイッチ、電池。`03_motor_pwm.py` の `speed` を 60 以上にする(低すぎると回らない) |
| 正転のはずが逆に回る | モーター線の差し込みを逆にする。またはコードの `in1` と `in2` を入れ替える |
| `GPIO busy` | 前のプログラムが残っている。`ps aux \| grep python` → `kill 番号` |
| 止まらない | `Ctrl + C`。それでもだめなら電源スイッチ OFF。原因は `finally` が無いか、ループに上限が無いこと |
| 両方 High にしてしまった | ブレーキ状態(壊れない)。片方を Low にする |
| `ModuleNotFoundError: lgpio` | ラズパイ以外で実行している。ラズパイで実行する |
