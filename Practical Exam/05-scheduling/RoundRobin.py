from process import Process
from collections import deque

quantum_time: int = 0

def round_robin_schedule(process_list: list[Process]):
    time = 0
    step = 0
    no_of_processes = len(process_list)
    no_of_executed_processes = 0
    current_process: Process = None
    
    ready_list = deque()
    scheduled_list : list[Process] = []

    while no_of_executed_processes != no_of_processes:
        
        for process in process_list:
            if process.at == time:
                ready_list.append(process)
        
        if current_process is not None and current_process.remaining_burst_time == 0:
            no_of_executed_processes += 1
            current_process.ct = time
            current_process.tat = current_process.ct - current_process.at
            current_process.wt = current_process.tat - current_process.bt
            scheduled_list.append(current_process)
            current_process = None
            step = 0

        if current_process is not None:
            print(f"Time = {time}\tProcess Id = {current_process.id}")

        if current_process is not None:
            current_process.remaining_burst_time -= 1
            if current_process.remaining_burst_time == 0:
                continue
            step += 1
            if step == quantum_time and current_process.remaining_burst_time > 0:
                step = 0
                ready_list.append(current_process)
                current_process = None

        if current_process is None and len(ready_list) > 0:
            step = 0
            current_process = ready_list.popleft()


        time += 1

    avg_tat = sum(proc.tat for proc in scheduled_list) / no_of_processes
    avg_wt = sum(proc.wt for proc in scheduled_list) / no_of_processes
    print(f"AVG TAT: {avg_tat}")
    print(f"AVG WT: {avg_wt}")
    for proc in scheduled_list:
        print(proc)
        



def main():
    global quantum_time
    
    no_of_processes = int(input("Enter no. of processes: "))
    arrival_times = list(map(int, str(input("Enter arrival times in space separated format: ")).split(" ")))
    burst_times = list(map(int, str(input("Enter burst times in space separated format: ")).split(" ")))
    quantum_time = int(input("Enter quantum time: "))

    if no_of_processes != len(arrival_times) != len(burst_times):
        print("no_of_processes != len(arrival_times) != len(burst_times)")
        exit(1)
    
    process_list: list[Process] = []

    for i in range(0, no_of_processes):
        proc = Process()
        proc.id = i + 1
        proc.at = arrival_times[i]
        proc.bt = burst_times[i]
        proc.remaining_burst_time = burst_times[i]
        process_list.append(proc)

    round_robin_schedule(process_list)


if __name__ == '__main__':
    main()