from mathutils import Vector
import bpy


default_dirt = bpy.data.materials.new(name="Dirt")

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
    return obj


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

    return obj
