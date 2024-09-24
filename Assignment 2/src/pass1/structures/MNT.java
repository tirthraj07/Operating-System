package src.pass1.structures;

import java.util.*;

import src.pass1.structures.helper.MNTRow;
import src.pass2.structures.Pair;

public class MNT{
    public static ArrayList<MNTRow> MacroNameTable;
    static {
        MacroNameTable = new ArrayList<>();
    }

    public static MNTRow geMntRow(String name, int pp, int kp) throws Exception {
        for(MNTRow row: MacroNameTable){
            if(row.name.equalsIgnoreCase(name) && row.pp==pp && row.kp==kp) return row;
        }
        throw new Exception("Error: Macro Name : " + name + " not found in MNT" );
    }

    public static MNTRow insertIntoMNT(String name, int pp, int kp) throws Exception {
        Boolean isPresent = true;
        try{
            geMntRow(name, pp, kp);
        }
        catch(Exception e){
            isPresent = false;
            MNTRow newRow = new MNTRow(name, pp, kp);
            MacroNameTable.add(newRow);
            return newRow;
        }

        if(isPresent) throw new Exception("Error: Duplicate Macro Name Found: " + name);
        return null;
    }

    public static void print() {
        System.out.println("-- Macro Name Table (MNT) --");
        System.out.println("name    : pp : kp : MDTP : PNTP : KPDTP");

        for(MNTRow row : MacroNameTable){
            System.out.println(row);
        }        

        System.out.println("\n");
    }

    // pass2 requirements

    public static boolean isMacroNamePresent(String macroName){
        for(MNTRow row: MacroNameTable){
            if(row.name.equalsIgnoreCase(macroName)) return true;
        }
        return false;
    }

    public static int getIndexOf(MNTRow requiredRow) throws Exception{
        for(int i=0; i<MacroNameTable.size(); i++){
            if(MacroNameTable.get(i).equals(requiredRow)) return i;
        }
        throw new Exception("Error: Index of MNT Row not found");
    }

    public static ArrayList<String> getPositionalParams(int index, int pp){
        ArrayList<String> positionalParams = new ArrayList<>();
        int PNTP = MacroNameTable.get(index).PNTP;
        while(pp > 0){
            positionalParams.add(PNT.ParameterNameTable.get(PNTP));
            PNTP += 1;
            pp -= 1;
        }

        return positionalParams;
    }

    public static ArrayList<Pair> getKeywordParams(int index){
        ArrayList<Pair> keywordParams = new ArrayList<>();
        int KPDTStart = MacroNameTable.get(index).KPDTP;

        int KPDTPEnd;
        if(index < MacroNameTable.size()-1){
            KPDTPEnd = MacroNameTable.get(index+1).KPDTP - 1;
        }
        else {
            KPDTPEnd = KPDT.getSize() - 1;
        }

        for(int i=KPDTStart; i<=KPDTPEnd; i++){
            String param = KPDT.KeywordParameterDefaultTable.get(i).param;
            String arg = KPDT.KeywordParameterDefaultTable.get(i).defaultArgument;
            keywordParams.add(new Pair(param, arg));
        }
        return keywordParams;
    }

    public static MNTRow searchMacro(String macroName,int pp, int kp, int totalParameterCount,ArrayList<Pair> keywordParameters) throws Exception{

        // check index of MNTRow where we find macro name
        for(int i=0; i<MacroNameTable.size(); i++){

            if(MacroNameTable.get(i).name.equalsIgnoreCase(macroName)){
                MNTRow row = MacroNameTable.get(i);

                if(row.pp != pp) continue;

                if(row.kp < kp) continue;

                if(row.kp > 0){
                    ArrayList<Pair> rowKeywordParams = getKeywordParams(i);

                    // check if non-default valued keyword parameters are present
                    for(Pair pair: rowKeywordParams){
                        if(pair.second.equalsIgnoreCase("NULL")){
                            boolean defaultParamFound = false;
                            for(int j=0; j<keywordParameters.size(); j++){
                                if(pair.first.equalsIgnoreCase(keywordParameters.get(j).first)){
                                    defaultParamFound = true;
                                    break;
                                }
                            }
                            if(defaultParamFound == false) throw new Exception("Error: Keyword Parameter without default value does not contain an argument : " + pair.first);
                        }
                    }

                    // check if all supplied parameters are in PNT
                    for(Pair suppliedKeywordParam: keywordParameters){
                        boolean isNotPresent = true;
                        for(Pair requiredKeywordParam: rowKeywordParams){
                            if(suppliedKeywordParam.first.equalsIgnoreCase(requiredKeywordParam.first)){
                                isNotPresent = false;
                                break;
                            }
                        }
                        if(isNotPresent) throw new Exception("Error: Supplied Keyword Parameter not in PNT : " + suppliedKeywordParam.first);
                    }
    
                }

                return row;
            }

        }


        throw new Exception("Error: Macro Definition matching Macro Name, Positional Parameters and Keyword Parameters not found. Error For Macro Call: " + macroName);
    }

}