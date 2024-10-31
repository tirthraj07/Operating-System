## Leader Election Algorithms

Many distributed algorithms require a process to act as a coordinator.  
The coordinator can be any process that organizes actions of other processes  

The leader/coordinator often assumes responsibilities such as coordination, resource allocation, or decision-making on behalf of the group. Ensures that there is always a designated node responsible for managing tasks or resources, even in dynamic environments where nodes can fail or join.

But the coordinator can fail. Then how is a new coordinator chosen or __elected__?

This is where election algorithms comes in picture

- Ring Election Algorithm
- Bully Election Algorithm

In Election algorithms, there are few assumptions
- Each process has a unique process number or process id to distinguish them
- Process know each other's process number
- All processes in the system are fully connected.
- The process with the highest priority number will be elected as coordinator.


## Bully Algorithm

The Bully Algorithm is a well-known leader election algorithm used in distributed systems that operates on the principle of higher priority.

- __Initiation__: When a node detects that the current leader has failed (usually through a timeout mechanism), it initiates an election.

- __Election Process__: The initiating node sends an “election” message to all other nodes with higher priority.
Nodes with higher priority respond by either acknowledging their current leader status or declaring themselves candidates.
If no higher-priority node responds, the initiating node assumes leadership.

- __Notification__: The newly elected leader informs all nodes of its leadership status, ensuring consistency across the distributed system.

Here is a working diagram of Bully Election Algorithm
![bully-election-algorithm](public/bully_algorithm.png)


How it works
- When a process P, notices that the coordinator is no longer responding to the request, it initiates an election

- P sends an `Election` message to all the processes with higher priority numbers

- If no one responds, P wins the election and becomes the coordinator

- If one of the higher ups answers, it takes over. P's job is done

- When higher up processes get an `Election` message from one of its lower priority colleagues: Receiver sends an OK message back to the sender to indicate that he is alive and will take over

- Eventually all processes give up apart from one and that one is the new coordinator

- The new coordinator announces it victory by sending all processes a `Coordinator` message telling them that it is the new coordinator

- Now if a process that was previously down comes back, it holds an election

- If it happens to be the highest priority process currently running, it will win the election and take over the coordinator's job

Thus __Biggest guy__ always wind and hence named __Bully Algorithm__
  
  
Input
```
Enter number of processes: 10
Higher the priority number, higher is the priority

Enter priority for process 0: 0
Is process 0 active? (T/F) (Default: T) : 

Enter priority for process 1: 1
Is process 1 active? (T/F) (Default: T) : 

Enter priority for process 2: 2
Is process 2 active? (T/F) (Default: T) : 

Enter priority for process 3: 3
Is process 3 active? (T/F) (Default: T) : 

Enter priority for process 4: 4
Is process 4 active? (T/F) (Default: T) : 

Enter priority for process 5: 5
Is process 5 active? (T/F) (Default: T) :

Enter priority for process 6: 6
Is process 6 active? (T/F) (Default: T) :

Enter priority for process 7: 7
Is process 7 active? (T/F) (Default: T) :

Enter priority for process 8: 8
Is process 8 active? (T/F) (Default: T) :

Enter priority for process 9: 9
Is process 9 active? (T/F) (Default: T) :
```


Output
```
--- BULLY ELECTION ALGORITHM ---
Leader Process: Process 9 with Priority = 9

Leader process failed

Selecting Random Process
Selected Process 4

Starting Simulation with Process 4

Process 4 [Priority 4] sent election message to Process 5 [Priority 5]
Process 4 [Priority 4] sent election message to Process 6 [Priority 6]
Process 4 [Priority 4] sent election message to Process 7 [Priority 7]
Process 4 [Priority 4] sent election message to Process 8 [Priority 8]
Process 4 [Priority 4] sent election message to Process 9 [Priority 9]

Process 7 replied with 'OK'

Received Okay message from one of the higher priority processes
Process 4 Job Done

Restarting algorithm again from Process 7

Starting Simulation with Process 7

Process 7 [Priority 7] sent election message to Process 8 [Priority 8]
Process 7 [Priority 7] sent election message to Process 9 [Priority 9]

Process 8 replied with 'OK'

Received Okay message from one of the higher priority processes
Process 7 Job Done

Restarting algorithm again from Process 8

Starting Simulation with Process 8

Process 8 [Priority 8] sent election message to Process 9 [Priority 9]
Process 9 replied with 'NOT OK'

No OK messages received from higher priority processes

Sending Coordinator message to all lower-priority processes
Process 8 sent Coordinator message to Process 0
Process 8 sent Coordinator message to Process 1
Process 8 sent Coordinator message to Process 2
Process 8 sent Coordinator message to Process 3
Process 8 sent Coordinator message to Process 4
Process 8 sent Coordinator message to Process 5
Process 8 sent Coordinator message to Process 6
Process 8 sent Coordinator message to Process 7

Process 0 replied: New Coordinator Set: Process 8
Process 1 replied: New Coordinator Set: Process 8
Process 2 replied: New Coordinator Set: Process 8
Process 3 replied: New Coordinator Set: Process 8
Process 4 replied: New Coordinator Set: Process 8
Process 5 replied: New Coordinator Set: Process 8
Process 6 replied: New Coordinator Set: Process 8
Process 7 replied: New Coordinator Set: Process 8
--- END ---
```