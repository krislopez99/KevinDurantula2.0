#coding:utf-8
import time 
import math
from lx16a_controller import LX16A_BUS

def mapNum(value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

class Servo:
    def __init__(self):
        self.controller = LX16A_BUS()         

    def setServoAngle(self, id, angle):  
            changed_angle = mapNum(angle, 0, 180, 0, 1000)
            self.controller.moveServo(id, changed_angle)