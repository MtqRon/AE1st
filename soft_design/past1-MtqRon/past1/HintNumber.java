package past1;

abstract class HintNumber {
	private int number;
	HintNumber(int number) {
		this.number = number;
	}
	int getNumber() {
		return number;
	}
	abstract void showHint(int n);

}