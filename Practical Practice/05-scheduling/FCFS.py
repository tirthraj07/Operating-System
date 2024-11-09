from process import Process
from collections import deque

process_list : list[Process] = []

def fcfs_schedule():
    time = 0
    number_of_processes = len(process_list)
    number_of_completed_processes = 0
    current_process: Process = None

    ready_list = deque()
    scheduled_list: list[Process] = []


    while number_of_completed_processes != number_of_processes:
        for i in range(0, number_of_processes):
            if process_list[i].at == time:
                ready_list.append(process_list[i])

        if current_process is not None and current_process.remaining_bt == 0:
            current_process.ct = time
            current_process.tat = current_process.ct - current_process.at
            current_process.wt = current_process.tat - current_process.bt
            scheduled_list.append(current_process)
            current_process = None
            number_of_completed_processes += 1

        if current_process is None and len(ready_list) > 0:
            current_process = ready_list.popleft()

        if current_process is not None:
            current_process.remaining_bt -= 1

        time += 1


    avg_wt = sum( [  proc.wt for proc in scheduled_list ] ) / number_of_processes
    avg_tat = sum( [ proc.tat for proc in scheduled_list ] ) / number_of_processes

    print(f" Average WT : {avg_wt} ")
    print(f" Average TAT : {avg_tat} ")

    print("Name\tArrival_Time\tBurst_Time\tWaiting_Time\tTAT\tCT\tPriority")
    for process in scheduled_list:
        print(process)



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

    fcfs_schedule()

if __name__ == '__main__':
    main()