#! /usr/bin/env python

"""
This service is launched by the start_bb8_move_custom_service_server.launch file. This service will
move the bb8 robot in circles for the requested time of the MyCustomServiceMessageRequest object that
was passed to it.
"""

import rospy
from my_custom_srv_msg_pkg.srv import MyCustomServiceMessage, MyCustomServiceMessageResponse
from geometry_msgs.msg import Twist

def my_callback(request):

    rospy.loginfo("Your request to move bb8 in a circle has been received.")

    # start moving robot in circle for request.duration in seconds
    move.linear.x = 0.5
    move.angular.z = 0.5
    pub.publish(move)
    rospy.sleep(request.duration)

    # stop moving robot once request.duration is completed
    move.linear.x = 0.0
    move.angular.z = 0.0
    pub.publish(move)

    rospy.loginfo("Your bb8 has executed circles for the requested duration.")

    # set response of message to True
    response = MyCustomServiceMessageResponse()
    response.success = True

    return response # the service Response class, in this case MyCustomServiceMessage

rospy.init_node('move_bb8_service_server')
my_service = rospy.Service('/move_bb8_in_circle_custom', MyCustomServiceMessage , my_callback) # create the Service called /move_bb8_in_circle_custom with the defined callback
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
move = Twist()
rospy.spin() # maintain the service open.
