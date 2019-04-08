from lumber_yard.two_bys import Board
from lumber_yard.utils import feet

import bpy
from mathutils import Vector


class DoorWindowBase:
    def __init__(self, label, l, w, h):
        self.l = l
        self.h = h
        self.w = w

        verts = [

            Vector((0, 0, 0)),
            Vector((0, 0,self.h)),
            Vector((self.w, 0,self.h)),
            Vector((self.w, 0, 0)),

            Vector((0, self.l, 0)),
            Vector((0, self.l, self.h)),
            Vector((self.w, self.l, self.h)),
            Vector((self.w, self.l, 0)),
        ]

        edges = []
        faces = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 4, 7, 3],
            [1, 5, 6, 2],
            [0, 1, 5, 4],
            [3, 2, 6, 7]
        ]


        mesh = bpy.data.meshes.new(name=label)
        mesh.from_pydata(verts, edges, faces)
        mesh.validate(verbose=True)
        self.object = bpy.data.objects.new(label, mesh)
        self.object["scripted"] = True
        self.object["label"] = label


class Door(DoorWindowBase):

    def __init__(self, label, height, length):
        thickness = feet(0.5)
        super(Door, self).__init__(label, length, thickness, height)


class Window(DoorWindowBase):

    def __init__(self, label, height, length):
        thickness = feet(0.5)
        super(Window, self).__init__(label, length, thickness, height)



