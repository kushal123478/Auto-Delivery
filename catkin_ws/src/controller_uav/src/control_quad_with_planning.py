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

class HectorBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('hector_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/uav1/cmd_vel',Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/uav1/ground_truth/state',Odometry, self.update_pose)
	self.traj_subscriber = rospy.Subscriber('/hector_traj_sp',Odometry, self.update_setpoint)
	self.traj_sp = Odometry()
        self.odom = Odometry()
        self.rate = rospy.Rate(10)

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

    def x_vel(self, goal_pose, constant=0.4):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        op =  constant * self.euclidean_distance_x(goal_pose)
        #print(op)
        return op
        
    def y_vel(self, goal_pose, constant=0.4):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        op =  constant * self.euclidean_distance_y(goal_pose)
        #print(op)
        return op    
        
    def z_vel(self, goal_pose, constant=0.4):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        op =  constant * self.euclidean_distance_z(goal_pose)
        #print(op)
        return op

    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""        
        return atan2((goal_pose.pose.pose.position.y - self.odom.pose.pose.position.y), (goal_pose.pose.pose.position.x - self.odom.pose.pose.position.x))

    def yaw_vel(self, goal_pose, constant=0.5):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM.""" 
        x = self.odom.pose.pose.orientation.x
        y = self.odom.pose.pose.orientation.y
        z = self.odom.pose.pose.orientation.z
        w = self.odom.pose.pose.orientation.w
        #angle = atan2(2*(w*z + y*x),(1-2*(z**2 + y**2)))
        quaternion = [self.odom.pose.pose.orientation.x,
                      self.odom.pose.pose.orientation.y,
                      self.odom.pose.pose.orientation.z,
                      self.odom.pose.pose.orientation.w]        
        [roll,pitch,yaw] = tf.transformations.euler_from_quaternion(quaternion)
	print("The current yaw")
	print(yaw)
        return constant * (self.steering_angle(goal_pose) - yaw)



    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = self.traj_sp


        # Please, insert a number slightly greater than 0 (e.g. 0.01).

        vel_msg = Twist()

        while True:#self.euclidean_distance_x(goal_pose) >= 0.1 or self.euclidean_distance_z(goal_pose) >= 0.1 or self.euclidean_distance_z(goal_pose) >= 0.1 :

            # Porportional controller.
            # https://en.wikipedia.org/wiki/Proportional_control
	    print(goal_pose)
            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.x_vel(goal_pose)
            vel_msg.linear.y = self.y_vel(goal_pose)
            vel_msg.linear.z = self.z_vel(goal_pose)

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0#self.yaw_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
   #     vel_msg.linear.x = 0
   #     vel_msg.angular.z = 0
   #     self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

if __name__ == '__main__':
    try:
        x = HectorBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass
