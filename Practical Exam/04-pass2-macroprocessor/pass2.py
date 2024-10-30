mdt_file_location: str = ""
mnt_file_location: str = ""
kpdt_file_location: str = ""
pnt_file_location: str = ""
pass1_output_location: str = ""

mdt: list[list[str]] = []

# [ [ macro_name, pp, kp, MDTP, KPDTP, PNTP ] ]
mnt: list[list[str, int, int, int, int, int]] = []
kpdt: list[list[str, str]]
pnt: list[str]
pass1_output: list[list[str]] = []

# Define new structure for pass-2 -> APT : Actual Parameter Table
apt: list[str] = []

# Output storage
output_lines: list[str] = []

# We will tokenize the MDT so that we can use it in the future easily
def read_mdt():
    global mdt
    contents: str = ""
    with open(mdt_file_location, "r") as file:
        contents = file.read()
    lines = contents.split("\n")
    mdt = [line.split() for line in lines]

def read_mnt():
    global mnt
    contents: str = ""
    with open(mnt_file_location, "r") as file:
        contents = file.read()
    lines = contents.split("\n")
    lst = [line.split() for line in lines]
    for line in lst:
        mnt.append([line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5])])

def read_pnt():
    global pnt
    contents: str = ""
    with open(pnt_file_location, "r") as file:
        contents = file.read()
    pnt = contents.split("\n")

def read_kpdt():
    global kpdt
    contents: str = ""
    with open(kpdt_file_location, "r") as file:
        contents = file.read()
    lines = contents.split("\n")
    kpdt = [line.split() for line in lines]

def read_pass1_output():
    global pass1_output
    contents: str = ""
    with open(pass1_output_location, "r") as file:
        contents = file.read()
    lines = contents.split("\n")
    pass1_output = [line.split() for line in lines]
    
def macro_name_found(card: list[str]) -> bool:
    if len(card) == 0:
        return False
    
    for macro_name_entry in mnt:
        # First column in each entry is macro name
        # so we are checking if the card[0] matches any macro name in MNT
        if macro_name_entry[0] == card[0]:
            return True

    return False

def parse_macro_call(card: list[str]) -> tuple[str, int, int, int, list, list]:
    macro_name:str = ""
    pp:int = 0
    kp:int = 0
    total_params:int = 0

    macro_name = card[0]

    positional_params: list[str] = []
    keyword_params: list[list[str,str]] = []

    for i in range(1, len(card)):
        argument = card[i]
        total_params += 1

        if '=' in argument:
            kp += 1
            argument_tokens = argument.split("=")
            parameter, passed_arg = argument_tokens[0], argument_tokens[1]
            keyword_params.append([parameter, passed_arg])
        else:
            pp += 1
            positional_params.append(argument)

    return (macro_name, pp, kp, total_params, positional_params, keyword_params)

def get_mnt_entry(macro_name, pp, kp):
    for mnt_entry in mnt:
        if mnt_entry[0] == macro_name and mnt_entry[1] == pp and mnt_entry[2] >= kp:
            return mnt_entry
    return None

def setup_argument_list_array(positional_params:list, keyword_params:list, pnt_start:int, pnt_end:int, kpdt_start:int, kpdt_end:int):
    global apt
    apt = []
    for i in range(0,len(positional_params)):
        apt.append(positional_params[i])

    pp = len(positional_params)

    # just look at keyword params
    for i in range(pnt_start + pp, pnt_end + 1):
        keyword = pnt[i]
        found: bool = False
        for j in range(0, len(keyword_params)):
            if keyword_params[j][0] == keyword:
                apt.append(keyword_params[j][1])
                found = True
                break
        if not found:
            default_param = ""
            for j in range(kpdt_start, kpdt_end + 1):
                if kpdt[j][0] == keyword:
                    default_param = kpdt[j][1]
                    if default_param == "_":
                        print(f"Argument not provided for keyword {keyword}")
                        exit(1)
                    break
            apt.append(default_param)
    print("APT : ", apt)
    

def substitute_arguments_macro_call(line_tokens: list[str], pnt_start:int) -> str:
    output_line:str = ""
    for token in line_tokens:
        if "(" in token:
            argument_index = int(token.strip("(").strip(")").split(",")[1].strip()) - 1 - pnt_start
            output_line += apt[argument_index] + " "
        else:
            output_line += token + " "
    return output_line.strip()


def main(): 
    global output_lines

    # Step 1: Read all the input from pass 1
    read_mdt()
    read_mnt()
    read_pnt()
    read_kpdt()
    read_pass1_output()    

    for i in range(0, len(pass1_output)):
        # Read Source Card
        card = pass1_output[i]

        # Macro name found?
        if macro_name_found(card):

            macro_name, pp, kp, total_params, positional_params, keyword_params = parse_macro_call(card)    

            mnt_entry = get_mnt_entry(macro_name, pp, kp)

            if mnt_entry is None:
                print("Invalid Macro Call ->", macro_name, " Line: ", i+1)
                return

            # setup the argument list array
            pnt_start = mnt_entry[5] - 1
            pnt_end = pnt_start + mnt_entry[1] + mnt_entry[2] - 1
            kpdt_start = mnt_entry[4] - 1
            kpdt_end = kpdt_start + mnt_entry[2] - 1

            setup_argument_list_array(positional_params, keyword_params, pnt_start, pnt_end, kpdt_start, kpdt_end)

            MDT_index = mnt_entry[3] - 1

            while 'MEND' not in mdt[MDT_index]:
                macro_line = mdt[MDT_index]
                new_macro_line = substitute_arguments_macro_call(macro_line, pnt_start)
                output_lines.append(new_macro_line)
                MDT_index += 1
        else:
            output_line = " ".join(card)
            output_lines.append(output_line)

    print("--- OUTPUT ---")
    for i in range(0, len(output_lines)):
        print(output_lines[i])





if __name__ == '__main__':
    testcase_folder_location = str(input("Enter testcase folder: "))
    mdt_file_location = testcase_folder_location + "/MDT.txt"
    mnt_file_location = testcase_folder_location + "/MNT.txt"
    kpdt_file_location = testcase_folder_location + "/KPDT.txt"
    pnt_file_location = testcase_folder_location + "/PNT.txt"
    pass1_output_location = testcase_folder_location + "/pass1_output.txt"
    
    main()