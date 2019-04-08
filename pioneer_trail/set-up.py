


bl_info = {
    "name": "2 x 12",
    "author": "Wil Black    ",
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
from lumber_yard.two_bys import add_2by12
from lumber_yard.utils import feet

scene = bpy.context.scene
mat_dirt = bpy.data.materials.new(name="Dirt")
mat_tree_top = bpy.data.materials.new(name="Tree Top")
canopy_green = (0.1, 0.4, 0.1)




TREE_1 = 'tree1'
TREE_2 = 'tree2'

BERM_POST_1 = 'berm post 1'
BERM_POST_2 = 'berm post 2'
BERM_POST_3 = 'berm post 3'
BERM_POST_4 = 'berm post 4'

TABLE_B1 = 'table top B1'
TABLE_B2 = 'table top B2'
TABLE_B3 = 'table top B3'
TABLE_B4 = 'table top B4'


backstop_x = 24


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


def create_berm_posts():

    berm_posts = [
        (BERM_POST_1, (backstop_x, 168, 0), (0, 0, radians(90))),
        (BERM_POST_2, (backstop_x, 216, 0), (0, 0, radians(90))),
        (BERM_POST_3, (backstop_x, 264, 0), (0, 0, radians(90))),
        (BERM_POST_4, (backstop_x + 72, 324, 0), (0, 0, 0))
    ]

    verts = [
        Vector((0, 0, 0)),
        Vector((3.5, 0, 0)),
        Vector((3.5, 5.5, 0)),
        Vector((0, 5.5, 0)),

        Vector((0, 0, 12 * 9)),
        Vector((3.5, 0, 12 * 9)),
        Vector((3.5, 5.5, 12 * 9)),
        Vector((0, 5.5, 12 * 9)),

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

    for post in berm_posts:
        mesh = bpy.data.meshes.new(name="Berm Post")
        mesh.from_pydata(verts, edges, faces)
        mesh.validate(verbose=True)
        obj = bpy.data.objects.new(post[0], mesh)
        obj.location = post[1]
        obj.rotation_euler = post[2]
        obj["scripted"] = True
        scene.objects.link(obj)


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
create_berm_posts()




print("Create_table_tops")
tree1_x = 12 + 5 * 12
right_y = 60 + 18 * 12
locations = [
    (TABLE_B2, (tree1_x + 26 * 12, 60, 0), (0,0,0)),
    (TABLE_B1, (tree1_x + 26 * 12 + 19 *12, 72, 0), (0,0,radians(5))),
    (TABLE_B3, (tree1_x + 26 * 12, right_y, 0), (0,0,0)),
    (TABLE_B4, (tree1_x + 26 * 12 + 18 *12, right_y, 0), (0,0,0))
]
for location in locations:
    create_table_top(location[0], 10 * 12, 4 * 12, 4 * 12, 2.5 * 12, location[1], rotation=location[2])


print("Creating A line jump")
location = (tree1_x + 28 * 12, 11*12, 0.1)
rotation = (0, 0, radians(5))
create_double_jump(5 * 12, 5 *12, 12*12, 7*12, 10 * 12, location, rotation)


print("Adding in 2by12's")
y = feet(4) + 48
z = 18
rotation = (0, radians(90), 0)
_2by12s = [
    [backstop_x, y, z],
    [backstop_x, y, z + 11.5],
    [backstop_x, y, z + 11.5 * 2],
    [backstop_x, y, z + 11.5 * 3],
    [backstop_x, y, z + 11.5 * 4],
    [backstop_x, y, z + 11.5 * 5],
    [backstop_x, y, z + 11.5 * 6],
    [backstop_x, y, z + 11.5 * 7],
    [backstop_x, y, z + 11.5 * 8],
    [backstop_x, y, z + 11.5 * 9],
]
for location in _2by12s:
    obj = add_2by12(scene, feet(16), location, rotation)

print("Adding South 2x12's")
y = 60 + 4 * 12
z = 18
x = backstop_x + 2
rotation = (0, radians(90), radians(-124))
_2by12s = [
    [x, y, z],
    [x, y, z + 11.5],
    [x, y, z + 11.5 * 2],
    [x, y, z + 11.5 * 3],
    [x, y, z + 11.5 * 4],
    [x, y, z + 11.5 * 5],
    [x, y, z + 11.5 * 6],
    [x, y, z + 11.5 * 7],
    [x, y, z + 11.5 * 8],
    [x, y, z + 11.5 * 9],
]
for location in _2by12s:
    obj = add_2by12(scene, feet(10), location, rotation)

print("Adding North 2x12's")
y = 270
z = 18
x = backstop_x + 1.5
rotation = (0, radians(90), radians(-54.5))
_2by12s = [
    [x, y, z],
    [x, y, z + 11.5],
    [x, y, z + 11.5 * 2],
    [x, y, z + 11.5 * 3],
    [x, y, z + 11.5 * 4],
    [x, y, z + 11.5 * 5],
    [x, y, z + 11.5 * 6],
    [x, y, z + 11.5 * 7],
    [x, y, z + 11.5 * 8],
    [x, y, z + 11.5 * 9],
]
for location in _2by12s:
    obj = add_2by12(scene, feet(10), location, rotation)


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

# bpy.ops.view3d.zoom(context, mx=500)
# bpy.ops.view3d.view_pan(context, type='PANLEFT')
bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type='TOP')
bpy.ops.view3d.view_persportho(context, 'EXEC_DEFAULT')


# cam = bpy.data.cameras.new("Cam")
# cam_obj = bpy.data.objects.new("Cam", cam)
# bpy.context.scene.objects.link(cam_obj)
# scene.camera = cam_obj

# camera = bpy.ops.object.camera_add(view_align=False,
#                           location=[feet(50), feet(50), feet(100)],
#                           rotation=[0, 0, 0])


