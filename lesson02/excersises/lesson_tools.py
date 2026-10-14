# 共通処理を読み込むためのファイル。編集しないでください。
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lesson_gpio import led_on, led_off, sleep, read_distance, dry_run
