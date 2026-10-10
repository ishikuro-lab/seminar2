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
# work/ の下で作業する
git add work/
git commit -m "何をしたか短く書く"
git push                      # 自分の班のブランチに送る
```

くわしくは [docs/branch-workflow.md](docs/branch-workflow.md) を見てください。

## フォルダの役割

| フォルダ | 内容 | 編集 |
|---|---|---|
| `materials/` | 各回の教材(先生が追加) | しない(読むだけ) |
| `motor/` | モーターを回すサンプル([motor/README.md](motor/README.md)) | コピーして使う |
| `work/` | 班の作業場所。ここに自分たちのコードを置く | する |
| `docs/` | ラズパイの使い方、AI の使い方、トラブル対処 | 読む |
| `scripts/` | 先生用のスクリプト | 触らない |

## 安全のルール(モーター)

- モーターを回す前に **車輪を浮かせる**。床に置くのは直進のテストが済んでから。
- 新しいコードはまず `--dry-run` で確認する(GPIO に触らず、出す値だけ表示します)。
- 止めるときは `Ctrl + C`。SSH が切れても全ピンが Low になるように書いてあります。

## AI を使う

このリポジトリは AI コーディングツール(Claude Code、Codex、Gemini CLI、GitHub Copilot など)で開くことを前提にしています。

- 自分の PC にこのリポジトリを clone して AI ツールで開くと、[CLAUDE.md](CLAUDE.md) や [AGENTS.md](AGENTS.md) の指示を AI が読み、授業のルール(安全、ブランチ)を守って手伝ってくれます。
- `.claude/skills/` に、配線・Git の手順・トラブル対処の「スキル」があります。AI に「raspi-gpio スキルを読んで」のように頼めます。
- ブラウザの ChatGPT や Gemini に貼り付けて使う方法も [docs/ai-guide.md](docs/ai-guide.md) に書いてあります。
- ラズパイ Zero 2 W はメモリが少ないので、AI ツールは PC で動かし、できたコードをラズパイに push / pull で運びます。

## 困ったとき

- `git push` が拒否された: `main` に push しようとしていないか `git branch` で確認する。
- `CONFLICT` と出た: [docs/branch-workflow.md](docs/branch-workflow.md) の「衝突したとき」を見る。直せなければ先生を呼ぶ。
- ラズパイにつながらない、GPIO busy と出る: [docs/raspi-setup.md](docs/raspi-setup.md) の「トラブル対処」。

## 先生向け

- 教材の配布: `main` に push すると GitHub Actions(`.github/workflows/distribute.yml`)が `group-*` に merge します。手動は `scripts/distribute.sh`。
- 受講生の招待: `scripts/add-collaborators.sh ユーザー名...`。受講生は organization のメンバーにせず、このリポジトリだけの outside collaborator にします。
- 解答や未公開資料は private リポジトリ `ishikuro-lab/seminar2-dev` で扱います。
