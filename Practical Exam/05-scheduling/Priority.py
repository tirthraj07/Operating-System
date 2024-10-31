'''
In Priority scheduling, there is a priority number assigned to each process. 
In some systems, the lower the number, the higher the priority.
While, in the others, the higher the number, the higher will be the priority. 

In this program, lower the priority_no, higher will be the priority i.e it will be given CPU Time in event of collision
'''
from process import Process
from collections import deque

def priority_schedule(process_list: list[Process]):
    time = 0
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
        
        if current_process is None and len(ready_list) > 0:
            current_process = min(ready_list, key= lambda proc: proc.priority)
            ready_list.remove(current_process) 

        if current_process is not None:
            current_process.remaining_burst_time -= 1

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
    priorities = list(map(int, str(input("Enter priorities in space separated format: ")).split(" ")))
    

    if no_of_processes != len(arrival_times) != len(burst_times) != len(priorities):
        print("no_of_processes != len(arrival_times) != len(burst_times) != len(priorities)")
        exit(1)
    
    process_list: list[Process] = []

    for i in range(0, no_of_processes):
        proc = Process()
        proc.id = i + 1
        proc.at = arrival_times[i]
        proc.bt = burst_times[i]
        proc.remaining_burst_time = burst_times[i]
        proc.priority = priorities[i]
        process_list.append(proc)

    priority_schedule(process_list)

if __name__ == '__main__':
    main()