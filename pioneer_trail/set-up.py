bl_info = {
    "name": "2 x 12",
    "author": "Wil Black",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > 2x12",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


import bpy, os, pdb, sys
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from math import radians


dir = os.path.dirname(bpy.data.filepath)
print("dir ".format(dir))
if not dir in sys.path:
    sys.path.append(dir )

from pioneer_trail.ground import create_ground
from pioneer_trail.house import create_house, create_deck
from pioneer_trail.mtb_track import create_mtb_track
from lumber_yard.two_bys import add_2by12
from lumber_yard.utils import feet

scene = bpy.context.scene
mat_dirt = bpy.data.materials.new(name="Dirt")
mat_tree_top = bpy.data.materials.new(name="Tree Top")
canopy_green = (0.1, 0.4, 0.1)


TREE_1 = 'tree1'
TREE_2 = 'tree2'

TABLE_B1 = 'table top B1'
TABLE_B2 = 'table top B2'
TABLE_B3 = 'table top B3'
TABLE_B4 = 'table top B4'


def create_trees():

    trunk_height = 200
    location1 = (12 + 5 * 12, 60, trunk_height / 2)
    tree1 = bpy.ops.mesh.primitive_cylinder_add(
        radius=12,
        depth=trunk_height,
        location=location1)
    obj = bpy.context.object
    obj.name = TREE_1
    obj["scripted"] = True
    # create top of tree
    obj = bpy.ops.mesh.primitive_cone_add(
        radius1=10 * 12,
        depth=30 * 12,
        location=(12 + 5 * 12, 60, 350))
    bpy.context.object.data.materials.append(mat_tree_top)
    bpy.context.object.active_material.diffuse_color = canopy_green



    location2 = (12, 60 + 4 * 12, trunk_height / 2)
    tree2 = bpy.ops.mesh.primitive_cylinder_add(
        radius=12,
        depth=trunk_height,
        location=location2)
    obj = bpy.context.object
    obj.name = TREE_2
    obj["scripted"] = True
    bpy.ops.mesh.primitive_cone_add(
        radius1=8 * 12,
        depth=25 * 12,
        location=(12, 60 + 4 * 12, 320))
    bpy.context.object.data.materials.append(mat_tree_top)
    bpy.context.object.active_material.diffuse_color = canopy_green


def create_table_top(name, total_length, top_length, width, height, location, rotation):
    ramp_x = (total_length - top_length) * 0.5
    verts = [
        # Front face
        Vector((total_length, 0, 0)),
        Vector((total_length - ramp_x, 0, height)),
        Vector((total_length - ramp_x, width, height)),
        Vector((total_length, width, 0)),

        # Back face
        Vector((ramp_x, 0, height)),
        Vector((ramp_x, width, height)),
        Vector((0, width, 0)),
        Vector((0, 0, 0)),
    ]

    edges = []
    faces = [
        [0, 1, 2, 3],
        [1, 2, 5, 4],
        [4, 5, 6, 7],

        [0, 1, 4, 7], # Left side
        [2, 3, 6, 5], # Right side
    ]

    mesh = bpy.data.meshes.new(name="New Table Top")
    mesh.from_pydata(verts, edges, faces)
    mesh.validate(verbose=True)
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    obj["scripted"] = True
    scene.objects.link(obj)

    bpy.context.scene.objects.active = obj
    obj.data.materials.append(mat_dirt)
    bpy.context.object.active_material.diffuse_color = (0.5, 0.3, 0)


def create_double_jump(height, width, gap, takeoff_dx, landing_dx, location, rotation=(0,0,0)):
    total_length = gap + takeoff_dx + landing_dx
    landing_x = total_length - takeoff_dx - gap
    verts = [
        # Takeoff Front face
        Vector((total_length, 0, 0)),
        Vector((total_length - takeoff_dx, 0, height)),
        Vector((total_length - takeoff_dx, width, height)),
        Vector((total_length, width, 0)),

        # Takeoff back face
        Vector((total_length - takeoff_dx, 0, height)),
        Vector((total_length - takeoff_dx, width, height)),
        Vector((total_length - takeoff_dx, width, 0)),
        Vector((total_length - takeoff_dx, 0, 0)),

        # Landing back
        Vector((landing_x, 0, 0)),
        Vector((landing_x, width, 0)),
        Vector((landing_x, width, height)),
        Vector((landing_x, 0, height)),

        # Landing face
        Vector((landing_x, width, height)),
        Vector((landing_x, 0, height)),
        Vector((landing_x -landing_dx, 0, 0)),
        Vector((landing_x - landing_dx, width, 0)),
    ]

    edges = []
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7], # Takeoff back
        [6, 7, 8, 9], # Hole
        [8, 9, 10, 11], # Landing back
        [12, 13, 14, 15], # Landing face

        [0, 1, 7], # Takeoff left side
        [3, 5, 6], # Takeoff right side
        [8, 11, 14], # Landing left side
        [9, 10, 15], # Landing left side
    ]

    mesh = bpy.data.meshes.new(name="New Table Top")
    mesh.from_pydata(verts, edges, faces)
    mesh.validate(verbose=True)
    obj = bpy.data.objects.new("Double Jump", mesh)
    obj.location = location
    obj.rotation_euler = rotation
    obj["scripted"] = True
    scene.objects.link(obj)

    bpy.context.scene.objects.active = obj
    obj.data.materials.append(mat_dirt)
    bpy.context.object.active_material.diffuse_color = (0.5, 0.3, 0)


# print("Clear objects")
# for obj in bpy.data.objects:
#
#     # if obj.get('scripted') :
#     print("Deleting {}".format(obj.name))
#     bpy.data.objects.remove(obj, True)

print("create_ground")
create_ground(scene)

print("Creating house")
create_house(scene)
create_deck(scene)

print("Adding Trees")
create_trees()

print("Adding Berm Uprights")
create_mtb_track(scene)

print("Create_table_tops")
tree1_x = 12 + 5 * 12

bline_y_offset = feet(10)
bline_x_offset = feet(15)
bline_return_y_offset = feet(5) + feet(18)

locations = [
    (TABLE_B2, (tree1_x + bline_x_offset, bline_y_offset, 0), (0, 0, 0)),
    (TABLE_B1, (tree1_x + bline_x_offset + + feet(18), bline_y_offset, 0), (0, 0, 0)),
    (TABLE_B1, (tree1_x + bline_x_offset + feet(36), bline_y_offset, 0), (0, 0, 0)),

    ('fsdf', (tree1_x + bline_x_offset, bline_return_y_offset, 0), (0, 0, 0)),
    (TABLE_B3, (tree1_x + bline_x_offset + feet(18), bline_return_y_offset, 0), (0, 0, 0)),
    (TABLE_B4, (tree1_x + bline_x_offset + feet(36), bline_return_y_offset, 0), (0, 0, 0))
]
for location in locations:
    create_table_top(location[0], 10 * 12, 4 * 12, 4 * 12, 2.5 * 12, location[1], rotation=location[2])

print("Creating A line jumps")

aline_y_offset = feet(5)
locations = [
    (tree1_x + feet(14), aline_y_offset, 0.1),
    (tree1_x + feet(14) + feet(30), aline_y_offset, 0.1)
]
gap = feet(10)
height = feet(5)
width = feet(5)
takeoff_dx = feet(7)
landing_dx = feet(10)
rotation = (0, 0, 0)
for location in locations:
    create_double_jump(height, width, gap, takeoff_dx, landing_dx, location, rotation)


for area in bpy.context.screen.areas:
    if area.type == "VIEW_3D":
        break

for region in area.regions:
    if region.type == "WINDOW":
        break

space = area.spaces[0]

context = bpy.context.copy()
context['area'] = area
context['region'] = region
context['space_data'] = space


bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type='TOP')
bpy.ops.view3d.view_persportho(context, 'EXEC_DEFAULT')
