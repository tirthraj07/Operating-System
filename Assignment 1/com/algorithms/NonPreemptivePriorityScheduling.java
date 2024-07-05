package com.algorithms;

import java.util.Scanner;
import java.util.Arrays;

public class NonPreemptivePriorityScheduling {
    Jobs[] jobArray;
    int noOfProcesses;

    public NonPreemptivePriorityScheduling(int noOfProcesses, Jobs[] v){
        this.noOfProcesses = noOfProcesses;
        jobArray = new Jobs[noOfProcesses];
        for(int i=0; i<noOfProcesses; i++){
            jobArray[i] = new Jobs(v[i]);
        }
        assignPriorityToJobs();
        sortJobsBasedOnArrivalTimeAndPriority();
        calculateWaitingTimeForEachJob();
    }

    private void assignPriorityToJobs() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Assign Priority to the following tasks.");
        System.out.println("Note: Generally, the lower the priority number, the higher is the priority of the process.");
        for(int i=0; i<noOfProcesses; i++){
            System.out.print(jobArray[i].name + " : ");
            jobArray[i].priority = sc.nextInt();
            sc.nextLine();
        }
        sc.close();
    }

    private void sortJobsBasedOnArrivalTimeAndPriority() {
        Arrays.sort(jobArray, (job1, job2)->{
            if(job1.arrivalTime != job2.arrivalTime) return Integer.compare(job1.arrivalTime, job2.arrivalTime);
            return Integer.compare(job1.priority, job2.priority);
        });
    }

    private void calculateWaitingTimeForEachJob() {
        int completedJobs = 0;
        boolean[] completedJobsArray = new boolean[noOfProcesses];

        int currJobIndex = 0;
        jobArray[currJobIndex].waitingTime = 0;
        while(completedJobs < noOfProcesses){
            System.out.println("Executing Task: :" + jobArray[currJobIndex].name);
            jobArray[currJobIndex].completionTime = jobArray[currJobIndex].arrivalTime + jobArray[currJobIndex].waitingTime + jobArray[currJobIndex].burstTime;
            jobArray[currJobIndex].turnaroundTime = jobArray[currJobIndex].completionTime - jobArray[currJobIndex].arrivalTime;
            int completionTimeOfCurrentJob = jobArray[currJobIndex].completionTime;
            completedJobsArray[currJobIndex] = true;
            completedJobs++;
            if(completedJobs == noOfProcesses) break;
            int maxPriorityOfJob = Integer.MAX_VALUE;
            for(int i=0; i<noOfProcesses; i++){
                if(!completedJobsArray[i] && jobArray[i].arrivalTime <= completionTimeOfCurrentJob && jobArray[i].priority < maxPriorityOfJob){
                    currJobIndex = i;
                    maxPriorityOfJob = jobArray[i].priority;
                }
            }
            jobArray[currJobIndex].waitingTime = completionTimeOfCurrentJob - jobArray[currJobIndex].arrivalTime;
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
        System.out.println("Non - Preemptive Priority Scheduling Algorithm");
        System.out.println("Process Name Priority Arrival Time Burst Time Waiting Time Turnaround Time Completion Time");
        for(int i=0; i<noOfProcesses; i++){
            System.out.println(jobArray[i]);
        }

        System.out.println("Average Waiting Time is : " + calculateAverageWaitingTime());
    }

}
