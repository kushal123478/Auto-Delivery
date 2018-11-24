	# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:56:33 2018

@author: kushal
"""

#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt, atan
import tf.transformations

class HectorPlanner:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('hector_planner', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.traj_publisher = rospy.Publisher('/hector_traj_sp',Odometry, queue_size=10)
	self.traj_sp = Odometry()
        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/uav1/ground_truth/state',Odometry, self.update_pose)	
	
        self.odom = Odometry()
        self.rate = rospy.Rate(0.1)

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.odom = data
        self.odom.pose.pose.position.x = round(self.odom.pose.pose.position.x, 4)
        self.odom.pose.pose.position.y = round(self.odom.pose.pose.position.y, 4)
	self.odom.pose.pose.position.z = round(self.odom.pose.pose.position.z, 4)

    def update_setpoint(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.traj_sp = data
        self.traj_sp.pose.pose.position.x = round(self.traj_sp.pose.pose.position.x, 4)
        self.traj_sp.pose.pose.position.y = round(self.traj_sp.pose.pose.position.y, 4)
	self.traj_sp.pose.pose.position.z = round(self.traj_sp.pose.pose.position.z, 4)

    def euclidean_distance_x(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        euc = (goal_pose.pose.pose.position.x - self.odom.pose.pose.position.x)
        #print(euc)
        return euc
        
    def euclidean_distance_y(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        euc = (goal_pose.pose.pose.position.y - self.odom.pose.pose.position.y)
        #print(euc)
        return euc

    def euclidean_distance_z(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        euc = goal_pose.pose.pose.position.z - self.odom.pose.pose.position.z
        #print(euc)
        return euc  
	 


    def plan2goal(self):
        """Moves the turtle to the goal."""
        distance_tolerance = 0.1
        self.traj_sp.pose.pose.position.x = path[0][0]
        self.traj_sp.pose.pose.position.y = path[0][1]
        self.traj_sp.pose.pose.position.z = path[0][2]
        self.traj_publisher.publish(self.traj_sp)
        j = 0
	while(True):
         self.traj_sp.pose.pose.position.x = path[j][0]
         self.traj_sp.pose.pose.position.y = path[j][1]
         self.traj_sp.pose.pose.position.z = path[j][2]
         self.traj_publisher.publish(self.traj_sp)
         if self.euclidean_distance_x(self.traj_sp)< distance_tolerance and self.euclidean_distance_y(self.traj_sp)<distance_tolerance and self.euclidean_distance_z(self.traj_sp)<distance_tolerance:
             j +=1
         if j == len(path):
             break
	#for i in range(1,11,2):
	 #   for j in range(1,11,2):
          #      self.traj_sp.pose.pose.position.x = i
           #     self.traj_sp.pose.pose.position.y = j
            #    self.traj_sp.pose.pose.position.z = 10

#	while self.euclidean_distance_x(self.traj_sp)>= distance_tolerance or self.euclidean_distance_z(self.traj_sp)>= distance_tolerance or self.euclidean_distance_z(self.traj_sp)>=distance_tolerance:
            # Publishing our vel_msg
#	while True:
#            self.traj_sp.pose.pose.position.x = 0
#            self.traj_sp.pose.pose.position.y = 0
#            self.traj_sp.pose.pose.position.z = i	            
#            self.traj_publisher.publish(self.traj_sp)
#            # Publish at the desired rate.
#            self.rate.sleep()
	rospy.spin()

if __name__ == '__main__':
    try:
        path = [(1,1,1),(2,4,2),(3,6,4),(4,4,4,),(1,1,1)]
        x = HectorPlanner()
        x.plan2goal()
    except rospy.ROSInterruptException:
        pass
