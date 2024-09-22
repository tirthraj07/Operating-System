package src.pass1.structures;

import java.util.*;

public class PNT {
    public static ArrayList<String> ParameterNameTable;

    static {
        ParameterNameTable = new ArrayList<>();
    }

    public static void insert(ArrayList<String> ListOfParams) throws Exception{
        HashSet<String> insertedParams = new HashSet<>();
        for(String param: ListOfParams){
            if(insertedParams.contains(param)){
                throw new Exception("Error: Ambiguous Parameter "+param+" : Parameter supplied more than once");
            }
            else{
                ParameterNameTable.add(param);
                insertedParams.add(param);
            }
        }
    }

    public static int getSize(){
        return ParameterNameTable.size();
    }

    // the function returns parameter location: 1-indexing (i.e index+1)
    public static int getParameterLocation(String param, int start) throws Exception{
        for(int index=start; index<ParameterNameTable.size(); index++){
            if(ParameterNameTable.get(index).equalsIgnoreCase(param)) return index + 1;
        }
        throw new Exception("Error: Parameter not in PNT : "+ param);
    }

    public static void print() {

        System.out.println("-- Parameter Name Table (PNT) --");
        
        System.out.println("position : parameter");

        for(int index=0; index < ParameterNameTable.size(); index++){
        System.out.println(Integer.toString(index+1) + " : " + ParameterNameTable.get(index));
        }
        System.out.println("\n");
    }


}