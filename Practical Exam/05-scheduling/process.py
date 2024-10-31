'''
Refer to the process-time diagram in the folder for more easy understanding

1. Arrival Time
The time at which the process enters into the ready queue is called the arrival time.

2. Burst Time
The total amount of time required by the CPU to execute the whole process is called the Burst Time. This does not include the waiting time. It is confusing to calculate the execution time for a process even before executing it hence the scheduling problems based on the burst time cannot be implemented in reality.

3. Completion Time
The Time at which the process enters into the completion state or the time at which the process completes its execution, is called completion time.

4. Turnaround time
The total amount of time spent by the process from its arrival to its completion, is called Turnaround time.

5. Waiting Time
The Total amount of time for which the process waits for the CPU to be assigned is called waiting time.
'''

class Process:
    def __init__(self):
        self.id = 0                 # Process Id
        self.priority : int = 0     # Process Priority
        self.at : int = 0           # Process Arrival Time
        self.bt : int = 0           # Process Burst Time
        self.ct : int = 0           # Process Completion Time
        self.tat : int = 0          # Process Turn around time
        self.wt : int = 0           # Process Waiting Time
        self.remaining_burst_time: int = 0

    def __str__( self ) -> str:
        return f"process: {self.id} AT = {self.at} , BT = {self.bt} , CT = {self.ct} , TAT = {self.tat} , WT = {self.wt} , PRIORITY = {self.priority}"  
    
    def __eq__( self, other) -> bool:
        return self.id == other.id
        