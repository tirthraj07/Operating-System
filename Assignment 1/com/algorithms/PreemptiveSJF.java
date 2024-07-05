package com.algorithms;

import java.util.Arrays;

public class PreemptiveSJF {
    Jobs[] jobArray;
    int noOfProcesses;

    public PreemptiveSJF(int noOfProcesses, Jobs[] v){
        this.noOfProcesses = noOfProcesses;
        jobArray = new Jobs[noOfProcesses];
        for(int i=0; i<noOfProcesses; i++){
            jobArray[i] = new Jobs(v[i]);
            jobArray[i].remainingBurstTime = jobArray[i].burstTime;
        }
        sortJobsBasedOnArrivalTimeAndBurstTime();
        calculateWaitingTimeForEachJob();
    }


    private void sortJobsBasedOnArrivalTimeAndBurstTime() {
        Arrays.sort(jobArray, (job1, job2)->{
            if(job1.arrivalTime != job2.arrivalTime) return Integer.compare(job1.arrivalTime, job2.arrivalTime);
            return Integer.compare(job1.burstTime, job2.burstTime);
        });
    }

    private void calculateWaitingTimeForEachJob() {
        int completedProcesses = 0;
        int currentTime = 0;
        boolean[] completedProcessesArray = new boolean[noOfProcesses];


        while(completedProcesses != noOfProcesses){
            int minJobIndex = -1;
            int minJobRemainingBurstTime = Integer.MAX_VALUE;
            for(int i=0; i<noOfProcesses; i++){
                
                if(!completedProcessesArray[i] && jobArray[i].arrivalTime <= currentTime && jobArray[i].remainingBurstTime < minJobRemainingBurstTime){
                    minJobIndex = i;
                    minJobRemainingBurstTime = jobArray[i].remainingBurstTime;
                }
            }

            for(int i=0; i<noOfProcesses; i++){
                if(!completedProcessesArray[i] && jobArray[i].arrivalTime <= currentTime && i!=minJobIndex){
                    jobArray[i].waitingTime++;
                }
            }
            Jobs currentJob = jobArray[minJobIndex];
            currentJob.remainingBurstTime--;
            if(currentJob.remainingBurstTime == 0){
                jobArray[minJobIndex].completionTime = currentTime + 1;
                jobArray[minJobIndex].turnaroundTime = jobArray[minJobIndex].completionTime - jobArray[minJobIndex].arrivalTime;
                completedProcessesArray[minJobIndex] = true;
                completedProcesses++;
            }
            currentTime++;
        }

    }

    private double calculateAverageWaitingTime() {
        int totalWaitingTime = 0;
        for(int i=0; i<noOfProcesses; i++){
            totalWaitingTime = totalWaitingTime + jobArray[i].waitingTime;
        }
        return (double)totalWaitingTime/noOfProcesses;
    }

    public void printJobs(){
        System.out.println("Preemptive Shortest Job First Algorithm");
        System.out.println("Process Name Priority Arrival Time Burst Time Waiting Time Turnaround Time Completion Time");
        for(int i=0; i<noOfProcesses; i++){
            System.out.println(jobArray[i]);
        }
        
        System.out.println("Average Waiting Time is : " + calculateAverageWaitingTime());
    }

}
