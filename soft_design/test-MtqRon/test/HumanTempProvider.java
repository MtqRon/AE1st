package test;

import java.util.Scanner;

public class HumanTempProvider extends TempProvider {
    private int maxTemp;        // 最高気温
    public int getMaxTemp() {   // 最高気温を取得する
        return maxTemp;
    }
    public void execute() {
    	Scanner in = new Scanner(System.in);
    	while (true) {
    		System.out.print("Max temp?: ");
    		maxTemp = in.nextInt();
    		if (maxTemp == 999) // 999なら終了
    			break;
    		notifyObservers();
    	}
    	in.close();
    }
}
