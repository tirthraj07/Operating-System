'''
def main() is the start of the program
'''

optab : dict[tuple[str, int]] = {
    
    # Imperative Statement
    "STOP"      :       ["IS", 0],
    "ADD"       :       ["IS", 1],
    "SUB"       :       ["IS", 2],
    "MULT"      :       ["IS", 3],
    "MOVER"     :       ["IS", 4],
    "MOVEM"     :       ["IS", 5],
    "COMP"      :       ["IS", 6],
    "BC"        :       ["IS", 7],
    "DIV"       :       ["IS", 8],
    "READ"      :       ["IS", 9],
    "PRINT"     :       ["IS", 10],

    # Assembler Directive
    "START"     :       ["AD", 1],
    "END"       :       ["AD", 2],
    "ORIGIN"    :       ["AD", 3],
    "EQU"       :       ["AD", 4],
    "LTORG"     :       ["AD", 5],

    # Declarative 
    "DC"        :       ["DL", 1],
    "DS"        :       ["DL", 2]
}

register_codes : dict[str, int] = {
    "AREG"      :       1,
    "BREG"      :       2,
    "CREG"      :       3,
    "DREG"      :       4
}

cond_codes : dict[str, int] = {
    "LT"        :       1,
    "LE"        :       2,
    "EQ"        :       3,
    "GT"        :       4,
    "GE"        :       5,
    "ANY"       :       6

}


ic_code : list[str] = [];
location_counter : int = 0;
source_lines : list[list[str]];

# Symbol Table, Literal Table, Pool Table

symbol_table  : list[list[str, int]] = []
literal_table : list[list[str, int, str]] = []
pool_table    : list[str] = ["#1"]

def read_file():
    global source_lines
    source_file_location = str(input("Enter Source File Location: "))
    source_content = ""
    with open(source_file_location, "r") as file:
        source_content = file.read()
    
    lines = source_content.split("\n");    
    source_lines = [ line.split() for line in lines ] 
    
def tokenize_line(line: list[str]) -> tuple[str, str, str, str] :
    label = ""
    opcode = ""
    operand1 = ""
    operand2 = ""

    if len(line) == 1 and line[0] in optab.keys():
        opcode = line[0]
    elif len(line) == 1:
        label = line[0]
    
    if len(line) == 2 and line[0] in optab.keys():
        opcode = line[0]
        operand1 = line[1]
    elif len(line) == 2:
        label = line[0]
        opcode = line[1]

    if len(line) == 3 and line[0] in optab.keys():
        opcode = line[0]
        operand1 = line[1]
        operand2 = line[2]
    elif len(line) == 3:
        label = line[0]
        opcode = line[1]
        operand1 = line[2]
    
    if len(line) == 4:
        label = line[0]
        opcode = line[1]
        operand1 = line[2]
        operand2 = line[3]
    
    return label, opcode, operand1, operand2

def increment_location_counter(val:int = 1):
    global location_counter
    location_counter += val

def set_location_counter(lc:int):
    global location_counter
    location_counter = lc

def get_symbol_position(symbol: str) -> int:
    for i in range(0, len(symbol_table)):
        if symbol_table[i][0] == symbol:
            return i+1
    return -1

def get_literal_position(literal) -> int:
    current_pool = pool_table[len(pool_table)-1]
    for i in range(0, len(literal_table)):
        if literal_table[i][0] == literal and literal_table[i][2] == current_pool:
            return i+1
    return -1

def get_symbol_location_counter(symbol: str) -> int:
    index = get_symbol_position(symbol) - 1
    if (index < 0): 
        return -1
    else: return symbol_table[index][1]

# forward_ref -> True : when variable if used before its declaration
# forward_ref = True -> lc = -1
# forward_ref = False -> if lc given then (label, lc) else (label, current location counter)

def insert_into_symbol_table(symbol:str, lc:int|None=None, forward_ref:bool=True):
    position = get_symbol_position(symbol) 
    if lc is None:
        lc = location_counter

    if forward_ref:
        if position == -1:
            symbol_table.append([symbol, -1])
    else:
        if position == -1:
            symbol_table.append([symbol, lc])
        else:
            symbol_table[position - 1][1] = lc

def insert_into_literal_table(literal):
    position = get_literal_position(literal)

    if position == -1:
        current_pool = pool_table[len(pool_table)-1]
        literal_table.append([literal, -1, current_pool])


# the 0th position checks if the operand is a constant or not and 1th position is the value of constant if return[0] is True
def get_constant_value(operand) -> tuple[bool, int]:
    is_constant: bool = False;
    operand_val: int = None

    if operand == "":
        is_constant = False

    elif operand.isnumeric():
        is_constant = True
        operand_val = int(operand)
    
    elif '+' in operand:
        is_constant = True
        operand_tokens = operand.split("+")
        symbol = operand_tokens[0]
        offset = int(operand_tokens[1])
        symbol_lc = get_symbol_location_counter(symbol)
        operand_val = symbol_lc + offset

    elif '-' in operand:
        is_constant = True
        operand_tokens = operand.split("-")
        symbol = operand_tokens[0]
        offset = int(operand_tokens[1])
        symbol_lc = get_symbol_location_counter(symbol)
        operand_val = symbol_lc - offset

    return is_constant, operand_val

def parse_operand(operand: str) -> tuple[str, int|str] :
    operand_type = ""
    operand_val = ""

    if operand[0] == '=':
        operand_type = "L"
        literal = operand[1:]
        insert_into_literal_table(literal)
        operand_val = get_literal_position(literal)
    
    elif operand in cond_codes:
        operand_type = "COND"
        operand_val = cond_codes.get(operand)

    elif operand in register_codes:
        operand_type = "REG"
        operand_val = register_codes.get(operand)

    elif get_constant_value(operand)[0] == True:
        operand_type = "C"
        operand_val = get_constant_value(operand)[1]

    else:
        operand_type = "S"
        insert_into_symbol_table(operand, forward_ref=True)
        operand_val = get_symbol_position(operand)

    return operand_type, operand_val

def get_operand_str(operand: str) -> str:
    if operand == "":
        return ""
    
    operand_type, operand_val = parse_operand(operand)
    if operand_type == "REG" or operand_type == "COND":
        return f" ({operand_val})"
    else:
        return f" ({operand_type}, {operand_val})"

def create_new_pool():
    current_pool = pool_table[len(pool_table)-1]
    pool_number = int(current_pool[1:])

    for i in range(0, len(literal_table)):
        if literal_table[i][1] == -1 and literal_table[i][2] == current_pool:
            literal_table[i][1] = location_counter
            output_line = f"(DL, 01) (C, {literal_table[i][0][1:]})"
            ic_code.append(output_line)
            increment_location_counter()

    pool_table.append(f"#{pool_number+1}")


def print_ic():
    for i in range(0, len(ic_code)):
        print(ic_code[i])

def print_symbol_table():
    for i in range(0, len(symbol_table)):
        print(f"{i+1}\t{symbol_table[i][0]}\t{symbol_table[i][1]}")

def print_literal_table():
    pool = "#1"
    i = 1
    for literal_entry in literal_table:
        if literal_entry[2] != pool:
            pool = literal_entry[2]
            print()
        print(f"{i}\t{literal_entry[0]}\t{literal_entry[1]}")
        i+= 1

def print_pool_table():
    for i in range(0, len(pool_table)-1):
        print(pool_table[i])

def handle_imperative_statement(label: str, opcode: str, operand1: str, operand2: str):
    global ic_code
    _, opcode_ic = optab.get(opcode)
    output_line = f"(IS, {opcode_ic})"
    output_line += get_operand_str(operand1)
    output_line += get_operand_str(operand2)
    ic_code.append(output_line)
    increment_location_counter();



def handle_assembler_directive(label: str, opcode: str, operand1: str, operand2: str):
    global ic_code
    _, opcode_ic = optab.get(opcode)
    output_line = f"(AD, {opcode_ic})"

    if opcode == "START" or opcode == "ORIGIN":
        is_constant, constant_value = get_constant_value(operand1)
    
        if is_constant == False:
            raise Exception("START and ORIGIN must have operand (constant type)")
        
        output_line += get_operand_str(operand1)
        ic_code.append(output_line)
        set_location_counter(constant_value)

    elif opcode == "END" or opcode == "LTORG":
        if opcode == "END":
            output_line += get_operand_str(operand1)
            ic_code.append(output_line)
        
        create_new_pool()
    
    elif opcode == "EQU":
        operand_type, operand_val = parse_operand(operand1)

        if operand_type not in ["S", "C"]:
            raise Exception("EQU must have operand (constant or symbol or equivalent)")

        if operand_type == "C":
            insert_into_symbol_table(label, operand_val, forward_ref=False)

        else:
            if operand_val == -1: raise Exception("Symbol must be initialized before using in EQU")
            symbol_lc = symbol_table[operand_val-1][1]
            insert_into_symbol_table(label, symbol_lc, forward_ref=False)

        output_line += get_operand_str(operand1)
        ic_code.append(output_line)




def handle_declarative(label: str, opcode: str, operand1: str, operand2: str):
    global ic_code
    _, opcode_ic = optab.get(opcode)

    output_line = f"(DL, {opcode_ic})"
    output_line += get_operand_str(operand1)
    ic_code.append(output_line)


    if opcode == "DC":
        increment_location_counter(1)
    
    elif opcode == "DS":
        is_constant, const_value = get_constant_value(operand1)
        if is_constant == False:
            raise Exception("Declare Space must have operand (constant type or equivalent)")

        increment_location_counter(const_value)

def main():
    # START
    read_file()

    # Initialize LC
    global location_counter
    location_counter = 0

    for line in source_lines:
        if location_counter == 1:
            print(line)

        label, opcode, operand1, operand2 = tokenize_line(line)

        if label != "":
            insert_into_symbol_table(label, forward_ref=False)
        
        if opcode != "":
            opcode_type, _ = optab.get(opcode)

            if opcode_type == "IS":
                handle_imperative_statement(label, opcode, operand1, operand2)
            
            elif opcode_type == "AD":
                handle_assembler_directive(label, opcode, operand1, operand2)

            elif opcode_type == "DL":
                handle_declarative(label, opcode, operand1, operand2)

    # END
    # Print IC
    print_ic()
    # Print Symbol Table
    print_symbol_table()
    # Print Literal Table
    print_literal_table()
    # Print Pool Table
    print_pool_table()


if __name__ == '__main__':
    main()