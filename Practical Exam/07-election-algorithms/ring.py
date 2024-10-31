'''
Refer to README.md for understanding the Ring Algorithm

Note: Higher the priority number, higher is the priority
'''
from time import sleep
import random


class Process:
    def __init__(self, id, priority: int):
        self.id = id
        self.priority = priority
        self.active: bool = True


process_list: list[Process] = []


def get_leader_index() -> int:
    max_priority = -1
    leader_index = -1
    for i in range(0, len(process_list)):
        if process_list[i].priority > max_priority:
            max_priority = process_list[i].priority
            leader_index = i
    return leader_index

def leader_fail()->int:
    leader_index:int = get_leader_index()
    leader_process = process_list[leader_index]

    sleep(3)
    print(f"Leader: Process {leader_process.id} with Priority {leader_process.priority}")
    sleep(3)

    leader_process.active = False
    print(f"Leader Process failed")
    return leader_index

def circulate_candidate_list(process_index:int, candidate_list:list[tuple[int,int]]):
    candidate_process = process_list[process_index]
    # End case for recursion
    if len(candidate_list) != 0 and candidate_list[0][0] == candidate_process.id:
        print(f"Process {candidate_process.id} received back the election message")
        sleep(3)
        return candidate_list

    if len(candidate_list) == 0:
        print(f"Process {candidate_process.id} circulating election message")
    else:
        print(f"Process {candidate_process.id} received election message")
        print("Candidate List : [", end=" ")
        for candidate in candidate_list:
            print(f"Process {candidate[0]} ," , end=" ")
        print("]")

    sleep(3)
    candidate_list.append([candidate_process.id, candidate_process.priority])
    sleep(3)

    next_candidate_index: int = (process_index + 1)%len(process_list)
    while process_list[next_candidate_index].active == False and next_candidate_index != process_index:
        next_candidate_index = (next_candidate_index + 1)%len(process_list)

    if next_candidate_index == process_index:
        print(f"No successor found")
        return candidate_list

    next_candidate = process_list[next_candidate_index]
    print(f"Sending election message to process {next_candidate.id}")
    sleep(3)
    return circulate_candidate_list(next_candidate_index, candidate_list)

def circulate_coordinator_message(process_index:int, initiator:int|None, message:str):
    process = process_list[process_index]
    if process_index == initiator:
        sleep(3)
        print(f"Process {process.id} received back the coordinator message")
        sleep(3)
        print("Ending Process")
        return

    if initiator == None:
        initiator = process_index
        print(f"Process {process.id} initiating coordinator message circulation")
        sleep(3)
    else:
        print(f"Process {process.id} received coordinator message: {message}")
        sleep(3)

    next_candidate_index: int = (process_index + 1)%len(process_list)
    while process_list[next_candidate_index].active == False and next_candidate_index != process_index:
        next_candidate_index = (next_candidate_index + 1)%len(process_list)

    next_candidate = process_list[next_candidate_index]
    print(f"Sending Process {next_candidate.id} coordinator message")
    sleep(3)
    circulate_coordinator_message(next_candidate_index, initiator, message)


def start_simulation(process_p:Process):
    sleep(3)
    print(f"Starting simulation with process: {process_p.id}")
    
    process_p_index = -1
    for i in range(0, len(process_list)):
        if process_list[i].id == process_p.id:
            process_p_index = i

    candidate_list: list[tuple[int,int]] = []

    sleep(3)
    candidate_list = circulate_candidate_list(process_p_index, candidate_list)

    new_leader_process_id:int = -1
    new_leader_process_priority:int = -1
    
    for candidate in candidate_list:
        if candidate[1] > new_leader_process_priority:
            new_leader_process_id = candidate[0]
            new_leader_process_priority = candidate[1]

    coordinator_message: str = f"Process {new_leader_process_id} is new coordinator"
    
    sleep(3)
    circulate_coordinator_message(process_p_index, None, coordinator_message)


def main():
    global process_list
    no_of_processes = int(input("Enter no. of processes: "))
    process_priority = set()
    i: int = 0
    while i < no_of_processes:
        priority = str(input(f"Enter Priority for Process {i} (Default {i}) : "))
        if priority == "":
            priority = int(i)
        else:
            priority = int(priority)
        if priority in process_priority:
            print(f"Priority {priority} has already been assigned to another process")
            continue
        
        is_active = str(input(f"Is Process {i} active? (T/F) (Default T) : "))
        
        process = Process(id=i, priority=priority)
        if is_active == "F":
            process.active = False
        process_list.append(process)
        i += 1

    print("\n\n\n\n\n\n\n\n\n\n")
    print("--- RING ELECTION ALGORITHM ---")

    leader_index:int = leader_fail()
    
    sleep(3)
    
    print("Selecting Random Process to initiate")

    random_index = leader_index
    while process_list[random_index].active == False:
        random_index = random.choice(range(0, len(process_list)))

    random_process = process_list[random_index]
    sleep(3)
    print(f"Selected Process {random_process.id} with Priority {random_process.priority}")

    
    start_simulation(random_process)


if __name__ == '__main__':
    main()
