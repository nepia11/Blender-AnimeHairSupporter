import bpy
import os
import math
import mathutils


def get_append_data_blend_path():
    return os.path.join(os.path.dirname(__file__), "_append_data.blend")


def get_taper_enum_items():
    items = [
        ('Tapered', "先細り", "", 'CURVE_DATA'),
        ('TaperedSuper', "より先細り", "", 'MOD_CURVE'),
        ('Sphere', "円", "", 'SPHERECURVE'),
        ('Reversed', "先太り", "", 'PMARKER'),
        ('ReversedSuper', "より先太り", "", 'CURVE_BEZCURVE'),
        ('TaperedOpen', "[根本開き] 先細り", "", 'CURVE_DATA'),
        ('TaperedSuperOpen', "[根本開き] より先細り", "", 'MOD_CURVE'),
        ('SphereOpen', "[根本開き] 円", "", 'SPHERECURVE'),
        ('ReversedOpen', "[根本開き] 先太り", "", 'PMARKER'),
        ('ReversedSuperOpen', "[根本開き] より先太り", "", 'CURVE_BEZCURVE'),
    ]
    for i, item in enumerate(items):
        items[i] = tuple(list(item) + [i + 1])
    return items


def get_bevel_enum_items():
    items = [
        ('Sphere', "円", "", 'MESH_CIRCLE'),
        ('2', "2本", "", 'OUTLINER_OB_META'),
        ('3', "3本", "", 'COLLAPSEMENU'),
        ('Triangle', "三角", "", 'EDITMODE_VEC_HLT'),
        ('TriangleLoose', "ゆるやか三角", "", 'PLAY_REVERSE'),
        ('Square', "四角", "", 'MESH_PLANE'),
        ('SquareLoose', "ゆるやか四角", "", 'LATTICE_DATA'),
        ('Diamond', "ひし形", "", 'SPACE3'),
        ('DiamondLoose', "ゆるやかひし形", "", 'KEYTYPE_EXTREME_VEC'),
        ('Sharp', "シャープ", "", 'LINCURVE'),
        ('Leaf', "葉っぱ", "", 'MAN_ROT'),
        ('V', "切り込み", "", 'FILE_TICK'),
        ('Tilde', "波", "", 'IPO_EASE_IN_OUT'),
        ('Step', "段差", "", 'IPO_CONSTANT'),
        ('Corrugated', "ギザギザ", "", 'RNDCURVE'),
        ('Cloud', "雲", "", 'IPO_ELASTIC'),
    ]
    for i, item in enumerate(items):
        items[i] = tuple(list(item) + [i + 1])
    return items


def relocation_taper_and_bevel(main_ob, sub_ob, is_taper):
    # 位置変更
    if len(main_ob.data.splines):
        if len(main_ob.data.splines[0].points):
            end_co = mul(main_ob.matrix_world, mathutils.Vector(main_ob.data.splines[0].points[-1].co[:3]))
            sub_ob.location = end_co.copy()

    # 回転変更
    if len(main_ob.data.splines):
        spline = main_ob.data.splines[0]
        if 2 <= len(spline.points):
            # 最後の辺をトラック
            sub_ob.rotation_mode = 'QUATERNION'
            last_direction = mul(main_ob.matrix_world, mathutils.Vector(spline.points[-2].co[:3])) - mul(main_ob.matrix_world, mathutils.Vector(spline.points[-1].co[:3]))
            up_direction = mathutils.Vector((0, 0, 1))
            sub_ob.rotation_quaternion = up_direction.rotation_difference(last_direction)
            # Z回転
            diff_co = mul(main_ob.matrix_world, mathutils.Vector(spline.points[-1].co[:3])) - mul(main_ob.matrix_world, mathutils.Vector(spline.points[0].co[:3]))
            rotation_z = math.atan2(diff_co.y, diff_co.x) - spline.points[-1].tilt
            if is_taper:
                sub_ob.rotation_quaternion = mul(sub_ob.rotation_quaternion, mathutils.Quaternion((0, 0, 1), rotation_z))
            else:
                sub_ob.rotation_quaternion = mul(sub_ob.rotation_quaternion, mathutils.Quaternion((0, 0, 1), rotation_z - math.radians(90)))


IS_LEGACY = (bpy.app.version < (2, 80, 0))


def select(obj, value):
    if IS_LEGACY:
        obj.select = value
    else:
        obj.select_set(value)


def get_scene_objects():
    if IS_LEGACY:
        return bpy.context.scene.objects
    else:
        return bpy.context.window.view_layer.objects


def set_active_object(obj):
    if IS_LEGACY:
        bpy.context.scene.objects.active = obj
    else:
        bpy.context.window.view_layer.objects.active = obj


def get_active_object():
    if IS_LEGACY:
        return bpy.context.scene.objects.active
    else:
        return bpy.context.window.view_layer.objects.active


def is_hide(obj):
    if IS_LEGACY:
        return obj.hide
    else:
        return obj.hide_viewport


def set_hide(obj, value):
    if IS_LEGACY:
        obj.hide = value
    else:
        obj.hide_viewport = value


def link_to_scene(obj):
    if IS_LEGACY:
        bpy.context.scene.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)


def region():
    if IS_LEGACY:
        return 'TOOLS'
    else:
        return 'UI'


def box_split(box, factor, align):
    if IS_LEGACY:
        return box.split(percentage=factor, align=align)
    else:
        return box.split(factor=factor, align=align)


def mul(a, b):
    if IS_LEGACY:
        return a * b
    else:
        return a @ b
