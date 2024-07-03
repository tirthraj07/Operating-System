import com.algorithms.*;
public class Main{
    public static void main(String[] args) {
        FCFS algo = new FCFS(5);
        algo.instantiateArrivalAndBurstTime();
        algo.printJobs();
    }
}