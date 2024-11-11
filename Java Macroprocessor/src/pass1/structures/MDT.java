package src.pass1.structures;

import java.util.*;
import src.pass1.utils.helper.*;
import src.pass2.structures.APT;;

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


    // pass 2 requirement

    public static ArrayList<String> getMacroBody(APT apt, int MDTP) throws Exception{
        ArrayList<String> body = new ArrayList<>();

        while(MDTP < MacroDefinitionTable.size() && !MacroDefinitionTable.get(MDTP).equalsIgnoreCase("MEND")){
            String outputLine = "";
            String line = MacroDefinitionTable.get(MDTP);

            String[] tokenizedLine = line.split("\\s+");
            for(String token: tokenizedLine){
                if(token.startsWith("(") && token.endsWith(")")){
                    int position = Integer.parseInt(token.substring(3, token.length()-1));
                    int index = position - 1;
                    String parameter = PNT.ParameterNameTable.get(index);
                    String argument = apt.get(parameter);
                    outputLine = outputLine + argument + " ";
                }
                else{
                    outputLine = outputLine + token + " ";
                }
            }
            outputLine = outputLine.trim();
            body.add(outputLine);
            MDTP++;
        }

        return body;
    }

}
