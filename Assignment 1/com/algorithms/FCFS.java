package com.algorithms;

import java.util.Scanner;

/*
First Come First Serve – CPU Scheduling (Non-Preemptive)
Simplest CPU scheduling algorithm that schedules according to arrival times of processes. 
The first come first serve scheduling algorithm states that the process that requests the CPU first is allocated the CPU first. 
It is implemented by using the FIFO queue. 
*/

public class FCFS {
    private int noOfProcesses;
    private Jobs[] jobArray;

    public FCFS(int noOfProcesses){
        this.noOfProcesses = noOfProcesses;
        jobArray = new Jobs[noOfProcesses];
        for(int i=0; i<noOfProcesses; i++){
            jobArray[i] = new Jobs();
            jobArray[i].name = "P" + Integer.toString(i+1);
        }
        
    } 

    public void instantiateArrivalAndBurstTime(){
        System.out.println("Enter Arrival Time and Burst Time for each process");
        Scanner sc = new Scanner(System.in);
        for(int i=0; i<noOfProcesses; i++){
            System.out.print(jobArray[i].name+" : ");
            jobArray[i].arrivalTime = sc.nextInt();
            jobArray[i].burstTime = sc.nextInt();
            sc.nextLine();
        }
        sc.close();
        sortJobArray();
        calculateWaitingTime();
    }

    private void sortJobArray(){
        boolean swapped;
        for(int i=0; i<noOfProcesses-1; i++){
            swapped = false;
            for(int j=0; j<noOfProcesses-i-1; j++){
                if(jobArray[i].arrivalTime > jobArray[i+1].arrivalTime){
                    Jobs temp = jobArray[i];
                    jobArray[i] = jobArray[i+1];
                    jobArray[i+1] = temp;
                    swapped = true;
                }
            }
            if(swapped == false){
                break;
            }
        }
    }

    public void calculateWaitingTime(){
        jobArray[0].waitingTime = 0;
        for(int i=1; i<noOfProcesses; i++){
            Jobs curr = jobArray[i];
            Jobs prev = jobArray[i-1];
            curr.waitingTime = (prev.arrivalTime + prev.burstTime + prev.waitingTime) - curr.arrivalTime;
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
        System.out.println("Process Name \t\t Arrival Time \t\t Burst Time \t\t Waiting Time");
        for(int i=0; i<noOfProcesses; i++){
            System.out.println(jobArray[i]);
        }

        System.out.println("Average Waiting Time is : " + calculateAverageWaitingTime());
    }



}
