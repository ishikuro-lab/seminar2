# 第 2 回 — LED を光らせる

今回はロボット基板を使わず、**ブレッドボード**で配線して Raspberry Pi の GPIO の使い方を学びます。

| 順番 | 内容 | スクリプト |
|---|---|---|
| 1 | LED を点ける・消す | `01_led_on.py` |
| 2 | LED を点滅させる(ループ) | `02_led_blink.py` |
| 3 | LED の明るさを変える(PWM) | `03_led_pwm.py`、`04_led_fade.py` |
| 4 | 演習 | `excersises/01_led_*.py`〜`05_led_*.py`(自分のフォルダにコピーして解く) |

超音波センサで距離を測る教材は第 3 回([lesson03/README.md](../lesson03/README.md))に移りました。

## 準備

```
cd ~/seminar2
git pull
mkdir -p students/$USER/lesson02
cp -n lesson02/excersises/*.py students/$USER/lesson02/
cd students/$USER/lesson02
```

`$USER` は自分のユーザー名(姓)に置き換わります。先生の教材(`lesson02/`)と問題(`lesson02/excersises/`)は編集せず、自分のフォルダ `students/自分のユーザー名/lesson02/` にコピーしたものを使います。`cp -n` は、すでにあるファイルを上書きしないので、2 回目に打っても自分の答えは消えません。

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
| 3.3 V | — | 1 または 17 |
| GND | — | 6, 9, 14, 20, 25, 30, 34, 39 のどれか |

## 配線: LED

```
GPIO12 (物理32) ──[抵抗 330Ω]──>|── GND (物理34)
                              LED
```

- LED には向きがあります。足の長い方(アノード、+)を抵抗側、短い方(カソード、−)を GND に。
- 抵抗は電流を抑えるために必ず入れます(無いと LED や GPIO が壊れます)。330 Ω で約 5 mA 流れます。
- 配線は **ラズパイの電源を切ってから**、または最低限プログラムを止めてから触ります。

## プログラムの基本形

独自の補助関数や共通ファイルは使わず、`lgpio` と `time` の関数を直接呼びます。GPIOの準備・操作・後片付けもコードで確認します。

```python
import lgpio
import time

h = lgpio.gpiochip_open(0)  # GPIOを使う準備
try:
    lgpio.gpio_claim_output(h, 12, 0)  # 出力に設定
    lgpio.gpio_write(h, 12, 1)         # 点灯
    time.sleep(3)
finally:
    lgpio.gpio_write(h, 12, 0)  # 途中で止めても必ず消灯
    lgpio.gpiochip_close(h)     # ピンを解放
```

上は準備から解放までの流れです。教材の全文には、`Ctrl+C` で止めたときの処理(`except KeyboardInterrupt`)も記載しています。

| 操作 | ライブラリの関数 |
|---|---|
| GPIOを使う準備 | `lgpio.gpiochip_open(0)` |
| 出力に設定 | `lgpio.gpio_claim_output(h, 12, 0)` |
| 点灯 | `lgpio.gpio_write(h, 12, 1)` |
| 消灯 | `lgpio.gpio_write(h, 12, 0)` |
| 0.5秒待つ | `time.sleep(0.5)` |
| PWMを出す | `lgpio.tx_pwm(h, 12, 1000, 50)` |
| ピンを解放 | `lgpio.gpiochip_close(h)` |

`h` は開いたGPIOチップを指定する値です。`try` の中が終わったときも、エラーや中断が起きたときも、`finally` の終了処理を実行します。

## 実行のしかた

```bash
cd ~/seminar2/lesson02
python3 01_led_on.py
python3 02_led_blink.py
```

ピン番号・点灯時間・回数を変えて試してください。途中で止めるときは `Ctrl+C` です。模擬GPIOでの検証と実機確認は別です。実機では配線を先生と確認してから実行します。

## 各スクリプト

| ファイル | やること | 学ぶこと |
|---|---|---|
| `01_led_on.py` | 3 秒点灯して消す | 点灯・待つ・消灯 |
| `02_led_blink.py` | 0.5 秒おきに10回点滅 | `for` と `time.sleep`、Ctrl+C |
| `03_led_pwm.py` | 明るさを 0〜100 % で固定 | PWM(高速に点滅させて明るさを変える) |
| `04_led_fade.py` | ゆっくり明るく → 暗くを3往復 | `for` ループで PWM の値を変える |

## PWM とは

PWM(Pulse Width Modulation)は、High と Low を高速に切り替え、High の時間の割合(デューティ比)で平均の電圧を変える方法です。1 秒に 1000 回切り替えると目には点滅が見えず、明るさが変わって見えます。

```
デューティ比 25 %:  ‾|___|‾|___|‾|___   → 暗い
デューティ比 75 %:  ‾‾‾|_|‾‾‾|_|‾‾‾|_  → 明るい
```

`lgpio.tx_pwm(h, 12, 1000, 50)` で「1000 Hz、デューティ比 50 %」になります。第 3 回のモーターの速度制御でも同じ仕組みを使います。

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| LED が点かない | 向き(長い足が抵抗側)、GPIO 番号、GND に戻っているか |
| `GPIO busy` | 前のプログラムが残っている。`ps aux \| grep python` → `kill 番号` |
| `ModuleNotFoundError: lgpio` | ラズパイ以外で実行している。ラズパイで実行する |


教材コードは `01_`〜`04_` の番号順に使います。補助ファイルは不要です。

## 練習問題

`excersises/` にLEDの練習問題が5問あります。「準備」で自分のフォルダにコピーしたものを解きます。練習は `cd ~/seminar2/students/$USER/lesson02` の後、例えば `python3 01_led_five_seconds.py` で実行します。問題文と指示は各 Python ファイルのコメントにあります。コメントの下に自分でコードを書いてから実行してください。

練習問題は01〜05の順に進めます。順番に実行・`for`・`while`・`if`を段階的に学びます。ループは関数ではなく、処理を繰り返す構文です。
