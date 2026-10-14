# seminar2 — 総合教育セミナーⅡ(2026 年度秋)

Raspberry Pi Zero 2 W とモーター基板(DRV8833)でロボットを動かす授業の教材と、班ごとの作業場所です。

- 教材は先生が `main` ブランチに置きます。
- 班の作業は `group-a` 〜 `group-d` ブランチで行います。自分の班のブランチだけを使ってください。
- 先生が教材を更新すると、自動で各班のブランチにも配られます。

## はじめにやること(初回)

1. GitHub アカウントを作る(持っていなければ)。ユーザー名を先生に伝えると、このリポジトリへの招待が届くので承諾する。
2. ラズパイにログインして、自分のアカウントで GitHub に認証する。手順は [docs/raspi-setup.md](docs/raspi-setup.md)。
3. 自分の班のブランチにいることを確認する。

   ```
   cd ~/seminar2
   git branch
   ```

   `*` が付いている行が今のブランチです(例: `* group-a`)。

## 毎回の授業の流れ

```
cd ~/seminar2
git pull                      # 先生の新しい教材と、班の仲間の変更を取り込む
# lesson02/work/ の下で作業する
git add lesson02/work/
git commit -m "何をしたか短く書く"
git push                      # 自分の班のブランチに送る
```

くわしくは [docs/branch-workflow.md](docs/branch-workflow.md) を見てください。

## フォルダの役割

| フォルダ | 内容 | 編集 |
|---|---|---|
| `lesson02/` | 第2回の教材と演習 | 教材は読むだけ |
| `motor/` | モーターを回すサンプル([motor/README.md](motor/README.md)) | コピーして使う |
| `lesson02/work/` | 班の作業場所。ここに自分たちのコードを置く | する |
| `docs/` | Git の基本、ラズパイの使い方、トラブル対処 | 読む |
| `scripts/` | ラズパイの初期設定用 | 触らない |

## 安全のルール(モーター)

- モーターを回す前に **車輪を浮かせる**。床に置くのは直進のテストが済んでから。
- 新しいコードはまず `--dry-run` で確認する(GPIO に触らず、出す値だけ表示します)。
- 止めるときは `Ctrl + C`。SSH が切れても全ピンが Low になるように書いてあります。

## Git と GitHub がはじめての人へ

[docs/git-basics.md](docs/git-basics.md) に、用語とこの授業で使うコマンドをまとめてあります。最初に一度読んでください。

## AI を使う場合

AI(Claude、ChatGPT、Gemini、GitHub Copilot など)を使ってもかまいません。使わなくても授業は進められます。使うときの注意と始め方は [docs/ai-guide.md](docs/ai-guide.md) にあります。

## 困ったとき

まず [docs/troubleshooting.md](docs/troubleshooting.md) を見てください。症状から引けるようになっています。

- PC からつながらない: 30 秒待ってもう一度。だめならラズパイの画面で `ping -c 3 192.168.2.1`。
- `git push` が拒否された: `main` に push しようとしていないか `git branch` で確認する。
- `CONFLICT` と出た: [docs/branch-workflow.md](docs/branch-workflow.md) の「衝突したとき」。直せなければ先生を呼ぶ。

## PDF版の案内

`docs/` の各説明には、同名のPDF版があります。

- [ラズパイの接続・準備（PDF）](docs/raspi-setup.pdf)
- [Gitの基本（PDF）](docs/git-basics.pdf)
- [班のブランチと作業手順（PDF）](docs/branch-workflow.pdf)
- [AIを使う場合（PDF）](docs/ai-guide.pdf)
- [困ったとき（PDF）](docs/troubleshooting.pdf)
