# [dp1] デザインパターン (1): Template Method

各問題に答えよ．本演習で提出する各プログラムのパッケージ名は，`dp1`とすること（各ソースコードの冒頭を，`package dp1;`とする）．


### 問題一覧
| 課題名                                          | 種別 | 配点 |
|-------------------------------------------------|------|------|
| [:notebook: 準備: AbstractDisplay](#dp1-0)   | -- | -- |
| [:green_book: dp1-1: FancyDisplay](#dp1-1)   | 必須| 5点|
| [:green_book: dp1-2: PasswordChecker（前半）](#dp1-2) | 必須| 5点|
| [:orange_book: dp1-3: PasswordChecker（後半）](#dp1-3) | 任意| 5点|


<a id="dp1-0"></a>
## :notebook: 準備: AbstractDisplay

まず，教科書のTemplate Methodの章(3章)を読み，AbstractDisplayクラスを含んだサンプルを実行してみよう．サンプルプログラムのファイルを入手したい場合は，教科書の公式サイトからダウンロードすると良い．

- 結城浩 「Java言語で学ぶ デザインパターン入門 第3版」: https://www.hyuki.com/dp/

<a id="dp1-1"></a>
## :green_book: dp1-1: FancyDisplay

上記「準備」で登場した「AbstractDisplay」というテンプレートにしたがって具体的な内容を定めたもの，つまり，抽象クラスAbstractDisplayのサブクラスとして，FancyDisplayクラスを実装せよ．

FancyDisplayは，フィールドとして，次のものを持っているとする．
- `private String string`: 文字列
- `private int margin`: マージン
- `private char frameChar`: 枠を描く文字

文字列を出力するという点では，StringDisplayと同じであるが，文字列を出力する部分の上下左右に，`margin`分の空白が入る．また，枠を描く文字は`frameChar`を使う．
実行例を参考にせよ．

#### 実行例

##### コード

```Java
package dp1;

public class FancyDisplayTest {
    public static void main(String[] args) {
        AbstractDisplay df1 = new FancyDisplay("test", 1, '#'); 
        df1.display();                                       
        AbstractDisplay df2 = new FancyDisplay("abc", 3, '+'); 
        df2.display();                                       
        AbstractDisplay df3 = new FancyDisplay("!!!", 0, '/'); 
        df3.display();    
    }
}
```

##### 実行結果


```text
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

### :arrow_right:提出TODO

- ソースコードの提出
  - FancyDisplay.java
  - FancyDisplayTest.java（実行結果の説明のために，内容を追記してもよい）
- README.mdへの追記
  - FancyDisplayTestの実行結果
  - 考察: FancyDisplayTestの実行結果から，FancyDisplayが期待する動作をするかを説明する．


<a id="dp1-2"></a>
## :green_book: dp1-2: PasswordChecker（前半）

この問題は前半と後半に分かれている．
後半部分は任意課題（配点はあり）となっている．

### PasswordCheckerクラス

PasswordCheckerクラスは，パスワードチェックの処理が定義されているクラスである．
同クラスのソースコードとクラス図を次に示す．

#### PasswordChecker.java

```Java
public abstract class PasswordChecker {
    public abstract void input(); // 情報を入力させる
    public abstract boolean validate(); // 認証する

    // パスワードチェックの手順 (template method)
    public void check() {
        System.out.println("<< Authentication Start >>");
        input(); 
        if (validate()) {
            System.out.println("OK!");            
        } else {
            System.out.println("Failed..");                        
        }
    }
}
```

#### クラス図

![PasswordChecker](passwordchecker_class.svg)

PasswordCheckerクラスについて説明する．
`check`メソッドでは，まず，情報を入力（`input`メソッド）させた後に，認証（`validate`メソッド）を行い，その結果に応じて「OK」か「Failed」かのメッセージを出すというパスワードチェックの一連の処理が記述されている．ただし，`input`メソッドと`validate`メソッドは具体的な内容が決められておらず，その実装はサブクラスに任されている（抽象メソッド）．つまり，`check`メソッドがTemplate Methodとなっており，情報を入力させる`input`メソッドと認証処理を行う`validate`メソッドを具体的に記述したサブクラスを実装すれば，それらに応じたパスワードチェック処理が行えることになる．


このようなPasswordCheckerクラスのサブクラス（具象クラス）として，
次の2クラスを実装したいとする．

1. 単純なパスワードチェックを行うPlainPasswordCheckerクラス
2. 「チャレンジ」が付いたパスワードチェックを行うChallengePasswordCheckerクラス

次のクラス図は，PasswordChecker，PlainPasswordChecker，ChallengePasswordCheckerの関係を表したものである．

![PasswordChecker](passwordchecker.svg)


これから実装する2クラスについて，説明を加える．

### PlainPasswordChecker

単純な認証機構を持つパスワードチェッカである．`input`では文字列を入力させ，`validate`では入力文字列と正解のパスワードを比較すればよい（一致すればtrueを返す）．

PlainPasswordCheckerを用いたコードの例とその実行例を次に示す．

```Java
PasswordChecker pc1 = new PlainPasswordChecker("kumamoto");
pc1.check();
```

#### 実行例1

```text
<< Authentication Start >>
Input password: kumamoto
OK!
```

#### 実行例2

```text
<< Authentication Start >>
Input password: abc
Failed..
```

コードの書き始めの例を示す．

#### PlainPasswordChecker.java (未完成)

```Java
public class PlainPasswordChecker extends PasswordChecker {
	private String password; // 正しいパスワード

	public PlainPasswordChecker(String password) {
		this.password = password;
	}
	
	@Override
	public void input() {
        // write your code
	}

	@Override
	public boolean validate() {
        // write your code
	}
}
```

PlainPasswordCheckerクラスを完成させよ．
また，PlainPasswordCheckerクラスと，その動作を確認するためのPlainPasswordCheckerTestクラスを作成せよ．

### :arrow_right:提出TODO

- ソースコードの提出
  - PlainPasswordChecker.java
  - PlainPasswordCheckerTest.java
- README.mdへの追記
  - PlainPasswordCheckerTestの実行結果を示し，結果を用いて期待する動作をするかを説明する．

<a id="dp1-3"></a>
## :orange_book: dp1-3: PasswordChecker（後半）


### ChallengePasswordChecker

ChallengePasswordCheckerは，小さい子どもが容易にログインできないようにするために，「チャレンジ」がついたパスワードチェッカである．`input`では，パスワードに加えて何らかの「チャレンジ」の答えを入力させ，`validate`ではそれらの認証を行う．
ChallengePasswordCheckerを用いたコードの例とその実行例を次に示す．
この例では，足し算や引き算の計算を行わせることをチャレンジとしている．

```Java
PasswordChecker pc2 = new ChallengePasswordChecker("saitama");
pc2.check();
```

#### 実行例1

```text
<< Authentication Start >>
Input password: abcde
Challenge: 20 + 81 = ?: 101
Failed..
```

#### 実行例2

```text
<< Authentication Start >>
Input password: saitama
Challenge: 33 - 11 = ?: 44
Failed..
```

#### 実行例3

```text
<< Authentication Start >>
Input password: saitama
Challenge: 90 + 18 = ?: 108
OK!
```

ChallengePasswordCheckerクラスと，その動作を確認するためのChallengePasswordCheckerTestクラスを作成せよ．

チャレンジの内容は，上記の例（足し算と引き算の計算）**以外**とする．よくあるペアレンタル・コントロールのように，パスワードを知っていても小さい子どもだとログインできないような
仕掛けを考えてみよう．

### :arrow_right:提出TODO

- ソースコードの提出
  - ChallengePasswordChecker.java
  - ChallengePasswordCheckerTest.java
- README.mdへの追記
  - 実装した「チャレンジ」について説明し，実行結果を用いて動作を説明する．

以上
