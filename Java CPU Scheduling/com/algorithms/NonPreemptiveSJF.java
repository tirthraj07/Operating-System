package com.algorithms;

import java.util.Arrays;

public class NonPreemptiveSJF {
    Jobs[] jobArray;
    int noOfProcesses;

    public NonPreemptiveSJF(int noOfProcesses, Jobs[] v){
        this.noOfProcesses = noOfProcesses;
        jobArray = new Jobs[noOfProcesses];
        for(int i=0; i<noOfProcesses; i++){
            jobArray[i] = new Jobs(v[i]);
        }
        sortJobsBasedOnArrivalTimeAndBurstTime();
        calculateWaitingTimeForEachJob();
    }


    private void sortJobsBasedOnArrivalTimeAndBurstTime() {
        Arrays.sort(jobArray, (job1, job2) -> {
            if (job1.arrivalTime != job2.arrivalTime) {
                return Integer.compare(job1.arrivalTime, job2.arrivalTime);
            }
            return Integer.compare(job1.burstTime, job2.burstTime);
        });
    }


    private void calculateWaitingTimeForEachJob() {
        jobArray[0].waitingTime = 0;
        Jobs curr = jobArray[0];
        boolean[] completedJobs = new boolean[noOfProcesses];
        completedJobs[0] = true;
        for(int i=0; i<noOfProcesses-1; i++){
            curr.completionTime = curr.arrivalTime + curr.waitingTime + curr.burstTime ;
            curr.turnaroundTime = curr.completionTime - curr.arrivalTime;
            int minJob = -1;
            for(int j = 0; j<noOfProcesses; j++){
                if(!completedJobs[j] && jobArray[j].arrivalTime <= curr.completionTime && (minJob==-1 || jobArray[j].burstTime < jobArray[minJob].burstTime)){
                    minJob = j;
                }
            }
            jobArray[minJob].waitingTime = curr.completionTime - jobArray[minJob].arrivalTime;
            curr = jobArray[minJob];
            completedJobs[minJob] = true;
        }
        curr.completionTime = curr.arrivalTime + curr.waitingTime + curr.burstTime ;
        curr.turnaroundTime = curr.completionTime - curr.arrivalTime;
    }

    private double calculateAverageWaitingTime() {
        int totalWaitingTime = 0;
        for(int i=0; i<noOfProcesses; i++){
            totalWaitingTime = totalWaitingTime + jobArray[i].waitingTime;
        }
        return (double)totalWaitingTime/noOfProcesses;
    }

    public void printJobs(){
        System.out.println("Non - Preemptive Shortest Job First Algorithm");
        System.out.println("Process Name Priority Arrival Time Burst Time Waiting Time Turnaround Time Completion Time");
        for(int i=0; i<noOfProcesses; i++){
            System.out.println(jobArray[i]);
        }
        
        System.out.println("Average Waiting Time is : " + calculateAverageWaitingTime());
    }



}
