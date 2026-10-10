#!/usr/bin/env bash
# 受講生を seminar2 の outside collaborator(write)として招待する(先生用)。
# organization のメンバーには追加しない(メンバーにすると private の研究リポジトリが読めてしまう)。
#
# 使い方:
#   scripts/add-collaborators.sh user1 user2 ...
#   cat users.txt | scripts/add-collaborators.sh      # 1 行 1 ユーザー名
#   scripts/add-collaborators.sh --remove user1       # 外す(授業終了後など)
#
# 事前に gh auth switch -u muto-iskrlab(admin のアカウント)にしておく。
set -euo pipefail

REPO="ishikuro-lab/seminar2"
mode="add"
if [ "${1:-}" = "--remove" ]; then
  mode="remove"
  shift
fi

users=("$@")
if [ ${#users[@]} -eq 0 ]; then
  while read -r u; do
    [ -n "$u" ] && users+=("$u")
  done
fi
if [ ${#users[@]} -eq 0 ]; then
  echo "ユーザー名を引数か標準入力で渡してください" >&2
  exit 1
fi

for u in "${users[@]}"; do
  u="${u#@}"
  if [ "$mode" = "add" ]; then
    if gh api -X PUT "repos/$REPO/collaborators/$u" -f permission=push >/dev/null; then
      echo "招待: $u (write)"
    else
      echo "失敗: $u(ユーザー名を確認)" >&2
    fi
  else
    if gh api -X DELETE "repos/$REPO/collaborators/$u" >/dev/null; then
      echo "削除: $u"
    else
      echo "失敗: $u" >&2
    fi
  fi
done

echo
echo "現在の collaborator:"
gh api "repos/$REPO/collaborators?affiliation=outside" --jq '.[] | "  \(.login)\t\(.role_name)"'
echo "承諾待ちの招待:"
gh api "repos/$REPO/invitations" --jq '.[] | "  \(.invitee.login)\t\(.permissions)"'
