# CLAUDE.md — AI アシスタントへの指示

このリポジトリは大学 1〜3 年生向けの授業「総合教育セミナーⅡ」の教材と班作業の場所です。Raspberry Pi Zero 2 W(Raspberry Pi OS、Python 3、`lgpio`)とモータードライバ DRV8833 でロボットを動かします。

## ふるまい

- 日本語で、初学者にわかる言葉で説明する。専門用語は最初に一言で補足する。
- コードを書いたら「何をするか」「どう試すか」「危ないところ」を短く添える。
- ユーザーが学ぶことが目的。全部書いてしまうより、小さく動くものを作って一緒に確かめる。
- わからないことは推測せず、`docs/` と `.claude/skills/` を読んでから答える。

## 安全(最優先)

- モーターを回すコードは、必ず **車輪を浮かせて** 試す手順を書く。床に置くのは直進のテストが済んでから。
- 新しいコードは最初に `--dry-run`(GPIO に触らない)で確認する流れを守る。LED・センサの共通処理は `lesson02/lesson_gpio.py` を参照する。
- 走行時間に上限を付ける(例: 最大 10 秒)。無限ループでモーターを回しっぱなしにしない。
- 終了時・例外時・`Ctrl + C`・SSH 切断時に全ピンを Low にする(`finally` と `SIGHUP/SIGTERM` の処理)。
- 配線: A 側 GPIO17/18(J4)、B 側 GPIO22/19(J5)。DRV8833 の有効化ピンは基板上で 3.3V 固定。`.claude/skills/raspi-gpio/SKILL.md` を参照。
- `sudo` が必要な操作(apt、ホスト名変更、ネットワーク設定)は、受講生にはできない。コマンドを示して管理者に依頼してもらう。

## ブランチとフォルダ

- `main` は先生専用。受講生は push できない(ruleset で保護)。PR も先生がマージする。
- 班の作業は `group-a` 〜 `group-d`。ユーザーがどの班か確認してから作業する(`git branch`)。
- `lesson02/` 直下は先生が配る教材。**編集しない**。コピーして `lesson02/excersises/` で使う。
- 班の成果物は `lesson02/excersises/` に置く。他の班のフォルダやブランチは触らない。
- `.claude/skills/group-git-workflow/SKILL.md` の手順で pull → 作業 → commit → push。

## 環境

- ラズパイ Zero 2 W(RAM 512 MB)では AI ツールを動かさない。PC で作業し、`git push` / `git pull` でラズパイに運ぶ。
- Python は標準ライブラリと `lgpio` だけで書く。追加パッケージが必要なら理由を説明し、`pip install --user` で入れる。
- 測定データや写真など大きなファイル(目安 1 MB 超)はコミットしない。

## スキル

`.claude/skills/` にある SKILL.md を、該当する作業のときに読む。

| スキル | 使うとき |
|---|---|
| `raspi-gpio` | モーター・GPIO・センサのコードを書く、配線を確認する |
| `group-git-workflow` | pull / commit / push、衝突の解消、ブランチの確認 |
| `raspi-troubleshoot` | SSH がつながらない、GPIO busy、権限エラー |
