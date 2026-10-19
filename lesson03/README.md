# 第 3 回 — センサを読む・モーターを動かす

前半は第 2 回のブレッドボードに **超音波距離センサ**(HC-SR04)を足して、物までの距離を測ります。
後半は **ロボット基板**(Raspberry Pi Zero 2 W を載せる基板。モータードライバ DRV8833 付き)を使って、DC モーターを回します。

| 順番 | 内容 | スクリプト |
|---|---|---|
| 1 | 超音波センサで距離を測る | `ultrasonic/01_distance_read.py` |
| 2 | 距離に応じて LED を点ける | `ultrasonic/02_distance_led.py` |
| 3 | 演習①(超音波) | [ultrasonic/excersises/](ultrasonic/excersises/) |
| 4 | モーターを回す・止める(ON/OFF) | `motor/01_motor_on_off.py` |
| 5 | 逆向きに回す | `motor/02_motor_reverse.py` |
| 6 | PWM で速さを変える | `motor/03_motor_pwm.py`、`motor/04_motor_ramp.py` |
| 7 | 演習②(モーター) | [motor/excersises/](motor/excersises/) |

フォルダは話題ごとに分かれています。前半は `ultrasonic/`、後半は `motor/`、演習はそれぞれの `excersises/` です。

## 準備

前半と後半で、それぞれ始まるときにコピーします。まとめて全部コピーしなくてよいです。

前半(超音波):

```
cd ~/seminar2
git pull
mkdir -p students/$USER/lesson03/ultrasonic
cp -n lesson03/ultrasonic/*.py lesson03/ultrasonic/excersises/*.py students/$USER/lesson03/ultrasonic/
cd students/$USER/lesson03/ultrasonic
```

後半(モーター):

```
cd ~/seminar2
mkdir -p students/$USER/lesson03/motor
cp -n lesson03/motor/*.py lesson03/motor/excersises/*.py students/$USER/lesson03/motor/
cd students/$USER/lesson03/motor
```

`$USER` は自分のユーザー名(姓)に置き換わります。`lesson03/` の教材と問題は直接編集せず、自分のフォルダにコピーしたものを使います。`cp -n` は、すでにあるファイルを上書きしないので、2 回目に打っても自分の答えは消えません。

---

## 前半: 超音波センサで距離を測る

## 今回使うピン(前半)

第 2 回と同じブレッドボードを使います。LED は第 2 回のままです。

| 用途 | GPIO | 物理ピン |
|---|---|---|
| LED | GPIO12 | 32 |
| 超音波センサ TRIG | GPIO23 | 16 |
| 超音波センサ ECHO（分圧後） | GPIO24 | 18 |
| 超音波センサ VCC（5 V） | — | 2 または 4 |
| GND | — | 6, 9, 14, 20, 25, 30, 34, 39 のどれか |

## 配線: 超音波距離センサ（HC-SR04、5 V版）

超音波を出して、物に反射して戻るまでの時間から距離を測ります。班で1個のセンサを使い、距離測定のプログラムは1人ずつ交代で実行してください。複数人から同時に動かさないでください。

| センサ端子 | つなぐ先 |
|---|---|
| VCC | 5 V（物理2） |
| GND | GND（物理6） |
| TRIG | GPIO23（物理16） |
| ECHO | **抵抗で電圧を下げてから** GPIO24（物理18） |

**ECHOをGPIOへ直接つながないでください。** HC-SR04の電源は5 Vですが、ラズパイのGPIOは3.3 Vの入力です。電源と信号の電圧を区別します。

ECHOの信号は、次の2本の抵抗で約3.0 Vへ下げます。

```text
HC-SR04 ECHO ──[1 kΩ]──┬── GPIO24（物理18）
                       │
                    [1.5 kΩ]
                       │
                      GND
```

抵抗の順番・値を確認し、電源を切って配線してから先生に確認してもらいます。VCCは5 Vへ接続し、LED用の抵抗330 Ωと混同しないでください。

`01_distance_read.py` を実行し、まず定規で10 / 20 / 30 cmに物を置いて表示を比べます。次に `02_distance_led.py` で、10 cmより近いときにLEDが点くことを確認します。

距離は目安です。Pythonの処理時間や反射する物によって値が揺れることがあります。

参考：[HC-SR04データシート](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)、[Raspberry PiのGPIO仕様](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)

## 前半の約束

1. センサは班で1個。実行は声をかけて **1人ずつ交代** する(同時に動かすと `GPIO busy`)。
2. 配線は **電源を切ってから** 触る。通電する前に、ECHOの分圧(1 kΩ + 1.5 kΩ)を先生に確認してもらう。
3. 距離が表示されずに止まったら、配線のまちがいです。`Ctrl + C` で止めて配線を見直します。

## 距離の測り方(プログラムの中身)

TRIGを一瞬だけHighにすると、センサが超音波を出します。ECHOは、超音波が出た瞬間にHighになり、反射が戻ってくるとLowに戻ります。つまり **ECHOがHighだった時間** が、音が往復した時間です。

```python
while lgpio.gpio_read(h, echo_pin) == 0:
    pass                   # Highになるまで待つ
start = time.monotonic()   # 超音波が出た時刻

while lgpio.gpio_read(h, echo_pin) == 1:
    pass                   # Lowに戻るまで待つ
end = time.monotonic()     # 反射が戻ってきた時刻

distance = round((end - start) * 34300 / 2, 1)
```

音は1秒に34300 cm進みます。往復した距離なので2で割ると、物までの距離になります。

第 2 回で使った関数に、入力用の3つが増えます。

| 操作 | ライブラリの関数 |
|---|---|
| 入力に設定 | `lgpio.gpio_claim_input(h, 24)` |
| 入力を読む | `lgpio.gpio_read(h, 24)` |
| 時刻を測る | `time.monotonic()` |

---

## 後半: モーターを動かす

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

第 2 回の LED と同じ形です。違いは「ピンが 2 本」と「終了時に必ず止める」ことの重みです。

教材のスクリプトには、これに `signal` の 2 行が入っています。**SSH が切れてもモーターが止まる** ようにするためです。切れたときも `finally` を通します。

## 実行のしかた

```
python3 01_motor_on_off.py       # A 側を 2 秒回す (車輪を浮かせて)
python3 03_motor_pwm.py          # 速さ 50 % で 2 秒
```

速さ・秒数・使う側(A か B)は、**ファイルの先頭の変数** を書き換えて変えます。引数はありません。

```python
in1 = 17     # A 側を使う。B 側にしたいときは 22
in2 = 18     # A 側を使う。B 側にしたいときは 19
speed = 50   # 速さ 0〜100 [%]
seconds = 2  # 回す秒数。10 秒より長くしない
```

---

## 各スクリプト

| ファイル | やること | 学ぶこと |
|---|---|---|
| `ultrasonic/01_distance_read.py` | 距離を cm で表示 | TRIG/ECHO、時間測定、距離計算 |
| `ultrasonic/02_distance_led.py` | 10 cmより近ければLED点灯 | `if` / `else` |
| `motor/01_motor_on_off.py` | 2 秒回して止める | IN1/IN2、try/finally、`signal` |
| `motor/02_motor_reverse.py` | 正転 → 停止 → 逆転 → 停止 | 向きの切り替え、間に停止を挟む理由 |
| `motor/03_motor_pwm.py` | 指定した速さで回す | PWM による速度制御 |
| `motor/04_motor_ramp.py` | ゆっくり加速 → 減速 | `for` ループで PWM を変える |

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| 距離が表示されずに止まる | 配線のまちがい。VCCが5 Vか、GNDが共通か、TRIG/ECHOが逆でないか、ECHOの分圧を先生と確認。`Ctrl + C` で止める |
| 距離が不安定 | センサの正面に平らな物を置く。他のプログラムを止め、1人ずつ測る |
| 回らない、うなるだけ | モーター電源スイッチ、電池。`03_motor_pwm.py` の `speed` を 60 以上にする(低すぎると回らない) |
| 正転のはずが逆に回る | モーター線の差し込みを逆にする。またはコードの `in1` と `in2` を入れ替える |
| `GPIO busy` | 前のプログラムが残っている。`ps aux \| grep python` → `kill 番号` |
| 止まらない | `Ctrl + C`。それでもだめなら電源スイッチ OFF。原因は `finally` が無いか、ループに上限が無いこと |
| 両方 High にしてしまった | ブレーキ状態(壊れない)。片方を Low にする |
| `ModuleNotFoundError: lgpio` | ラズパイ以外で実行している。ラズパイで実行する |
