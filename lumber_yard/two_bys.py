import bpy
from mathutils import Vector



class Board:
    """
    l is the length along y-axis
    h is the thickness, i.e. on a 2by is 1.5, along z-axis
    w is the width of the board, i.e. on a 2by6 its 5.5, along x-axis
    """
    name = '2by'
    def __init__(self, label, l, w, h, location, rotation=(0,0,0)):

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


        mesh = bpy.data.meshes.new(name=self.name)
        mesh.from_pydata(verts, edges, faces)
        mesh.validate(verbose=True)
        self.object = bpy.data.objects.new(self.name, mesh)
        self.object.location = location
        self.object.rotation_euler = rotation
        self.object["scripted"] = True
        self.object["label"] = label



class TwoBySix(Board):
    name = '2by6'
    width = 5.5
    thickness = 1.5

    def __init__(self, label, l, location, rotation=(0,0,0)):
        super(TwoBySix, self).__init__(label, l, self.width, self.thickness, location, rotation)


class TwoByEight(Board):
    name = '2by8'
    width = 7.5
    thickness = 1.5

    def __init__(self, label, l, location, rotation=(0,0,0)):
        super(TwoByEight, self).__init__(label, l, self.width, self.thickness, location, rotation)



class OneByOne(Board):
    name = '1by1'
    width = 1.0
    thickness = 1.0

    def __init__(self, label, l, location=(0, 0, 0), rotation=(0, 0, 0)):
        super(OneByOne, self).__init__(label, l, self.width, self.thickness, location, rotation)



def add_2by12(scene, length, location, rotation=(0,0,0)):

    verts = [
        Vector((0, 0, 0)),
        Vector((0, 0, 1.5)),
        Vector((11.5, 0, 1.5)),
        Vector((11.5, 0, 0)),

        Vector((0, length, 0)),
        Vector((0, length, 1.5)),
        Vector((11.5, length, 1.5)),
        Vector((11.5, length, 0)),
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

    mesh = bpy.data.meshes.new(name="New 2x12")
    mesh.from_pydata(verts, edges, faces)
    mesh.validate(verbose=True)
    obj = bpy.data.objects.new("2by12", mesh)
    obj.location = location
    obj.rotation_euler = rotation
    obj["scripted"] = True
    scene.objects.link(obj)

    mat = bpy.data.materials.new('Material 2')
    tex = bpy.data.textures.new(name="SomeName", type="IMAGE")
    # filepath = "//assests/Wood_Root.jpg"
    # image_path = os.path.expanduser(filepath)
    image_path = "/Users/wilblack/Projects/blender/mtb-track/assets/Wood_Root.jpg"
    image = bpy.data.images.load(image_path)
    tex.image = image

    slot = mat.texture_slots.add()
    slot.texture = tex
    slot.texture_coords = 'UV'
    slot.use_map_color_diffuse = True
    slot.use_map_color_emission = True
    slot.emission_color_factor = 0.5
    slot.use_map_density = True
    slot.mapping = 'FLAT'
    # mat.active_texture = tex
    # mat.texture_slots[0].texture_coords = "GLOBAL"
    # mat.texture_slots[0].mapping = "CUBE"

    bpy.context.scene.objects.active = obj
    obj.data.materials.append(mat)

