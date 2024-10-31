from process import Process
from collections import deque

def fcfs_schedule(process_list: list[Process]):
    current_proc: Process = None
    time: int = 0

    no_of_processes = len(process_list)
    no_of_executed_processes = 0

    ready_list = deque()
    scheduled_list: list = []

    while no_of_executed_processes != no_of_processes:
        # Add the processes that have arrived at time = t
        for process in process_list:
            if process.at == time:
                ready_list.append(process)

        # check if current process has completed execution
        if current_proc is not None and current_proc.remaining_burst_time == 0:
            current_proc.ct = time
            current_proc.tat = current_proc.ct - current_proc.at
            current_proc.wt = current_proc.tat - current_proc.bt
            scheduled_list.append(current_proc)
            current_proc = None
            no_of_executed_processes += 1
        
        if current_proc is None and len(ready_list) > 0:
            current_proc = ready_list.popleft()

        # Execute current process
        if current_proc is not None:
            current_proc.remaining_burst_time -= 1

        time += 1


    avg_tat = sum( [ proc.tat for proc in scheduled_list ] ) / len( process_list )
    avg_wt = sum( [ proc.wt for proc in scheduled_list ] ) / len( process_list )
    print( f"AVG TAT: {avg_tat}" )
    print( f"AVG WT: {avg_wt}" )
    for proc in scheduled_list:
        print( proc )



def main():
    no_of_processes = int(input("Enter no. of processes: "))
    arrival_times = list(map(int, str(input("Enter arrival times in space separated format: ")).split(" ")))
    burst_times = list(map(int, str(input("Enter burst times in space separated format: ")).split(" ")))

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

    fcfs_schedule(process_list)

if __name__ == '__main__':
    main()