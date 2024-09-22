package src.pass1.structures;

import java.util.*;
import src.pass1.utils.helper.*;;

public class MDT {
    public static ArrayList<String> MacroDefinitionTable;
    static {
        MacroDefinitionTable = new ArrayList<>();
    }

    public static int getSize(){
        return MacroDefinitionTable.size();
    }

    public static void insertLine(ArrayList<MBTokenRow> line, int PNTP) throws Exception{
        String outputLine = "";

        for(MBTokenRow token: line){
            if(token.tokenType == MacroBodyTokenType.NonVariable) outputLine += token.token + " ";
            else outputLine += "(P,"+ PNT.getParameterLocation(token.token, PNTP) +") ";
        }

        // trim the trailing spaces due to concatenation.
        outputLine = outputLine.trim();
        MacroDefinitionTable.add(outputLine);
    }

    public static void print() {
        System.out.println("-- Macro Definition Table --");
        
        for(String line: MacroDefinitionTable){
            System.out.println(line);
        }
        System.out.println("\n");

    }

}
