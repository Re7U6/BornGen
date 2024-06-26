import bpy
from .op_bone_gen import SkBoneGenOperator

class VIEW3D_PT_SkBoneGenPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_SkBoneGenPanel"
    bl_label = "SKBoneGen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Edit'

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')

    def draw(self, context):
        layout = self.layout
        layout.operator(SkBoneGenOperator.bl_idname, text="Gen")