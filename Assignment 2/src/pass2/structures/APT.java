package src.pass2.structures;

import java.util.*;

public class APT {
    public HashMap<String, String> actualParameterTable;

    public APT(){
        actualParameterTable = new HashMap<>();
    }   

    public void insert(String var, String defaultArg){
        actualParameterTable.put(var, defaultArg);
    }    

    public String get(String var) throws Exception{
        if(!actualParameterTable.containsKey(var)) throw new Exception("Error: Could not find variable in APT. Var: " + var);
        return actualParameterTable.get(var);
    }

    public void print(){
        for(Map.Entry<String, String> set: actualParameterTable.entrySet()){
            System.out.println(set.getKey() + " : " + set.getValue());
        }
    }

}
