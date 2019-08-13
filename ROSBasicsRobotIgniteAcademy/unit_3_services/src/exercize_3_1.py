#! /usr/bin/env python

# Import necessary packages
import rospy
import rospkg
from iri_wam_reproduce_trajectory.srv import ExecTraj

rospack = rospkg.RosPack()

# Initialise a ROS node with the name service_client
rospy.init_node('service_client')

# Wait for the service client /execute_trajectory to be running
rospy.wait_for_service('/execute_trajectory')

# Create the connection to the service
get_food_service = rospy.ServiceProxy('/execute_trajectory', ExecTraj)

# Set variable with trajectory path
traj = rospack.get_path('iri_wam_reproduce_trajectory') + "/config/get_food.txt"