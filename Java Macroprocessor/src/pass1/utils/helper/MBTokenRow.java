package src.pass1.utils.helper;

// helper class

public class MBTokenRow {
    public String token;
    public MacroBodyTokenType tokenType;
    public MBTokenRow(String token, MacroBodyTokenType tokenType){
        this.token = token;
        this.tokenType = tokenType;
    }
}
