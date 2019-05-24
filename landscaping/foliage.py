from mathutils import Vector
import bpy


mat_tree_top = bpy.data.materials.new(name="Tree Top")
canopy_green = (0.1, 0.4, 0.1)

def create_tree(location, name, trunk_radius, trunk_height, canopy_radius, canopy_depth, canopy_height):
    tree1 = bpy.ops.mesh.primitive_cylinder_add(
        radius=trunk_radius,
        depth=trunk_height,
        location=location)
    obj = bpy.context.object
    obj.name = name
    obj["scripted"] = True
    # create top of tree
    obj = bpy.ops.mesh.primitive_cone_add(
        radius1=canopy_radius,
        depth=canopy_depth,
        location=(location[0], location[1], canopy_height))
    bpy.context.object.data.materials.append(mat_tree_top)
    bpy.context.object.active_material.diffuse_color = canopy_green
    return obj
