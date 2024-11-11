package pass1;

import java.util.ArrayList;

class SymbolNode {
    public String symbol;
    public int locationCounter;
    public SymbolNode(){}
    public SymbolNode(String symbol){
        this.symbol = symbol;
        this.locationCounter = -1;
    }
    public SymbolNode(String symbol, int locationCounter){
        this.symbol = symbol;
        this.locationCounter = locationCounter;
    }
};

public class SymbolTable {
    public ArrayList<SymbolNode> symTable = new ArrayList<SymbolNode>();
    public SymbolTable(){}
    
    public void insert(String symbol){
        for(SymbolNode n: symTable){
            if(n.symbol.equalsIgnoreCase(symbol)) return;
        }
        symTable.add(new SymbolNode(symbol));
    }

    public void insert(String symbol, int locationCounter){
        for(SymbolNode n: symTable){
            if(n.symbol.equalsIgnoreCase(symbol)){
                n.locationCounter = locationCounter;
                return;
            }
        }
        symTable.add(new SymbolNode(symbol, locationCounter));
    }

    public int getLocationCounter(String symbol){
        for(SymbolNode n: symTable){
            if(n.symbol.equalsIgnoreCase(symbol)) return n.locationCounter;
        }
        return -1;
    }

    public String getSymbol(int locationCounter){
        for(SymbolNode n: symTable){
            if(n.locationCounter == locationCounter) return n.symbol;
        }
        return "";
    }

    // returns the index starting from 1
    public int getIndex(String symbol){
        for(int i=0; i<symTable.size(); i++){
            if(symTable.get(i).symbol.equalsIgnoreCase(symbol)) return i+1;
        }
        return -1;
    }

    public void print(){
        for(int i=0; i<symTable.size(); i++){
            System.out.println(symTable.get(i).symbol + " : " + symTable.get(i).locationCounter);
        }
        System.out.println();
    }

}
