# Jeff Junior
This project is part of the FHV Master-Mechatronics course Applied Robotics. 

A 3-axis robot is equipped with 2 cameras and a red laser pointer. 
The robot looks for a green laser dot on a white flip-chart. 
When the green dot is found, the robot aims its red laser at the same position.

The work of this project includes everything, from the design and construction of the robot
to development of the backwards kinematic and computer vision. 

We build this robot on the libraries of:
*	[Dynamixel](https://github.com/ROBOTIS-GIT/DynamixelSDK)
*	[OpenCV](https://opencv.org/)

The backwards kinematic is implemented in C. 
These functions are provided in a dll. 
The computer vision is implemented in python. 


Fun Fact: 
The name originates from a fellow student who (jokingly) insisted, that we bought the robot 
on amazon and ultimately did no work for this project by ourself. 
