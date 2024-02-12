##IM_ROBOT
Given a grid map, and a set of states for the robot, and an inverse sensor model, it builds an occupancy grid using Bayes' filter.  
The python code is to be run on raspberry pi which has been interfaced with an arduino UNO board. The arduino code will read sensor data from the ultrasonic sensor and relay it to the raspberry pi
where the python code uses it to create the occupancy grid. The python code then moves the robot through the arduino interface. 

The inverse sensor model used is as follows:
-The probability of an empty grid is 0.1.
-The probability of an occupied grid is 0.8.
-The probability of grid which can be occupied or be empty is 0.5. 