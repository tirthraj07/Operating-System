package com.algorithms;

public class Jobs{
    public String name;
    
    public int waitingTime;
    public int arrivalTime;
    public int burstTime;
    public int turnaroundTime;
    public int completionTime;
    public int remainingBurstTime;
    public int priority;

    public Jobs(){};

    public Jobs(Jobs cpy){
        this.name = cpy.name;
        this.waitingTime = cpy.waitingTime;
        this.arrivalTime = cpy.arrivalTime;
        this.burstTime = cpy.burstTime;
        this.turnaroundTime = cpy.turnaroundTime;
        this.completionTime = cpy.completionTime;
        this.remainingBurstTime = cpy.remainingBurstTime;
        this.priority = cpy.priority;
    }

    @Override
    public String toString(){
        return this.name + "\t\t\t" + this.priority + "\t\t\t" + this.arrivalTime + "\t\t\t" + this.burstTime + "\t\t\t" + this.waitingTime + "\t\t\t\t" + this.turnaroundTime + "\t\t\t\t" + this.completionTime;
    }
}
