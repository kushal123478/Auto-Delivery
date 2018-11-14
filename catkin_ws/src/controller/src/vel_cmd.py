#!/usr/bin/env python
# Software License Agreement (BSD License)

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry

def send_vel():

    pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)
    rospy.init_node('velocity_command', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        velocity = Twist()
	velocity.linear.x = 0 #dump vel cmd here
	velocity.angular.z = 0 #dump vel cmd here
        rospy.loginfo(velocity)
        pub.publish(velocity)
        rate.sleep()    

if __name__ == '__main__':
    try:
        send_vel()
    except rospy.ROSInterruptException:
        pass
