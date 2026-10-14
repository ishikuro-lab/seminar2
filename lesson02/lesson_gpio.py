"""第2回の共通処理。受講生はこのファイルを変更せずに使います。"""
import signal
import threading
import atexit
import time


class GPIO:
    """with の中で使った GPIO を、終了時に自動で片付ける。"""

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.handle = None
        self.outputs = set()
        self.inputs = set()
        self.signals = {}

    def __enter__(self):
        if not self.dry_run:
            import lgpio
            self.lgpio = lgpio
            self.handle = lgpio.gpiochip_open(0)
        if threading.current_thread() is threading.main_thread():
            for name in ("SIGHUP", "SIGTERM"):
                number = getattr(signal, name, None)
                if number is not None:
                    self.signals[number] = signal.signal(number, self._stop)
        return self

    def _stop(self, number, frame):
        self.__exit__(None, None, None)
        raise SystemExit("接続または実行が終了しました")

    def _output(self, pin):
        if pin in self.inputs:
            raise ValueError("入力に使っているピンは出力にできません")
        if pin not in self.outputs:
            if not self.dry_run:
                self.lgpio.gpio_claim_output(self.handle, pin, 0)
            self.outputs.add(pin)

    def on(self, pin):
        self.brightness(pin, 100)

    def off(self, pin):
        self.brightness(pin, 0)

    def brightness(self, pin, percent):
        if not 0 <= percent <= 100:
            raise ValueError("明るさは0〜100で指定してください")
        self._output(pin)
        if self.dry_run:
            print("GPIO", pin, "明るさ", percent, "%（模擬出力）")
        else:
            self.lgpio.tx_pwm(self.handle, pin, 1000, 0)
            if percent in (0, 100):
                self.lgpio.gpio_write(self.handle, pin, int(percent == 100))
            else:
                self.lgpio.tx_pwm(self.handle, pin, 1000, percent)

    def read(self, pin):
        if pin in self.outputs:
            raise ValueError("出力に使っているピンは入力にできません")
        if pin not in self.inputs:
            if not self.dry_run:
                self.lgpio.gpio_claim_input(self.handle, pin)
            self.inputs.add(pin)
        if self.dry_run:
            print("GPIO", pin, "模擬入力：0")
            return 0
        return self.lgpio.gpio_read(self.handle, pin)

    def __exit__(self, kind, value, traceback):
        try:
            if self.handle is not None:
                try:
                    for pin in self.outputs:
                        self.lgpio.tx_pwm(self.handle, pin, 1000, 0)
                        self.lgpio.gpio_write(self.handle, pin, 0)
                finally:
                    self.lgpio.gpiochip_close(self.handle)
                    self.handle = None
        finally:
            for number, handler in self.signals.items():
                signal.signal(number, handler)
        return kind is KeyboardInterrupt


# 初学者向けの操作。GPIO の準備は最初の操作時に自動で行う。
_gpio = None
_dry_run = False


def _call(method, *args):
    global _gpio
    try:
        if _gpio is None:
            _gpio = GPIO(dry_run=_dry_run)
            _gpio.__enter__()
        return getattr(_gpio, method)(*args)
    except BaseException:
        _cleanup()
        raise


def led_on(pin):
    _call("on", pin)


def led_off(pin):
    _call("off", pin)


def brightness(pin, percent):
    _call("brightness", pin, percent)


def read_sensor(pin):
    return _call("read", pin)


def sleep(seconds):
    try:
        time.sleep(seconds)
    except BaseException:
        _cleanup()
        raise


def _cleanup():
    """消灯し、ピンを解放する。何回呼んでもよい。"""
    global _gpio
    gpio, _gpio = _gpio, None
    if gpio is not None:
        gpio.__exit__(None, None, None)


def dry_run():
    """実機に触れず確認する。センサは模擬値0を返す。"""
    global _dry_run
    _cleanup()
    _dry_run = True


atexit.register(_cleanup)
