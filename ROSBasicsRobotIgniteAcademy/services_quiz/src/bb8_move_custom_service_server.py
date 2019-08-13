#! /usr/bin/env python

"""
This service is launched by the start_bb8_move_custom_service_server.launch file. This service will
move the bb8 robot in squares for the requested time of the BB8CustomServiceMessage object that
was passed to it.
"""

import rospy
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageResponse
from geometry_msgs.msg import Twist

def my_callback(request):

    executed_repetitions = 0

    rospy.loginfo("Your request to move bb8 in a square has been received.")

    def go_straight_bb8(side):
        move.linear.x = 0.2
        pub.publish(move)
        rospy.sleep(side)

    def turn_bb8():
        move.angular.z = 0.2
        pub.publish(move)
        rospy.sleep(3.9)

    def stop_bb8():
        move.angular.z = 0.0
        move.linear.x = 0.0
        pub.publish(move)
        rospy.sleep(1.5)

    def move_square_bb8():
        i = 0
        while i < 4:
            go_straight_bb8(request.side)
            stop_bb8()
            turn_bb8()
            stop_bb8()
            i+=1

    while executed_repetitions < request.repetitions:
        move_square_bb8()
        executed_repetitions += 1

    rospy.loginfo("Your bb8 has executed squares for the requested duration.")

    # set response of message to True
    response = BB8CustomServiceMessageResponse()
    response.success = True

    return response # the service Response class, in this case MyCustomServiceMessage

rospy.init_node('move_bb8_service_server')
my_service = rospy.Service('/move_bb8_in_square_custom', BB8CustomServiceMessage , my_callback) # create the Service called /move_bb8_in_circle_custom with the defined callback
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
move = Twist()
rospy.spin() # maintain the service open.
