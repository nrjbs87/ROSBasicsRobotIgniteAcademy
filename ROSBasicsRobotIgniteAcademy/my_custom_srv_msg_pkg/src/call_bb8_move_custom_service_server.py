#! /usr/bin/env python

"""
This node is launched by the call_bb8_move_custom_service_server.launch file. This node will
start the /move_bb8_in_circle_custom service by passing a MyCustomServiceMessageRequest object
into a /move_bb8_in_circle_custom proxy.
"""
import rospy
from my_custom_srv_msg_pkg.srv import MyCustomServiceMessage, MyCustomServiceMessageRequest

# initialise a ROS node with the name move_custom_circle
rospy.init_node('move_custom_circle')

# wait for the service client /move_bb8_in_circle_custom to be running
rospy.wait_for_service('/move_bb8_in_circle_custom')

# create the connection to the service
move_circle_service = rospy.ServiceProxy('/move_bb8_in_circle_custom', MyCustomServiceMessage)

# set variable with move custom circle request
request_object = MyCustomServiceMessageRequest()

# set custom circle request duration to 10 seconds
request_object.duration = 10

# pass service the request object
result = move_circle_service(request_object)

# print the result given by the service called
print(result)
