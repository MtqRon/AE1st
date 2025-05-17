package dp1;

public class FancyDisplayTest {
    public static void main(String[] args) {
        AbstractDisplay df1 = new FancyDisplay("test", 1, '#'); 
        df1.display();                                       
        AbstractDisplay df2 = new FancyDisplay("abc", 3, '+'); 
        df2.display();                                       
        AbstractDisplay df3 = new FancyDisplay("!!!", 0, '/'); 
        df3.display();    
    }
} 