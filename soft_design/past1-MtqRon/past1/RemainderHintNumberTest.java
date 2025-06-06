package past1;

public class RemainderHintNumberTest {
	public static void main(String[] args) {
		HintNumber hn1 = new RemainderHintNumber(23);
		System.out.println(hn1);
		System.out.println(5);
		hn1.showHint(5);
		System.out.println(3);
		hn1.showHint(3);
	}
}