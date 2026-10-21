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
3. 「測れません」が続いたら `Ctrl + C` で止めます。物の位置・向きや配線を先生と確認します。配線だけが原因とは限りません。

## 関数を使って距離を測る

まず `01_distance_read.py` を読みます。準備の後、次の処理を10回繰り返します。

```python
distance = read_distance(h)
if distance is None:
    print("測れません")
else:
    print(distance, "cm")
time.sleep(0.5)
```

- **定義**：`hcsr04.py` の `def read_distance(h):` は、距離を1回測る処理に名前を付けます。定義しただけでは測りません。
- **呼び出し**：`read_distance(h)` と書くと、その処理が動きます。
- **戻り値**：`return` で結果を返します。`distance = read_distance(h)` は返ってきた距離を変数に入れます。
- **引数**：関数へ渡す値です。`time.sleep(0.5)` の `0.5` は「待つ秒数」。`read_distance(h)` には `setup_gpio()` が返した `h`（GPIOを使うための番号）を渡します。

測れないときは数値の代わりに `None`（値がない）を返します。`0 cm` とは別です。`02_distance_led.py` は `None` なら消灯し、距離が10 cm未満のときだけ点灯します。演習は20 cm未満にします。判定には表示と同じ小数1桁の距離を使います。

## 距離の測り方（関数の中身）

次に **同じフォルダの `hcsr04.py` を開き、`def read_distance(h):` を読みます**。01/02の `from hcsr04 import ...` は、このファイルで定義した関数を使うための行です。準備は `setup_gpio`、測定は `read_distance`、終了は `close_gpio` の3つです。

1. TRIGを10マイクロ秒だけHighにして、測定の合図を送ります。
2. ECHOがHighになった時刻 `start` と、Lowに戻った時刻 `end` を記録します。**ECHOがHighだった時間** が音の往復時間です。
3. `return round((end - start) * 34300 / 2, 1)` で距離を返します。音速34300 cm/秒を掛け、往復なので2で割り、小数1桁にします。

`time.monotonic()` は経過時間を測る時計です。`deadline` は待つ期限で、High待ち・Low待ちがそれぞれ0.03秒を超えたら `None` を返します。測定前からECHOがHighの場合も `None` にします。成功・失敗のどちらでも次まで0.5秒待ちます。

`finally` は正常終了・エラー・Ctrl+Cの後片付けです。`close_gpio` が出力をLowにし、`gpiochip_close` で入力を含めてピンを解放します。ECHOは入力なので書き込みません。

## 超音波の実行と教材の更新

自分のアカウントでSSH接続し、上の準備でコピーした後に実行します。Sambaでは自分のファイルを編集し、実行はSSHの画面で行います。

```sh
source ~/venv/bin/activate
cd ~/seminar2/students/$USER/lesson03/ultrasonic
python3 01_distance_read.py
python3 02_distance_led.py
```

両方とも10回で終了し、途中で止めるときはCtrl+Cです。演習は `near_led.py` にwhile文で5回測るコードを書きます。

すでにコピー済みの場合、`git pull` で原本は更新されても `cp -n` は自分のファイルを上書きしません。自分の変更と見比べて使ってください。新しい例と補助ファイルを別のフォルダへコピーすれば、元のコードや演習の解答を残せます。

```sh
cd ~/seminar2
git pull
mkdir -p students/$USER/lesson03/ultrasonic_updated
cp -n lesson03/ultrasonic/*.py students/$USER/lesson03/ultrasonic_updated/
cd students/$USER/lesson03/ultrasonic_updated
python3 01_distance_read.py
```

`hcsr04.py` も01/02と同じフォルダに必要です。更新用フォルダがすでにあれば、さらに別名を使ってください。演習の解答は上書きしません。

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

## 関数を使ってモーターを動かす

まず `01_motor_on_off.py` を読みます。超音波と同じく、`setup_gpio` で準備し、`finally` の `close_gpio` で片付けます。

```python
h = setup_gpio(pins)
try:
    set_speed(h, in1, in2, 100)
    time.sleep(seconds)
finally:
    close_gpio(h, pins)
```

- **定義**：同じフォルダの **`motor_gpio.py` を開き、`def set_speed(h, in1, in2, speed):` を読みます**。`from motor_gpio import ...` はその関数を使うための行です。
- **呼び出しと引数**：`set_speed(h, in1, in2, 50)` は、使うGPIOの番号 `h`、モーターの2本のピン、速さ50%を渡して回します。速さ0は停止、100はHigh、途中はPWMです。
- **戻り値**：`setup_gpio(pins)` は準備したGPIOを使うための番号を返し、`h`に入れます。`set_speed`・`stop_motor`・`close_gpio` は動作を行う関数なので、結果を変数に入れません。
- **止める**：`stop_motor(h, pins)` はPWMを0にして全ピンをLowにします。`close_gpio(h, pins)` は停止してGPIOを解放します。

`pins = [in1, in2]` は使うピンのリストです。両輪の演習では4本を入れます。A側は17/18、B側は22/19です。番号や配線は上の表で確認してください。

## 向きとPWMの仕組み

`set_speed` は反対側のPWMを0にしてLowにしてから、回す側へ出力します。正転は `set_speed(h, in1, in2, 100)`、逆転は2本の順番を入れ替えた `set_speed(h, in2, in1, 100)` です。

**逆転前は `stop_motor` で止め、`time.sleep(1)` で1秒待ちます。** `02_motor_reverse.py` で、その順番を確認してください。急に逆転させるとモーターと電池に大きな電流が流れます。

`motor_gpio.py` の `lgpio.tx_pwm(h, in1, 1000, speed)` がPWMの出力です。第2回のLEDと同じく出力の割合を変え、モーターの速さを変えます。停止時はPWMを0にするだけでなく、全ピンをLowにします。100%はPWMではなくHighを出します。

`setup_gpio` にはSIGHUP・SIGTERMを受けたときも `finally` へ進む処理があります。Ctrl+C、正常終了、エラーでも停止・解放を試みます。SSHが切れた瞬間に必ず信号が届くとは限らないため、回す時間を短くし、異常時はモーター電源を切ってください。

## 実行のしかた

自分のアカウントでSSH接続し、上の準備でコピーしてから実行します。Sambaでは編集し、実行はSSHの画面で行います。

```sh
source ~/venv/bin/activate
cd ~/seminar2/students/$USER/lesson03/motor
python3 01_motor_on_off.py  # A側を2秒回す。まずsecondsを1にして車輪を浮かせる
python3 03_motor_pwm.py    # 50%で2秒回す
```

速さ・秒数・使う側はファイルの先頭の変数で変えます。回す時間は合計10秒以内です。04は最大速度を0〜100の10刻みにし、1段階0.1秒で加速・減速します。待ち時間を長くしすぎないでください。実行用のコマンドに引数はありません。

すでにコピー済みのコードを残して新しい例を試す場合は、別フォルダへコピーします。

```sh
cd ~/seminar2
git pull
mkdir -p students/$USER/lesson03/motor_updated
cp -n lesson03/motor/*.py students/$USER/lesson03/motor_updated/
cd students/$USER/lesson03/motor_updated
```

`motor_gpio.py` も同じフォルダに必要です。更新用フォルダがすでにあれば、さらに別名にします。`cp -n` は既存の解答を上書きしません。

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
| 「測れません」が続く | 物の距離・向き・反射を確認。Ctrl+Cで止め、VCC 5 V・共通GND・TRIG/ECHO・分圧を先生と確認 |
| 距離が不安定 | センサの正面に平らな物を置く。他のプログラムを止め、1人ずつ測る |
| 回らない、うなるだけ | モーター電源スイッチ、電池。`03_motor_pwm.py` の `speed` を 60 以上にする(低すぎると回らない) |
| 正転のはずが逆に回る | モーター線の差し込みを逆にする。またはコードの `in1` と `in2` を入れ替える |
| `GPIO busy` | 前のプログラムが残っている。`ps aux \| grep python` → `kill 番号` |
| 止まらない | `Ctrl + C`。それでもだめなら電源スイッチ OFF。原因は `finally` が無いか、ループに上限が無いこと |
| 両方 High にしてしまった | ブレーキ状態(壊れない)。片方を Low にする |
| `ModuleNotFoundError: lgpio` | ラズパイ以外で実行している。ラズパイで実行する |
