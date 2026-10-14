# ブランチの使い方と教材の配り方

## 全体の図

```mermaid
flowchart LR
    T[先生の PC] -- push --> M[(main\n教材)]
    M -- 自動 merge\nGitHub Actions --> A[(group-a)]
    M -- 自動 merge --> B[(group-b)]
    M -- 自動 merge --> C[(group-c)]
    M -- 自動 merge --> D[(group-d)]
    A <-- pull / push --> PA[A 班のラズパイ]
    B <-- pull / push --> PB[B 班のラズパイ]
    C <-- pull / push --> PC[C 班のラズパイ]
    D <-- pull / push --> PD[D 班のラズパイ]
```

| ブランチ | 誰が書くか | 内容 |
|---|---|---|
| `main` | 先生だけ | 教材(`lesson02/`、`motor/`、`docs/`) |
| `group-a` 〜 `group-d` | その班の受講生 | `main` の内容 + 班の作業(`lesson02/work/`) |

受講生は `main` に push できません(GitHub の ruleset で止まります)。間違えて `main` に切り替えて作業しても、push のときにエラーになるだけでデータは消えません。

## 毎回の流れ

```
cd ~/seminar2
git branch                    # * group-a のように自分の班か確認
git pull                      # 教材と仲間の変更を取り込む
# lesson02/work/ の下で編集・実行
git status                    # 何を変えたか確認
git add lesson02/work/                 # lesson02/work/ の変更だけを追加
git commit -m "直進のテストを追加"
git push
```

コミットメッセージは「何をしたか」を一言で。日本語でかまいません。

## 衝突したとき

同じファイルの同じ場所を 2 人が別々に直すと、`git pull` のときに `CONFLICT` と表示されます。

1. `git status` で `both modified` のファイルを見る。
2. そのファイルを開くと、こういう印があります。

   ```
   <<<<<<< HEAD
   自分の変更
   =======
   相手の変更
   >>>>>>> origin/group-a
   ```

3. 残したい方を選んで、印の行(`<<<<<<<`、`=======`、`>>>>>>>`)を消す。両方残してもよい。
4. `git add そのファイル` → `git commit` → `git push`。

直せなくなったら、先生を呼んでください。`git merge --abort` で pull 前の状態に戻せます。

## やってはいけないこと

- `git push --force`(履歴を書き換える)。ruleset で拒否されますが、やらないでください。
- 他の班のブランチへの push。
- `lesson02/` 直下の教材の編集(教材の更新と衝突します)。作業は `lesson02/work/` に置きます。

Git のコマンドそのものがはじめての人は [git-basics.md](git-basics.md) を先に読んでください。
