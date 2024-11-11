import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

import pass1.LiteralTable;
import pass1.PoolTable;
import pass1.SymbolTable;
import pass1.Translator;

public class Assembler{
    public static void main(String[] args){
        
        if(args.length != 1){
            System.out.println("Provide the file to execute");
            System.out.println("Syntax: java Assembler <file-name>");
            return;
        }

        String filePath = args[0];

        String[] lines = readFileToArray(filePath);

        Translator translator = new Translator();
        LiteralTable literalTable = new LiteralTable();
        SymbolTable symTable = new SymbolTable();
        PoolTable poolTable = new PoolTable();

        for(int i=0; i<lines.length; i++){
            try{
                translator.translateLine(lines[i], literalTable, symTable, poolTable);
            }
            catch(Exception e){
                System.err.println("Error at line " + (i+1));
                System.err.println(e.getMessage());
            }
        }

        System.out.println("---- Symbol Table ----");
        symTable.print();

        System.out.println("---- Literal Table ----");
        poolTable.print();

    }

    private static String[] readFileToArray(String filePath) {
        ArrayList<String> linesList = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                linesList.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Convert ArrayList to array
        return linesList.toArray(new String[0]);
    }
}