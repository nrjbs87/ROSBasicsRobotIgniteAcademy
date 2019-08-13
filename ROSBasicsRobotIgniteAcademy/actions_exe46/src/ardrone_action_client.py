#! /usr/bin/env python

import rospy
import time
import actionlib
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback

"""
class SimpleGoalState:
    PENDING = 0
    ACTIVE = 1
    DONE = 2
    WARN = 3
    ERROR = 4
"""

# Create some constants with the corresponing vaules from the ArdoneGoal Class
PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

nImage = 1

# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating which photo has been taken
def feedback_callback(feedback):
    global nImage
    print('[Feedback] image n.%d received'%nImage)
    nImage += 1

# initializes the action client node
rospy.init_node('drone_action_client')
rate = rospy.Rate(1)

#takeoff drone publisher
pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)

# fly drone publisher
pub_fly = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
var = Twist()
var.linear.x = 1.0
var.angular.z = 1.0

# land drone publisher
pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)

# create the connection to the action server
client = actionlib.SimpleActionClient('/ardrone_action_server', ArdroneAction)
# waits until the action server is up and running
rospy.loginfo('Waiting for action Server ')
client.wait_for_server()
rospy.loginfo('Action Server Found...')

# creates a goal to send to the action server
goal = ArdroneGoal()
goal.nseconds = 10 # indicates, take pictures along 10 seconds

# sends the goal to the action server, specifying which feedback function
# to call when feedback received

client.send_goal(goal, feedback_cb=feedback_callback)

state_result = client.get_state()

# give drone 3 seconds to take off
i = 0
while not i == 3:
    pub_takeoff.publish(Empty())
    time.sleep(1)
    rospy.loginfo("Drone is taking off..")
    i = i + 1

# while action is not completed, keep flying around
while state_result < DONE:
    state_result = client.get_state()
    rospy.loginfo('Moving around...')
    pub_fly.publish(var)
    rate.sleep()

# give drone 3 seconds to land
i = 0
while not i == 3:
    var.linear.x = 0.0
    var.angular.z = 0.0
    pub_fly.publish(var)
    pub_land.publish(Empty())
    time.sleep(1)
    rospy.loginfo("Drone is landing..")
    i = i + 1

print('[Result] State: %d'%(client.get_state()))

