#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt, atan
import tf.transformations
import pickle



class HuskyPlanner:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('husky_planner', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.traj_publisher = rospy.Publisher('/husky_traj_sp',Odometry, queue_size=10)
	self.traj_sp = Odometry()
        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/odometry/filtered',Odometry, self.update_pose)	
	
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

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        euc = sqrt(pow((goal_pose.pose.pose.position.x - self.odom.pose.pose.position.x), 2) +
                    pow((goal_pose.pose.pose.position.y - self.odom.pose.pose.position.y), 2))
        #print(euc)
        return euc

    def euclidean_distance_z(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        euc = goal_pose.pose.pose.position.z - self.odom.pose.pose.position.z
        #print(euc)
        return euc  
	 


    def plan2goal(self, path):
        """Moves the turtle to the goal."""
        self.traj_sp.pose.pose.position.x = path[0][0]
        self.traj_sp.pose.pose.position.y = path[0][1]	
        j = 0
        while(True):
            self.traj_sp.pose.pose.position.x = path[j][0]
            self.traj_sp.pose.pose.position.y = path[j][1]
            print("Current setpoint:")
            print(str(path[j][0]) + '\t' + str(path[j][1]))
            self.traj_publisher.publish(self.traj_sp)
            if self.euclidean_distance(self.traj_sp)<0.2:
                j +=1
            if j == len(path):
                break
        rospy.spin()
         
def get_path(path):
    with open(path, 'rb') as f:
        res = pickle.load(f)
    return res
  
	

	#while self.euclidean_distance_x(self.traj_sp)>= distance_tolerance or self.euclidean_distance_z(self.traj_sp)>= distance_tolerance or self.euclidean_distance_z(self.traj_sp)>=distance_tolerance:
            # Publishing our vel_msg
	#while True:
            #self.traj_sp.pose.pose.position.x = 
            #self.traj_sp.pose.pose.position.y = i	            
	    #self.traj_publisher.publish(self.traj_sp)
            # Publish at the desired rat
	

if __name__ == '__main__':
    try:
        file_path = 'ugv_op_path.pkl'
        path = get_path(file_path)
        x = HuskyPlanner()
        x.plan2goal(path)
    except rospy.ROSInterruptException:
        pass
