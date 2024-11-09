from process import Process
from collections import deque

process_list : list[Process] = []

def sjf_schedule() -> None:
    time = 0
    number_of_processes = len(process_list)
    number_of_completed_processes = 0
    current_process : Process = None

    ready_list = deque()
    scheduled_list : list[Process] = []

    while number_of_processes != number_of_completed_processes:
        for process in process_list:
            if process.at == time:
                ready_list.append(process)
            

        if current_process is not None and current_process.remaining_bt == 0:
            current_process.ct = time
            current_process.tat = current_process.ct - current_process.at
            current_process.wt = current_process.tat - current_process.bt
            scheduled_list.append(current_process)
            current_process = None
            number_of_completed_processes += 1


        if current_process is not None and len(ready_list) > 0:
            min_bt_process:Process = min(ready_list, key=lambda proc: proc.remaining_bt)
            if min_bt_process.remaining_bt < current_process.remaining_bt:
                ready_list.remove(min_bt_process)
                ready_list.append(current_process)
                current_process = min_bt_process

        if current_process is None and len(ready_list) > 0:
            current_process:Process = min(ready_list, key=lambda proc: proc.remaining_bt)
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

    if number_of_process != len(arrival_time) != len(burst_time):
        print("Number of processes do not match info")
        exit(1)

    for i in range(0, number_of_process):
        process = Process(i+1, arrival_time[i], burst_time[i])
        process_list.append(process)

    process_list.sort(key=lambda process: process.at)

    sjf_schedule()

if __name__ == '__main__':
    main()