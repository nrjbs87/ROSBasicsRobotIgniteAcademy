#! /usr/bin/env python
import rospy
import actionlib
from std_msgs.msg import Empty
from actions_quiz.msg import CustomActionMsgAction, CustomActionMsgResult, CustomActionMsgFeedback
import time

class Drone_Custom_Action_Class(object):

  # create messages that are used to publish feedback/result
  _feedback = CustomActionMsgFeedback()
  _result   = CustomActionMsgResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("/action_custom_msg_as", CustomActionMsgAction, self.goal_callback, False)
    self._as.start()
    self.rate = rospy.Rate(1)

  def goal_callback(self, goal):
    r = rospy.Rate(1)
    success = True

    if self._as.is_preempt_requested():
        rospy.loginfo('The goal has been cancelled/preempted')
        # the following line, sets the client in preempted state (goal cancelled)
        self._as.set_preempted()
        success = False

    # define the publishers we'll be using
    self.pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
    self._takeoff_msg = Empty()
    self.pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
    self._land_msg = Empty()

    command = goal.goal
    rospy.loginfo(command)

    if command == "TAKEOFF":

        rospy.loginfo('Drone is attempting to take off')

        while self.pub_takeoff.get_num_connections() < 1:
            rospy.loginfo("Waiting for connection to publisher...")
            self._feedback.feedback = command
            self._as.publish_feedback(self._feedback)
            self.rate.sleep()

        rospy.loginfo("Connected to publisher.")

        self._feedback.feedback = command
        self._as.publish_feedback(self._feedback)
        self.pub_takeoff.publish(self._takeoff_msg)
        self.rate.sleep()

    elif command == "LAND":

        rospy.loginfo('Drone is attempting to land')

        while self.pub_land.get_num_connections() < 1:
            rospy.loginfo("Waiting for connection to publisher...")
            self._feedback.feedback = command
            self._as.publish_feedback(self._feedback)
            self.rate.sleep()

        self._feedback.feedback = command
        self._as.publish_feedback(self._feedback)
        self.pub_land.publish(self._land_msg)
        self.rate.sleep()

    if success:
        self._as.set_succeeded(self._result)

if __name__ == '__main__':
  rospy.init_node('drone_command_via_string')
  Drone_Custom_Action_Class()
  rospy.spin()

