package test;

public class AlertObserver implements Observer {
	static final int MAX_THRESHOLD = 35;  // 警告する気温のしきい値
    public void update(TempProvider provider) {
    	if (provider.getMaxTemp() >= MAX_THRESHOLD)
    		System.out.println("AlertObserver: 熱中症に注意！");
    }

}
