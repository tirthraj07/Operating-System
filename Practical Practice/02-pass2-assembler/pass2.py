'''
Start from def main() -> Entry point of the program
'''

source_code : list[list[str]] = []
symbol_table : list[tuple[str, int]] = []
literal_table : list[tuple[str, int]] = []

location_counter : int = 0

output_lines : list[str] = []

testcase_folder:str = ""

def read_source_code() -> None :
    global source_code
    source_code_file = f"{testcase_folder}/ic.txt"
    source_contents = ""

    with open(source_code_file, "r") as file:
        source_contents = file.read()
    
    source_code = [ line.split(")(") for line in source_contents.split("\n") ]
    


def read_symbol_table() -> None:
    global symbol_table
    source_code_file = f"{testcase_folder}/symbol_table.txt"
    source_contents = ""

    with open(source_code_file, "r") as file:
        source_contents = file.read()
    
    # print(source_contents.split('\n'))

    source_code_list = source_contents.split('\n')
    for line in source_code_list:
        line_tokens = line.split(" ")
        symbol = line_tokens[0]
        lc = line_tokens[1]
        symbol_table.append([symbol, int(lc)])    


def read_literal_table() -> None:
    global literal_table
    source_code_file = f"{testcase_folder}/literal_table.txt"
    source_contents = ""

    with open(source_code_file, "r") as file:
        source_contents = file.read()
    
    source_code_list = source_contents.split('\n')
    for line in source_code_list:
        line_tokens = line.split(" ")
        literal = line_tokens[0]
        lc = line_tokens[1]
        literal_table.append([literal, int(lc)])    


def parse_opcode(opcode: str) -> tuple[str, int] :
    opcode_tokens = opcode.strip('(').strip(')').split(',')
    opcode_type = opcode_tokens[0]
    opcode_val = int(opcode_tokens[1].strip())
    return opcode_type, opcode_val

def parse_operand(operand: str) -> tuple[str|None, int]:
    operand_tokens = operand.strip('(').strip(')').split(',')
    if len(operand_tokens) == 1:
        operand_type = None
        operand_val = int(operand_tokens[0].strip())
        return operand_type, operand_val
    else:
        operand_type = operand_tokens[0]
        operand_val = int(operand_tokens[1].strip())
        return operand_type, operand_val



def parse_card(card:list[str]) -> tuple[str, int, str, int, str, int]:
    opcode_type : str = ""
    opcode_val : int = 0
    operand1_type: str = ""
    operand1_val: int = 0
    operand2_type: str = ""
    operand2_val: int = 0

    if len(card) == 1:
        opcode_type, opcode_val = parse_opcode(card[0])

    elif len(card) == 2:
        opcode_type, opcode_val = parse_opcode(card[0])
        operand_type, operand_val = parse_operand(card[1])
        if operand_type == None:
            operand1_type = operand_type
            operand1_val = operand_val
        else:
            operand2_type = operand_type
            operand2_val = operand_val

    elif len(card) == 3:
        opcode_type, opcode_val = parse_opcode(card[0])
        operand1_type, operand1_val = parse_operand(card[1])
        operand2_type, operand2_val = parse_operand(card[2])

    return opcode_type, opcode_val, operand1_type, operand1_val, operand2_type, operand2_val



def main():
    read_source_code()
    read_symbol_table()
    read_literal_table()
    global location_counter
    location_counter = 0

    for card in source_code:
        opcode_type, opcode_val, operand1_type, operand1_val, operand2_type, operand2_val = parse_card(card)

        if opcode_type == "AD" and (opcode_val == 1 or opcode_val == 3) :
            location_counter = operand2_val;
        
        elif opcode_type == "IS":
            if operand2_val != 0:
                if operand2_type == "S":
                    operand2_val = symbol_table[operand2_val-1][1]
                elif operand2_type == "L":
                    operand2_val = literal_table[operand2_val-1][1]

            output_line = f"{location_counter:03d}\t{opcode_val:02d}\t{operand1_val:02d}\t{operand2_val:03d}"
            output_lines.append(output_line)
            location_counter += 1
        
        elif opcode_type == "DL":
            if opcode_val == 1:
                output_line = f"{location_counter:03d}\t00\t{operand1_val:02d}\t{operand2_val:03d}"
                output_lines.append(output_line)
                location_counter += 1

            elif opcode_val == 2:
                for _ in range(0, operand2_val):
                    output_line = f"{location_counter:03d}\t00\t00\t000"
                    location_counter += 1
                    output_lines.append(output_line)


    for line in output_lines:
        print(line)


if __name__ == '__main__':
    testcase_folder = str(input("Input testcase folder: "))
    main()