# 第 2 回 — LED を光らせる・センサを読む

今回はロボット基板を使わず、**ブレッドボード**で配線して Raspberry Pi の GPIO の使い方を学びます。

| 順番 | 内容 | スクリプト |
|---|---|---|
| 1 | LED を点ける・消す | `01_led_on.py` |
| 2 | LED を点滅させる(ループ) | `02_led_blink.py` |
| 3 | LED の明るさを変える(PWM) | `03_led_pwm.py`、`04_led_fade.py` |
| 4 | 演習① | `excersises/01_led_*.py`〜`05_led_*.py` |
| 5 | 超音波センサで距離を測る | `05_distance_read.py` |
| 6 | 距離に応じて LED を点ける | `06_distance_led.py` |
| 7 | 演習② | `excersises/06_ultrasonic_*.py`〜`10_ultrasonic_*.py` |

## 準備

```
cd ~/seminar2
git pull
mkdir -p lesson02/excersises
cd lesson02/excersises
```

## GPIO とは

Raspberry Pi の端にある 40 本のピンのうち、プログラムから「電圧を出す(出力)」「電圧を読む(入力)」ができるピンを GPIO(General Purpose Input/Output)と呼びます。

- 出力: High = 3.3 V、Low = 0 V。LED を点けたり消したりできる。
- 入力: ピンの電圧が高ければ 1(High)、低ければ 0(Low)として読める。
- 番号は **GPIO 番号**(BCM 番号)で指定します。ピンの物理的な位置(1〜40)とは別の番号です。

```
      3.3V  (1) (2)  5V
     GPIO2  (3) (4)  5V
     GPIO3  (5) (6)  GND
     GPIO4  (7) (8)  GPIO14
       GND  (9) (10) GPIO15
    GPIO17 (11) (12) GPIO18
    GPIO27 (13) (14) GND
    GPIO22 (15) (16) GPIO23
      3.3V (17) (18) GPIO24
    GPIO10 (19) (20) GND
     GPIO9 (21) (22) GPIO25
    GPIO11 (23) (24) GPIO8
       GND (25) (26) GPIO7
     GPIO0 (27) (28) GPIO1
     GPIO5 (29) (30) GND
     GPIO6 (31) (32) GPIO12
    GPIO13 (33) (34) GND
    GPIO19 (35) (36) GPIO16
    GPIO26 (37) (38) GPIO20
       GND (39) (40) GPIO21
```

(基板の端子側から見た配置。ラズパイの SD カード側が 1・2 番)

今回使うピン:

| 用途 | GPIO | 物理ピン |
|---|---|---|
| LED | GPIO12 | 32 |
| 超音波センサ TRIG | GPIO23 | 16 |
| 超音波センサ ECHO（分圧後） | GPIO24 | 18 |
| 超音波センサ VCC（5 V） | — | 2 または 4 |
| 3.3 V | — | 1 または 17 |
| GND | — | 6, 9, 14, 20, 25, 30, 34, 39 のどれか |

## 配線 1: LED

```
GPIO12 (物理32) ──[抵抗 330Ω]──>|── GND (物理34)
                              LED
```

- LED には向きがあります。足の長い方(アノード、+)を抵抗側、短い方(カソード、−)を GND に。
- 抵抗は電流を抑えるために必ず入れます(無いと LED や GPIO が壊れます)。330 Ω で約 5 mA 流れます。
- 配線は **ラズパイの電源を切ってから**、または最低限プログラムを止めてから触ります。

## 配線 2: 超音波距離センサ（HC-SR04、5 V版）

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

`05_distance_read.py` を実行し、まず定規で10 / 20 / 30 cmに物を置いて表示を比べます。測定できないときは「測れません」と表示します。次に `06_distance_led.py` で、10 cmより近いときにLEDが点くことを確認します。

距離は目安です。Pythonの処理時間や反射する物によって値が揺れることがあります。実機での精度は授業前に確認してください。

参考：[HC-SR04データシート](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)、[Raspberry PiのGPIO仕様](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)

## プログラムの基本形

プログラムは上から順に実行します。GPIO の準備と後片付けは、同じフォルダの `lesson_gpio.py` にまとめています。この共通ファイルは編集せず、教材・演習のファイルと一緒に置いてください。中では `lgpio` を使います。

```python
from lesson_gpio import led_on, led_off, sleep

led_on(12)   # GPIO12 の LED を点ける
sleep(3)     # 3秒待つ
led_off(12)  # 消す
```

最初の `import` は道具の読み込みです。その下に、やりたい操作を順番に書きます。

| 操作 | 書き方 |
|---|---|
| LED を点ける | `led_on(12)` |
| LED を消す | `led_off(12)` |
| 0.5秒待つ | `sleep(0.5)` |
| PWM のデューティ比を50 %にする | `brightness(12, 50)` |
| 距離を測る（cm） | `distance = read_distance()` |
| 読んだ値を表示する | `print(value)` |

準備は最初の操作時に自動で行います。LED を点けたら最後に `led_off()` で消します。プログラム終了時のGPIO解放は共通ファイルが行います。繰り返すプログラムを `Ctrl+C` で止めた場合も、共通の操作処理で後片付けします。終了時に `KeyboardInterrupt` と表示されても、中断によるものです。

## 実行のしかた

```
cd ~/seminar2/lesson02
python3 01_led_on.py
python3 02_led_blink.py
python3 03_led_pwm.py
```

Thonny では、ラズパイ側の `lesson_gpio.py` と同じフォルダに教材・演習を保存して実行します。ターミナルでは `Ctrl+C` で止められます。

ピンを変えるときは `led_on(12)` などの番号と配線を変えます。点滅間隔は `sleep(0.5)` の数字、明るさは `brightness(12, 50)` の2つ目の数字を変えて試してください。

まず GPIO に触れずに確認するときは、`import` の下に次の2行を追加します。PC でも動き、模擬出力を画面に表示します。超音波センサは模擬距離20 cmを返します。本番では追加した2行を外します。

```python
from lesson_gpio import dry_run
dry_run()
```

## 各スクリプト

| ファイル | やること | 学ぶこと |
|---|---|---|
| `01_led_on.py` | 3 秒点灯して消す | 点灯・待つ・消灯 |
| `02_led_blink.py` | 0.5 秒おきに点滅 | `while True` と `sleep`、Ctrl+C |
| `03_led_pwm.py` | 明るさを 0〜100 % で固定 | PWM(高速に点滅させて明るさを変える) |
| `04_led_fade.py` | ゆっくり明るく → 暗く | `for` ループで PWM の値を変える |
| `05_distance_read.py` | 距離を cm で表示 | `read_distance`、`print`、繰り返し |
| `06_distance_led.py` | 10 cmより近ければLED点灯 | `if` / `elif` / `else` |

## PWM とは

PWM(Pulse Width Modulation)は、High と Low を高速に切り替え、High の時間の割合(デューティ比)で平均の電圧を変える方法です。1 秒に 1000 回切り替えると目には点滅が見えず、明るさが変わって見えます。

```
デューティ比 25 %:  ‾|___|‾|___|‾|___   → 暗い
デューティ比 75 %:  ‾‾‾|_|‾‾‾|_|‾‾‾|_  → 明るい
```

`brightness(12, 50)` で「1000 Hz、デューティ比 50 %」になります。第 3 回のモーターの速度制御でも同じ仕組みを使います。

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| LED が点かない | 向き(長い足が抵抗側)、GPIO 番号、GND に戻っているか |
| `GPIO busy` | 前のプログラムが残っている。`ps aux \| grep python` → `kill 番号` |
| `ModuleNotFoundError: lgpio` | ラズパイ以外で実行している。ラズパイで実行する |
| 「測れません」と出る | VCCが5 Vか、GNDが共通か、TRIG/ECHOが逆でないか、ECHOの分圧を先生と確認 |
| 距離が不安定 | センサの正面に平らな物を置く。他のプログラムを止め、1人ずつ測る |


教材コードは `01_`〜`06_` の番号順に使います。`lesson_gpio.py` は読み込む共通ファイルなので、名前を変えずに一緒にコピーしてください。

## 穴埋め練習

`excersises/` に LED 5問と超音波センサ5問があります。練習は `cd ~/seminar2/lesson02/excersises` の後、例えば `python3 01_led_five_seconds.py` で実行します。問題文と指示は各 Python ファイルのコメントにあります。`___` を埋めてから実行してください。`lesson_tools.py` は共通処理の読み込み用なので編集しません。

練習問題は01〜10の順に進めます。LEDの01〜05、超音波センサの06〜10で、順番に実行・`for`・`while`・`if`を段階的に学びます。ループは関数ではなく、処理を繰り返す構文です。
