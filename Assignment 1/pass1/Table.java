package pass1;

import java.util.HashMap;

enum OpcodeType {
    ASSEMBLER_DIRECTIVE,
    IMPERATIVE_STATEMENT,
    DECLARATIVES
}

class Pair {
    public String first;
    public int second;
    public Pair(String first, int second){
        this.first = first;
        this.second = second;
    }
    @Override
    public String toString(){
        return first + " : " + second;
    }
}

public class Table {
    HashMap<String, Pair> OPTAB = new HashMap<String, Pair>();
    HashMap<String, Integer> REG = new HashMap<String,Integer>();
    HashMap<String, Integer> COND = new HashMap<String, Integer>();

    public static HashMap<String, OpcodeType> OPCODE_TYPES = new HashMap<String,OpcodeType>();

    static {
        initOpcodeTypes();
    }

    

    public Table(){
        InitOPTAB();
        InitREG();
        InitCOND();
    }




    private static void initOpcodeTypes() {
        // Imperative Statements
        OPCODE_TYPES.put("STOP", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("ADD", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("SUB", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("MULT", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("MOVER", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("MOVEM", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("COMP", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("BC", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("DIV", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("READ", OpcodeType.IMPERATIVE_STATEMENT);
        OPCODE_TYPES.put("PRINT", OpcodeType.IMPERATIVE_STATEMENT);
        
        // Assembler Directive
        OPCODE_TYPES.put("START", OpcodeType.ASSEMBLER_DIRECTIVE);
        OPCODE_TYPES.put("END", OpcodeType.ASSEMBLER_DIRECTIVE);
        OPCODE_TYPES.put("ORIGIN", OpcodeType.ASSEMBLER_DIRECTIVE);
        OPCODE_TYPES.put("EQU", OpcodeType.ASSEMBLER_DIRECTIVE);
        OPCODE_TYPES.put("LTORG", OpcodeType.ASSEMBLER_DIRECTIVE);
        
        // Declaratives
        OPCODE_TYPES.put("DC", OpcodeType.DECLARATIVES);
        OPCODE_TYPES.put("DS", OpcodeType.DECLARATIVES);
    }




    private void InitOPTAB(){
        // Imperative Statements
        OPTAB.put("STOP", new Pair("IS", 0));
        OPTAB.put("ADD", new Pair("IS", 1));
        OPTAB.put("SUB", new Pair("IS", 2));
        OPTAB.put("MULT", new Pair("IS", 3));
        OPTAB.put("MOVER", new Pair("IS", 4));
        OPTAB.put("MOVEM", new Pair("IS", 5));
        OPTAB.put("COMP", new Pair("IS", 6));
        OPTAB.put("BC", new Pair("IS", 7));
        OPTAB.put("DIV", new Pair("IS", 8));
        OPTAB.put("READ", new Pair("IS", 9));
        OPTAB.put("PRINT", new Pair("IS", 10));
        
        // Assembler Directive
        OPTAB.put("START", new Pair("AD", 1));
        OPTAB.put("END", new Pair("AD", 2));
        OPTAB.put("ORIGIN", new Pair("AD", 3));
        OPTAB.put("EQU", new Pair("AD", 4));
        OPTAB.put("LTORG", new Pair("AD", 5));
        
        // Declaratives
        OPTAB.put("DC", new Pair("DL", 1));
        OPTAB.put("DS", new Pair("DL", 2));
    }

    private void InitREG(){
        REG.put("AREG",1);
        REG.put("BREG",2);
        REG.put("CREG",3);
        REG.put("DREG",4);
    }

    private void InitCOND(){
        COND.put("LT", 1);
        COND.put("LE", 2);
        COND.put("EQ", 3);
        COND.put("GT", 4);
        COND.put("GE", 5);
        COND.put("ANY", 6);
    }

}
