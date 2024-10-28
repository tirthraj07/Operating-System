'''
This is a simplified version of pass 1 assembler compared to one i did during our lab sessions
Does't contain syntax analysis and error detection
Probably what they expect during practical exams due to time constraints

Refer to the flowchart in the folder for more information about the program

def main() -> Entry Point to the program

'''

op_tab : dict[ str, tuple [str, int]] = {
    "STOP"      : ( "IS" , 1 ) , 
    "ADD"       : ( "IS" , 2) ,
    "SUB"       : ( "IS" , 3) ,
    "MULT"      : ( "IS" , 4) ,
    "MOVER"     : ( "IS" , 5) ,
    "MOVEM"     : ( "IS" , 6) ,
    "COMP"      : ( "IS" , 7) ,
    "BC"        : ( "IS" , 8) ,
    "DIV"       : ( "IS" , 9) , 
    "READ"      : ( "IS" , 10) , 
    "PRINT"     : ( "IS" , 11) ,

    "START"     : ( "AD" , 1 ) ,
    "END"       : ( "AD" , 2 ) , 
    "ORIGIN"    : ( "AD" , 3 ) ,
    "EQU"       : ( "AD" , 4 ) , 
    "LTORG"     : ( "AD" , 5 ) ,

    "DC"        : ( "DL" , 1 ) ,  
    "DS"        : ( "DL" , 2 )   
} 

register_codes : dict[ str, int ] = {
    "AREG" : 1,
    "BREG" : 2,
    "CREG" : 3,
    "DREG" : 4
}

condition_codes: dict[ str , int ] = {
    "LT" : 1 , 
    "LE" : 2 , 
    "EQ" : 3 , 
    "GT" : 4 , 
    "GE" : 5 , 
    "ANY" : 6
}

def read_file() -> list[list[str]]:
    input_file_path: str = input("Enter input file path : ")
    input_content = ""
    with open( input_file_path, "r" ) as file:
        input_content : str = file.read()
    
    source_lines: list[str] = input_content.split("\n")
    source_line_tokens : list[list[str]] = [ line.split() for line in source_lines ]
    return source_line_tokens

def tokenize_line(card: list[str]) -> tuple[str, str, str, str]:
    label = ""
    op_code = ""
    operand_1 = ""
    operand_2 = ""

    if len(card) == 0:
        pass

    # we are not doing error detection so we will directly assume that it is an opcode
    elif len(card) == 1:
        op_code = card[0]
    

    elif len(card) == 2:
        if card[0] in op_tab.keys():
            # Opcode operand
            op_code = card[0]
            operand_1 = card[1]
        else:
            # label opcode
            label = card[0]
            op_code = card[1]

    elif len(card) == 3:
        if card[0] in op_tab.keys():
            # op_code operand_1 operand_2
            op_code = card[0]
            operand_1 = card[1]
            operand_2 = card[2]
        else:
            # label opcode operand
            label = card[0]
            op_code = card[1]
            operand_1 = card[2]

    elif len(card) == 4:
        # label opcode operand_1 operand_2
        label = card[0]
        op_code = card[1]
        operand_1 = card[2]
        operand_2 = card[3]

    return (label, op_code, operand_1, operand_2)

# forward ref -> symbol is used before it is defined.
def insert_in_symbol_table(symbol: str, forward_ref:bool):
    pass

def insert_in_literal_table(literal: str):
    pass

def get_literal_location(literal: str):
    pass

def get_symbol_location(symbol: str):
    pass

def get_literal_location_counter(literal: str):
    pass

def get_symbol_location_counter(symbol:str):
    pass

def output_operand(operand:str) -> str:
    if operand == "":
        return ""
    
    # operand can be a symbol, literal, reg, cond, constant
    if operand[0] == "=":
        # literal
        insert_in_literal_table(operand)
        literal_location: int = get_literal_location(operand[1:])
        return f"(L, {literal_location})"

    elif operand in register_codes.keys():
        # reg
        reg_index = register_codes.get(operand)
        return f"({reg_index})"

    elif operand in condition_codes.keys():
        # cond
        cond_index = condition_codes.get(operand)
        return f"({cond_index})"        

    elif operand.isnumeric():
        return f"(C, {operand})"

    elif '+' in operand or '-' in operand:
        # constant
        if '+' in operand:
            operands = operand.split('+')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            solution: int = int(symbol_location_counter) + int(operands[1])
            return f"(C, {solution})"
        else:
            operands = operand.split('+')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            solution: int = int(symbol_location_counter) - int(operands[1])
            return f"(C, {solution})"
        
    else:
        # symbol
        insert_in_symbol_table(operand, forward_ref=True)
        symbol_location = get_symbol_location(operand)
        return f"(S, {symbol_location})"


def handle_imperative_statement(label, op_code, operand_1, operand_2):
    type_of_opcode, opcode_ic_val = op_tab.get(op_code)

    output_line = f"({type_of_opcode},{opcode_ic_val})"

    output_line += output_operand(operand_1)

    output_line += output_operand(operand_2)

    ic_code.append(output_line)

    location_counter += 1


def handle_assembler_directive(label, op_code, operand_1, operand_2):
    if op_code == "ORIGIN" or op_code == "START":
        pass
    
    elif op_code == "END" or op_code == "LTORG":
        pass

    elif op_code == "EQU":
        pass

def handle_declarative(label, op_code, operand_1, operand_2):
    if op_code == "DC":
        pass
    elif op_code == "DS":
        pass

def main():
    # Output storage
    global ic_code
    ic_code : list[str] = []

    # define symbol table, literal table and pool table
    global symbol_table, literal_table, pool_table
    symbol_table : list[tuple[str, int]] = []
    literal_table : list[tuple[str, int]] = []
    pool_table : list[int] = []

    # Step 1: Read File
    source_line_tokens = read_file()

    # Step 2: Initialize Location counter
    global location_counter
    location_counter = 0

    for i in range(0, len(source_line_tokens)):
        # Read Card
        card = source_line_tokens[i]

        # tokenize line
        [ label, op_code, operand_1, operand_2 ] = tokenize_line(card)

        if label != "":
            insert_in_symbol_table(label, forward_ref=False)

        
        if op_code != "":

            type_of_opcode, opcode_ic_val = op_tab.get(op_code)

            if type_of_opcode == "IS":
                handle_imperative_statement(label, op_code, operand_1, operand_2)
            
            elif type_of_opcode == "AD":
                handle_assembler_directive(label, op_code, operand_1, operand_2)
            
            elif type_of_opcode == "DL":
                handle_declarative(label, op_code, operand_1, operand_2)

            

if __name__ == '__main__':
    main()