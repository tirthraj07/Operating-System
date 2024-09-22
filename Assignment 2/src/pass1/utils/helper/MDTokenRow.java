package src.pass1.utils.helper;

// helper class

public class MDTokenRow {
    public String token;
    public MacroDefinitionTokenType tokenType;
    public MDTokenRow(String token, MacroDefinitionTokenType tokenType){
        this.token = token;
        this.tokenType = tokenType;
    }
}
