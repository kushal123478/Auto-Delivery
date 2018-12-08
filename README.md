# Auto-Delivery
This repository contains the catkin_workspaces and scripts for the robot motion planning project on Autodelivery using a team of robots

I have added the script I used to control the Husky.

Some useful links:
1. A sample of PID controller

https://github.com/ivmech/ivPID/blob/master/PID.py

2. Proportional control for turtlebot

http://wiki.ros.org/turtlesim/Tutorials/Go%20to%20Goal

3. Installing hector

http://wiki.ros.org/hector_quadrotor/Tutorials/Quadrotor%20indoor%20SLAM%20demo

4. Installing husky

http://www.clearpathrobotics.com/assets/guides/husky/SimulatingHusky.html

Change the distro to kinetic. They are using indigo in these tutorials I think.

Latest Update: The ROS framework is working for both UGV and UAV.


#############################################
Execution instructions:
1. roslaunch controller_uav start.launch     !!launch hector and husky together in empty world
2. cd ~/catkin_ws/src/controller_uav/src/
3. python control_quad_with_planning.py
4. python hector_planner.py
