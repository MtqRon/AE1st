package past1;

public class RemainderHintNumber extends HintNumber {
	public RemainderHintNumber(int number) {
		super(number);
	}
    // 追記せよ

    void showHint(int n){
        System.out.println("Reminder:" + getNumber() % n);
    }

    @Override
    public String toString(){
        return "RemainderHintNumber(" + getNumber() + ")";
    }

}