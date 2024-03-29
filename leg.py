import numpy as np
from math import isnan
from time import sleep
from lx16a_controller import LX16A_BUS

def mapNum(value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

class Leg:
    def __init__(self,
                id,
                controller,
                junction_servos,
                correction=[0, 0, 0],
                scale=[1, 1, 1],
                constraint=[[0, 180], [0, 180], [0, 180]]):
        self.id = id
        self.junction_servos = junction_servos
        self.correction = correction
        self.constraint = constraint
        self.controller = controller

        self.curr_ang_rec = 0
        self.ang_rec_max = 100

    def set_angle(self, junction, angle):
        if self.curr_ang_rec == self.ang_rec_max:
            set_angle = np.min(
                [angle+self.correction[junction], self.constraint[junction][1]+self.correction[junction], 180])
            set_angle = np.max(
                [set_angle, self.constraint[junction][0]+self.correction[junction], 0])
            
            new_ang = mapNum(set_angle, 0, 180, 0, 1000)
            if not isnan(new_ang):
                self.controller.moveServo(self.junction_servos[junction], int(new_ang))

                self.curr_ang_rec = 0
            print("memes")

        else:
            self.curr_ang_rec += 1


    def move_junctions(self, angles):
        self.set_angle(0, angles[0])
        self.set_angle(1, angles[1])
        self.set_angle(2, angles[2])

    def reset(self, calibrated=False):
        self.set_angle(0, 90)
        self.set_angle(1, 90)
        self.set_angle(2, 90)
