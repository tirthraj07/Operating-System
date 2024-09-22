package src.pass1.utils;

import java.util.*;
import src.pass1.utils.helper.*;

/*
    When we are reading lines between 'MACRO' and 'MEND', the types of tokens we might come across are as follows
    MacroDefinitionTokenType -> Tokens that we may come across while reading the first line after the 'Macro' Keyword
    1. MacroName -> This is the first token of the first line after 'MACRO' keyword. Sometimes it is preceded with a label but I'am not handling that case
    2. PositionalParameters -> Parameters in general are started with '&' symbol. The PositionalParameters are mapped based on their positions
    3. KeywordParametersWithoutDefault -> These parameters are mapped with their name explicitly mentioned in the Macro Call. These do not have default values
    4. KeywordParametersWithDefault -> These parameters are mapped with their name explicitly mentioned in the Macro Call. These have default values

    MacroBodyTokenType -> The tokens of lines after MacroDefinition 
    1. Variable -> It can be positional, keyword with/without default parameters
    2. NonVariable -> It can be Instruction, Non-variable Operand
*/



public class Tokenizer {
    
    // definition -> First line after MACRO keyword
    public static ArrayList<MDTokenRow> tokenizeMacroDefinition(String definition) throws Exception {
        String[] tokenizedLine = definition.split("\\s+");
        
        if(tokenizedLine.length == 0) throw new Exception("Error: Invalid Macro Definition");

        ArrayList<MDTokenRow> tokens = new ArrayList<>();

        tokens.add(new MDTokenRow(tokenizedLine[0], MacroDefinitionTokenType.MacroName));

        for(int i=1; i<tokenizedLine.length; i++){
            if(tokenizedLine[i].startsWith("&") == false) throw new Exception("Error: Invalid Variable : "+tokenizedLine[i]+". Variables must start from &");

            // Check if last character is '=' : if yes, then KeywordParameterWithoutDefault
            if(tokenizedLine[i].charAt(tokenizedLine[i].length()-1) == '='){
                tokens.add(new MDTokenRow(tokenizedLine[i], MacroDefinitionTokenType.KeywordParamWithoutDefault));
            }

            // Else if it contains = sign but not at last position then KeywordParameterWithDefault
            else if(tokenizedLine[i].contains("=")){
                tokens.add(new MDTokenRow(tokenizedLine[i], MacroDefinitionTokenType.KeywordParamWithDefault)); 
            }

            // Else it is a positional parameters
            // We need to check that positional parameters are first. If they are preceded by Keyword Parameters, then throw an error

            else if(tokens.get(i-1).tokenType==MacroDefinitionTokenType.KeywordParamWithDefault || tokens.get(i-1).tokenType==MacroDefinitionTokenType.KeywordParamWithoutDefault) throw new Exception("Error: Positional Parameters cannot be preceded by Keyword Parameters");

            else tokens.add(new MDTokenRow(tokenizedLine[i], MacroDefinitionTokenType.PositionalParameter));
        }
        
        return tokens;
    }

    // bodyLine -> Lines after the definition
    public static ArrayList<MBTokenRow> tokenizeMacroBody(String bodyLine) throws Exception {
        String[] tokenizedLine = bodyLine.split("\\s+");
        
        if(tokenizedLine.length == 0) throw new Exception("Error: Invalid Macro Definition");

        ArrayList<MBTokenRow> tokens = new ArrayList<>();

        for(String token: tokenizedLine){
            if(token.startsWith("&")) tokens.add(new MBTokenRow(token, MacroBodyTokenType.Variable));
            else tokens.add(new MBTokenRow(token, MacroBodyTokenType.NonVariable));
        }

        return tokens;
    }

}
