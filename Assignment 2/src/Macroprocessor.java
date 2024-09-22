package src;

import java.nio.file.Path;
import java.nio.file.Paths;

import src.pass1.*;

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
            new pass1(path);
        }
        catch(Exception e){
            System.out.println("Error during pass 1");
            System.out.println(e.getMessage());
            return;
        }

    }
}