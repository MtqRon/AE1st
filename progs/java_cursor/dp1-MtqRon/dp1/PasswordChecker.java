package dp1;

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