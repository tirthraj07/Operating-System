class Process:
    def __init__(self, id ,arrival_time, burst_time, priority=0):
        self.id = id
        self.at = arrival_time
        self.bt = burst_time
        self.ct = 0
        self.wt = 0
        self.tat = 0
        self.remaining_bt = burst_time
        self.priority = priority

    def __str__(self):
        # f"ID\tArrival Time\tBurst Time\tCompletion Time\tWaiting Time\tTAT\tPriority"
        return f"{self.id}\t{self.at}\t\t{self.bt}\t\t{self.ct}\t\t{self.wt}\t\t{self.tat}\t{self.priority}"
