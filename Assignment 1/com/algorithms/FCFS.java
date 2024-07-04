package com.algorithms;

import java.util.Arrays;
import java.util.Comparator;


/*
First Come First Serve – CPU Scheduling (Non-Preemptive)
Simplest CPU scheduling algorithm that schedules according to arrival times of processes. 
The first come first serve scheduling algorithm states that the process that requests the CPU first is allocated the CPU first. 
It is implemented by using the FIFO queue. 
*/

public class FCFS {
    private int noOfProcesses;
    private Jobs[] jobArray;

    public FCFS(int noOfProcesses, Jobs[] v){
        this.noOfProcesses = noOfProcesses;
        jobArray = new Jobs[noOfProcesses];
        for(int i=0; i<noOfProcesses; i++){
            jobArray[i] = new Jobs(v[i]);
        }
        sortJobArray();
        calculateWaitingTime();
    }

    private void sortJobArray(){
        Arrays.sort(jobArray, Comparator.comparingInt(job -> job.arrivalTime));
    }

    public void calculateWaitingTime(){
        jobArray[0].waitingTime = 0;
        jobArray[0].completionTime = jobArray[0].arrivalTime + jobArray[0].burstTime;
        jobArray[0].turnaroundTime = jobArray[0].completionTime - jobArray[0].arrivalTime;
        if(noOfProcesses > 1) {
            Jobs curr = jobArray[1], prev = jobArray[0];
            for (int i = 1; i < noOfProcesses; i++) {
                curr = jobArray[i];
                prev = jobArray[i - 1];
                prev.completionTime = prev.arrivalTime + prev.waitingTime + prev.burstTime;
                prev.turnaroundTime = prev.completionTime - prev.burstTime;
                curr.waitingTime = prev.completionTime - curr.arrivalTime;
            }
            curr.completionTime = curr.arrivalTime + curr.waitingTime + curr.burstTime;
            curr.turnaroundTime = curr.completionTime - curr.arrivalTime;
        }
    }

    public double calculateAverageWaitingTime(){
        int totalWaitingTime = 0;
        for(int i=0; i<noOfProcesses; i++){
            totalWaitingTime = totalWaitingTime + jobArray[i].waitingTime;
        }
        double averageWaitingTime = (double)totalWaitingTime/noOfProcesses;
        return averageWaitingTime;
    }

    public void printJobs(){
        System.out.println("Non - Preemptive First Come First Serve Algorithm");
        System.out.println("Process Name Arrival Time Burst Time Waiting Time Turnaround Time Completion Time");
        for(int i=0; i<noOfProcesses; i++){
            System.out.println(jobArray[i]);
        }

        System.out.println("Average Waiting Time is : " + calculateAverageWaitingTime());
    }



}
