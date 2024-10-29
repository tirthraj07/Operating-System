'''
This is a simplified version of pass 1 assembler compared to one I did during our lab sessions
Does't contain syntax and sematic analysis and error detection and is built on TRUST that the input provided is valid else you wouldn't know where or which error has occurred. (Happy DEBUGGING :) )
But probably what they expect during practical exams due to time constraints

Reduced the code from ~700 lines (Java version) to ~400 lines (this version). Thank you python :)

Refer to the flowchart in the folder for more information about the program

def main() -> Entry Point to the program. Start there and follow the flowchart. You'll understand the code then easily
'''

op_tab : dict[ str, tuple [str, int]] = {
    "STOP"      : ( "IS" , 0 ) , 
    "ADD"       : ( "IS" , 1) ,
    "SUB"       : ( "IS" , 2) ,
    "MULT"      : ( "IS" , 3) ,
    "MOVER"     : ( "IS" , 4) ,
    "MOVEM"     : ( "IS" , 5) ,
    "COMP"      : ( "IS" , 6) ,
    "BC"        : ( "IS" , 7) ,
    "DIV"       : ( "IS" , 8) , 
    "READ"      : ( "IS" , 9) , 
    "PRINT"     : ( "IS" , 10) ,

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

# Output storage
ic_code : list[str] = []

# define symbol table, literal table and pool table

# list of symbol, location_counter
symbol_table : list[list[str, int]] = []
# list of literals, location_counter, pool
literal_table : list[list[str, int, str]] = []
# list of pools
pool_table : list[str] = ["#1"]

# define location counter
location_counter: int = 0

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

# forward ref -> symbol is used before it is defined. If forward_ref = True then assign '-1' as location counter for symbol
# if location parameter is not given then and forward ref = False, then assign the current location_counter value
def insert_in_symbol_table(symbol: str, forward_ref:bool, location=None):
    if forward_ref:
        # check if the (symbol,current_pool) already exists. If not, then insert new one
        for i in range(0, len(symbol_table)):
            if symbol_table[i][0] == symbol:
                return
        lst:list[str,int,str] = [symbol, -1]
        symbol_table.append(lst)

    else:
        new_symbol_location = location if location is not None else location_counter

        for i in range(0, len(symbol_table)):
            if symbol_table[i][0] == symbol:
                symbol_table[i][1] = new_symbol_location
                return
            
        lst:list[str,int,str] = [symbol, new_symbol_location]
        symbol_table.append(lst)
        

def insert_in_literal_table(literal: str):
    # fetch the current pool
    current_pool = pool_table[len(pool_table)-1]
    
    for i in range(0, len(literal_table)):
        if literal_table[i][0] == literal and literal_table[i][2] == current_pool:
            literal_table[i][1] = -1
            return
    lst:list[str, int, str] = [literal, -1, current_pool]
    literal_table.append(lst)


# returns the (index+1) location in literal_table not location counter!
def get_literal_location(literal: str) -> int:
    # fetch the current pool
    current_pool = pool_table[len(pool_table)-1]
    
    for i in range(0, len(literal_table)):
        if literal_table[i][0] == literal and literal_table[i][2] == current_pool:
            return i+1
        
    return -1

# returns the (index+1) location in symbol_table not location counter!
def get_symbol_location(symbol: str) -> int:

    for i in range(0, len(symbol_table)):
        if symbol_table[i][0] == symbol:
            return i+1
    
    return -1

# returns the location_counter of the literal in literal_table
def get_literal_location_counter(literal: str) -> int:
    # fetch the current pool
    current_pool = pool_table[len(pool_table)-1]
    
    for i in range(0, len(literal_table)):
        if literal_table[i][0] == literal and literal_table[i][2] == current_pool:
            return literal_table[i][1]
        
    return -1

# returns the location_counter of the symbol in symbol_table
def get_symbol_location_counter(symbol:str) -> int:
    for i in range(0, len(symbol_table)):
        if symbol_table[i][0] == symbol:
            return symbol_table[i][1]
    
    return -1

def create_new_pool() -> int:
    global location_counter
    # fetch the current pool
    current_pool = pool_table[len(pool_table)-1]

    # find all the literals that belong to current_pool but have location_counter = -1
    for i in range(0, len(literal_table)):
        if literal_table[i][1] == -1 and literal_table[i][2] == current_pool:
            literal_table[i][1] = location_counter
            location_counter += 1
            output_line = f"(DL, 02) (C, {literal_table[i][0][1:]})"
            ic_code.append(output_line)
            
    new_pool = "#" + str(int(current_pool[1:])+1)
    pool_table.append(new_pool)

def output_operand(operand:str) -> str:
    if operand == "":
        return ""
    
    # operand can be a symbol, literal, reg, cond, constant
    if operand[0] == "=":
        # literal
        insert_in_literal_table(operand[1:])
        literal_location: int = get_literal_location(operand[1:])
        return f" (L, {literal_location})"

    elif operand in register_codes.keys():
        # reg
        reg_index = register_codes.get(operand)
        return f" ({reg_index})"

    elif operand in condition_codes.keys():
        # cond
        cond_index = condition_codes.get(operand)
        return f" ({cond_index})"        

    elif operand.isnumeric():
        return f" (C, {operand})"

    elif '+' in operand or '-' in operand:
        # constant
        if '+' in operand:
            operands = operand.split('+')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            solution: int = int(symbol_location_counter) + int(operands[1])
            return f" (C, {solution})"
        else:
            operands = operand.split('-')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            solution: int = int(symbol_location_counter) - int(operands[1])
            return f" (C, {solution})"
        
    else:
        # symbol
        insert_in_symbol_table(operand, forward_ref=True)
        symbol_location = get_symbol_location(operand)
        return f" (S, {symbol_location})"


def handle_imperative_statement(label, op_code, operand_1, operand_2):
    global location_counter
    type_of_opcode, opcode_ic_val = op_tab.get(op_code)

    output_line = f"({type_of_opcode}, {opcode_ic_val})"

    output_line += output_operand(operand_1)

    output_line += output_operand(operand_2)

    ic_code.append(output_line)

    # increment location counter for imperative statements
    location_counter += 1


def handle_assembler_directive(label:str, op_code:str, operand_1:str, operand_2:str):
    global location_counter
    type_of_opcode, opcode_ic_val = op_tab.get(op_code)

    output_line = f"({type_of_opcode}, {opcode_ic_val})"

    # assuming that there is only operand_1 and it is of constant type
    if op_code == "ORIGIN" or op_code == "START":
        output_line += output_operand(operand_1)
        ic_code.append(output_line)
        if operand_1.isnumeric():
            # if directly a numeric then assign it as location counter   
            location_counter = int(operand_1)
        elif '+' in operand_1:
            operands = operand_1.split('+')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            location_counter = int(symbol_location_counter) + int(operands[1])
        elif '-' in operand_1:
            operands = operand_1.split('-')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            location_counter = int(symbol_location_counter) - int(operands[1])
    
    elif op_code == "END" or op_code == "LTORG":
        # we only print the output_line for END, not LTORG. For Both, we append the DL,02 line
        if op_code == "END":
            if operand_1 != "":
                output_line += output_operand(operand_1)
            ic_code.append(output_line)
        create_new_pool()

    # assuming that it is of format label opcode operand and operand is of type symbol or Constant
    elif op_code == "EQU":
        # if operand is of type constant
        if operand_1.isnumeric():
            output_line += f" (C, {operand_1})"
            insert_in_symbol_table(symbol=label, forward_ref=False, location=operand_1)            
        elif '+' in operand_1:
            operands = operand_1.split('+')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            location = int(symbol_location_counter) + int(operands[1])
            insert_in_symbol_table(symbol=label, forward_ref=False, location=location) 
            output_line += f" (C, {location})"           
        elif '-' in operand_1:
            operands = operand_1.split('-')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            location = int(symbol_location_counter) - int(operands[1])
            insert_in_symbol_table(symbol=label, forward_ref=False, location=location)  
            output_line += f" (C, {location})"          
        else:
            # if operand if of type symbol
            symbol_lc = get_symbol_location_counter(operand_1)
            insert_in_symbol_table(symbol=label, forward_ref=False, location=symbol_lc)
            output_line += f" (C, {get_symbol_location_counter(label)})"
        ic_code.append(output_line)


    # do not increment location counter for assembler directives

def handle_declarative(label:str, op_code:str, operand_1:str, operand_2:str):
    global location_counter
    type_of_opcode, opcode_ic_val = op_tab.get(op_code)

    output_line = f"({type_of_opcode}, {opcode_ic_val})"
    output_line += f" (C, {operand_1})"
    ic_code.append(output_line)

    # define constant -> increment location_counter by 1. Assuming operand_1 is given
    if op_code == "DC":
        location_counter += 1
        
    # define space -> increment location_counter by the operand_1
    elif op_code == "DS":
        if operand_1.isnumeric():
            location_counter += int(operand_1)
        elif '+' in operand_1:
            operands = operand_1.split('+')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            location_counter += int(symbol_location_counter) + int(operands[1])
        elif '-' in operand_1:
            operands = operand_1.split('-')
            symbol_location_counter = get_symbol_location_counter(operands[0])
            location_counter += int(symbol_location_counter) - int(operands[1])

def print_symbol_table():
    print("--- Symbol Table ---")
    for i in range(0, len(symbol_table)):
        print(f"{i+1}.\t\t{symbol_table[i][0]}\t\t{symbol_table[i][1]}")

def print_literal_table():
    pool = pool_table[0]
    index = 1
    print("--- Literal Table ---")

    for i in range(0, len(literal_table)):
        if literal_table[i][2] != pool:
            index = 1
            pool = literal_table[i][2]
            print()
        print(f"{index}.\t\t{literal_table[i][0]}\t\t{literal_table[i][1]}")
        index += 1

def print_pool_table():
    # note: one extra pool gets generated after to END statement so don't print it
    print("--- Pool Table ---")
    for i in range(0, len(pool_table)-1):
        print(pool_table[i])

def main():
    # Step 1: Read File
    source_line_tokens: list[list[str]] = read_file()

    # Step 2: Initialize Location counter
    global location_counter
    location_counter = 0

    for i in range(0, len(source_line_tokens)):
        # Step 3: Read Card
        card = source_line_tokens[i]

        # tokenize line
        label, op_code, operand_1, operand_2 = tokenize_line(card)

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

    for i in range(0, len(ic_code)):
        print(ic_code[i])

    
    print_symbol_table()

    print_literal_table()

    print_pool_table()


if __name__ == '__main__':
    main()