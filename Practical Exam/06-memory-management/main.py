'''
def main() -> entry point of the program
'''
import random
no_of_chunks = 10
no_of_programs = 5

last_inserted_chunk: int = 0
memory = []
total_memory = 0
program_chunks = []

def print_memory():
    # display memory
    print("Sr.\tBlock Size\tRemaining Size\tIs Free")
    for i in range(0, no_of_chunks):
        chunk = memory[i]
        print(f"{i+1}\t{chunk[0]}\t\t{chunk[1]}\t\t{chunk[2]}\t")
    print(f"Total Memory = {total_memory}")

def print_programs():
    print("Program No\tProgram Space")
    for i in range(0, len(program_chunks)):
        print(f"Program {i+1}\t{program_chunks[i]}")

def best_fit(required_memory:int):
    global program_chunks, memory, last_inserted_chunk
    minMemoryChunk = -1
    minMemorySize = float('inf')
    for i in range(0, len(memory)):
        block_size = memory[i][0]
        available_space = memory[i][1]
        is_free = memory[i][2]

        if is_free == True and block_size >= required_memory:   
            if minMemoryChunk == -1 or minMemorySize > block_size:
                minMemoryChunk = i
                minMemorySize = block_size

    if minMemoryChunk != -1:
        memory[minMemoryChunk][2] = False
        memory[minMemoryChunk][1] = minMemorySize - required_memory
        last_inserted_chunk = minMemoryChunk
        print(f"Allocated {required_memory} in chunk {minMemoryChunk + 1}")

    else:
        print("Not enough Space for memory")


def first_fit(required_memory: int) -> None:
    global program_chunks, memory, last_inserted_chunk
    for i in range(0, len(memory)):
        block_size = memory[i][0]
        available_space = memory[i][1]
        is_free = memory[i][2]

        if is_free == True and block_size >= required_memory:   
            memory[i][2] = False
            memory[i][1] = memory[i][0] - required_memory
            last_inserted_chunk = i
            print(f"Allocated {required_memory} in chunk {i + 1}")
            return

    print("Not enough Space for memory")


def worst_fit(required_memory: int) -> None:
    global program_chunks, memory, last_inserted_chunk
    maxMemoryChunk = -1
    maxMemorySize = float('-inf')
    for i in range(0, len(memory)):
        block_size = memory[i][0]
        available_space = memory[i][1]
        is_free = memory[i][2]

        if is_free == True and block_size >= required_memory:   
            if maxMemoryChunk == -1 or maxMemorySize < block_size:
                maxMemoryChunk = i
                maxMemorySize = block_size

    if maxMemoryChunk != -1:
        memory[maxMemoryChunk][2] = False
        memory[maxMemoryChunk][1] = maxMemorySize - required_memory
        last_inserted_chunk = maxMemoryChunk
        print(f"Allocated {required_memory} in chunk {maxMemoryChunk + 1}")

    else:
        print("Not enough Space for memory")

def next_fit(required_memory: int) -> None:
    global program_chunks, memory, last_inserted_chunk
    for i in range(last_inserted_chunk, len(memory)):
        block_size = memory[i][0]
        available_space = memory[i][1]
        is_free = memory[i][2]

        if is_free == True and block_size >= required_memory:   
            memory[i][2] = False
            memory[i][1] = memory[i][0] - required_memory
            last_inserted_chunk = i
            print(f"Allocated {required_memory} in chunk {i + 1}")
            return

    for i in range(0, last_inserted_chunk):
        block_size = memory[i][0]
        available_space = memory[i][1]
        is_free = memory[i][2]

        if is_free == True and block_size >= required_memory:   
            memory[i][2] = False
            memory[i][1] = memory[i][0] - required_memory
            last_inserted_chunk = i
            print(f"Allocated {required_memory} in chunk {i + 1}")
            return

    print("Not enough Space for memory")
        

def main() -> None:
    global memory, total_memory, program_chunks

    # initialize memory
    for _ in range(0, no_of_chunks):
        block_size = random.randint(a=10, b=100)
        available_size = block_size
        is_free = True
        memory.append([block_size, available_size, is_free])
        total_memory += block_size
    
    # print_memory()

    for _ in range(0, no_of_programs):
        program_size = random.randint(a=10, b=50)
        program_chunks.append(program_size)
    
    print_programs()


    for i in range(0, len(program_chunks)):
        print_memory()
        print(f"Program {i+1}: Size = {program_chunks[i]} to be allocated")
        choice = int(input("What do you want to do?\n1.Best fit\n2.First Fit\n3.Worst Fit\n4.Next Fit\n>>> "))

        if choice == 1:
            best_fit(required_memory=program_chunks[i])
        
        elif choice == 2:
            first_fit(required_memory=program_chunks[i])

        elif choice == 3:
            worst_fit(required_memory=program_chunks[i])

        elif choice == 4:
            next_fit(required_memory=program_chunks[i])




if __name__ == '__main__':
    main()