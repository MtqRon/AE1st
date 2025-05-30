package test;

public class Main2_1 {
    public static void main(String[] args) {
    	TempProvider provider = new HumanTempProvider();
        Observer observer1 = new AlertObserver();
        provider.addObserver(observer1);
        provider.execute();
    }
}
