from process import Process
from collections import deque

process_list : list[Process] = []
quantum_time : int = 2

def round_robin() -> None:
    time = 0
    step = 0
    no_of_processes = len(process_list)
    no_of_executed_processes = 0
    current_process: Process = None
    
    ready_list = deque()
    scheduled_list : list[Process] = []


    while no_of_processes != no_of_executed_processes:
        for process in process_list:
            if process.at == time: 
                ready_list.append(process)

        if current_process is not None and current_process.remaining_bt == 0:
            current_process.ct = time
            current_process.tat = current_process.ct - current_process.at
            current_process.wt = current_process.tat - current_process.bt
            scheduled_list.append(current_process)
            current_process = None
            no_of_executed_processes += 1
            step = 0

        
        if current_process is not None:
            current_process.remaining_bt -= 1
            if current_process.remaining_bt == 0:
                continue
            step += 1
            if step == quantum_time and current_process.remaining_bt > 0:
                step = 0
                ready_list.append(current_process)
                current_process = None


        if current_process is None and len(ready_list) > 0:
            step = 0
            current_process = ready_list.popleft()

        time += 1

    avg_tat = sum( [ proc.tat for proc in scheduled_list ] ) / len( process_list )
    avg_wt = sum( [ proc.wt for proc in scheduled_list ] ) / len( process_list )
    print( f"AVG TAT: {avg_tat}" )
    print( f"AVG WT: {avg_wt}" )
    print("Name\tArrival_Time\tBurst_Time\tWaiting_Time\tTAT\tCT\tPriority")
    for proc in scheduled_list:
        print( proc )



def main() -> None:
    global quantum_time
    number_of_process = int(input("Enter number of processes: "))
    arrival_time = list(map(int, str(input("Enter arrival time: >>> ")).split()))
    burst_time = list(map(int, str(input("Enter burst time: >>> ")).split()))

    if number_of_process != len(arrival_time) != len(burst_time):
        print("Number of processes do not match info")
        exit(1)

    for i in range(0, number_of_process):
        process = Process(i+1, arrival_time[i], burst_time[i])
        process_list.append(process)

    process_list.sort(key=lambda process: process.at)

    quantum_time = int(input("Enter quantum time : "))

    round_robin()

if __name__ == '__main__':
    main()