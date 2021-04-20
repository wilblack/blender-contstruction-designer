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

dir = os.path.dirname(bpy.data.filepath)
print("dir ".format(dir))
if not dir in sys.path:
    sys.path.append(dir )

from pioneer_trail.grounds import create_grounds
from pioneer_trail.house import create_house, create_deck
from pioneer_trail.mtb_track import create_mtb_track
from lumber_yard.utils import feet

scene = bpy.context.scene
trunk_height = 200
TREE1_LOCATION = (12 + feet(5), feet(5), trunk_height / 2)


print("create_ground")
create_grounds(scene, TREE1_LOCATION)

print("Creating house")
create_house(scene)
create_deck(scene)


print("Adding Berm Uprights")
create_mtb_track(scene, anchor=TREE1_LOCATION)


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
