package javaprac;
/*パスワードを設定する際に，次のような条件をすべて満たす必要があるとする．
6文字以上である
アルファベット（小文字または大文字）を1文字以上含む
数字を1文字以上含む
アルファベットや数字以外の文字は含まない
入力された文字列が，上記のパスワード設定の条件を満たしていればOK，そうでなければNGと出力するプログラムを作成せよ．*/
public class SetPassword{
    String password;
    public statiic void main(String[] args){
        Scanner sp = new Scanner(System.in);
        System.out.print("Input string：");
        String password = sp.nextLine();
        in.close();
    }

    int len = String.length(password);
    boolean isAlpha = false;
    boolean isDigit = false;
    boolean isValid = true;

    if (len < 6 ){
        isValid = false;
    }else{
        for(int i = 0; i < len; i++){
            char c = password.charAt(i);
            if(Character.isLetter(c)){
                isAlpha = true;
            }else if(Character.isDigit(c)){
                isDigit = true;
            }else{
                isValid = false;
                break;
            }
        }
    }
    if(isValid && isAlpha && isDigit){
        System.out.println("OK");
    }else{
        System.out.println("NG");
    }
}