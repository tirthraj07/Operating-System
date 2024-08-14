package pass1;

import java.util.ArrayList;

enum TokenType {
    LABEL,
    OPCODE,
    OPERAND
}

enum LineType {
    EMPTY,
    OPCODE,
    LABEL_OPCODE,
    OPCODE_OPERAND,
    LABEL_OPCODE_OPERAND,
    OPCODE_OPERAND_OPERAND,
    LABEL_OPCODE_OPERAND_OPERAND
}

class Token {
    public String token;
    public TokenType type;
    public Token(String token, TokenType type){
        this.token = token;
        this.type = type;
    }
}

public class Tokenizer {
    
    private SyntaxAnalyzer synAnalyze = new SyntaxAnalyzer();

    public Tokenizer(){}

    public ArrayList<Token> getTokens(String line) throws Exception {

        String[] tokens = tokenize(line);
        ArrayList<Token> listOfTokens = new ArrayList<Token>();

        if(tokens.length == 0){
            return listOfTokens;
        }

        // Only Opcode
        else if(tokens.length == 1){
            if(synAnalyze.isOpcode(tokens[0])){
                listOfTokens.add(new Token(tokens[0], TokenType.OPCODE));
            }
            else throw new Exception("Token length of 1 must only contain Opcode");
        }

        // Opcode Operand
        // Lable Opcode
        else if(tokens.length == 2){
            if(synAnalyze.isOpcode(tokens[0]) && synAnalyze.isOperand(tokens[1])){
                listOfTokens.add(new Token(tokens[0], TokenType.OPCODE));
                listOfTokens.add(new Token(tokens[1], TokenType.OPERAND));
            }
            else if(synAnalyze.isLabel(tokens[0]) && synAnalyze.isOpcode(tokens[1])){
                listOfTokens.add(new Token(tokens[0], TokenType.LABEL));
                listOfTokens.add(new Token(tokens[1], TokenType.OPCODE));
            }
            else throw new Exception("Token length of 2 must only be of type OPCODE-OPERAND or LABEL-OPCODE");
        }

        // Lable Opcode Operand
        // Opcode Operand Operand
        else if(tokens.length == 3){
            if(synAnalyze.isLabel(tokens[0]) && synAnalyze.isOpcode(tokens[1]) && synAnalyze.isOperand(tokens[2])){
                listOfTokens.add(new Token(tokens[0], TokenType.LABEL));
                listOfTokens.add(new Token(tokens[1], TokenType.OPCODE));
                listOfTokens.add(new Token(tokens[2], TokenType.OPERAND));
            }
            else if(synAnalyze.isOpcode(tokens[0]) && synAnalyze.isOperand(tokens[1]) && synAnalyze.isOperand(tokens[2])){
                listOfTokens.add(new Token(tokens[0], TokenType.OPCODE));
                listOfTokens.add(new Token(tokens[1], TokenType.OPERAND));
                listOfTokens.add(new Token(tokens[2], TokenType.OPERAND));
            }
            else throw new Exception("Token length of 3 must only be of type LABEL-OPCODE-OPERAND or OPCODE-OPERAND-OPERAND");
        }

        // Label Opcode Operand Operand
        else if(tokens.length == 4){
            if(synAnalyze.isLabel(tokens[0]) && synAnalyze.isOpcode(tokens[1]) && synAnalyze.isOperand(tokens[2]) && synAnalyze.isOperand(tokens[3])){
                listOfTokens.add(new Token(tokens[0], TokenType.LABEL));
                listOfTokens.add(new Token(tokens[1], TokenType.OPCODE));
                listOfTokens.add(new Token(tokens[2], TokenType.OPERAND));
                listOfTokens.add(new Token(tokens[3], TokenType.OPERAND));
            }
            else throw new Exception("Token length of 4 must be of type LABEL-OPCODE-OPERAND-OPERAND");
        }
        else {
            throw new Exception("Syntax Error: Unable to parse lines with token length = " + tokens.length);
        }
        return listOfTokens;
    }

    private String[] tokenize(String line) {
        
        // We will split the line into tokens by taking whitespaces and commas as delimiters

        line = line.replace(",", " ");
        
        return line.split("\\s+");
    }

    public LineType getLineType(ArrayList<Token> tokens){
        if(tokens.size() == 0) return LineType.EMPTY;
        else if(tokens.size() == 1) return LineType.OPCODE;
        else if(tokens.size() == 2){
            if(tokens.get(0).type == TokenType.LABEL) return LineType.LABEL_OPCODE;
            else return LineType.OPCODE_OPERAND;
        }
        else if(tokens.size() == 3){
            if(tokens.get(0).type == TokenType.LABEL) return LineType.LABEL_OPCODE_OPERAND;
            else return LineType.OPCODE_OPERAND_OPERAND;
        }
        else return LineType.LABEL_OPCODE_OPERAND_OPERAND;
    }

}
