package past1;

public class IncludeHintNumberTest {
	public static void main(String[] args) {
		HintNumber hn2 = new IncludeHintNumber(35);
		System.out.println(hn2);
		System.out.println(3);
		hn2.showHint(3);			
		System.out.println(7);
		hn2.showHint(7);			
	}
}