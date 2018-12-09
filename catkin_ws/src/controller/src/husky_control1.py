#!/usr/bin/env python

import rospy, tf
import geometry_msgs.msg, nav_msgs.msg
from math import *
from time import sleep
import pickle
import copy

def get_path(filename):
    with open(filename, 'rb') as f:
        res = pickle.load(f)
    return res

def huskyOdomCallback(message,cargs):
    # Implementation of proportional position control 
    # For comparison to Simulink implementation

    # Callback arguments 
    pub,msg,goal,path = cargs

    # Tunable parameters

    wgain = 10.0 # Gain for the angular velocity [rad/s / rad]
    vconst = 0.3 # Linear velocity when far away [m/s]
    distThresh = 1 # Distance treshold [m]


    # Generate a simplified pose
    pos = message.pose.pose
    quat = pos.orientation
    # From quaternion to Euler
    angles = tf.transformations.euler_from_quaternion((quat.x,quat.y,
                                                       quat.z,quat.w))
    theta = angles[2]
    pose = [pos.position.x, pos.position.y, theta]  # X, Y, Theta 
    
    # Proportional Controller
    v = 0 # default linear velocity
    w = 0 # default angluar velocity
    distance = sqrt((pose[0]-goal[0])**2+(pose[1]-goal[1])**2)
    if (distance > distThresh):
        v = vconst
        desireYaw = atan2(goal[1]-pose[1],goal[0]-pose[0])
        u = desireYaw-theta
        bound = atan2(sin(u),cos(u))
        w = min(0.5 , max(-0.5, wgain*bound))
    elif not(len(path)==0):
        sleep(1) 
        a=path.pop()
        goal[0]=a[0]
        goal[1]=a[1]

        goal[2]=a[2]

        
    # Publish
    msg.linear.x = v
    msg.angular.z = w
    pub.publish(msg)
    
    # Reporting
    print('huskyOdomCallback: x=%4.1f,y=%4.1f dist=%4.2f, cmd.v=%4.2f, cmd.w=%4.2f'%(pose[0],pose[1],distance,v,w))
    if not(len(path)==0):
        print("Next point: ", path[len(path)-1], "Current goal: ", goal[0], goal[1], goal[2])


########################################
# Main Script
# Initialize our node

rospy.init_node('huskycontrol',anonymous=True)


    

# Setup publisher
cmdmsg = geometry_msgs.msg.Twist()
cmdpub = rospy.Publisher('/cmd_vel',geometry_msgs.msg.Twist, queue_size=10)

# Setup subscription - which implemets our controller.
# We pass the publisher, the message to publish and the goal as 
# additional parameters to the callback function.

# Set waypoint for Husky to drive to

goal = [0,0,0]  # Goal
path=get_path('ugv_op_path.pkl')

print(path)
path.reverse()

rospy.Subscriber('odometry/filtered',nav_msgs.msg.Odometry,huskyOdomCallback, 
                 (cmdpub,cmdmsg,goal,path))

    
   

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()

