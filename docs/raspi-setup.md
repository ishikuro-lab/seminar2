# ラズパイの使い方

班ごとに Raspberry Pi Zero 2 W が 1 台あります。ログイン名はどの班も `seminar2` です。

## 1. ラズパイにつなぐ(SSH)

同じ Wi-Fi につないだ PC から:

```
ssh seminar2@groupa.local        # 自分の班の名前に読み替える(groupa〜groupd)
```

パスワードは授業で伝えます。`.local` で見つからないときは、ラズパイの画面か先生に IP アドレスを聞いて `ssh seminar2@192.168.x.x` とします。

## 2. GitHub に自分のアカウントで認証する(初回だけ)

ラズパイには `gh`(GitHub CLI)が入っています。

```
gh auth login
```

質問には次のように答えます。

| 質問 | 答え |
|---|---|
| Where do you use GitHub? | GitHub.com |
| Preferred protocol | HTTPS |
| Authenticate Git with your GitHub credentials? | Yes |
| How would you like to authenticate? | Login with a web browser |

表示される 8 文字のコードをメモして、スマホか PC で https://github.com/login/device を開き、コードを入力して承認します。終わったら:

```
gh auth setup-git
git config --global user.name  "自分の名前(ローマ字可)"
git config --global user.email "GitHub に登録したメールアドレス"
```

これで `git push` が自分の名前で記録されます。班の仲間が別の人として push したいときは、その人が `gh auth login` をやり直します。

## 3. リポジトリの場所

```
cd ~/seminar2
git branch        # * group-a のように自分の班が表示されればOK
git pull
```

初回クローンは先生が済ませてあります。もし `~/seminar2` が無ければ:

```
git clone -b group-a https://github.com/ishikuro-lab/seminar2.git ~/seminar2
```

(`group-a` は自分の班に読み替え)

## 4. 第2回の教材を動かす

穴埋め練習は `lesson02/excersises/` にあります。各コードのコメントを読み、`___` を埋めて保存してから実行します。

```bash
cd ~/seminar2
mkdir -p lesson02/excersises
cd lesson02/excersises
python3 led_01_five_seconds.py
```

LED は GPIO12 → 抵抗330 Ω → LED → GND に接続します。先に [第2回の配線と説明](../lesson02/README.md) を確認してください。

## 5. ファイルの編集

- ラズパイ上で直接: `nano ~/seminar2/lesson02/excersises/led_01_five_seconds.py`(保存は `Ctrl+O`、終了は `Ctrl+X`)
- PC で編集して運ぶ: PC で clone → 編集 → `git push` → ラズパイで `git pull`。使い慣れたエディタで書きたいときはこちら。
- VS Code の Remote-SSH でラズパイのファイルを直接開くこともできます(重いときは PC 編集に切り替え)。

## トラブル対処

くわしくは [troubleshooting.md](troubleshooting.md)(症状から引ける一覧)。よくあるものだけ:

| 症状 | 対処 |
|---|---|
| `ssh` がつながらない | 30 秒待ってもう一度。だめならラズパイの画面で `ping -c 3 192.168.2.1` → `nmcli device disconnect wlan0 && nmcli device connect wlan0` |
| `Name or service not known` | ラズパイで `hostname -I` を見て `ssh seminar2@192.168.x.x` |
| `GPIO busy` と出る | 前のプログラムが残っています。`ps aux \| grep python` で見つけて `kill <番号>` |
| `git push` が `GH013` で拒否 | `main` に push しようとしています。`git branch` で確認し、`git checkout group-a` に戻る |
| `sudo` が必要と言われた | 受講生は使えません。先生を呼んでください |
