#! /usr/bin/env python

import rospy
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

reading = LaserScan()
var = Twist()

def callback(reading):

    print reading.ranges[360]

    if reading.ranges[360] > 1:
        var.linear.x = 0.5
        var.angular.z = 0.0

    if reading.ranges[360] < 1:
        var.linear.x = 0.0
        var.angular.z = 0.5

    if reading.ranges[0] < 1:
        var.linear.x = 0.0
        var.angular.z = 0.5

    if reading.ranges[719] < 1:
        var.linear.x = 0.0
        var.angular.z = -0.5

    pub.publish(var)

rospy.init_node('dont_hit_wall')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, callback)
rate = rospy.Rate(2)

while not rospy.is_shutdown():
    rate.sleep()