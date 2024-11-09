class Process:
    def __init__(self, name, arrival_time: int, burst_time: int):
        self.name = name
        self.at = arrival_time
        self.bt = burst_time
        self.wt = 0
        self.tat = 0
        self.ct = 0
        self.priority = 0
        self.remaining_bt = burst_time
    
    def __str__(self):
        return f"{self.name}\t{self.at}\t\t{self.bt}\t\t{self.wt}\t\t{self.tat}\t{self.ct}\t\t{self.priority}"