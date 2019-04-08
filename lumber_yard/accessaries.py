from math import pi

from lumber_yard.doors import DoorWindowBase
from lumber_yard.two_bys import OneByOne


class Table:

    def __init__(self, label, dx, dy, height):
        self.label = label
        self.dx = dx
        self.dy = dy
        self.thickness = 0.2
        self.height = height
        self.objects = []
        top = DoorWindowBase(label, dy, dx, self.thickness)
        top.object.location = (0, 0, self.height)
        top.object['label'] = label
        self.objects.append(top.object)


        legs = self.get_legs()
        for leg in legs:
            self.objects.append(leg.object)



    def get_legs(self):
        legs = []
        location = (self.dx/2, self.dy/2, 0)
        leg = OneByOne(self.label, self.height, location)
        leg.object['label'] = self.label
        leg.object.rotation_euler = (pi/2, 0, 0)

        legs.append(leg)
        return legs
