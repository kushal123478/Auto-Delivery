#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt, pi, asin, acos, atan
import tf.transformations

class HuskyBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('husky_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/odometry/filtered',
                                                Odometry, self.update_pose)
        self.traj_subscriber = rospy.Subscriber('/husky_traj_sp',Odometry, self.update_setpoint)
        self.traj_sp = Odometry()
        self.odom = Odometry()
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.odom = data
        self.odom.pose.pose.position.x = round(self.odom.pose.pose.position.x, 4)
        self.odom.pose.pose.position.y = round(self.odom.pose.pose.position.y, 4)

    def update_setpoint(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.traj_sp = data
	
        self.traj_sp.pose.pose.position.x = round(self.traj_sp.pose.pose.position.x, 4)
        self.traj_sp.pose.pose.position.y = round(self.traj_sp.pose.pose.position.y, 4)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        euc = sqrt(pow((goal_pose.pose.pose.position.x - self.odom.pose.pose.position.x), 2) +
                    pow((goal_pose.pose.pose.position.y - self.odom.pose.pose.position.y), 2))
        #print(euc)
        return euc

    def linear_vel(self, goal_pose, constant=0.7):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        op =  constant * self.euclidean_distance(goal_pose)
        #print(op)
        return op

    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return atan2((goal_pose.pose.pose.position.y - self.odom.pose.pose.position.y), (goal_pose.pose.pose.position.x - self.odom.pose.pose.position.x))

    def angular_vel(self, goal_pose, constant=0.5):
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
        


        # Please, insert a number slightly greater than 0 (e.g. 0.01).


        vel_msg = Twist()

        while True:
	    goal_pose = self.traj_sp
            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

if __name__ == '__main__':
    try:
        x = HuskyBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass
