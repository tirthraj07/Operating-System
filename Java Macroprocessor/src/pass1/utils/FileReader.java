package src.pass1.utils;

import java.util.*;
import java.util.stream.Collectors;
import java.nio.file.Files;
import java.nio.file.Path;


public class FileReader {
    
    public static List<String> readFile(Path path) throws Exception{
        List<String> lines = Files.readAllLines(path);
        lines = lines.stream()
                    .filter(line -> !line.trim().isEmpty())
                    .collect(Collectors.toList());
        return lines;
    }

}
