package pass1;

import java.util.ArrayList;

public class PoolTable {
    public ArrayList<ArrayList<LiteralNode>> pool;
    public PoolTable(){
        pool = new ArrayList<ArrayList<LiteralNode>>();
    }

    public void insert(ArrayList<LiteralNode> literalTable){
        pool.add(literalTable);
    }

    public void print(){
        for(ArrayList<LiteralNode> table : pool){
            for(int i=0; i<table.size(); i++){
                System.out.println(table.get(i).literal + " : " + table.get(i).locationCounter);
            }
            System.out.println();
        }
        System.out.println();
    }

}
