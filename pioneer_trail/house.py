import bpy, os, pdb, sys
from mathutils import Vector

from lumber_yard.utils import feet

def create_house(scene):
    location = (0, 40* 12, 0)
    WALL_HEIGHT = 20 * 12
    SOUTH_LENGTH = 40 * 12
    WEST_LENGTH = feet(30)


    SW_CORNER_BOT = Vector((0, 0, 0))
    SW_CORNER_TOP = Vector((0, 0, WALL_HEIGHT))

    SE_CORNER_TOP = Vector((SOUTH_LENGTH, 0, WALL_HEIGHT))
    SE_CORNER_BOT = Vector((SOUTH_LENGTH, 0, 0))

    NW_CORNER_TOP = Vector((0, WEST_LENGTH, WALL_HEIGHT))
    NW_CORNER_BOT = Vector((0, WEST_LENGTH, 0))

    NE_CORNER_TOP = Vector((SOUTH_LENGTH, WEST_LENGTH, WALL_HEIGHT))
    NE_CORNER_BOT = Vector((SOUTH_LENGTH, WEST_LENGTH, 0))

    verts = [
        # South Wall
        SW_CORNER_BOT,
        SW_CORNER_TOP,
        SE_CORNER_TOP,
        SE_CORNER_BOT,

        # West All
        SW_CORNER_BOT,
        SW_CORNER_TOP,
        NW_CORNER_TOP,
        NW_CORNER_BOT,

        # North Wall
        NW_CORNER_BOT,
        NW_CORNER_TOP,
        NE_CORNER_TOP,
        NE_CORNER_BOT,

        # East Wall
        NE_CORNER_BOT,
        NE_CORNER_TOP,
        SE_CORNER_TOP,
        SE_CORNER_BOT

    ]

    edges = []
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15]
    ]

    mesh = bpy.data.meshes.new(name="South Exterior Wall")
    mesh.from_pydata(verts, edges, faces)
    mesh.validate(verbose=True)
    obj = bpy.data.objects.new("2by12", mesh)
    obj.location = location
    obj["scripted"] = True
    scene.objects.link(obj)

