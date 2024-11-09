'''
def main() -> Entry point to the program
'''
              # Name pp kp MDTP KPDT PNTP
MNT:list[tuple[str,int, int, int, int, int]] = []
MDT: list[str] = []
KPDT: list[tuple[str, str]]  = []
PNT: list[str] = []

source_location: str = ""
source_code : list[list[str]] = []
output_lines: list[str] = []


def read_lines() -> None:
    global source_code
    source_content = ""
    with open(source_location, "r") as file:
        source_content = file.read()
    
    source_lines: list[str] = source_content.split("\n")
    source_code = [ line.split() for line in source_lines ]

def analyze_macro_definition(md_tokens:list[str]) -> None:
    macro_name: str = md_tokens[0]
    pp: int = 0
    kp: int = 0
    MDTP: int = len(MDT) + 1
    KPDTP: int = len(KPDT) + 1
    PNTP: int = len(PNT) + 1

    for i in range(1, len(md_tokens)):
        if '=' in md_tokens[i]:
            param_tokens = md_tokens[i].split('=')
            parameter = param_tokens[0]
            default_argument = param_tokens[1] if len(param_tokens) > 1 and len(param_tokens[1]) > 0 else "_"
            kp += 1
            PNT.append(parameter)
            KPDT.append([parameter, default_argument])

        else:
            pp += 1
            parameter = md_tokens[i]
            PNT.append(parameter)

    MNT.append([macro_name, pp, kp, MDTP, KPDTP, PNTP])



def substitute_index_notations_for_argument(line_tokens: list[str]) -> None:
    global MDT
    mnt_definition = MNT[len(MNT) - 1]
    total_params = int(mnt_definition[1]) + int(mnt_definition[2])
    pnt_start = int(mnt_definition[5]) - 1
    

    output_line:str = ""

    for i in range(0, len(line_tokens)):
        token = line_tokens[i]
        if token[0] == '&':
            index = -1
            for j in range(0, total_params):
                if token == PNT[pnt_start + j]:
                    index = j + 1
                    break
            output_line += f"(P, {index}) "

        else:
            output_line += f"{token} "

    output_line = output_line.strip()
    MDT.append(output_line)

def print_output() -> None:
    print("----- OUTPUT -----")
    for line in output_lines:
        print(line)

def print_mnt() -> None:
    print("----- MNT -----")
    print(f"Name\tpp\tkp\tMDTP\tKPDT\tPNTP")
    for i in range(0, len(MNT)):
        print(f"{MNT[i][0]}\t{MNT[i][1]}\t{MNT[i][2]}\t{MNT[i][3]}\t{MNT[i][4]}\t{MNT[i][5]}")

def print_pnt() -> None:
    print("----- PNT -----")
    for i in range(0, len(PNT)):
        print(PNT[i])

def print_kpdt() -> None:
    print("----- KPDT -----")
    print(f"Name\tDefault")
    for i in range(0, len(KPDT)):
        print(f"{KPDT[i][0]}\t{KPDT[i][1]}")

def print_mdt() -> None:
    print("----- MDT -----")
    for line in MDT:
        print(line)

def main():
    global output_lines
    read_lines()
    
    line_number = 0

    while line_number < len(source_code):
        line_tokens = source_code[line_number]

        if 'MACRO' in line_tokens:
            line_number += 1
            macro_definition_tokens = source_code[line_number]
            # Analyse Macro Definition
            analyze_macro_definition(macro_definition_tokens)

            line_number += 1

            while(True):
                line_tokens = source_code[line_number]
                
                # Substitute Arguments to Positions from PNT
                substitute_index_notations_for_argument(line_tokens)

                if 'MEND' in line_tokens:
                    break
                line_number += 1
            line_number += 1
        else:
            output_line = ' '.join(line_tokens)
            output_lines.append(output_line)
            line_number += 1

    
    print_output()
    print_mnt()
    print_pnt()
    print_kpdt()
    print_mdt()


if __name__ == '__main__':
    source_location = str(input("Source input file: "))
    main()