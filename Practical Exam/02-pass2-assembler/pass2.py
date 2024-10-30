'''
This is a simplified version of pass 2 without any error detection.

Note that each testcase folder must have following text files named exactly as below
- symbol_table.txt
- literal_table.txt
- pool_table.txt
- intermediate_code.txt

Each entry in each files MUST be in SPACE SEPARATED FORMAT

Start Reading the code from def main() to understand the flow :)

'''

# file locations
ic_location: str = ""
symbol_table_location: str = ""
literal_table_location: str = ""
pool_table_location: str = ""

# [ [symbol, location_counter] ]
symbol_table : list[list[str, int]] = []

# [ [symbol, location_counter] ]
literal_table : list[list[str, int]] = []

# [ "#1", "#2", .. ]
pool_table : list[str] = []

# [ [ "(AD,01)", "(C,100)" ] ]
ic_code : list[list[str]] = []

location_counter = 0


# output storage
output_code: list[str] = []

def read_symbol_table():
    global symbol_table
    src_contents: str = ""

    with open(symbol_table_location, "r") as file:
        src_contents = file.read()

    src_lines: list[str] = src_contents.split('\n')
    for line in src_lines:
        line_token = line.split()
        if len(line_token) == 2:
            symbol_table.append([line_token[0], int(line_token[1])])


def read_literal_table():
    global literal_table
    src_contents: str = ""

    with open(literal_table_location, "r") as file:
        src_contents = file.read()

    src_lines: list[str] = src_contents.split('\n')
    for line in src_lines:
        line_token = line.split()
        if len(line_token) == 2:
            literal_table.append([line_token[0], int(line_token[1])])

def read_pool_table():
    global pool_table
    src_content: str = ""
    with open(pool_table_location, "r") as file:
        src_content = file.read()
    pool_table = src_content.split("\n")

def read_intermediate_code():
    global ic_code
    src_contents: str = ""
    with open(ic_location, "r") as file:
        src_contents = file.read()
    src_lines = src_contents.split('\n')
    ic_code = [ line.split(') (') for line in src_lines ]
    

def parse_opcode(token: str) -> tuple[str, int]:
    opcode_tokens = token.strip("(").strip(")").split(", ")
    opcode_type = opcode_tokens[0]
    opcode_val = int(opcode_tokens[1])
    return (opcode_type, opcode_val)

def parse_operand(token: str) -> tuple[str|None, int]:
    operand_tokens = token.strip("(").strip(")").split(", ")
    # for COND and REG
    if len(operand_tokens) == 1:
        return (None, int(operand_tokens[0]))
    
    if operand_tokens[0] == "S":
        symbol_location = int(operand_tokens[1])
        symbol_index  = symbol_location - 1
        symbol, symbol_lc = symbol_table[symbol_index]
        return (operand_tokens[0], symbol_lc)

    if operand_tokens[0] == "L":
        literal_location = int(operand_tokens[1])
        literal_index = literal_location - 1
        literal, literal_lc = literal_table[literal_index]
        return (operand_tokens[0], literal_lc)

    if operand_tokens[0] == "C":
        return (operand_tokens[0], int(operand_tokens[1]))

def change_location_counter(location: int):
    global location_counter
    location_counter = location

def increment_location_counter():
    global location_counter
    location_counter += 1

def main():
    # Store the symbol table
    read_symbol_table()

    # Store the literal table
    read_literal_table()

    # Store the pool table
    read_pool_table()

    # Read the intermediate code
    read_intermediate_code()

    for i in range(0, len(ic_code)):
        card = ic_code[i]
        # only opcode
        if len(card) == 1:
            opcode_type, opcode_val = parse_opcode(card[0])

            if opcode_type == "AD":
                pass
            else:
                output_line = f"{location_counter}\t{opcode_val}\t0\t0"
                output_code.append(output_line)
                increment_location_counter()


        # opcode operand_1
        elif len(card) == 2:
            opcode_type, opcode_val = parse_opcode(card[0])
            operand_1_type, operand_1_val = parse_operand(card[1])

            if opcode_type == "AD":
                # if START or ORIGIN, then change the LC
                if opcode_val == 1 or opcode_val == 3:
                    change_location_counter(operand_1_val)
            elif opcode_type == "DL":
                # when define constant -> just print the constant value in last column
                if opcode_val == 1:
                    output_line = f"{location_counter}\t0\t0\t{operand_1_val}"
                    output_code.append(output_line)
                    increment_location_counter()
                # when define space -> print 00 00 00 * the operand value
                elif opcode_val == 2:
                    for i in range(0, operand_1_val):
                        output_line = f"{location_counter}\t0\t0\t0"
                        output_code.append(output_line)
                        increment_location_counter()
            else:
                if operand_1_type is None:
                    output_line = f"{location_counter}\t{opcode_val}\t{operand_1_val}\t0"
                else:
                    output_line = f"{location_counter}\t{opcode_val}\t0\t{operand_1_val}"
                output_code.append(output_line)
                increment_location_counter()


        # opcode operand_1 operand_2
        elif len(card) == 3:
            opcode_type, opcode_val = parse_opcode(card[0])
            operand_1_type, operand_1_val = parse_operand(card[1])
            operand_2_type, operand_2_val = parse_operand(card[2])

            if opcode_type == "AD":
                pass
            else:
                output_line = f"{location_counter}\t{opcode_val}\t{operand_1_val}\t{operand_2_val}"
                output_code.append(output_line)
                increment_location_counter()

    for i in range(0, len(output_code)):
        print(output_code[i])
        

if __name__ == '__main__':
    testcase_location = str(input("Enter Testcase folder : "))
    
    literal_table_location = testcase_location + "/literal_table.txt"
    symbol_table_location = testcase_location + "/symbol_table.txt"
    pool_table_location = testcase_location + "/pool_table.txt"
    ic_location = testcase_location + "/intermediate_code.txt"

    main()