#! /usr/bin/env python

# Import necessary packages
import rospy
import rospkg
from std_srvs.srv import Empty, EmptyRequest # you import the service message python classes generated from Empty.srv.

# Initialise a ROS node with the name 'move_bb8_service_client'
rospy.init_node('move_bb8_service_client')
rospy.wait_for_service('/move_bb8_in_circle')

# Create the connection to the service
move_bb8_client = rospy.ServiceProxy('/move_bb8_in_circle', Empty)
move_bb8_object = EmptyRequest()
result = move_bb8_client(move_bb8_object)
print(result)