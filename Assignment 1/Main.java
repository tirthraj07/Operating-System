import com.algorithms.*;

import java.util.Scanner;

/*
Write a program to simulate CPU Scheduling Algorithms: FCFS, SJF (Preemptive),
Priority (Non-Preemptive) and Round Robin (Preemptive). 
*/

public class Main{
    public Jobs[] instantiateArrivalAndBurstTime(int noOfProcesses){
        Jobs[] jobArray = new Jobs[noOfProcesses];
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter Arrival Time and Burst Time for each process");
        for(int i=0; i<noOfProcesses; i++){
            jobArray[i] = new Jobs();
            jobArray[i].name = "P" + Integer.toString(i+1);
            System.out.print(jobArray[i].name+" : ");
            jobArray[i].arrivalTime = sc.nextInt();
            jobArray[i].burstTime = sc.nextInt();
            sc.nextLine();
        }
        return jobArray;
    }

    public static void main(String[] args) {
        int noOfProcesses = 7;
        Jobs[] jobArray = new Main().instantiateArrivalAndBurstTime(noOfProcesses);
        FCFS fcfs_algo = new FCFS(noOfProcesses, jobArray);
        fcfs_algo.printJobs();

        NonPreemptiveSJF nonPreemptiveSJFScheduler = new NonPreemptiveSJF(noOfProcesses, jobArray);
        nonPreemptiveSJFScheduler.printJobs();

        PreemptiveSJF preemptiveSJFScheduler = new PreemptiveSJF(noOfProcesses, jobArray);
        preemptiveSJFScheduler.printJobs();

        NonPreemptivePriorityScheduling nonPreemptivePriorityScheduler = new NonPreemptivePriorityScheduling(noOfProcesses, jobArray);
        nonPreemptivePriorityScheduler.printJobs();

    }
}
