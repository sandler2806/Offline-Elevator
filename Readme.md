
![alt text](https://github.com/noamv2/offlineElevator/blob/main/Offline_Elevator_algorithm.png)


### The Problem

after constructing a live version of this algorithm, which assign call to elevator in real time. we are tasked with writing an **Offline algorithm**, which receive a data base containing all the calls that occured in some time period and assign all of them to one of the elevators in the building. 
### literature review:


- https://paradigm.suss.edu.sg/the-smart-elevator-scheduling-algorithm-an-illustration-of-computational-intelligence/]
- https://github.com/jhlenes/ElevatorProject
- https://www.geeksforgeeks.org/smart-elevator-pro-geek-cup
- https://www.quora.com/What-algorithm-is-used-in-modern-day-elevators
### The Algorithm:
our algorithm is influenced from it's online version, with some unique features that take advantage of the fact that we can "see into the future when assigning calls.

its important to note that the actuall commanding of the elevator is not defined by our code. the commanding logic is quite simple, the elevator will keep moving in the same direction as long as it has active calls in that direction.

#### algorithms principles:
