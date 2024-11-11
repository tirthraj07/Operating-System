package pass1;

enum OperandType {
    LITERAL,
    SYMBOL,
    REG,
    COND,
    CONSTANT
}

public class SyntaxAnalyzer {
    private Table optable;
    public SyntaxAnalyzer(){
        optable = new Table();
    }

    public boolean isOpcode(String keyword){
        return optable.OPTAB.containsKey(keyword);
    }
    
    public boolean isLabel(String keyword){
        return !isOpcode(keyword);
    }

    public boolean isOperand(String keyword){
        return !isOpcode(keyword);
    }

    private boolean isConstant( String input ) {
        try {
            Integer.parseInt( input );
            return true;
        }
        catch( Exception e ) {
            if(input.contains("+")||input.contains("-")) return true;
            return false;
        }
    }

    // if operand starts with ='' then LITERAL
    // else it is taken as symbol

    public OperandType getOperandType(String keyword) throws Exception{
        if(isOperand(keyword)){
            if(keyword.charAt(0) == '=') return OperandType.LITERAL;
            else if (optable.REG.containsKey(keyword)) return OperandType.REG;
            else if (optable.COND.containsKey(keyword)) return OperandType.COND;
            else if (isConstant(keyword)) return OperandType.CONSTANT;
            else return OperandType.SYMBOL;
        }
        else throw new Exception("Incorrect argument to getOperandType function. Passed : " + keyword);
    }

    public OpcodeType getOpcodeType(String keyword) throws Exception {
        if(isOpcode(keyword)){
            if(Table.OPCODE_TYPES.containsKey(keyword)){
                return Table.OPCODE_TYPES.get(keyword);
            }
            else throw new Exception("Invalid Opcode: " + keyword);
        }
        else throw new Exception("Incorrect argument to getOpcodeType function. Passed : " + keyword);
    }

    public int getConstantValue (String input, SymbolTable symTable) throws Exception {
        try {
            int constVal = Integer.parseInt( input );
            return constVal;
        }
        catch( Exception e ) {
            if(input.contains("+") || input.contains("-")){
                String[] arr;
                if(input.contains("+")) arr = input.split("\\+");
                else arr = input.split("-");

                if(arr.length!=2) throw new Exception("Cannot evalute : " + input + ". It must be inform Symbol+CONSTANT");
                int lc = symTable.getLocationCounter(arr[0]);
                if(lc==-1) throw new Exception("Cannot evauate: "+input+". Operand 1 must be Symbol which is initialized before usage");
                try{
                    if(input.contains("+")) return lc + Integer.parseInt(arr[1]);
                    else return lc - Integer.parseInt(arr[1]);
                } catch(Exception e2){
                    throw new Exception("Cannot evalute Constant: " + input + ". It must be inform Symbol+CONSTANT");
                }
            }
            else throw new Exception("Cannot Evaluate : "+ input);
        }
    }

}
