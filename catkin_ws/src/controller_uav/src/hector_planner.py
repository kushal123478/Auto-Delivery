#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt, atan
import tf.transformations
import pickle


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
        self.path = []

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
        
    def get_path(self, filename):
        with open(filename, 'rb') as f:
            res = pickle.load(f)
        return res

    def plan2goal(self):
        distance_tolerance = 0.2
        print(self.path)
        self.traj_sp.pose.pose.position.x = self.path[0][0]
        self.traj_sp.pose.pose.position.y = self.path[0][1]
        self.traj_sp.pose.pose.position.z = self.path[0][2]
        self.traj_publisher.publish(self.traj_sp)

        j = 1
        while(True):

            self.traj_sp.pose.pose.position.x = self.path[j][0]
            self.traj_sp.pose.pose.position.y = self.path[j][1]
            self.traj_sp.pose.pose.position.z = self.path[j][2]
            self.traj_publisher.publish(self.traj_sp)

            if abs(self.euclidean_distance_x(self.traj_sp))< distance_tolerance and abs(self.euclidean_distance_y(self.traj_sp))<distance_tolerance and abs(self.euclidean_distance_z(self.traj_sp))<distance_tolerance:
                j +=1
		#print('here')
		#print('Current odom')
		#print((self.odom.pose.pose.position.x,self.odom.pose.pose.position.y,self.odom.pose.pose.position.z))
		#print('Goal point')
		#print((self.traj_sp.pose.pose.position.x,self.traj_sp.pose.pose.position.y,self.traj_sp.pose.pose.position.z))
		#print('Distances')
		#print((self.euclidean_distance_x(self.traj_sp), self.euclidean_distance_y(self.traj_sp), self.euclidean_distance_z(self.traj_sp)))
		#print("---------------------------------------------------")
	
            if j == len(self.path):
                break
        rospy.spin()

if __name__ == '__main__':
    
    try:
        

        uav_pkl_path = '/home/kushal/catkin_ws/src/controller_uav/src/uav_op_path.pkl'


        x = HectorPlanner()
        x.path = x.get_path(uav_pkl_path)
        x.plan2goal()
        
    except rospy.ROSInterruptException:
        pass
