# HC-SR04の仕組みを読むファイル。まず01/02の呼び出しから読みましょう。
import lgpio
import time

trig_pin = 23  # BCM23（物理16）
echo_pin = 24  # BCM24（物理18）。1kΩ/1.5kΩで分圧する


def setup_gpio(led_pin=None):  # 引数：LEDを使うときだけ、そのGPIO番号を渡す
    h = lgpio.gpiochip_open(0)
    try:
        lgpio.gpio_claim_output(h, trig_pin, 0)
        lgpio.gpio_claim_input(h, echo_pin)
        if led_pin is not None:
            lgpio.gpio_claim_output(h, led_pin, 0)
        time.sleep(0.1)  # 信号が落ち着くのを待つ
        return h  # 戻り値：準備したGPIOを使うための番号
    except BaseException:  # 準備中のエラーやCtrl+Cでも解放する
        lgpio.gpiochip_close(h)
        raise


def read_distance(h):  # 定義：距離を1回測る処理に名前を付ける
    # 戻り値は距離(cm)。測れないときは None（値がない）。
    if lgpio.gpio_read(h, echo_pin) == 1:
        return None  # 測定前からHighなら、今回は測らない
    lgpio.gpio_write(h, trig_pin, 1)
    time.sleep(0.00001)  # 10マイクロ秒の合図
    lgpio.gpio_write(h, trig_pin, 0)

    deadline = time.monotonic() + 0.03  # 待つのは最大0.03秒
    while lgpio.gpio_read(h, echo_pin) == 0:
        if time.monotonic() >= deadline:
            return None
    start = time.monotonic()  # ECHOがHighになった時刻

    deadline = start + 0.03
    while lgpio.gpio_read(h, echo_pin) == 1:
        if time.monotonic() >= deadline:
            return None
    end = time.monotonic()  # ECHOがLowに戻った時刻
    return round((end - start) * 34300 / 2, 1)  # 往復の時間→片道のcm



def close_gpio(h, led_pin=None):  # 終了：出力をLowに戻してGPIOを解放する
    try:
        if led_pin is not None:
            lgpio.gpio_write(h, led_pin, 0)
        lgpio.gpio_write(h, trig_pin, 0)
    finally:
        lgpio.gpiochip_close(h)  # 書き込みでエラーが出ても解放する
