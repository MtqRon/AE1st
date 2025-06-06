package past1;

public class IncludeHintNumber extends HintNumber {
	public IncludeHintNumber(int number) {
		super(number);
	}
    // 追記せよ

    boolean Include;

    void showHint(int n){
        Include = false;
        for(int exp = 1; getNumber() / exp > 0; exp *= 10){
            if(((getNumber() / exp) % 10) % n == 0){
                Include = true;
            }
        }
        if(Include){
            System.out.println("Included");
        }else{
            System.out.println("Not Included");
        }
    }

    @Override
    public String toString(){
        return "IncludeHintNumber(" + getNumber() + ")";
    }

}