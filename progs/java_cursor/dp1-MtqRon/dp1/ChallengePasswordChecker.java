package dp1;

import java.util.Scanner;
import java.util.Random;

public class ChallengePasswordChecker extends PasswordChecker {
    private String password; // 正しいパスワード
    private String inputPassword; // 入力パスワード
    private String challenge; // チャレンジの内容
    private String expectedAnswer; // 期待される回答
    private String userAnswer; // ユーザーの回答
    
    public ChallengePasswordChecker(String password) {
        this.password = password;
        generateChallenge();
    }
    
    private void generateChallenge() {
        Random random = new Random();
        char randomChar = (char) (random.nextInt(26) + 'a'); // ランダムな小文字アルファベット
        int shift = random.nextInt(5) + 1; // 1〜5のシフト数
        
        char encodedChar = (char) ((randomChar - 'a' + shift) % 26 + 'a');
        
        challenge = "'" + randomChar + "' をシーザー暗号で " + shift + " 文字シフトすると？: ";
        expectedAnswer = String.valueOf(encodedChar);
    }
    
    @Override
    public void input() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Input password: ");
        inputPassword = scanner.nextLine();
        
        // パスワードが合っていればチャレンジを出題
        if (password.equals(inputPassword)) {
            System.out.print("Challenge: " + challenge);
            userAnswer = scanner.nextLine();
        }
    }
    
    @Override
    public boolean validate() {
        if (!password.equals(inputPassword)) {
            return false;
        }
        return expectedAnswer.equals(userAnswer);
    }
} 