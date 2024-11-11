'''
def main() -> Entry Point of the program
'''
testcase_folder: str = ""

src_lines: list[list[str]] = []
mnt: list[tuple[str, int, int, int, int]] = []
mdt: list[list[str]] = []
kpdt: list[tuple[str, str]] = []


apt: list[str] = []
output_lines : list[str] = []

def read_src() -> None:
    global src_lines
    src_content: str = ""
    src_file_location = f"{testcase_folder}/src.txt"
    with open(src_file_location, "r") as file:
        src_content = file.read()
    src_content = src_content.split('\n')
    src_lines = [ line.split() for line in src_content ] 


def read_mnt() -> None:
    global mnt
    src_content: str = ""
    src_file_location = f"{testcase_folder}/MNT.txt"
    with open(src_file_location, "r") as file:
        src_content = file.read()
    src_content = src_content.split('\n')
    for line in src_content:
        line_tokens = line.split()
        macro_name = line_tokens[0]
        pp = int(line_tokens[1])
        kp = int(line_tokens[2])
        mdtp = int(line_tokens[3])
        kpdtp = int(line_tokens[4])
        mnt.append([macro_name, pp, kp, mdtp, kpdtp])


def read_mdt() -> None:
    global mdt
    src_content: str = ""
    src_file_location = f"{testcase_folder}/MDT.txt"
    with open(src_file_location, "r") as file:
        src_content = file.read()
    src_content = src_content.split('\n')
    mdt = [ line.split() for line in src_content ]

def read_kpdt() -> None:
    global kpdt
    src_content: str = ""
    src_file_location = f"{testcase_folder}/KPDT.txt"
    with open(src_file_location, "r") as file:
        src_content = file.read()
    src_content = src_content.split('\n')
    kpdt = [line.split() for line in src_content]


def is_macro_call(line: list[str]) -> tuple[bool, list[tuple]]:
    # macro call
    kp = 0
    pp = 0
    for i in range(1, len(line)):
        if '=' in line[i]:
            kp += 1
        else:
            pp += 1
            
    for i in range(0, len(mnt)):
        mnt_entry = mnt[i]
        if line[0] == mnt_entry[0] and pp == mnt_entry[1] and kp <= mnt_entry[2]:    
            return True, mnt_entry
    return False, None

def get_parameters(called_line:list[str], mnt_entry:list[tuple]):
    params = []
    # Added positional params
    for i in range(1, len(called_line)):
        if '=' not in called_line[i]:
            params.append(called_line[i])

    # copy keyword params
    keyword_params : list[list[str, str]] = []

    kp = mnt_entry[2]

    kpdt_start = mnt_entry[4] - 1


    for i in range(0, kp):
        kpdt_entry = kpdt[kpdt_start + i][:]
        keyword_params.append(kpdt_entry)


    # substitute new arguments
    for i in range(1, len(called_line)):
        if '=' in called_line[i]:
            argument_tokens = called_line[i].split('=')
            parameter = argument_tokens[0]
            argument = argument_tokens[1]
            for j in range(0, len(keyword_params)):
                if keyword_params[j][0] == parameter:
                    keyword_params[j][1] = argument
                    break
    
    # insert into apt
    for i in range(0, len(keyword_params)):
        if keyword_params[i][1] != '_':
            params.append(keyword_params[i][1])
        else:
            raise Exception(f"Argument not provided for parameter {keyword_params[i][0]}")

    return params

def expand_macro_call(mdt_start: int):
    i = mdt_start
    mdt_entry = mdt[i]
    while 'MEND' not in mdt_entry:
        output_line = ""
        for j in range(0, len(mdt_entry)):
            if '(' in mdt_entry[j]:
                parameter_token = mdt_entry[j].strip('(').strip(')').split(',')
                index = int(parameter_token[1].strip()) - 1
                output_line += f"{apt[index]} "
            else:
                output_line += f"{mdt_entry[j]} "
        output_lines.append(output_line)
        i += 1
        mdt_entry = mdt[i]



def main():
    global output_lines, apt

    read_src()
    read_mnt()
    read_mdt()
    read_kpdt()


    for line in src_lines:
        

        is_valid_call, mnt_entry = is_macro_call(line);
        if is_valid_call:
            apt = get_parameters(line, mnt_entry)
            mdt_start = mnt_entry[3] - 1
            expand_macro_call(mdt_start)
        
        else:
            output_line = ' '.join(line)
            output_lines.append(output_line)

    for i in range(0, len(output_lines)):
        print(output_lines[i])


if __name__ == '__main__':
    testcase_folder = str(input("Enter Testcase folder: "))
    main()
