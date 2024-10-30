'''
Simplified version of pass-1 macro-processor
It does not do any syntax or semantic analysis like i did during our actual lab sessions
~ 150 lines of code

def main() -> Entry point of the program

Check the flowchart for more information
start reading the flowchart and def main(), you'll understand the flow of code
'''

input_file_location: str = ""
input_line_tokens: list[list[str]] = ""

# Output storage
output_lines: list[str] = []

# Structures

# [ "Parameter-Name" ]
PNT: list[str] = []

# [ [ "Macro name", pp, kp, MDTP, KPDTP, PNTP ] ]
MNT: list[list[str, int, int, int, int, int]] = []

# [ "Macro Line" ]
MDT: list[str] = []

# [ [ "Keyword Param Name", "Default Argument" ] ]
KPDT: list[list[str, str]] = []

# Pointers -> There is no actual use of these. Idk, why they have given this in flowchart
MNTC: int = 0
MDTC: int = 0

# reads input file and stores the line tokens in input_line_tokens
def read_input_file():
    global input_line_tokens
    input_file_contents: str = ""
    with open(input_file_location, "r") as file:
        input_file_contents = file.read()
    input_lines = input_file_contents.split("\n")
    input_line_tokens = [line.split() for line in input_lines]

def parse_operand(operand_str: str) -> tuple[str, str, str]:
    type_of_operand: str = ""
    operand: str = ""
    default_value: str = ""

    if '=' in operand_str:
        type_of_operand = "keyword"
        operand_tokens = operand_str.split("=")
        operand = operand_tokens[0]
        default_value = operand_tokens[1] if len(operand_tokens) == 2 and operand_tokens[1] != "" else "_"
        return type_of_operand, operand, default_value
    else:
        type_of_operand = "positional"
        operand = operand_str
        return type_of_operand, operand, default_value


# MACRO-NAME, ..Arguments
def parse_macro_definition(card: str):
    global PNT, KPDT, MNT, MNTC

    macro_name = card[0]
    pp = 0
    kp = 0
    MDTP = len(MDT) + 1
    KPDTP = len(KPDT) + 1
    PNTP = len(PNT) + 1

    for i in range(1, len(card)):
        type_of_operand, operand, default_value = parse_operand(card[i])
        # Positional parameter
        if type_of_operand == "positional":
            PNT.append(operand)
            pp += 1
        # Keyword parameter
        else:
            PNT.append(operand)
            KPDT.append([operand, default_value])
            kp += 1

    MNT.append([macro_name, pp, kp, MDTP, KPDTP, PNTP])
    MNTC += 1


def substitute_index_notations_for_arguments(line_tokens: list[str]) -> str:
    macro_line: str = ""
    
    mnt_line = MNT[len(MNT)-1]

    pnt_start = mnt_line[5] - 1

    total_params = mnt_line[1] + mnt_line[2] # pp + kp

    for token in line_tokens:
        if '&' in token:
            operand_position: int = -1
            for i in range(pnt_start, pnt_start + total_params + 1):
                if PNT[i] == token:
                    operand_position = i+1
                    break
            macro_line += f"(P, {operand_position}) "
        else:
            macro_line += token + " "

    return macro_line.strip()

def insert_into_MDT(line: str):
    global MDT, MDTC
    MDT.append(line)
    MDTC += 1

def main():
    # Start Pass 1

    # Step 1: Read input file
    read_input_file()

    # Step 2: Set MNTC = 1 and MDTC = 1
    global MNTC, MDTC
    MNTC = 1
    MDTC = 1

    i: int = 0
    while i < len(input_line_tokens):
        
        # Step 3: Read Card
        card = input_line_tokens[i]

        # Step 4: Macro Opcode? 
        if "MACRO" in card:
            # Step 5: read next source card
            macro_definition_card = input_line_tokens[i+1]

            # Step 6: Enter Macro Name in MNT and Prepare Argument List
            parse_macro_definition(macro_definition_card)
            
            i = i+2
            # While not MEND:
            while "MEND" not in input_line_tokens[i]:
                line = input_line_tokens[i]

                # Step 7: substitute index notations for arguments
                new_line = substitute_index_notations_for_arguments(line)
                insert_into_MDT(new_line)
                i += 1
            insert_into_MDT("MEND")
            i += 1
        else:
            # Step 5: Write copy of source card
            output_line = " ".join(card)
            output_lines.append(output_line)
            i += 1

    # --- END ---

    # print output
    print("----- OUTPUT -----")
    for i in range(0, len(output_lines)):
        print(output_lines[i])

    # print MDT
    print("----- MDT -----")
    for i in range(0, len(MDT)):
        print(MDT[i])

    print("----- MNT -----")
    for i in range(0, len(MNT)):
        print(f"{MNT[i][0]}\t{MNT[i][1]}\t{MNT[i][2]}\t{MNT[i][3]}\t{MNT[i][4]}\t{MNT[i][5]}")

    print("----- PNT -----")
    for i in range(0, len(PNT)):
        print(f"{i+1}\t{PNT[i]}")

    print("----- KPDT -----")
    for i in range(0, len(KPDT)):
        print(f"{KPDT[i][0]}\t{KPDT[i][1]}")


if __name__ == '__main__':
    input_file_location = str(input("Enter testcase file : "))
    main()