---
name: group-git-workflow
description: 班ブランチ(group-a〜group-d)での pull → 作業 → commit → push の手順、衝突の解消、やってはいけない操作。Git の操作を頼まれたとき、push が拒否されたとき、CONFLICT が出たときに使う。
---

# group-git-workflow — 班ブランチでの Git 作業

## 前提

- `main` は先生専用。受講生は push できない(ruleset)。
- 班は `group-a` / `group-b` / `group-c` / `group-d` のどれか 1 つ。最初に `git branch` で確認し、違うブランチにいたら `git checkout group-x` に戻す。
- `materials/` は編集しない。成果物は `work/`。
- 先生が `main` を更新すると GitHub Actions が各班ブランチに merge する。受講生は `git pull` するだけでよい。

## 基本の流れ

```
git branch                       # * group-a を確認
git pull                         # 取り込み
# work/ で編集・実行
git status                       # 変更を確認(materials/ が出ていたら戻す)
git add work/
git commit -m "何をしたか(例: カーブ走行を追加)"
git push
```

- `git add .` は便利だが、`materials/` や大きなファイルを巻き込みやすい。`git add work/` を基本にする。
- 大きなファイル(1 MB 超、動画、CSV)はコミットしない。`.gitignore` にある。

## 衝突(CONFLICT)の解消

1. `git status` で `both modified` のファイルを確認。
2. ファイルを開き、`<<<<<<< HEAD` 〜 `=======` 〜 `>>>>>>>` の範囲を、残す内容に書き換えて印を消す。
3. `git add <ファイル>` → `git commit`(メッセージは自動で入る)→ `git push`。
4. 戻したいときは `git merge --abort`。

AI が解消を手伝うときは、両方の変更の意図をユーザーに確認してから統合する。勝手に片方を捨てない。

## 間違えたとき

| 状況 | 対処 |
|---|---|
| `main` に commit してしまった | `git branch -f group-a` ではなく、`git checkout -b tmp` → `git checkout group-a` → `git merge tmp` でブランチに移す。`main` は `git checkout main && git reset --hard origin/main` で戻す |
| `materials/` を編集してしまった | `git checkout -- materials/` で戻し、必要な部分を `work/` にコピー |
| 間違えて `git add` した | `git restore --staged <ファイル>` |
| 直前の commit をやり直したい(push 前) | `git commit --amend` |
| push 済みを取り消したい | `git revert <コミット>`(履歴を消さない)。`--force` は使わない(拒否される) |

## やってはいけない

- `git push --force` / `git push -f`
- 他の班のブランチへの checkout・push
- `main` への push(ruleset で拒否されるが、試さない)
- トークンやパスワードをファイルに書いてコミットする
