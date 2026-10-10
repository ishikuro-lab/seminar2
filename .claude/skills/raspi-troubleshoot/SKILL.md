---
name: raspi-troubleshoot
description: 授業用ラズパイ(Zero 2 W、ユーザー seminar2)の SSH・Wi-Fi・GPIO busy・権限・GitHub 認証のトラブルを切り分ける手順。つながらない、動かない、エラーが出たときに使う。
---

# raspi-troubleshoot — ラズパイのトラブル切り分け

## 原則

- 受講生は `sudo` を使えない。`sudo` が要る対処はコマンドを示して先生に頼む。
- 1 つずつ確かめる。症状 → 確認コマンド → 対処 の順で進める。
- 直ったら「何をしたら直ったか」を `work/README.md` に 1 行残す。

## SSH がつながらない

| 確認 | コマンド(PC 側) | 対処 |
|---|---|---|
| ラズパイが起動しているか | 電源 LED、画面 | 電源を入れ直す |
| 名前解決できるか | `ping groupa.local` | だめなら IP で `ssh seminar2@192.168.x.x`。IP はラズパイで `hostname -I` |
| 同じ Wi-Fi か | PC の Wi-Fi 設定 | ラズパイと同じ SSID に接続 |
| ラズパイの Wi-Fi が落ちていないか | ラズパイで `nmcli device status` | `nmcli device disconnect wlan0; nmcli device connect wlan0`(sudo 不要、2 回必要なことがある) |

Wi-Fi の省電力オフは設定済みだが、それでも切れることがある。原因は未確定なので「省電力が原因」とは言わない。

## GPIO busy / lgpio のエラー

```
ps aux | grep -v grep | grep python
kill <PID>            # 残っているプログラムを止める
```

それでも出るときは `lgpio.gpiochip_open(0)` を別のプログラムが握っている。ログアウトして入り直す。最後の手段は先生に再起動を依頼(`sudo reboot`)。

## モーターが動かない

1. `python3 motor/motor_test.py --dry-run` で、出す値が表示されるか(コードの問題か配線の問題かを分ける)。
2. モーター電源スイッチ、電池の残量。
3. `--speed 0.6` 以上にして「うなるだけ」から脱するか。
4. 片側だけ `--motor A` / `--motor B` で切り分け。
5. コネクタの向き(逆だと逆転するだけ。`straight.py` の `FORWARD` か `--flip` で対応)。

## Git / GitHub

| 症状 | 原因 | 対処 |
|---|---|---|
| `GH013: Repository rule violations` | `main` に push した | `git branch` で確認、`git checkout group-x` |
| `Permission denied` / `403` | 認証が切れた、招待未承諾 | `gh auth status` → `gh auth login`。招待メールを承諾したか確認 |
| `fatal: not a git repository` | 場所が違う | `cd ~/seminar2` |
| `Your branch is behind` | 仲間が先に push した | `git pull` してから push |
| `CONFLICT` | 同じ場所を別々に編集 | `group-git-workflow` スキルの手順 |

## 権限・パッケージ

- `pip install` は `pip install --user パッケージ名`。`sudo pip` は使わない。
- `apt` は sudo が要るので先生に依頼。`lgpio` は最初から入っている。

## 先生に伝えるときの情報

- 班名、ラズパイのホスト名、いつから
- 実行したコマンドとエラーの全文(スクリーンショットより文字で)
- `uname -a`、`hostname -I`、`git branch`、`git status` の結果
