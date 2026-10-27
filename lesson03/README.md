# 第 3 回 — センサを読む

第 2 回のブレッドボードに **超音波距離センサ**(HC-SR04)を足して、物までの距離を測ります。

モーターを動かす教材は第 4 回([lesson04/README.md](../lesson04/README.md))に移りました。

| 順番 | 内容 | スクリプト |
|---|---|---|
| 1 | 超音波センサで距離を測る | `ultrasonic/01_distance_read.py` |
| 2 | 距離に応じて LED を点ける | `ultrasonic/02_distance_led.py` |
| 3 | 演習(超音波) | [ultrasonic/excersises/](ultrasonic/excersises/) |

教材は `ultrasonic/`、演習は `ultrasonic/excersises/` にあります。

## 準備

```
cd ~/seminar2
git pull
mkdir -p students/$USER/lesson03/ultrasonic
cp -n lesson03/ultrasonic/*.py lesson03/ultrasonic/excersises/*.py students/$USER/lesson03/ultrasonic/
cd students/$USER/lesson03/ultrasonic
```

`$USER` は自分のユーザー名(姓)に置き換わります。`lesson03/` の教材と問題は直接編集せず、自分のフォルダにコピーしたものを使います。`cp -n` は、すでにあるファイルを上書きしないので、2 回目に打っても自分の答えは消えません。

---

## 今回使うピン

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

## 約束

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

## 各スクリプト

| ファイル | やること | 学ぶこと |
|---|---|---|
| `ultrasonic/01_distance_read.py` | 距離を cm で表示 | TRIG/ECHO、時間測定、距離計算 |
| `ultrasonic/02_distance_led.py` | 10 cmより近ければLED点灯 | `if` / `else` |

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| 「測れません」が続く | 物の距離・向き・反射を確認。Ctrl+Cで止め、VCC 5 V・共通GND・TRIG/ECHO・分圧を先生と確認 |
| 距離が不安定 | センサの正面に平らな物を置く。他のプログラムを止め、1人ずつ測る |
| `GPIO busy` | 前のプログラムが残っている。`ps aux \| grep python` → `kill 番号` |
| `ModuleNotFoundError: lgpio` | ラズパイ以外で実行している。ラズパイで実行する |
