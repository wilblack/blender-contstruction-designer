import bpy, os, pdb, sys
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from math import radians

from lumber_yard.utils import feet


GROUND = 'ground'
GRASS_GREEN = (0.1, 0.6, 0.1)

def create_ground(scene):
    width = feet(100)
    flat_length = feet(38) * 12
    verts = [

        Vector((feet(-20), feet(-20), 0)),  # SW Corner
        Vector((flat_length, feet(-20), 0)),        # SE Corner
        Vector((flat_length, width, 0)),      # NE Corner
        Vector((feet(-20), width, 0)),                # NW Corner

        Vector((flat_length + 20 * 12, 0, 6 * 12)),
        Vector((flat_length + 20 * 12, width, 6 * 12)),

    ]

    edges = []
    faces = [
        [0, 1, 2, 3],
        [1, 2, 5, 4]
    ]

    mesh = bpy.data.meshes.new(name="Ground")
    mesh.from_pydata(verts, edges, faces)
    mesh.validate(verbose=True)
    obj = bpy.data.objects.new(GROUND, mesh)
    obj.location = (0, 0, 0)
    obj["scripted"] = True
    scene.objects.link(obj)
    mat = bpy.data.materials.new(name="MaterialName")
    bpy.context.scene.objects.active = obj
    obj.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = GRASS_GREEN

