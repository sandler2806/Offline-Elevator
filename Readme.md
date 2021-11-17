
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

it is important to note that the actuall commanding of the elevator is not defined by our code. the commanding logic is quite simple, the elevator will keep moving in the same direction as long as it has active calls in that direction.

#### algorithms principles:
the algorithm is desigend to allocate calls in a way that will leave us with a low average waiting time

the algorithm will allocare an elevator for the call based on sevral parameters :
- the time it take to the elevator to complete the call (based on it's current unfinished missions)
- the delay cuased to other users of the elevator from handling the call
- how will it affect the next calls - win the war not the fight
- 

we take advantage of the fact that we can "see in to the future" to check if picking certain elevator will affect badly on our average waiting time. the algorithm con comfortably calculate the best chioce while looking 3-4 calls ahead on heavy cases and more on small cases.

### UML Diagram
![UML](https://user-images.githubusercontent.com/74304423/142268875-f4ae05f6-f5fe-46d5-bdc0-8f462576023f.png)


