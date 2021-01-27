import bpy
import mathutils
from . import _common


class ahs_maincurve_activate(bpy.types.Operator):
    bl_idname = 'object.ahs_maincurve_activate'
    bl_label = "メインカーブをアクティブ化"
    bl_description = "参照元であるメインカーブへアクティブを移す"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            # poll内でリスト作ると重そう
            taper_and_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object] + [c.bevel_object for c in context.blend_data.curves if c.bevel_object]
            if _common.get_active_object() not in taper_and_bevel_objects:
                return False
        except:
            return False
        return True

    def execute(self, context):
        ob = _common.get_active_object()

        parent_objects = []
        for o in context.blend_data.objects:
            if o.type != 'CURVE':
                continue
            if o.data.taper_object == ob:
                parent_objects.append(o)
            if o.data.bevel_object == ob:
                parent_objects.append(o)

        for o in context.blend_data.objects:
            _common.select(o, False)

        def get_center(ob):
            total_co = mathutils.Vector()
            for seq in ob.bound_box:
                total_co += ob.matrix_world * mathutils.Vector((seq[0], seq[1], seq[2]))
            return total_co / 8

        nearest_length = 9**9
        for target_ob in parent_objects:
            _common.select(target_ob, True)
            _common.set_hide(target_ob, False)

            length = (ob.location - get_center(target_ob)).length
            if length < nearest_length:
                nearest_length = length
                _common.set_active_object(target_ob)

        return {'FINISHED'}
