package com.algorithms;

import java.util.Arrays;
import java.util.Scanner;

public class RoundRobinScheduling {
    Jobs[] jobArray;
    int noOfProcesses;
    int quantumTime;

    public RoundRobinScheduling(int noOfProcesses, Jobs[] v){
        this.noOfProcesses = noOfProcesses;
        jobArray = new Jobs[noOfProcesses];
        for(int i=0; i<noOfProcesses; i++){
            jobArray[i] = new Jobs(v[i]);
            jobArray[i].remainingBurstTime = jobArray[i].burstTime;
        }
        setQuantumTime();
        sortJobsBasedOnArrivalTimeAndBurstTime();
        calculateWaitingTimeForEachJob();
    }

    private void setQuantumTime(){
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter Quantum Time : ");
        quantumTime = sc.nextInt();
        sc.nextLine();
    }

    private void sortJobsBasedOnArrivalTimeAndBurstTime() {
        Arrays.sort(jobArray, (job1, job2)->{
            if(job1.arrivalTime != job2.arrivalTime) return Integer.compare(job1.arrivalTime, job2.arrivalTime);
            return Integer.compare(job1.burstTime, job2.burstTime);
        });

        for(int i=0; i<noOfProcesses; i++){
            System.out.print(jobArray[i].name + ", ");
        }
        System.out.println();
    }


    private void calculateWaitingTimeForEachJob() {
        int currentTime = 0;
        int completedProcesses = 0;
        boolean[] completedProcessesArray = new boolean[noOfProcesses];

        while(completedProcesses != noOfProcesses){
            
            for(int i=0; i<noOfProcesses; i++){
                if(!completedProcessesArray[i] && jobArray[i].arrivalTime <= currentTime){
                    if(jobArray[i].remainingBurstTime > quantumTime){
                        currentTime += quantumTime;
                        jobArray[i].remainingBurstTime -= quantumTime;
                    }
                    else{
                        currentTime += jobArray[i].remainingBurstTime;
                        jobArray[i].remainingBurstTime = 0;
                    }

                    if(jobArray[i].remainingBurstTime == 0){
                        completedProcesses++;
                        completedProcessesArray[i] = true;
                        jobArray[i].completionTime = currentTime;
                        jobArray[i].turnaroundTime = jobArray[i].completionTime - jobArray[i].arrivalTime;
                        jobArray[i].waitingTime = jobArray[i].turnaroundTime - jobArray[i].burstTime;
                    }
                }
            }
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
        System.out.println("Preemptive Round Robin Algorithm");
        System.out.println("Process Name Priority Arrival Time Burst Time Waiting Time Turnaround Time Completion Time");
        for(int i=0; i<noOfProcesses; i++){
            System.out.println(jobArray[i]);
        }
        
        System.out.println("Average Waiting Time is : " + calculateAverageWaitingTime());
    }


}
