import bpy, math

IMG = "/home/wallago/Personal-Projects/wallago/assets/wallago.png"
OUT = "/home/wallago/Personal-Projects/wallago/assets/spin/frame_"
FRAMES = 120  # frames for a full 360° turn
THICKNESS = 0.06  # card depth (world units); bigger = chunkier edge
RES = 500  # output square resolution

# --- clean scene -----------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# --- load image, get aspect ------------------------------------------------
img = bpy.data.images.load(IMG)
w, h = img.size
aspect = w / h

# --- build a vertical card, object rotation left at identity ---------------
bpy.ops.mesh.primitive_plane_add(size=2)
card = bpy.context.active_object
card.scale = (aspect, 1, 1)
card.rotation_euler = (math.radians(90), 0, 0)  # stand it up (normal -> -Y)
bpy.ops.object.transform_apply(scale=True, rotation=True)

sol = card.modifiers.new("solidify", "SOLIDIFY")
sol.thickness = THICKNESS

# --- material: emit the texture so it stays evenly "lit" while spinning ----
mat = bpy.data.materials.new("logo")
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes["Principled BSDF"]
tex = nt.nodes.new("ShaderNodeTexImage")
tex.image = img
nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
bsdf.inputs["Emission Strength"].default_value = 1.0
bsdf.inputs["Base Color"].default_value = (0, 0, 0, 1)
card.data.materials.append(mat)

# --- turntable animation (linear, clean spin about vertical Z) -------------
# set linear interp as the default BEFORE inserting keys (no fcurve poking)
bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"

card.rotation_euler = (0, 0, 0)
card.keyframe_insert("rotation_euler", frame=1)
# full turn placed one frame PAST the render range, so frame 1 and the last
# rendered frame aren't the same pose -> the gif loops seamlessly
card.rotation_euler = (0, 0, math.radians(360))
card.keyframe_insert("rotation_euler", frame=FRAMES + 1)

# --- camera ----------------------------------------------------------------
bpy.ops.object.camera_add(location=(0, -3.2, 0), rotation=(math.radians(90), 0, 0))
scene.camera = bpy.context.active_object

# --- render settings -------------------------------------------------------
# Eevee was renamed in Blender 4.2+; try the new name, fall back to old.
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except TypeError:
    scene.render.engine = "BLENDER_EEVEE"
scene.render.film_transparent = True
scene.render.resolution_x = RES
scene.render.resolution_y = RES
scene.frame_start = 1
scene.frame_end = FRAMES
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.filepath = OUT
bpy.ops.render.render(animation=True)
