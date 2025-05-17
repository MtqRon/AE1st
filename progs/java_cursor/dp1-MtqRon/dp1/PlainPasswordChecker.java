package dp1;

import java.util.Scanner;

public class PlainPasswordChecker extends PasswordChecker {
    private String password; // 正しいパスワード
    private String inputPassword; // 入力パスワード

    public PlainPasswordChecker(String password) {
        this.password = password;
    }
    
    @Override
    public void input() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Input password: ");
        inputPassword = scanner.nextLine();
    }

    @Override
    public boolean validate() {
        return password.equals(inputPassword);
    }
} 