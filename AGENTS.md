# AGENTS.md — Codex / Gemini CLI / GitHub Copilot などへの指示

Claude Code 向けの [CLAUDE.md](CLAUDE.md) と同じ内容です。どのツールでもこのファイルの指示に従ってください。

## このリポジトリ

大学 1〜3 年生向け授業「総合教育セミナーⅡ」の教材と班作業の場所。Raspberry Pi Zero 2 W(Raspberry Pi OS、Python 3、`lgpio`)とモータードライバ DRV8833 でロボットを動かす。

## ふるまい

- 日本語で、初学者にわかる言葉で説明する。専門用語は最初に一言で補足する。
- コードを書いたら「何をするか」「どう試すか」「危ないところ」を短く添える。
- ユーザーが学ぶことが目的。小さく動くものを作って一緒に確かめる。
- 推測で答えず、`docs/` と `.claude/skills/` を読んでから答える。

## 安全(最優先)

- モーターを回すコードは、必ず車輪を浮かせて試す手順を書く。
- 新しいコードは最初に `--dry-run`(GPIO に触らない)で確認する。LED・センサの共通処理は `lesson02/lesson_gpio.py` を参照する。
- 走行時間に上限を付ける。無限ループでモーターを回しっぱなしにしない。
- 終了時・例外時・`Ctrl + C`・SSH 切断時に全ピンを Low にする。
- 配線: A 側 GPIO17/18(J4)、B 側 GPIO22/19(J5)。有効化ピンは基板上で 3.3V 固定。
- `sudo` が必要な操作は受講生にはできない。コマンドを示して管理者に依頼してもらう。

## ブランチとフォルダ

- `main` は先生専用(受講生は push 不可)。班の作業は `group-a` 〜 `group-d`。
- `lesson02/` 直下の教材は編集しない。班の成果物は `lesson02/work/` に置く。
- 他の班のフォルダやブランチは触らない。

## 環境

- ラズパイでは AI ツールを動かさない。PC で作業し、`git push` / `git pull` で運ぶ。
- Python は標準ライブラリと `lgpio` だけで書く。
- 大きなファイル(目安 1 MB 超)はコミットしない。

## スキル(手順書)

`.claude/skills/<名前>/SKILL.md` に手順をまとめてある。該当する作業のときに読むこと。

- `.claude/skills/raspi-gpio/SKILL.md` — モーター・GPIO・センサのコードと配線
- `.claude/skills/group-git-workflow/SKILL.md` — pull / commit / push と衝突の解消
- `.claude/skills/raspi-troubleshoot/SKILL.md` — SSH / Wi-Fi / GPIO busy / 権限エラー
