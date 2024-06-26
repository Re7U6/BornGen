import bpy
from mathutils import Vector
import bmesh

class SkBoneGenOperator(bpy.types.Operator):
    bl_idname = "bone.skbonegen"
    bl_label = "頂点に沿ってボーンを生成"
    bl_description = "選択した頂点に沿ってボーンを生成します"
    bl_options = {'REGISTER', 'UNDO'}
    
    bone_name: bpy.props.StringProperty(
        name="BoneName",
        description="ボーンの名前",
        default="SK_bone"
    )

    bone_num: bpy.props.IntProperty(
        name="BoneNum",
        description="ボーンの番号",
        default=1,
        min=0
    )

    def execute(self, context):
        bone_name = self.bone_name
        bone_num = str(self.bone_num)

        obj = bpy.context.object

        bm = bmesh.from_edit_mesh(obj.data)

        # blenderのバージョンが2.73以上の時に必要
        if bpy.app.version[0] >= 2 and bpy.app.version[1] >= 73:
            bm.verts.ensure_lookup_table()
        
        # 頂点座標、頂点ノーマルを取得
        selected_verts = []
        selected_normal = []

        # 頂点の選択順序を表示
        for v in bm.select_history:
            if isinstance(v, bmesh.types.BMVert) and v.select:
                selected_verts.append(v.co.copy())
                selected_normal.append(v.normal)
        # print(selected_verts)   
        # print(selected_normal)     
        bm.free()


        # アーマチュアを生成
        armature = bpy.data.armatures.new(name='BoneGen.000')
        armature_obj = bpy.data.objects.new('BoneGen.000', armature)
        bpy.context.collection.objects.link(armature_obj)
        bpy.context.view_layer.objects.active = armature_obj
        armature_obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')

        # 選択された頂点の座標に沿ってボーンを配置
        for i in range(len(selected_verts) - 1):
            if i == 0:
                bone_head = selected_verts[i]
                bone_tail = selected_verts[i + 1]
                bone_roll = selected_normal[i]
                bpy.ops.armature.bone_primitive_add(name=bone_name + bone_num + '_1')
                edit_bone = armature_obj.data.edit_bones[-1]
                edit_bone.head = bone_head
                edit_bone.tail = bone_tail
                edit_bone.align_roll(bone_roll)
            else:
                bone_tail = selected_verts[i + 1]
                bone_roll = selected_normal[i + 1]
                vec = selected_verts[i + 1]
                bpy.ops.armature.extrude_move()
                edit_bone = armature_obj.data.edit_bones[-1]
                edit_bone.name = bone_name + '_' + bone_num + '_' + str(i + 1)
                edit_bone.tail = bone_tail
                edit_bone.align_roll(bone_roll)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')



        return {'FINISHED'}