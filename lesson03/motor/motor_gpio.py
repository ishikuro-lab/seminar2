# モーターの仕組みを読むファイル。実行例から各関数のdefへ進みましょう。
import lgpio
import signal


def setup_gpio(pins):  # 引数：使うGPIO番号のリスト。戻り値：GPIOを使うための番号
    # SSH切断や終了要求でも、実行例のfinallyへ進む
    signal.signal(signal.SIGHUP, signal.default_int_handler)
    signal.signal(signal.SIGTERM, signal.default_int_handler)
    h = lgpio.gpiochip_open(0)
    try:
        for pin in pins:
            lgpio.gpio_claim_output(h, pin, 0)  # 最初は全てLow
        return h
    except BaseException:  # 準備中のエラー・Ctrl+Cでも解放する
        lgpio.gpiochip_close(h)
        raise


def set_speed(h, in1, in2, speed):  # 動作：in1側へ速さ0〜100%で回す
    if not 0 <= speed <= 100:
        stop_motor(h, [in1, in2])
        raise ValueError("速さは0〜100にしてください")
    # 反対側を先に止める。両方がHighになる切替を避ける
    lgpio.tx_pwm(h, in2, 1000, 0)
    lgpio.gpio_write(h, in2, 0)
    if speed == 0:
        stop_motor(h, [in1, in2])
    elif speed == 100:
        lgpio.tx_pwm(h, in1, 1000, 0)
        lgpio.gpio_write(h, in1, 1)  # 100%はHighを出す
    else:
        lgpio.tx_pwm(h, in1, 1000, speed)  # PWM：1000Hzで出力の割合を変える


def stop_motor(h, pins):  # 動作：全ピンのPWMを止め、Lowにする
    error = None
    for pin in pins:
        try:
            lgpio.tx_pwm(h, pin, 1000, 0)
        except Exception as exc:
            error = exc
        try:
            lgpio.gpio_write(h, pin, 0)
        except Exception as exc:
            error = exc  # 1本で失敗しても、残りのピンも止める
    if error is not None:
        raise error


def close_gpio(h, pins):  # 終了：停止してからGPIOを解放する
    try:
        stop_motor(h, pins)
    finally:
        lgpio.gpiochip_close(h)  # 停止処理でエラーが出ても解放する
