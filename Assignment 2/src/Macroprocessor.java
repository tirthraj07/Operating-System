package src;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;

import src.pass1.*;
import src.pass2.pass2;

public class Macroprocessor {

    public static void main(String[] args){ 

        if(args.length != 1){
            System.out.println("Provide the file to execute");
            System.out.println("Syntax: java Macroprocessor <file-name>");
            return;
        }

        String filePath = args[0];
        Path path = Paths.get(filePath);

        try{
            pass1 p1 = new pass1(path);
            
            ArrayList<String> pass1_output = p1.getOutput();

            System.out.println();

            new pass2(pass1_output);

            System.out.println("\n--END OF PASS 2--");
        }
        catch(Exception e){
            System.out.println("Error during pre-processing");
            System.out.println(e.getMessage());
            return;
        }

    }
}