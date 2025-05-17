# Template Method パターン実装

## dp1-1: FancyDisplay

### 実行結果
```
########
#      #
# test #
# test #
# test #
# test #
# test #
#      #
########
+++++++++++
+         +
+         +
+         +
+   abc   +
+   abc   +
+   abc   +
+   abc   +
+   abc   +
+         +
+         +
+         +
+++++++++++
/////
/!!!/
/!!!/
/!!!/
/!!!/
/!!!/
/////
```

### 考察
FancyDisplayクラスは、AbstractDisplayクラスを継承し、Template Methodパターンを実装しています。実行結果から、以下の動作を確認できます：

1. `df1`（margin=1, frameChar='#'）では、文字列の周りに1マスの余白と#の枠が表示されています。
2. `df2`（margin=3, frameChar='+'）では、文字列の周りに3マスの余白と+の枠が表示されています。
3. `df3`（margin=0, frameChar='/'）では、余白なしで/の枠が表示されています。

これらの結果から、FancyDisplayクラスが期待通りに動作していることがわかります。マージンのサイズや枠文字を変更することで、異なる表示形式を実現できています。

## dp1-2: PlainPasswordChecker

### 実行結果
```
<< Authentication Start >>
Input password: kumamoto
OK!
```

または、間違ったパスワードを入力した場合：
```
<< Authentication Start >>
Input password: abc
Failed..
```

### 考察
PlainPasswordCheckerクラスは、PasswordCheckerクラスを継承し、Template Methodパターンを実装しています。実行結果から、次のことが確認できます：

1. パスワード入力を促すプロンプトが表示されます。
2. 正しいパスワード（この例では「kumamoto」）が入力された場合、「OK!」と表示されます。
3. 間違ったパスワードが入力された場合、「Failed..」と表示されます。

これらの結果から、PlainPasswordCheckerクラスが期待通りの認証機能を提供していることが確認できます。

## dp1-3: ChallengePasswordChecker

### 実装したチャレンジについて
このChallengePasswordCheckerでは、シーザー暗号（Caesar cipher）を解読するチャレンジを実装しました。シーザー暗号はアルファベットをある一定数だけシフトさせる単純な暗号化方式です。

例えば、「a」を2文字シフトすると「c」になります。このような簡単な暗号解読問題は、小さな子どもにとっては難しい課題となり、本人確認のためのチャレンジとして適しています。

### 実行結果
正しいパスワードと正しいチャレンジの回答：
```
<< Authentication Start >>
Input password: saitama
Challenge: 'b' をシーザー暗号で 3 文字シフトすると？: e
OK!
```

正しいパスワードだが間違ったチャレンジの回答：
```
<< Authentication Start >>
Input password: saitama
Challenge: 'm' をシーザー暗号で 2 文字シフトすると？: p
Failed..
```

間違ったパスワード：
```
<< Authentication Start >>
Input password: wrong
Failed..
```

### 動作説明
1. まず、パスワードの入力を求めます。
2. パスワードが正しい場合のみ、シーザー暗号のチャレンジが出題されます。
3. ランダムに選ばれたアルファベット一文字と、1〜5の範囲でランダムに選ばれたシフト数が提示されます。
4. ユーザーは、指定されたアルファベットを指定されたシフト数だけシフトした結果を答える必要があります。
5. パスワードとチャレンジの両方が正しい場合のみ認証が成功します。

このチャレンジは単純な計算ではなく、アルファベットの知識と簡単な暗号解読能力を要求するため、小さな子どもにとっては難しい課題となります。 