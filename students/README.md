# students — 受講生 1 人ずつの作業場所

ラズパイの自分のアカウント(ユーザー名 = 姓のローマ字)で、`students/自分のユーザー名/` を作って作業します。
自分のフォルダ以外は編集しません。班の仲間のフォルダは `git pull` で届くので、読むだけにします。

```
students/
  sato/
    lesson02/    第 2 回の練習問題(lesson02/excersises/ からコピーして解く)
    lesson03/
      ultrasonic/  第 3 回 前半(lesson03/ultrasonic/ からコピーして解く)
      motor/       第 3 回 後半(lesson03/motor/ からコピーして解く)
  ito/
    lesson02/
```

第 2 回の準備(全員同じコマンド。`$USER` が自分のユーザー名に置き換わる):

```
cd ~/seminar2
git pull
mkdir -p students/$USER/lesson02
cp -n lesson02/excersises/*.py students/$USER/lesson02/
cd students/$USER/lesson02
```

第 3 回の準備:

```
cd ~/seminar2
git pull
mkdir -p students/$USER/lesson03/ultrasonic
cp -n lesson03/ultrasonic/*.py lesson03/ultrasonic/excersises/*.py students/$USER/lesson03/ultrasonic/
cd students/$USER/lesson03/ultrasonic
```

後半(モーター)は、始まるときに同じようにコピーします:

```
cd ~/seminar2
mkdir -p students/$USER/lesson03/motor
cp -n lesson03/motor/*.py lesson03/motor/excersises/*.py students/$USER/lesson03/motor/
cd students/$USER/lesson03/motor
```

記録して送るとき:

```
cd ~/seminar2
git add students/$USER/
git commit -m "何をしたか"
git pull
git push
```
