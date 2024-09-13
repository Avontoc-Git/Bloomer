import bpy

bl_info = {
    "name": "Bloomer",
    "blender": (4, 20, 0),
    "category": "Render",
}

def AddNodes():
    bpy.data.scenes["Scene"].use_nodes = True
    scene = bpy.context.scene
    node_tree = scene.node_tree
    node_tree.nodes.clear()
    glare_node = node_tree.nodes.new(type="CompositorNodeGlare")
    output_node = node_tree.nodes.new(type="CompositorNodeComposite")
    input_node = node_tree.nodes.new(type="CompositorNodeRLayers")

    bpy.data.scenes["Scene"].node_tree.nodes["Glare"].glare_type = 'BLOOM'
    bpy.data.scenes["Scene"].node_tree.nodes["Glare"].threshold = 2
    node_tree.links.new(glare_node.outputs['Image'], output_node.inputs[0])
    node_tree.links.new(input_node.outputs['Image'], glare_node.inputs[0])

def SetViewportEnabled():
    for area in bpy.context.screen.areas: # iterate through areas in current screen
        if area.type == 'VIEW_3D':
            for space in area.spaces: # iterate through spaces in current VIEW_3D area
                if space.type == 'VIEW_3D': # check if space is a 3D view
                    space.shading.use_compositor = 'ALWAYS' # set the viewport shading to rendered

def SetViewportDisabled():
    for area in bpy.context.screen.areas: # iterate through areas in current screen
        if area.type == 'VIEW_3D':
            for space in area.spaces: # iterate through spaces in current VIEW_3D area
                if space.type == 'VIEW_3D': # check if space is a 3D view
                    space.shading.use_compositor = 'DISABLED' # set the viewport shading to rendered


class BLOOM_ADDNODES_Operator(bpy.types.Operator):
    bl_idname = "bloom.addnodes"
    bl_label = "Bloom - Add Nodes"

    def execute(self, context):
        AddNodes()
        return {'FINISHED'}

class BLOOM_ENABLE_Operator(bpy.types.Operator):
    bl_idname = "bloom.enable"
    bl_label = "Bloom - Add Nodes"

    def execute(self, context):
        SetViewportEnabled()
        return {'FINISHED'}

class BLOOM_DISABLE_Operator(bpy.types.Operator):
    bl_idname = "bloom.disable"
    bl_label = "Bloom - Add Nodes"

    def execute(self, context):
        SetViewportDisabled()
        return {'FINISHED'}



class BloomPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Bloom"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Big render button
        row = layout.row()
        row.operator("bloom.addnodes", text="Initialize Bloom")
        row = layout.row()
        split = layout.split()

        # First column
        col = split.column()
        col.operator("bloom.enable", text="Enable Bloom")
        col = split.column(align=True)
        col.operator("bloom.disable", text="Disable Bloom")


def register():
    bpy.utils.register_class(BLOOM_ADDNODES_Operator)
    bpy.utils.register_class(BLOOM_ENABLE_Operator)
    bpy.utils.register_class(BLOOM_DISABLE_Operator)
    bpy.utils.register_class(BloomPanel)

def unregister():
    bpy.utils.unregister_class(BLOOM_ADDNODES_Operator)
    bpy.utils.unregister_class(BLOOM_ENABLE_Operator)
    bpy.utils.unregister_class(BLOOM_DISABLE_Operator)
    bpy.utils.unregister_class(BloomPanel)



if __name__ == "__main__":
    register()
