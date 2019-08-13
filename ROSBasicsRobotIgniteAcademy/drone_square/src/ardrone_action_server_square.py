#! /usr/bin/env python
import rospy
import actionlib
from actionlib.msg import TestAction, TestActionResult, TestActionFeedback
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import time

class Move_Drone_Class(object):

  # create messages that are used to publish feedback/result
  _feedback = TestActionFeedback()
  _result   = TestActionResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("ardrone_square_as", TestAction, self.goal_callback, False)
    self._as.start()
    self.rate = rospy.Rate(1)

  def stop_drone(self):

    self.move_msg.linear.x = 0.0
    self.move_msg.angular.z = 0.0
    rospy.loginfo("Stopping drone...")
    self.pub_move.publish(self.move_msg)

  def move_forward_drone(self):

    self.move_msg.linear.x = 1.0
    self.move_msg.angular.z = 0.0
    rospy.loginfo("Moving drone forward...")
    self.pub_move.publish(self.move_msg)

  def turn_drone(self):

    self.move_msg.linear.x = 0.0
    self.move_msg.angular.z = 1.0
    rospy.loginfo("Turning drone...")
    self.pub_move.publish(self.move_msg)

  def goal_callback(self, goal):

    success = True

    # define the publishers we'll be using
    self.pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
    self.takeoff_msg = Empty()
    self.pub_move = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    self.move_msg = Twist()
    self.pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
    self.land_msg = Empty()

    side_time = goal.goal
    turn_time = 1.8

    # let drone take off for 3 seconds
    i = 0
    while not i == 3:
      self.pub_takeoff.publish(self.takeoff_msg)
      time.sleep(1)
      rospy.loginfo("Drone is taking off..")
      i = i + 1

    # move drone in square
    sides_completed = 0
    for sides_completed in xrange(0,4):
      print ("in for loop")
      # check that preempt (cancelation) has not been requested by the action client
      if self._as.is_preempt_requested():
        rospy.loginfo('The goal has been cancelled/preempted')
        # the following line, sets the client in preempted state (goal cancelled)
        self._as.set_preempted()
        success = False
        # we end the calculation of the Fibonacci sequence
        break

      self.move_forward_drone()
      time.sleep(side_time)
      self.turn_drone()
      time.sleep(turn_time)

      self._feedback.feedback = sides_completed
      self._as.publish_feedback(self._feedback)
      # the sequence is computed at 1 Hz frequency
      self.rate.sleep()

    if success:
        self._result.result = (side_time*4) + (turn_time*4)
        rospy.loginfo('The total seconds it took the drone to perform the square was %i' % self._result.result )
        self._as.set_succeeded(self._result)

    # land drone for 3 seconds
    i = 0
    while not i == 3:
      self.move_msg.linear.x = 0.0
      self.move_msg.angular.z = 0.0
      self.pub_move.publish(self.move_msg)
      self.pub_land.publish(self.land_msg)
      time.sleep(1)
      rospy.loginfo("Drone is landing..")
      i = i + 1

if __name__ == '__main__':
  rospy.init_node('move_drone_square')
  Move_Drone_Class()
  rospy.spin()