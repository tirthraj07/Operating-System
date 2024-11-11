package src.pass2;

import java.util.*;

import src.pass1.structures.MDT;
import src.pass1.structures.MNT;
import src.pass1.structures.helper.MNTRow;
import src.pass2.structures.APT;
import src.pass2.structures.Pair;


// pass 2 of 2-pass macro-preprocessor
// Take input from pass1 which will only contain the asm code with macro calls and non-macro calls
// Start reading the input till you get to the macro call
// If line is not a macro call then just copy the line as it is

// If line is a macro call, then do further analysis

// How would one identify a macro call?
// Split the line with space as delimiter
// Then if the 0th index is inside the MNT, then identify that line as MACRO CALL

// What analysis should i do?
// Firstly, tokenize the macro call
// 0th index -> MACRO NAME
// if the word have '=' symbol -> keyword parameter (increment kp) else positional parameter (increment pp)

// At the end, you'll get MACRO name, pp, kp and totalParameterCount and also the positional parameter list and keyword parameter list
// Check for MACRO definition having the same name and pp first
// Then check kp
// if current kp > MNT kp, then wrong MACRO definition
// if current kp <= MNT kp, then analyze the given keyword parameters
// check if all keyword parameters without default values have been supplied or not. If not then wrong MACRO definition
// check if rest of the keyword parameters are there in PNT. If not then wrong MACRO definition
// create APT for the currentMacroCall

// Start reading the MDT using MDTP from MNT and until you find 'MEND'
// Tokenize each line
// Check if the word starts and ends with ( and ) respectively
// Since the start of Parameter Reference is always the same i.e (P,__)
// if n if the length of (P,__) then get the number from String 3 to n-2 both inclusive
// Search the parameter index in PNT and get back the parameter
// Search the parameter in APT and get back the actual value
// Replace it in the output line
// Do this for Rest of the line
// Repeat the entire process for next line


public class pass2 {
    ArrayList<String> output;
    public pass2(ArrayList<String> input) throws Exception{
        output = new ArrayList<>();

        for(String line: input){
            if(line.length()<1) continue;

            String[] tokenizedLine = line.split("\\s+");

            if(MNT.isMacroNamePresent(tokenizedLine[0]) == false){
                output.add(line);
                continue;
            }

            ArrayList<String> newBody = analyzeMacroCall(tokenizedLine);

            for(String new_line : newBody){
                output.add(new_line);
            }

        }

        System.out.println("--- OUTPUT OF PASS 2 ---");
        for(String line: output){
            System.out.println(line);
        }

    }

    public static ArrayList<String> analyzeMacroCall(String[] tokenizedLine) throws Exception{
        String macroName = tokenizedLine[0];
        int pp = 0;
        int kp = 0;
        int totalParameterCount = 0;
        ArrayList<String> positionalParameters = new ArrayList<>();
        ArrayList<Pair> keywordParameters = new ArrayList<>();

        for(int i=1; i<tokenizedLine.length; i++){
            if(tokenizedLine[i].startsWith("&")){
                // keyword parameter
                String[] tokenizeKeywordArgument = tokenizedLine[i].split("=");
                
                if(tokenizeKeywordArgument.length != 2) throw new Exception("Error: Incorrect way to pass keyword argument. Syntax: $var=arg. Passed "+tokenizedLine[i]);

                String var = tokenizeKeywordArgument[0];
                String arg = tokenizeKeywordArgument[1];
                
                kp+=1;
                keywordParameters.add(new Pair(var, arg));
            }
            else{
                // positional parameter
                pp+=1;
                positionalParameters.add(tokenizedLine[i]);
            }
            totalParameterCount += 1;
        }

        MNTRow macroNameDefinition = MNT.searchMacro(macroName, pp, kp, totalParameterCount, keywordParameters);

        int indexOfMNTRow = MNT.getIndexOf(macroNameDefinition);

        ArrayList<String> MNTPositionalParams = MNT.getPositionalParams(indexOfMNTRow, pp);
        ArrayList<Pair> MNTKeywordParams = MNT.getKeywordParams(indexOfMNTRow);

        if(MNTPositionalParams.size() !=positionalParameters.size()) throw new Exception("Error: MNTPositionParams does not match supplied PositionalParams");

        APT apt = new APT();

        for(int i=0; i<MNTPositionalParams.size(); i++){
            apt.insert(MNTPositionalParams.get(i), positionalParameters.get(i));
        }

        for(Pair pair: MNTKeywordParams){
            apt.insert(pair.first, pair.second);
        }

        for(Pair pair: keywordParameters){
            apt.insert(pair.first, pair.second);
        }

        int MDTP = macroNameDefinition.MDTP;

        ArrayList<String> macroBody = MDT.getMacroBody(apt, MDTP);

        return macroBody;

    }

}
