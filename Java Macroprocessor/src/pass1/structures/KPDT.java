package src.pass1.structures;

import java.util.*;

class KPDTRow {
    public String param;
    public String defaultArgument;
    public KPDTRow(String param){
        this.param = param;
        this.defaultArgument = "NULL";
    }
    public KPDTRow(String param, String defaultArgument){
        this.param = param;
        this.defaultArgument = defaultArgument;
    }
    @Override
    public String toString(){
        if(this.defaultArgument.equalsIgnoreCase("NULL")){
            return this.param + " : " + " __ ";
        }
        return this.param + " : " + this.defaultArgument;
    }
}

public class KPDT {
    public static ArrayList<KPDTRow> KeywordParameterDefaultTable;
    static {
        KeywordParameterDefaultTable = new ArrayList<>();
    }

    public static void insert(ArrayList<String> params) throws Exception{
        HashSet<String> insertedParams = new HashSet<>();

        for(String param: params){
            if(insertedParams.contains(param)){
                throw new Exception("Error: Ambiguous Parameter "+param+" : Keyword Parameter supplied more than once");
            }
            else{
                KeywordParameterDefaultTable.add(new KPDTRow(param));
                insertedParams.add(param);
            }
        }

    }

    public static void insert(HashMap<String, String> params){
        for(Map.Entry<String, String> set: params.entrySet()){
            KeywordParameterDefaultTable.add(new KPDTRow(set.getKey(), set.getValue()));
        }
    }

    public static int getSize(){
        return KeywordParameterDefaultTable.size();
    }

    public static void print() {

        System.out.println("-- Keyword Parameter Default Table --");

        System.out.println("parameter  :  default argument");

        for(KPDTRow row : KeywordParameterDefaultTable){
            System.out.println(row);
        }
        System.out.println("\n");
    }

}