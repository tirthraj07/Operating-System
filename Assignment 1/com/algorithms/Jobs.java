package com.algorithms;

public class Jobs{
    String name;
    
    int waitingTime;
    int arrivalTime;
    int burstTime;

    @Override
    public String toString(){
        return this.name + "\t\t\t" + this.arrivalTime + "\t\t\t" + this.burstTime + "\t\t\t" + this.waitingTime;
    }
}
