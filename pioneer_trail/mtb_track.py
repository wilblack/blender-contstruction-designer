import bpy
from mathutils import Vector
from math import radians, sin, cos, pi

from lumber_yard.two_bys import FourBySix, add_2by12
from lumber_yard.utils import feet


BERM_POST_1 = 'berm post 1'
BERM_POST_2 = 'berm post 2'
BERM_POST_3 = 'berm post 3'
BERM_POST_4 = 'berm post 4'


mat_dirt = bpy.data.materials.new(name="Dirt2")


class Berm:
    type = 'berm'
    num_segments = 30
    def __init__(self,label, radius, width, height, d_theta, location=(0, 0, 0), rotation= (0, 0, 0)):
        self.radius = radius
        self.inner_radius = radius - width
        self.height = height
        self.d_theta = d_theta

        print("Creating berm object")
        self.creat_object()
        print("Done creating berm object")
        self.object.location = location
        self.object.rotation_euler = rotation
        self.object["scripted"] = True
        self.object["label"] = label
        self.object['type'] = self.type



    def creat_object(self):
        faces = []
        triangles = []
        dt = self.d_theta / self.num_segments
        for i in range(self.num_segments):
            theta = i * dt
            inner_x = self.inner_radius * sin(theta)
            inner_y = self.inner_radius * cos(theta)
            outer_x = self.radius * sin(theta)
            outer_y = self.radius * cos(theta)

            triangles.extend([
                Vector((inner_x, inner_y, 0)),           # inner bot
                Vector((outer_x, outer_y, self.height)), # outer top
                Vector((outer_x, outer_y, 0))            # outer bottom
            ])

        for i in range(self.num_segments):
            if i == 0:
                continue

            cursor = 3 * (i - 1)

            front_face = [
                cursor,
                cursor + 3,
                cursor + 4,
                cursor + 1
            ]

            back_face = [
                cursor + 1,
                cursor + 4,
                cursor + 5,
                cursor + 2,
            ]
            faces.append(front_face)
            faces.append(back_face)

        print("Creating mesh")
        mesh = bpy.data.meshes.new(name=self.type)
        mesh.from_pydata(triangles, [], faces)
        print("Validating mesh")
        mesh.validate(verbose=True)
        self.object = bpy.data.objects.new(self.type, mesh)
        self.object.data.materials.append(mat_dirt)


def create_berm(scene):
    foo = 0.85
    d_theta = foo * pi
    rot = 180 * (1 - (1 - foo) / 2)
    rotation = (0, 0, radians(rot))
    location = (feet(14.5), feet(17), 0)
    radius = feet(13)
    berm = Berm('berm', radius, feet(5), feet(5), d_theta, location, rotation)
    scene.objects.link(berm.object)
    bpy.context.scene.objects.active = berm.object
    bpy.context.object.active_material.diffuse_color = (0.5, 0.3, 0)


def create_berm_posts(scene, TREE_LOCATION):

    backstop_x = 18.5
    tree_y_offset = TREE_LOCATION[1]
    tree_x_offset = TREE_LOCATION[0]

    back_tree_y_offset = feet(10)
    berm_posts = [
        ((backstop_x, back_tree_y_offset + feet(5), -feet(3)), (radians(90), 0, 0)),
        ((backstop_x, back_tree_y_offset + feet(9), -feet(3)), (radians(90), 0, 0)),
        ((backstop_x, back_tree_y_offset + feet(15), -feet(3)), (radians(90), 0, 0)),
        ((backstop_x + feet(6), back_tree_y_offset + feet(19), -feet(3)), (radians(90), 0, 0))
    ]

    height = feet(10)
    boards = []
    label = 'berm_post'
    for post in berm_posts:
        location = post[0]
        rotation = post[1]
        board = FourBySix(label, height, location, rotation=rotation)
        boards.append(board.object)
        scene.objects.link(board.object)

    bpy.ops.object.select_all(action='DESELECT')
    objects = bpy.context.scene.objects
    for obj in objects:
        obj_label = obj.get('label', None)
        if obj_label and obj_label == label:
            print("Selecting {0}".format(label))
            obj.select = True
            # obj.data.materials.append(mat_doors)
            bpy.context.scene.objects.active = obj


    bpy.ops.object.join()



def create_2by12s(scene):
    print("Adding in 2by12's")
    y = feet(4) + 48
    z = 18
    backstop_x = 24
    rotation = (0, radians(90), 0)
    _2by12s = [
        [backstop_x, y, z],
        [backstop_x, y, z + 11.5],
        [backstop_x, y, z + 11.5 * 2],
        [backstop_x, y, z + 11.5 * 3],
        [backstop_x, y, z + 11.5 * 4],
        [backstop_x, y, z + 11.5 * 5],
        # [backstop_x, y, z + 11.5 * 6],
        # [backstop_x, y, z + 11.5 * 7],
        # [backstop_x, y, z + 11.5 * 8],
        # [backstop_x, y, z + 11.5 * 9],
    ]
    for location in _2by12s:
        obj = add_2by12(scene, feet(18), location, rotation)

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
        # [x, y, z + 11.5 * 6],
        # [x, y, z + 11.5 * 7],
        # [x, y, z + 11.5 * 8],
        # [x, y, z + 11.5 * 9],
    ]
    for location in _2by12s:
        obj = add_2by12(scene, feet(10), location, rotation)

    print("Adding North 2x12's")
    y = feet(24.5)
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
        # [x, y, z + 11.5 * 6],
        # [x, y, z + 11.5 * 7],
        # [x, y, z + 11.5 * 8],
        # [x, y, z + 11.5 * 9],
    ]
    for location in _2by12s:
        obj = add_2by12(scene, feet(10), location, rotation)


def create_mtb_track(scene, TREE_LOCATION):
    create_berm_posts(scene, TREE_LOCATION)
    create_2by12s(scene)
    create_berm(scene)
