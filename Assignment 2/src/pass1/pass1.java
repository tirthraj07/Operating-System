package src.pass1;

import java.nio.file.*;
import java.util.*;

import src.pass1.structures.KPDT;
import src.pass1.structures.MDT;
import src.pass1.structures.MNT;
import src.pass1.structures.helper.*;
import src.pass1.structures.PNT;
import src.pass1.utils.FileReader;
import src.pass1.utils.Tokenizer;
import src.pass1.utils.helper.MBTokenRow;
import src.pass1.utils.helper.MDTokenRow;
import src.pass1.utils.helper.MacroDefinitionTokenType;

// Then iterate the lines array 
// Until we find 'MACRO' keep inserting the line in lines array into output array
// Then Read the 1st line after MACRO keyword, use Tokenizer.tokenizeMacroDefinition to tokenize the definition
// According to the tokens, insert into KPDT, PNT, MDT
// Then Read rest of the lines till we get MEND
// Tokenize those lines using Tokenizer.tokenizeMacroBody
// Repeat from Step 3 till we get to the end

public class pass1{
    
    public Path fileName;
    ArrayList<String> outputLines;

    public pass1(Path fileName) throws Exception{
        this.fileName = fileName;
        List<String> lines;

        outputLines = new ArrayList<>();
        try{
            lines = FileReader.readFile(fileName);
        }
        catch(Exception e){
            System.out.println("Error occurred while reading the file");
            e.printStackTrace();
            return;
        }   

        int i=0;

        while(i<lines.size()){
            if(lines.get(i).toUpperCase().contains("MACRO")){
                i++;    // Next line -> Macro Name Definition;
                
                String macroDefinition = lines.get(i);
                
                ArrayList<MDTokenRow> definitionTokens = Tokenizer.tokenizeMacroDefinition(macroDefinition);
                
                MNTRow insertedRow =  analyzeMacroDefinition(definitionTokens);

                i++;    // Next line -> Macro Body;
                while(!lines.get(i).toUpperCase().contains("MEND")){
                    if(i>=lines.size()) throw new Exception("Error: MEND not declared for MACRO");
                    ArrayList<MBTokenRow> bodyTokens = Tokenizer.tokenizeMacroBody(lines.get(i));
                    MDT.insertLine(bodyTokens, insertedRow.PNTP);
                    i++;
                }
                ArrayList<MBTokenRow> bodyTokens = Tokenizer.tokenizeMacroBody(lines.get(i));
                MDT.insertLine(bodyTokens, insertedRow.PNTP);
                i++;
            }
            else{
                outputLines.add(lines.get(i));
                i++;
            }
        }
        
        System.out.println("--- PASS 1 Completed ---");

        MNT.print();
        PNT.print();
        KPDT.print();
        MDT.print();

        System.out.println("PASS 1 Output : ");
        for(String line : outputLines){
            System.out.println(line);
        }

        System.out.println("\n");

        System.out.println("-- END OF PASS 1 --");
    }

    public ArrayList<String> getOutput(){
        return outputLines;
    }

    // Insert data into MNT, PNT, KPDT
    public static MNTRow analyzeMacroDefinition(ArrayList<MDTokenRow> definitionTokens) throws Exception{
        int pp = 0;
        int kp = 0;
        String name = "";
        ArrayList<String> ListOfParams = new ArrayList<>();
        ArrayList<String> keywordParamsWithoutDefault = new ArrayList<>();
        HashMap<String, String> keywordParamsWithDefault = new HashMap<>();

        for(MDTokenRow token: definitionTokens){
            if(token.tokenType ==  MacroDefinitionTokenType.MacroName){ 
                name = token.token;
            }
            else if(token.tokenType == MacroDefinitionTokenType.PositionalParameter){ 
                pp+=1;
                ListOfParams.add(token.token);
            }
            else if(token.tokenType == MacroDefinitionTokenType.KeywordParamWithoutDefault){
                kp+=1;
                String param = token.token.split("=")[0];
                ListOfParams.add(param);
                keywordParamsWithoutDefault.add(param);
            }
            else if(token.tokenType == MacroDefinitionTokenType.KeywordParamWithDefault){
                kp+=1;
                String[] splitParams = token.token.split("=");
                String param = splitParams[0];
                String defaultArgument = splitParams[1];
                ListOfParams.add(param);
                if(keywordParamsWithDefault.containsKey(param)){ 
                    throw new Exception("Error: Ambiguous Parameter "+param+" : Keyword Parameter supplied more than once");
                }
                keywordParamsWithDefault.put(param, defaultArgument);
            }
        }

        MNTRow insertedMacro = MNT.insertIntoMNT(name, pp, kp);
        PNT.insert(ListOfParams);
        KPDT.insert(keywordParamsWithoutDefault);
        KPDT.insert(keywordParamsWithDefault);

        return insertedMacro;
    }
    

}