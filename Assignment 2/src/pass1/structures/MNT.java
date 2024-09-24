package src.pass1.structures;

import java.util.*;

import src.pass1.structures.helper.MNTRow;

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

}