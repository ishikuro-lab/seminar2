# 第 2 回 — LED を光らせる・センサを読む

今回はロボット基板を使わず、**ブレッドボード**で配線して Raspberry Pi の GPIO の使い方を学びます。

| 順番 | 内容 | スクリプト |
|---|---|---|
| 1 | LED を点ける・消す | `led_on.py` |
| 2 | LED を点滅させる(ループ) | `led_blink.py` |
| 3 | LED の明るさを変える(PWM) | `led_pwm.py`、`led_fade.py` |
| 4 | 演習① | [exercises.md](exercises.md) |
| 5 | ライントレースセンサを読む(1 ch) | `sensor_read.py` |
| 6 | 8 ch まとめて読む | `sensor_8ch.py` |
| 7 | 演習② | [exercises.md](exercises.md) |

## 準備

```
cd ~/seminar2
git pull
cp -r materials/lesson02 work/lesson02    # 自分の班の作業場所にコピーしてから編集する
cd work/lesson02
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
| センサ OUT1 | GPIO4 | 7 |
| センサ OUT2〜8 | GPIO5, 6, 16, 20, 21, 23, 24 | 29, 31, 36, 38, 40, 16, 18 |
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

## 配線 2: ライントレースセンサ(AE-NJL5901AR-8ch)

秋月電子のライントレース用センサ基板です。赤外線を出して反射を見るセンサ(フォトリフレクタ)が 8 個並んでいます。

- 白い床(よく反射する) → 出力は **Low(0)**
- 黒い線(反射しない)や何も無い → 出力は **High(1)**
- 各センサの横の半固定抵抗(VR)で感度を調整できます。基板上の LED が点くと「反射を検出」です。

| センサ基板 CN1 | つなぐ先 |
|---|---|
| OUT1 | GPIO4(物理 7) |
| OUT2 | GPIO5(物理 29) |
| OUT3 | GPIO6(物理 31) |
| OUT4 | GPIO16(物理 36) |
| OUT5 | GPIO20(物理 38) |
| OUT6 | GPIO21(物理 40) |
| OUT7 | GPIO23(物理 16) |
| OUT8 | GPIO24(物理 18) |
| VCC(+) | **3.3 V(物理 1)** |
| GND | GND(物理 9) |

**重要**: このセンサ基板の説明書には電源 5 V と書いてありますが、**3.3 V につないでください**。5 V で動かすと出力が 3.3 V を超え、Raspberry Pi の GPIO が壊れます。3.3 V でも動きます(感度が少し下がるので VR で調整します)。CN1 の端子の並びは基板のシルク印刷で確認してください。

まずは OUT1 だけつないで `sensor_read.py` を試し、動いたら 8 本つなぎます。

## プログラムの基本形

この回のプログラムは全部、次の形をしています。

```python
import lgpio                      # GPIO を操作するライブラリ(ラズパイに最初から入っている)

h = lgpio.gpiochip_open(0)        # GPIO を使う準備(0 番のチップ = 40 ピン)
lgpio.gpio_claim_output(h, 12, 0) # GPIO12 を出力にして、最初は Low(0)
try:
    lgpio.gpio_write(h, 12, 1)    # High にする(LED 点灯)
    ...
finally:
    lgpio.gpio_write(h, 12, 0)    # 終わるときは必ず Low に戻す
    lgpio.gpiochip_close(h)       # 後片付け
```

- `try` と `finally`: 途中でエラーが出ても、`Ctrl + C` で止めても、`finally` の中は必ず実行されます。LED やモーターを「点けっぱなし」にしないための書き方です。
- ライブラリ: よく使う機能をまとめたもの。`import` で読み込んで使います。

## 実行のしかた

```
python3 led_on.py             # 既定(GPIO12)で実行
python3 led_on.py --pin 21    # 別のピンで試す(配線も変える)
python3 led_on.py --help      # 使える引数を見る
```

`Ctrl + C` で止められます。

## 各スクリプト

| ファイル | やること | 学ぶこと |
|---|---|---|
| `led_on.py` | 3 秒点灯して消す | 出力の基本、try/finally |
| `led_blink.py` | 0.5 秒おきに点滅 | `while True` と `time.sleep`、Ctrl+C |
| `led_pwm.py` | 明るさを 0〜100 % で固定 | PWM(高速に点滅させて明るさを変える) |
| `led_fade.py` | ゆっくり明るく → 暗く | `for` ループで PWM の値を変える |
| `sensor_read.py` | センサ 1 ch を読み続ける | 入力の基本、`gpio_read` |
| `sensor_8ch.py` | 8 ch を一行で表示 | リストとループ、`--pins` で番号を変える |

## PWM とは

PWM(Pulse Width Modulation)は、High と Low を高速に切り替え、High の時間の割合(デューティ比)で平均の電圧を変える方法です。1 秒に 1000 回切り替えると目には点滅が見えず、明るさが変わって見えます。

```
デューティ比 25 %:  ‾|___|‾|___|‾|___   → 暗い
デューティ比 75 %:  ‾‾‾|_|‾‾‾|_|‾‾‾|_  → 明るい
```

`lgpio.tx_pwm(h, pin, 1000, 50)` で「1000 Hz、デューティ比 50 %」になります。第 3 回のモーターの速度制御でも同じ仕組みを使います。

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| LED が点かない | 向き(長い足が抵抗側)、GPIO 番号、GND に戻っているか |
| `GPIO busy` | 前のプログラムが残っている。`ps aux \| grep python` → `kill 番号` |
| `ModuleNotFoundError: lgpio` | ラズパイ以外で実行している。ラズパイで実行する |
| センサがずっと 1(または 0) | 3.3 V と GND を確認。VR を回して感度を調整。床との距離は 5 mm 前後 |
| センサ基板の LED が全部点きっぱなし | 感度が高すぎる。VR を逆に回す |
