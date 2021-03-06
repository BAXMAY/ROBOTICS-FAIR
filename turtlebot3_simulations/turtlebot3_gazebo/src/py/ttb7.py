#!/usr/bin/env python
from turtlebot_drive import Turtlebot3_drive
import rospy

class drive(Turtlebot3_drive):

    def __init__(self, team):
        super(drive, self).__init__(team)

    def logic(self):
        if self.initial:
            self.initial = False
            return "walk"

        # 1. Declare variable to know that TTB got a target direction. 0 = not get direction, 1 = get direction
        get_direction = self.mem[0] 

        center_dist = self.top_center_sensor - self.bottom_center_sensor
        left_dist = self.top_left_sensor - self.bottom_left_sensor
        right_dist = self.top_right_sensor - self.bottom_right_sensor

        # When it hit the wall, stop and turn right
        if center_dist < 0.1:
            get_direction = 0
            self.mem[0] = get_direction # Hit the wall means TTB need to find new direction
            if self.current_vel != 0:
                return "stop"
            else:
                return "turn right"
    
        # when return "run" it will exit function
        if get_direction == 1:
            return "run"

        else:
            # Seek for the shortest and turn to its direction
            if center_dist < left_dist:
                min_dist = center_dist
            else:
                min_dist = left_dist
            
            if right_dist < min_dist:
                min_dist = right_dist
            

            # turn to direction and set get_direction
            get_direction = 1
            self.mem[0] = get_direction
            if min_dist == center_dist:
                return "run"
            elif min_dist == right_dist:
                return "turn right"
            elif min_dist == left_dist:
                return "turn left"

if __name__ == '__main__':
    rospy.init_node('drive', anonymous=True)
    rate = rospy.Rate(10)
    try:
        ttb = drive("white")
        while not rospy.is_shutdown():
            ttb.controlLoop()
            rate.sleep()
    except rospy.ROSInterruptException:
        ttb.updatecommandVelocity(0.0, 0.0)
