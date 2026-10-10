#!/usr/bin/env bash
# main の内容を group-a〜group-d にマージして push する(先生用)。
# GitHub Actions の distribute.yml と同じことを手元で行う。衝突したときの手動解決にも使う。
#
# 使い方:
#   scripts/distribute.sh            # 全班
#   scripts/distribute.sh group-b    # 指定した班だけ
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
groups=("$@")
if [ ${#groups[@]} -eq 0 ]; then
  groups=(group-a group-b group-c group-d)
fi

git fetch origin --prune
current=$(git branch --show-current)

for g in "${groups[@]}"; do
  echo "=== $g ==="
  if ! git show-ref --verify --quiet "refs/remotes/origin/$g"; then
    echo "origin/$g がありません。main から作成します。"
    git push origin "origin/main:refs/heads/$g"
    continue
  fi
  git checkout -q -B "$g" "origin/$g"
  if git merge --no-edit origin/main -m "chore: main の教材を $g に配布"; then
    git push origin "$g"
  else
    echo "!!! $g で衝突しました。ファイルを直して git add → git commit → git push origin $g を実行してください。"
    echo "    やめるときは git merge --abort"
    exit 1
  fi
done

git checkout -q "$current"
echo "完了"
