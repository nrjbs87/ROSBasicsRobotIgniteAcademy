#! /usr/bin/env python

# import necessary packages
import rospy
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageRequest

# initialise a ROS node with the name 'move_bb8_service_client'
rospy.init_node('move_bb8_service_client')
rospy.wait_for_service('/move_bb8_in_square_custom')

# create the connection to the /move_bb8_in_square_custom service and create a server proxy object
move_bb8_square_client = rospy.ServiceProxy('/move_bb8_in_square_custom', BB8CustomServiceMessage)

# define the side and repetitions of the small square movement
move_bb8_small_square_object = BB8CustomServiceMessageRequest()
move_bb8_small_square_object.side = 2.0
move_bb8_small_square_object.repetitions = 2.0
result = move_bb8_square_client(move_bb8_small_square_object)
print(result)

# define the side and repetitions of the large square movement
move_bb8_large_square_object = BB8CustomServiceMessageRequest()
move_bb8_large_square_object.side = 4.0
move_bb8_large_square_object.repetitions = 1.0
result = move_bb8_square_client(move_bb8_large_square_object)
print(result)