
![alt text](https://github.com/noamv2/offlineElevator/blob/main/pics/Offline_Elevator_algorithm.png)


### The Problem

after constructing a live version of this algorithm, which assign call to an elevator in real-time. we are tasked with writing an **Offline algorithm**, which receives a database containing all the calls that occurred in some period and assigns all of them to one of the elevators in the building. 
### literature review:


- https://paradigm.suss.edu.sg/the-smart-elevator-scheduling-algorithm-an-illustration-of-computational-intelligence/]
- https://github.com/jhlenes/ElevatorProject
- https://www.geeksforgeeks.org/smart-elevator-pro-geek-cup
- https://www.quora.com/What-algorithm-is-used-in-modern-day-elevators
### The Algorithm:
our algorithm is influenced by its online version, with some unique features that take advantage of the fact that we can "see into the future when assigning calls.

it is important to note that the actual commanding of the elevator is not defined by our code. the commanding logic is quite simple, the elevator will keep moving in the same direction as long as it has active calls in that direction.

#### algorithms principles:
the algorithm is designed to allocate calls in a way that will leave us with a low average waiting time

the algorithm will allocate an elevator for the call based on several parameters :
- the time it takes to the elevator to complete the call (based on its current unfinished missions)
- the delay suffered by other users of the elevator from handling the call
- how will it affect the next calls - win the war not the fight

we take advantage of the fact that we can "see into the future" to check if picking a certain elevator will affect badly on our average waiting time. the algorithm can comfortably calculate the best choice while looking 3-4 calls ahead on heavy cases and more on small cases.


#### Simulator
we need a set of functions that will help us to simulate the elevators system at any given moment. for that, we built a whole class (simulatorTools)
that helps us to know where are the elevators at a given time, when will an elevator finish its current mission list, and more...
using these tools will help us make the right allocations.

<hr>

### How to run the project

To run the project we have to insert two different command in the terminal <br>
1) to produce the allocations file,  we have to pass the main module 3 files, Building File(json) , Calls File(csv), and another csv to for the output
<br> example:
![image](https://user-images.githubusercontent.com/74304423/142473541-f54f52c0-ce7a-4a92-91fa-1bde2c9ca1b9.png)


2) now we run the checker and supply it with id's, the chosen building and allocations file from before and output log file
<br> example: 
![image](https://user-images.githubusercontent.com/74304423/142473273-b6c2b310-6f0a-436d-940a-23438206fab6.png)

the average waiting time will be shown in the terminal right after running the checker
<br>
![image](https://user-images.githubusercontent.com/74304423/142474384-e591b7a2-9bf7-4490-a304-8320488cb43e.png)

<hr>
### UML Diagram

![UML](https://user-images.githubusercontent.com/74304423/142268875-f4ae05f6-f5fe-46d5-bdc0-8f462576023f.png)


### Results for the elementary cases
Our best results for the elementary cases

![resulat table](https://github.com/noamv2/offlineElevator/blob/main/pics/result%20table.jfif)


### Graphic simulator

using the simulatorTools class and the turtle library we created a simple GUI simulator of the algorithm.
aside from having a visualization, the simulator helped us with finding errors in our logic, as it is much easier to spot them
when you see the elevators moving rather than looking at a boring log file.
#### implementing
the animation was created by using the "turtle" library. each elevator
#### runing the simulator
to run the simulator you have to run 
