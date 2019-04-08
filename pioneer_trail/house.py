from math import ceil, radians, pi

import bpy, os, pdb, sys
from mathutils import Vector

from lumber_yard.decking import Decking, Stairs
from lumber_yard.doors import Door, Window
from lumber_yard.utils import feet



DECK_HEIGHT = feet(12)
HOUSE_Y_OFFSET = feet(50)

DECK_LENGTH = feet(12.25)
CURRENT_DECK_WIDTH = feet(19)
CURRENT_DECK_Y_OFFSET = HOUSE_Y_OFFSET + feet(3)

DECK_WIDTH = CURRENT_DECK_WIDTH + feet(8)
DECK_Y_OFFSET = HOUSE_Y_OFFSET - feet(5)
DECK_X_OFFSET = feet(40) + DECK_LENGTH


STEP_EXTENSION_WIDTH = feet(4)
STEP_EXTENSION_LENGTH = feet(4)
STEP_EXTENSION_HEIGHT = DECK_HEIGHT
STEP_EXTENSION_X_OFFSET = DECK_X_OFFSET
STEP_EXTENSION_Y_OFFSET = DECK_Y_OFFSET - STEP_EXTENSION_WIDTH

STAIRS_X_OFFSET = STEP_EXTENSION_X_OFFSET - STEP_EXTENSION_LENGTH
STAIRS_Y_OFFSET = STEP_EXTENSION_Y_OFFSET + STEP_EXTENSION_WIDTH


mat_decking = bpy.data.materials.new(name="mat_decking")
mat2 = bpy.data.materials.new(name="mat2")
mat3 = bpy.data.materials.new(name="mat3")
mat4 = bpy.data.materials.new(name="mat4")
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
        if label and label == '{0}_2by6'.format(name):
            print("Selecting {0}".format(label))
            obj.select = True
            obj.data.materials.append(mat_decking)
            bpy.context.scene.objects.active = obj
            bpy.context.object.active_material.diffuse_color = (0.8, 0.5, 0.5)

    bpy.ops.object.join()
    bpy.ops.transform.translate(value=(DECK_X_OFFSET, DECK_Y_OFFSET, 0))
    bpy.ops.transform.rotate(value=pi/2, axis=(False, False, True))
    bpy.context.scene.objects.active = None



    name = 'old_deck'
    decking = Decking(name, length, CURRENT_DECK_WIDTH, height + feet(0.5))
    for board in decking.boards:
        scene.objects.link(board)
    # Rotate and translate deck
    bpy.ops.object.select_all(action='DESELECT')
    objects = bpy.context.scene.objects
    for obj in objects:
        label = obj.get('label', None)
        if label and label == '{0}_2by6'.format(name):
            print("Selecting {0}".format(label))
            obj.select = True
            obj.data.materials.append(mat2)
            bpy.context.scene.objects.active = obj
            bpy.context.object.active_material.diffuse_color = (0.6, 0.6, 0.6)
    bpy.ops.object.join()
    bpy.ops.transform.translate(value=(DECK_X_OFFSET, CURRENT_DECK_Y_OFFSET, 0))
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
        if label and label == '{0}_2by6'.format(name):
            print("Selecting {0}".format(label))
            obj.select = True
            obj.data.materials.append(mat_decking)
            bpy.context.scene.objects.active = obj
            bpy.context.object.active_material.diffuse_color = (0.8, 0.5, 0.5)

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
        if label and label == '{0}_2by6'.format(name):
            print("Selecting {0}".format(label))
            obj.select = True
            obj.data.materials.append(mat_decking)
            bpy.context.scene.objects.active = obj

    bpy.ops.object.join()
    bpy.ops.transform.translate(value=(STAIRS_X_OFFSET, STAIRS_Y_OFFSET, 0))
    bpy.ops.transform.rotate(value=pi, axis=(False, False, True))
    bpy.context.scene.objects.active = None



def create_house(scene):
    location = (0, HOUSE_Y_OFFSET, 0)
    WALL_HEIGHT = feet(20)
    SOUTH_LENGTH = feet(40)
    WEST_LENGTH = feet(27.8)


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
        SE_CORNER_BOT,

        # ROOF
        SW_CORNER_TOP,
        SE_CORNER_TOP,
        NE_CORNER_TOP,
        NW_CORNER_TOP

    ]

    edges = []
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15],
        [16, 17, 18, 19]
    ]

    mesh = bpy.data.meshes.new(name="South Exterior Wall")
    mesh.from_pydata(verts, edges, faces)
    mesh.validate(verbose=True)
    obj = bpy.data.objects.new("2by12", mesh)
    obj.location = location
    obj["scripted"] = True
    scene.objects.link(obj)


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
