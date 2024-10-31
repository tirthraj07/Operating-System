'''
Refer to README.md for understanding the Bully Algorithm

Note: Higher the priority number, higher is the priority


def main() -> Entry point to the algorithm

This is a SIMULATION of the leader election algorithm. In real world case, you'd run n number of processes in parallel

Here we use random module to simulate the message receiving at different times

First we select the leader based on priority

Then we fail the leader on purpose of simulation

Then we pick a random active process to start the simulation

Then we send the election message

Then we randomize the received messages to simulate that different processes reply at different times

If we get a okay message then it recursively calls the start_simulation function

Else new leader gets elected and sends the coordination message
'''
from time import sleep, time
import random

class Process:
    def __init__(self, id, priority):
        self.id = id
        self.priority:int = priority
        self.active: bool = True

    def send_election_message(self) -> tuple[int, str]:
        if self.active:
            return self.id, "OK"
        return self.id, "NOT OK"

    def send_coordinator_message(self, process_id) -> tuple[int, str]:
        return self.id, f"New Coordinator Set: Process {process_id}"

process_list : list[Process] = []

# Identifies the leader process and make it fail

def get_leader_index():
    max_priority:int = -1
    leader_process_index: int = -1
    for i in range(0, len(process_list)):
        if process_list[i].priority > max_priority:
            max_priority = process_list[i].priority
            leader_process_index = i
    return leader_process_index, max_priority

def leader_fail():
    sleep(3)
    leader_process_index, leader_priority = get_leader_index()
    print(f"Leader Process: Process {process_list[leader_process_index].id} with Priority = {leader_priority}")
    sleep(3)
    process_list[leader_process_index].active = False
    print("Leader process failed")
    return leader_process_index 


def start_simulation(process_p: Process):
    print(f"Starting Simulation with Process {process_p.id}")
    sleep(3)
    received_messages: list[list[int, str]] = []
    
    for i in range(0, len(process_list)):
        if process_list[i].priority > process_p.priority:
            process_id, process_status = process_list[i].send_election_message()
            print(f"Process {process_p.id} [Priority {process_p.priority}] sent election message to Process {process_id} [Priority {process_list[i].priority}]")
            sleep(1)
            received_messages.append([process_id, process_status])

    # simulate that different processes reply at different rates
    random.shuffle(received_messages)

    received_okay_message : bool = False
    new_process_p_id = None

    for message in received_messages:
        sleep(2)
        print(f"Process {message[0]} replied with '{message[1]}'")
        if message[1] == "OK":
            received_okay_message = True
            new_process_p_id = message[0]
            break

    if received_okay_message:
        print("Received Okay message from one of the higher priority processes")
        print(f"Process {process_p.id} Job Done")
        print(f"Restarting algorithm again from Process {new_process_p_id}")

        for process in process_list:
            if process.id == new_process_p_id:
                process_p = process
                break
        start_simulation(process_p)
        return
    else:
        print("No OK messages received from higher priority processes")
        print("Sending Coordinator message to all lower-priority processes")
        received_messages = []
        for process in process_list:
            if process.priority < process_p.priority:
                print(f"Process {process_p.id} sent Coordinator message to Process {process.id}")
                process_id, process_message = process.send_coordinator_message(process_p.id)
                received_messages.append([process_id, process_message])
        
        for messages in received_messages:
            print(f"Process {messages[0]} replied: {messages[1]}")
            sleep(1)

def main():
    global process_list
    no_of_processes = int(input("Enter number of processes: "))

    print("Higher the priority number, higher is the priority")
    priority_set = set()

    i: int = 0
    while i < no_of_processes:
        priority = int(input(f"Enter priority for process {i}: "))
        if priority in priority_set:
            print(f"Priority {priority} already assigned to different process")
            continue
        is_active = str(input(f"Is process {i} active? (T/F) (Default: T) : "))
        
        priority_set.add(priority)
        process = Process(i, priority)
        if is_active == "F":
            process.active = False
        process_list.append(process)
        i += 1

    print("\n\n\n\n\n\n\n\n\n\n\n\n")
    print("--- BULLY ELECTION ALGORITHM ---")

    leader_process_index = leader_fail()
    sleep(3)
    # Select a random process that is active
    print("Selecting Random Process")

    random_index: int = leader_process_index
    while process_list[random_index].active == False:
        random_index = random.choice(range(0, no_of_processes))

    random_process = process_list[random_index]

    sleep(3)

    print(f"Selected Process {random_process.id}")

    random.seed(time())
    start_simulation(random_process)


if __name__ == '__main__':
    main()