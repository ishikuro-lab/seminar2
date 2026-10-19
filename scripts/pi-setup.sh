#!/usr/bin/env bash
# ラズパイの初期化(sudo が要らない部分)。各班のラズパイで 1 回だけ実行する。
#
# 使い方(ラズパイ上で):
#   bash pi-setup.sh group-a        # 自分の班名
#
# やること:
#   - ~/seminar2 に班のブランチを clone
#   - git の基本設定(pull は merge、push は現在のブランチのみ)
#
# sudo が要るもの(管理者が実行): sudo apt install gh / ホスト名の変更
set -euo pipefail

group="${1:-}"
case "$group" in
  group-a|group-b|group-c|group-d) ;;
  *) echo "使い方: bash pi-setup.sh group-a|group-b|group-c|group-d" >&2; exit 1 ;;
esac

REPO_URL="https://github.com/ishikuro-lab/seminar2.git"
if [ -d ~/seminar2/.git ]; then
  echo "~/seminar2 は既にあります。ブランチを $group に合わせます。"
  git -C ~/seminar2 fetch origin
  git -C ~/seminar2 checkout "$group"
  git -C ~/seminar2 pull
else
  git clone -b "$group" "$REPO_URL" ~/seminar2
fi

git config --global pull.rebase false
git config --global push.default current
git config --global init.defaultBranch main
git config --global core.editor nano

if ! command -v gh >/dev/null 2>&1; then
  echo
  echo "gh(GitHub CLI)が入っていません。管理者に次を実行してもらってください:"
  echo "  sudo apt update && sudo apt install -y gh"
fi

echo
echo "完了: ~/seminar2 ($group)"
echo "次は各自 gh auth login で GitHub に認証してください(docs/raspi-setup.md)。"
