from math import ceil, radians, pi

import bpy, os, pdb, sys
from mathutils import Vector

from lumber_yard.accessaries import Table
from lumber_yard.decking import Decking, Stairs
from lumber_yard.doors import Door, Window
from lumber_yard.utils import feet



COLOR_SADDLE = (107.0/255, 78.0/255, 19.0/255)
COLOR_HOUSE = (163.0/255, 94.0/255, 26.0/255)
COLOR_ROOF = (15.0/255, 80.0/255, 10.0/255)

HOUSE_Y_OFFSET = feet(60)
WALL_HEIGHT = feet(20)
SOUTH_LENGTH = feet(40)
WEST_LENGTH = feet(27.8)


DECK_COLOR = COLOR_SADDLE
DECK_HEIGHT = feet(12)
DECK_LENGTH = feet(12.25)
CURRENT_DECK_WIDTH = feet(19)
CURRENT_DECK_Y_OFFSET = HOUSE_Y_OFFSET + feet(3)

DECK_WIDTH = CURRENT_DECK_WIDTH + feet(9)
DECK_Y_OFFSET = HOUSE_Y_OFFSET - feet(6)
DECK_X_OFFSET = feet(40) + DECK_LENGTH


STEP_EXTENSION_WIDTH = feet(4.5)
STEP_EXTENSION_LENGTH = feet(4)
STEP_EXTENSION_HEIGHT = DECK_HEIGHT
STEP_EXTENSION_X_OFFSET = DECK_X_OFFSET
STEP_EXTENSION_Y_OFFSET = DECK_Y_OFFSET - STEP_EXTENSION_WIDTH

STAIRS_X_OFFSET = STEP_EXTENSION_X_OFFSET - STEP_EXTENSION_LENGTH
STAIRS_Y_OFFSET = STEP_EXTENSION_Y_OFFSET + STEP_EXTENSION_WIDTH


mat_decking = bpy.data.materials.new(name="mat_decking")
mat2 = bpy.data.materials.new(name="mat2")
mat_roof = bpy.data.materials.new(name="mat_roof")
mat_house = bpy.data.materials.new(name="mat_house")
mat_doors = bpy.data.materials.new(name="mat_doors")
mat_windows = bpy.data.materials.new(name="mat_windows")


def create_deck(scene):
    length = DECK_LENGTH
    width = DECK_WIDTH
    height = DECK_HEIGHT

    name = 'new_deck'
    decking = Decking(name, length, width, height)

    for board in decking.boards:
        scene.objects.link(board)
    # Rotate and translate deck
    bpy.ops.object.select_all(action='DESELECT')
    objects = bpy.context.scene.objects
    for obj in objects:
        label = obj.get('label', None)
        if label and label == name:
            print("Selecting {0}".format(label))
            obj.select = True
            obj.data.materials.append(mat_decking)
            bpy.context.scene.objects.active = obj
            bpy.context.object.active_material.diffuse_color = DECK_COLOR

    bpy.ops.object.join()
    bpy.ops.transform.translate(value=(DECK_X_OFFSET, DECK_Y_OFFSET, 0))
    bpy.ops.transform.rotate(value=pi/2, axis=(False, False, True))
    bpy.context.scene.objects.active = None


    # Add step extension
    name = 'step_extension'
    step_extension = Decking(name, STEP_EXTENSION_LENGTH, STEP_EXTENSION_WIDTH, STEP_EXTENSION_HEIGHT)

    for board in step_extension.boards:
        scene.objects.link(board)
    # Rotate and translate deck
    bpy.ops.object.select_all(action='DESELECT')
    objects = bpy.context.scene.objects
    for obj in objects:
        label = obj.get('label', None)
        if label and label == '{0}'.format(name):
            print("Selecting {0}".format(label))
            obj.select = True
            obj.data.materials.append(mat_decking)
            bpy.context.scene.objects.active = obj

    bpy.ops.object.join()
    bpy.ops.transform.translate(value=(STEP_EXTENSION_X_OFFSET, STEP_EXTENSION_Y_OFFSET, 0))
    bpy.ops.transform.rotate(value=pi/2, axis=(False, False, True))
    bpy.context.scene.objects.active = None


    # Add stairs
    name = 'stairs'
    rise = 8.0
    height = DECK_HEIGHT
    length = feet(4)
    board_width = 5.5
    boards_per_step = 2
    stairs = Stairs(name, rise, height, length, board_width, boards_per_step)

    for board in stairs.boards:
        scene.objects.link(board)

    # Rotate and translate stairs
    bpy.ops.object.select_all(action='DESELECT')
    objects = bpy.context.scene.objects
    for obj in objects:
        label = obj.get('label', None)
        if label and label == '{0}'.format(name):
            print("Selecting {0}".format(label))
            obj.select = True
            obj.data.materials.append(mat_decking)
            bpy.context.scene.objects.active = obj

    bpy.ops.object.join()
    bpy.ops.transform.translate(value=(STAIRS_X_OFFSET, STAIRS_Y_OFFSET - feet(0.5), 0))
    bpy.ops.transform.rotate(value=pi, axis=(False, False, True))
    bpy.context.scene.objects.active = None


    # Add a table
    table = Table('table', dx=feet(3), dy=feet(4), height=feet(2.5))
    for object in table.objects:
        scene.objects.link(object)

    bpy.ops.object.select_all(action='DESELECT')
    objects = bpy.context.scene.objects
    for obj in objects:
        label = obj.get('label', None)
        if label and label == 'table'.format(name):
            print("Selecting {0}".format(label))
            obj.select = True
            obj.data.materials.append(mat_doors)
            bpy.context.scene.objects.active = obj

    bpy.ops.object.join()
    bpy.ops.transform.rotate(value=pi/2, axis=(False, False, True))
    bpy.ops.transform.translate(value=(STAIRS_X_OFFSET - feet(1), STAIRS_Y_OFFSET + feet(2), DECK_HEIGHT))


def create_house(scene):
    location = (0, HOUSE_Y_OFFSET, 0)



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
    # House sides
    mesh = bpy.data.meshes.new(name="South Exterior Wall")
    mesh.from_pydata(verts, edges, faces)
    mesh.validate(verbose=True)
    obj = bpy.data.objects.new("house_sides", mesh)
    obj.location = location
    obj["scripted"] = True
    scene.objects.link(obj)
    obj.data.materials.append(mat_house)
    bpy.context.scene.objects.active = obj
    bpy.context.object.active_material.diffuse_color = COLOR_HOUSE

    # House roof
    verts = [
        # ROOF
        SW_CORNER_TOP,
        SE_CORNER_TOP,
        NE_CORNER_TOP,
        NW_CORNER_TOP
    ]
    faces = [
        [0, 1, 2, 3]
    ]
    mesh = bpy.data.meshes.new(name="Roof")
    mesh.from_pydata(verts, edges, faces)
    mesh.validate(verbose=True)
    obj = bpy.data.objects.new("roof", mesh)
    obj.location = location
    obj["scripted"] = True
    scene.objects.link(obj)
    obj.data.materials.append(mat_roof)
    bpy.context.scene.objects.active = obj
    bpy.context.object.active_material.diffuse_color = COLOR_ROOF


    name = 'kitchen_exterior_door'
    door_y_offset = CURRENT_DECK_Y_OFFSET + feet(4)
    length = feet(3.33)
    height = feet(7)
    door = Door(name, height=height, length=length)
    scene.objects.link(door.object)
    bpy.ops.object.select_all(action='DESELECT')
    door.object.select = True
    door.object.data.materials.append(mat_doors)
    bpy.context.scene.objects.active = door.object
    bpy.context.object.active_material.diffuse_color = (1, 1, 1)
    bpy.ops.transform.translate(value=(DECK_X_OFFSET - DECK_LENGTH, door_y_offset, DECK_HEIGHT))
    bpy.context.scene.objects.active = None

    name = 'large_window'
    window_y_offset = door_y_offset + feet(8)
    length = feet(6)
    height = feet(4)
    window = Window(name, height=height, length=length)
    scene.objects.link(window.object)
    bpy.ops.object.select_all(action='DESELECT')
    window.object.select = True
    window.object.data.materials.append(mat_windows)
    bpy.context.scene.objects.active = window.object
    bpy.context.object.active_material.diffuse_color = (1, 1, 1)
    bpy.ops.transform.translate(value=(DECK_X_OFFSET - DECK_LENGTH, window_y_offset, DECK_HEIGHT + feet(2)))
    bpy.context.scene.objects.active = None

    name = 'se_large_window_bot'
    length = feet(5)
    height = feet(3)
    window = Window(name, height=height, length=length)
    scene.objects.link(window.object)
    bpy.ops.object.select_all(action='DESELECT')
    window.object.select = True
    window.object.data.materials.append(mat_windows)
    bpy.context.scene.objects.active = window.object
    bpy.context.object.active_material.diffuse_color = (1, 1, 1)
    bpy.ops.transform.translate(value=(SOUTH_LENGTH - feet(4), HOUSE_Y_OFFSET - 3, feet(3)))
    bpy.ops.transform.rotate(value=pi/2, axis=(False, False, True))
    bpy.context.scene.objects.active = None

    name = 'sw_large_window_bot'
    length = feet(5)
    height = feet(3)
    window = Window(name, height=height, length=length)
    scene.objects.link(window.object)
    bpy.ops.object.select_all(action='DESELECT')
    window.object.select = True
    window.object.data.materials.append(mat_windows)
    bpy.context.scene.objects.active = window.object
    bpy.context.object.active_material.diffuse_color = (1, 1, 1)
    bpy.ops.transform.translate(value=(feet(10), HOUSE_Y_OFFSET - 3, feet(3)))
    bpy.ops.transform.rotate(value=pi/2, axis=(False, False, True))
    bpy.context.scene.objects.active = None


    name = 'se_large_window_top'
    window_y_offset = HOUSE_Y_OFFSET - 3
    length = feet(5)
    height = feet(3)
    window = Window(name, height=height, length=length)
    scene.objects.link(window.object)
    bpy.ops.object.select_all(action='DESELECT')
    window.object.select = True
    window.object.data.materials.append(mat_windows)
    bpy.context.scene.objects.active = window.object
    bpy.context.object.active_material.diffuse_color = (1, 1, 1)
    bpy.ops.transform.translate(value=(SOUTH_LENGTH - feet(3.25), window_y_offset, DECK_HEIGHT + feet(3)))
    bpy.ops.transform.rotate(value=pi/2, axis=(False, False, True))
    bpy.context.scene.objects.active = None
