package pass1;

import java.util.ArrayList;

public class Translator {
    Tokenizer tokenizer;
    int locationCounter;
    SyntaxAnalyzer syntaxAnalyzer;
    Table table;

    public Translator(){
        locationCounter = 0;
        tokenizer = new Tokenizer();
        syntaxAnalyzer = new SyntaxAnalyzer();
        table = new Table();
    }
    
    public void translateLine(String line, LiteralTable literalTable, SymbolTable symTable, PoolTable poolTable) throws Exception{
        ArrayList<Token> tokens = tokenizer.getTokens(line);
        LineType lineType = tokenizer.getLineType(tokens);
        boolean incrementLCFlag = true;
        // System.out.println("LineType : "+lineType);
        for(int i=0; i<tokens.size(); i++){
            if(tokens.get(i).type == TokenType.LABEL){
                Token label = tokens.get(i);
                symTable.insert(label.token, locationCounter);
            }

            else if(tokens.get(i).type == TokenType.OPCODE){
                Token opcode = tokens.get(i);
                OpcodeType opType = syntaxAnalyzer.getOpcodeType(opcode.token);

                System.out.print("(" + table.OPTAB.get(opcode.token).first + ", " + table.OPTAB.get(opcode.token).second + ")");

                if(opType == OpcodeType.ASSEMBLER_DIRECTIVE){
                    incrementLCFlag = false;
                    if(lineType == LineType.OPCODE_OPERAND_OPERAND || lineType == LineType.LABEL_OPCODE_OPERAND_OPERAND) throw new Exception("Invalid Syntax: Token Syntax Mismatch: Assembler Directives can only be of types OPCODE or OPCODE-OPERAND or LABEL OPCODE or LABEL-OPCODE-OPERAND");

                    if(opcode.token.equalsIgnoreCase("START") || opcode.token.equalsIgnoreCase("ORIGIN")){
                        if(lineType == LineType.OPCODE_OPERAND || lineType == LineType.LABEL_OPCODE_OPERAND){
                            if(syntaxAnalyzer.getOperandType(tokens.get(i+1).token) != OperandType.CONSTANT) throw new Exception("Invalid Syntax: Assember Directive 'START' and 'ORIGIN' must have Operand Type CONSTANT");
                            locationCounter = syntaxAnalyzer.getConstantValue(tokens.get(i+1).token, symTable);
                        }   
                        else throw new Exception("Invalid Syntax: Assember Directive 'START' and 'ORIGIN' must have line type OPCODE-OPERAND or LABEL-OPCODE-OPERAND");
                    }
                    else if(opcode.token.equalsIgnoreCase("END") || opcode.token.equalsIgnoreCase("LTORG")){
                        if(lineType == LineType.OPCODE || lineType == LineType.OPCODE_OPERAND){ 
                            int assigned = literalTable.handleNewPool(locationCounter, poolTable);
                            locationCounter = locationCounter + assigned;
                        }
                        else throw new Exception("Invalid Syntax: Token Syntax Mismatch: 'END' can only be of line type OPCODE or OPCODE OPERAND");
                    }
                    else if(opcode.token.equalsIgnoreCase("EQU")){
                        if(lineType != LineType.LABEL_OPCODE_OPERAND) throw new Exception("Invalid Syntax: Assember Directive 'EQU' must have line type LABEL-OPCODE-OPERAND");
                        if(syntaxAnalyzer.getOperandType(tokens.get(i+1).token) == OperandType.SYMBOL) {
                            int symbolLC = symTable.getLocationCounter(tokens.get(i+1).token);
                            if(symbolLC == -1) throw new Exception("Runtime Error: Trying to assign LC of unassigned symbol to another symbol") ;
                            symTable.insert(tokens.get(i-1).token, symbolLC);
                        }
                        else if(syntaxAnalyzer.getOperandType(tokens.get(i+1).token) == OperandType.CONSTANT){
                            int symbolLC = syntaxAnalyzer.getConstantValue(tokens.get(i+1).token, symTable);
                            symTable.insert(tokens.get(i-1).token, symbolLC);
                        }
                        else throw new Exception("Invalid Syntax: Assember Directive 'EQU' must have Operand Type SYMBOL OR CONSTANT");


                    }
                }
                else if(opType == OpcodeType.IMPERATIVE_STATEMENT){
                    incrementLCFlag = true; 
                }
                else if(opType == OpcodeType.DECLARATIVES){
                    incrementLCFlag = false;
                    if(lineType == LineType.OPCODE_OPERAND || lineType == LineType.LABEL_OPCODE_OPERAND){ 
                        if(syntaxAnalyzer.getOperandType(tokens.get(i+1).token) != OperandType.CONSTANT) throw new Exception("Invalid Syntax: OpcodeType DECLARATIVES must have OPERAND TYPE CONSTANT");
                        int offset = syntaxAnalyzer.getConstantValue(tokens.get(i+1).token, symTable);;
                        locationCounter+= offset;
                    }
                    else throw new Exception("Invalid Syntax: OpcodeType DECLARATIVES must have lineType LABEL_OPCODE_OPERAND");                
                }
            }
            else if(tokens.get(i).type == TokenType.OPERAND){
                Token operand = tokens.get(i);
                OperandType operandType = syntaxAnalyzer.getOperandType(operand.token);   
                switch(operandType){
                    case LITERAL:
                        literalTable.insert(operand.token);
                        System.out.print("(L, " + literalTable.getIndex(operand.token) + ")");                
                        break;
                    case CONSTANT:
                        System.out.print("(C, " + syntaxAnalyzer.getConstantValue(tokens.get(i).token, symTable) + ")");
                        break;
                    case REG:
                        System.out.print("("+table.REG.get(operand.token)+")");
                        break;
                    case COND:
                        System.out.print("("+table.COND.get(operand.token)+")");
                        break;
                    case SYMBOL:
                        symTable.insert(operand.token);
                        System.out.print("(S, " + symTable.getIndex(operand.token)+")");
                        break;
                    default:
                        throw new Exception("Inavlid Operand Type");
                }
    
            }
            else throw new Exception("Syntax Error: Token Type mismatch");
        }
        if(incrementLCFlag){ 
            locationCounter++;
        }

        System.out.println();
    }
}
