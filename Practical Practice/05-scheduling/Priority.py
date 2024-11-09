from process import Process
from collections import deque
process_list : list[Process] = []

def priority_schedule() -> None:
    time: int = 0
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
            no_of_executed_processes += 1
            current_process = None
        
        if current_process is None and len(ready_list) > 0:
            current_process = min(ready_list, key= lambda proc: proc.priority)
            ready_list.remove(current_process)

        if current_process is not None:
            current_process.remaining_bt -= 1

        time += 1

    avg_tat = sum( [ proc.tat for proc in scheduled_list ] ) / len( process_list )
    avg_wt = sum( [ proc.wt for proc in scheduled_list ] ) / len( process_list )
    print( f"AVG TAT: {avg_tat}" )
    print( f"AVG WT: {avg_wt}" )
    print("Name\tArrival_Time\tBurst_Time\tWaiting_Time\tTAT\tCT\tPriority")
    for proc in scheduled_list:
        print( proc )



def main() -> None:
    number_of_process = int(input("Enter number of processes: "))

    arrival_time = list(map(int, str(input("Enter arrival time: >>> ")).split()))
    burst_time = list(map(int, str(input("Enter burst time: >>> ")).split()))
    priority = list(map(int, str(input("Enter Priority: >>> ")).split()))


    if number_of_process != len(arrival_time) != len(burst_time) != len(priority):
        print("Number of processes do not match info")
        exit(1)

    for i in range(0, number_of_process):
        process = Process(i+1, arrival_time[i], burst_time[i])
        process.priority = priority[i]
        process_list.append(process)

    process_list.sort(key=lambda process: process.at)

    priority_schedule()

if __name__ == '__main__':
    main()