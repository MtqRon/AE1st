package dp1;

public class FancyDisplay extends AbstractDisplay {
    private String string;
    private int margin;
    private char frameChar;
    private int width;
    
    public FancyDisplay(String string, int margin, char frameChar) {
        this.string = string;
        this.margin = margin;
        this.frameChar = frameChar;
        this.width = string.length() + margin * 2;
    }
    
    @Override
    public void open() {
        printLine();
        for (int i = 0; i < margin; i++) {
            printEmptyLine();
        }
    }
    
    @Override
    public void print() {
        StringBuilder sb = new StringBuilder();
        sb.append(frameChar);
        for (int i = 0; i < margin; i++) {
            sb.append(' ');
        }
        sb.append(string);
        for (int i = 0; i < margin; i++) {
            sb.append(' ');
        }
        sb.append(frameChar);
        System.out.println(sb.toString());
    }
    
    @Override
    public void close() {
        for (int i = 0; i < margin; i++) {
            printEmptyLine();
        }
        printLine();
    }
    
    private void printLine() {
        StringBuilder line = new StringBuilder();
        for (int i = 0; i < width + 2; i++) {
            line.append(frameChar);
        }
        System.out.println(line.toString());
    }
    
    private void printEmptyLine() {
        StringBuilder emptyLine = new StringBuilder();
        emptyLine.append(frameChar);
        for (int i = 0; i < width; i++) {
            emptyLine.append(' ');
        }
        emptyLine.append(frameChar);
        System.out.println(emptyLine.toString());
    }
} 