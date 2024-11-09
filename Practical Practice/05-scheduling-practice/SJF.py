from process import Process
from collections import deque

process_list : list[Process] = []

def sjf_schedule() -> None:
    time = 0
    no_processes = len(process_list)
    no_executed = 0
    current_process: Process = None
    ready_list = deque()
    scheduled_list : list[Process] = []

    while no_executed != no_processes:
        for process in process_list:
            if process.at == time:
                ready_list.append(process)
        
        if current_process is not None and current_process.remaining_bt == 0:
            current_process.ct = time
            current_process.tat = current_process.ct - current_process.at
            current_process.wt = current_process.tat - current_process.bt
            scheduled_list.append(current_process)
            no_executed += 1
            current_process = None
        
        if current_process is not None and len(ready_list) > 0:
            min_bt_process = min(ready_list, key=lambda proc: proc.remaining_bt)
            if min_bt_process.remaining_bt < current_process.remaining_bt:
                ready_list.remove(min_bt_process)
                ready_list.append(current_process)
                current_process = min_bt_process

        if current_process is None and len(ready_list) > 0:
            current_process = min(ready_list, key=lambda proc : proc.remaining_bt)
            ready_list.remove(current_process)

        if current_process is not None:
            current_process.remaining_bt -= 1

        time += 1


    avg_wt = sum([proc.wt for proc in scheduled_list])/no_processes
    avg_tat = sum([proc.tat for proc in scheduled_list])/no_processes
    print(f"Avg WT : {avg_wt}")
    print(f"Avg TAT : {avg_tat}")

    print("ID\tArrival Time\tBurst Time\tCompletion Time\tWaiting Time\tTAT\tPriority")
    for process in scheduled_list:
        print(process)


def main():
    arrival_times = list(map(int, str(input("Enter Arrival Times >>> ")).split()))
    burst_times = list(map(int, str(input("Enter Arrival Times >>> ")).split()))

    if len(arrival_times) != len(burst_times):
        print("Incomplete Info about processes")
        exit(1)
    
    for i in range(0, len(arrival_times)):
        process = Process(i+1, arrival_times[i], burst_times[i])
        process_list.append(process)
    
    process_list.sort(key=lambda proc: proc.at)
    sjf_schedule()

if __name__ == '__main__':
    main()