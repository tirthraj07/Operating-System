package pass1;

import java.util.ArrayList;

class LiteralNode {
    public String literal;
    public int locationCounter;
    public LiteralNode(){}
    public LiteralNode(String literal){
        this.literal = literal;
        this.locationCounter = -1;
    }
    public LiteralNode(String literal, int locationCounter){
        this.literal = literal;
        this.locationCounter = locationCounter;
    }
};


public class LiteralTable {
    public ArrayList<LiteralNode> literalTable = new ArrayList<LiteralNode>();
    public LiteralTable(){}
    public int offset = 1;
    
    public void insert(String literal){
        for(LiteralNode n: literalTable){
            if(n.literal.equalsIgnoreCase(literal)) return;
        }
        literalTable.add(new LiteralNode(literal));
    }

    public void insert(String literal, int locationCounter){
        for(LiteralNode n: literalTable){
            if(n.literal.equalsIgnoreCase(literal)){
                if(n.locationCounter == -1) n.locationCounter = locationCounter;
                return;
            };
        }
        literalTable.add(new LiteralNode(literal, locationCounter));
    }

    public int getLocationCounter(String literal){
        for(LiteralNode n: literalTable){
            if(n.literal.equalsIgnoreCase(literal)) return n.locationCounter;
        }
        return -1;
    }

    public String getLiteral(int locationCounter){
        for(LiteralNode n: literalTable){
            if(n.locationCounter == locationCounter) return n.literal;
        }
        return "";
    }

    // returns the index starting from offset = 1
    public int getIndex(String literal){
        for(int i=0; i<literalTable.size(); i++){
            if(literalTable.get(i).literal.equalsIgnoreCase(literal)) return i+offset;
        }
        return -1;
    }

    public int assignLCToUnAssignedLiterals(int locationCounter){
        int assigned = 0;
        for(int i=0; i<literalTable.size(); i++){
            if(literalTable.get(i).locationCounter == -1) {
                literalTable.get(i).locationCounter = locationCounter;
                locationCounter++;
                assigned++;
            }
        }
        return assigned;
    }

    public void print(){
        for(int i=0; i<literalTable.size(); i++){
            System.out.println(literalTable.get(i).literal + " : " + literalTable.get(i).locationCounter);
        }

        System.out.println();
    }

    public int handleNewPool(int locationCounter, PoolTable poolTable){
        int assigned = assignLCToUnAssignedLiterals(locationCounter);
        poolTable.insert(literalTable);
        offset = literalTable.size()+1;
        literalTable = new ArrayList<LiteralNode>();
        return assigned;
    }

}