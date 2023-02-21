# domino
from domino.core.api import (nurbs,
                             joint,
                             attribute)
from domino.core.api import controller, icon, matrix, fcurve
from domino.edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Spine01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "spine"
    side = "C"
    index = 0
    description = "maya의 spline ik를 사용한 spine setting입니다. 사용 방법은 mgear의 spine과 거의 같습니다."


class Spine01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))
    _m1.rotate = dt.EulerRotation(0, 0, 90).asQuaternion()
    _m2 = matrix.get_matrix_from_pos((0, 3, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Spine01Identifier(self)
        super(Spine01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Spine01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1, self._m2],
                        "multi": True},
            "offset": {"typ": "doubleAngle",
                       "value": 0,
                       "keyable": False,
                       "channelBox": True},
            "offset_matrix": {"typ": "matrix",
                              "value": self._m1},
            "division": {"typ": "long",
                         "value": 3,
                         "keyable": False},
            "position": {"typ": "double",
                         "value": 0,
                         "keyable": False},
            "max_stretch": {"typ": "double",
                            "value": 1.1,
                            "keyable": False},
            "max_squash": {"typ": "double",
                           "value": 0.95,
                           "keyable": False},
            "hip_position": {"typ": "double",
                             "value": 0.5,
                             "minValue": 0,
                             "maxValue": 1,
                             "keyable": False},
            "stretch_volume_fcurve": {"typ": "double",
                                      "value": 0,
                                      "keyable": False,
                                      "fcurve": {"name": "stretch_volume_fcurve_UU",
                                                 "driven": [],
                                                 "driver": [],
                                                 "floatChange": [0.0, 0.5, 1.0],
                                                 "inAngle": [0.0, 0.0, 0.0],
                                                 "inTangentType": ["auto", "auto", "auto"],
                                                 "inWeight": [1.0, 1.0, 1.0],
                                                 "lock": [True, True, True],
                                                 "outAngle": [0.0, 0.0, 0.0],
                                                 "outTangentType": ["auto", "auto", "auto"],
                                                 "outWeight": [1.0, 1.0, 1.0],
                                                 "time": [],
                                                 "type": "animCurveUU",
                                                 "valueChange": [0.0, -1.0, 0.0],
                                                 "weightedTangents": [False]}},
            "squash_volume_fcurve": {"typ": "double",
                                     "value": 0,
                                     "keyable": False,
                                     "fcurve": {"name": "squash_volume_fcurve_UU",
                                                "driven": [],
                                                "driver": [],
                                                "floatChange": [0.0, 0.5, 1.0],
                                                "inAngle": [0.0, 0.0, 0.0],
                                                "inTangentType": ["auto", "auto", "auto"],
                                                "inWeight": [1.0, 1.0, 1.0],
                                                "lock": [True, True, True],
                                                "outAngle": [0.0, 0.0, 0.0],
                                                "outTangentType": ["auto", "auto", "auto"],
                                                "outWeight": [1.0, 1.0, 1.0],
                                                "time": [],
                                                "type": "animCurveUU",
                                                "valueChange": [0.0, 1.0, 0.0],
                                                "weightedTangents": [False]}}
        })
        return preset


class Spine01Guide(piece.Guide):

    def guide(self):
        data = self.data(Spine01Data.SELF)
        root = super(Spine01Guide, self).guide()
        pos = self.create_position(root, data["anchors"][1])
        self.create_orientation(root, pos)


class Spine01Rig(piece.Rig):

    def objects(self, context):
        super(Spine01Rig, self).objects(context)

        data = self.data(Spine01Data.SELF)
        assembly_data = self.data(Spine01Data.ASSEMBLY)

        uni_scale = False
        if assembly_data["force_uni_scale"]:
            uni_scale = True

        ik_color = self.get_ik_ctl_color()
        fk_color = self.get_fk_ctl_color()

        orient_xyz = matrix.OrientXYZ(dt.Matrix(data["offset_matrix"]))
        normal = orient_xyz.y

        start_pos, end_pos = [dt.Matrix(x).translate for x in data["anchors"]]

        division = data["division"] - 1
        positions = []
        for i in range(division):
            positions.append((end_pos - start_pos) * ((i + 1) / division) + start_pos)

        look_at_m = matrix.get_matrix_look_at(start_pos, end_pos, normal, "xz", self.ddata.negate)
        if self.ddata.negate:
            look_at_ik_m = matrix.get_matrix_look_at(start_pos, end_pos, normal, "x-z", self.ddata.negate)
        else:
            look_at_ik_m = matrix.get_matrix_look_at(start_pos, end_pos, normal, "xz", self.ddata.negate)
        root = self.create_root(context, start_pos)

        m = matrix.set_matrix_position(look_at_m, (end_pos - start_pos) * data["hip_position"] + start_pos)
        name = self.naming("hip", _s="ctl")
        self.hip_ctl, self.hip_loc = self.create_ctl(context=context,
                                                     parent=None,
                                                     name=name,
                                                     parent_ctl=None,
                                                     color=fk_color,
                                                     keyable_attrs=["rx", "ry", "rz"],
                                                     m=m,
                                                     shape="circle",
                                                     width=2,
                                                     height=3.2,
                                                     depth=3.2,
                                                     ro=(0, 0, 90))
        m = matrix.set_matrix_position(look_at_ik_m, start_pos)
        name = self.naming("ik0", _s="ctl")
        self.ik0_ctl, self.ik0_loc = self.create_ctl(context=context,
                                                     parent=self.hip_loc,
                                                     name=name,
                                                     parent_ctl=self.hip_ctl,
                                                     color=ik_color,
                                                     keyable_attrs=["tx", "ty", "tz",
                                                                    "rx", "ry", "rz", "ro"],
                                                     m=m,
                                                     shape="arrow4",
                                                     width=5,
                                                     ro=(0, 0, 90))

        m = matrix.set_matrix_position(look_at_m, start_pos - ((end_pos - start_pos) * 0.01))
        name = self.naming("pelvis", _s="ctl")
        self.pelvis_ctl, self.pelvis_loc = self.create_ctl(context=context,
                                                           parent=None,
                                                           name=name,
                                                           parent_ctl=self.ik0_ctl,
                                                           color=fk_color,
                                                           keyable_attrs=["rx", "ry", "rz", "ro"],
                                                           m=m,
                                                           shape="cube",
                                                           height=2.2,
                                                           depth=2.2)

        m = matrix.set_matrix_position(look_at_ik_m, (end_pos - start_pos) * 0.5 + start_pos)
        name = self.naming("ik_tan", _s="ctl")
        self.ik_tan_ctl, self.ik_tan_loc = self.create_ctl(context=context,
                                                           parent=None,
                                                           name=name,
                                                           parent_ctl=None,
                                                           color=ik_color,
                                                           keyable_attrs=["tx", "ty", "tz"],
                                                           m=m,
                                                           shape="circle3",
                                                           width=0.4)

        m = matrix.set_matrix_position(look_at_ik_m, end_pos)
        name = self.naming("direction", _s="ctl")
        self.direction_ctl, self.direction_loc = self.create_ctl(context=context,
                                                                 parent=None,
                                                                 name=name,
                                                                 parent_ctl=None,
                                                                 color=ik_color,
                                                                 keyable_attrs=["tx", "ty", "tz", "rx"],
                                                                 m=m,
                                                                 shape="circle3",
                                                                 width=0.5)
        name = self.naming("display", "crv", _s="ctl")
        self.display_curve = matrix.transform(root, name, dt.Matrix())
        icon.generate(self.display_curve,
                      [(0, 0, 0), (0, 0, 0)],
                      1,
                      dt.Color(0.55, 0.55, 0.55, 0.55),
                      thickness=1)
        nurbs.constraint(self.display_curve, [self.pelvis_loc, self.direction_loc])
        self.display_curve.getShape().attr("overrideDisplayType").set(2)
        self.display_curve.attr("inheritsTransform").set(0)
        self.display_curve.attr("translate").set((0, 0, 0))
        self.display_curve.attr("rotate").set((0, 0, 0))

        name = self.naming("SC%s", _s="jnt")
        sc_normal = orient_xyz.y * -1
        self.sc_chain = joint.add_chain(root, name, [start_pos, end_pos], sc_normal, negate=self.ddata.negate)
        name = self.naming("SC", "ikh", _s="ctl")
        joint.ikh(self.direction_loc, name, self.sc_chain, solver="ikSCsolver")

        m = matrix.set_matrix_position(look_at_ik_m, end_pos)
        name = self.naming("ik1", _s="ctl")
        self.ik1_ctl, self.ik1_loc = self.create_ctl(context=context,
                                                     parent=self.sc_chain[0],
                                                     name=name,
                                                     parent_ctl=self.direction_ctl,
                                                     color=ik_color,
                                                     keyable_attrs=["tx", "ty", "tz",
                                                                    "rx", "ry", "rz",
                                                                    "ro"],
                                                     m=m,
                                                     shape="arrow4",
                                                     width=5,
                                                     ro=(0, 0, 90))
        name = self.naming("ik1", "autoRot", _s="ctl")
        m = matrix.get_matrix_look_at(end_pos, start_pos, sc_normal, "-xz", False)
        self.ik1_auto_rotate = matrix.transform(self.sc_chain[-1], name, m, offsetParentMatrix=True)
        pm.parent(self.ik1_ctl.getParent(), self.ik1_auto_rotate)

        m = matrix.set_matrix_position(look_at_ik_m, (end_pos - start_pos) * 0.4 + start_pos)
        name = self.naming("ik0_tan", _s="ctl")
        self.ik0_tan_ctl, self.ik0_tan_loc = self.create_ctl(context=context,
                                                             parent=self.ik0_loc,
                                                             name=name,
                                                             parent_ctl=self.ik0_ctl,
                                                             color=ik_color,
                                                             keyable_attrs=["tx", "ty", "tz"],
                                                             m=m,
                                                             shape="circle3",
                                                             width=0.2)
        curve_points = [start_pos, m.translate]
        self.ik0_tan_npo = self.ik0_tan_ctl.getParent()
        name = self.naming("ik0_tan", "offset", _s="ctl")
        self.ik0_tan_offset = controller.npo(self.ik0_tan_ctl, name)

        m = matrix.set_matrix_position(look_at_ik_m, (end_pos - start_pos) * 0.6 + start_pos)
        name = self.naming("ik1_tan", _s="ctl")
        self.ik1_tan_ctl, self.ik1_tan_loc = self.create_ctl(context=context,
                                                             parent=self.ik1_loc,
                                                             name=name,
                                                             parent_ctl=self.ik1_ctl,
                                                             color=ik_color,
                                                             keyable_attrs=["tx", "ty", "tz"],
                                                             m=m,
                                                             shape="circle3",
                                                             width=0.2)
        curve_points.append(m.translate)
        curve_points.append(end_pos)
        self.ik1_tan_npo = self.ik1_tan_ctl.getParent()
        name = self.naming("ik1_tan", "offset", _s="ctl")
        self.ik1_tan_offset = controller.npo(self.ik1_tan_ctl, name)

        name = self.naming("original", "crv", _s="ctl")
        self.spline_original_crv = nurbs.create(root,
                                                name,
                                                degree=3,
                                                positions=curve_points,
                                                m=root.getMatrix(worldSpace=True),
                                                bezier=False,
                                                vis=False,
                                                inherits=True,
                                                display_type=1)
        name = self.naming("deform", "crv", _s="ctl")
        self.spline_deform_crv = nurbs.create(root,
                                              name,
                                              degree=3,
                                              positions=curve_points,
                                              m=root.getMatrix(worldSpace=True),
                                              bezier=False,
                                              vis=False,
                                              inherits=False,
                                              display_type=1)
        nurbs.constraint(self.spline_deform_crv, [self.ik0_loc, self.ik0_tan_loc, self.ik1_tan_loc, self.ik1_loc])

        fk_offset = (end_pos - start_pos) / division
        name = self.naming("SP%s", _s="jnt")
        self.sp_chain = joint.add_chain(root,
                                        name,
                                        [start_pos + fk_offset * i for i in range(division + 1)],
                                        normal,
                                        negate=self.ddata.negate)
        name = self.naming("SP0", "loc", _s="ctl")
        self.sp0_loc = pm.createNode("transform", name=name, parent=self.root)
        pm.connectAttr(self.sp_chain[0].attr("matrix"), self.sp0_loc.attr("offsetParentMatrix"))

        name = self.naming("SP", "ikh", _s="ctl")
        self.sp_ik_h = joint.sp_ikh(root, name, self.sp_chain, self.spline_deform_crv)

        parent_ctl = self.ik0_ctl
        parent = root
        self.fk_ctls = []
        self.fk_locs = []
        for i, m in enumerate(range(division + 1)):
            name = self.naming(f"fk{i}", _s="ctl")
            m = matrix.set_matrix_position(look_at_m, start_pos + fk_offset * i)
            fk_ctl, fk_loc = self.create_ctl(context=context,
                                             parent=parent,
                                             name=name,
                                             parent_ctl=parent_ctl,
                                             color=fk_color,
                                             keyable_attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz", "ro"],
                                             m=m,
                                             shape="cube",
                                             width=0.1,
                                             height=3,
                                             depth=3)
            parent_ctl = fk_ctl
            parent = fk_ctl
            self.fk_ctls.append(fk_ctl)
            self.fk_locs.append(fk_loc)

        name = self.naming("volume", "crv", _s="ctl")
        self.spline_volume_crv = nurbs.create(root,
                                              name,
                                              degree=1,
                                              positions=[dt.Vector((0, 0, 0)) for _ in self.fk_ctls],
                                              m=root.getMatrix(worldSpace=True),
                                              bezier=False,
                                              vis=False,
                                              inherits=False,
                                              display_type=1)
        nurbs.constraint(self.spline_volume_crv, self.fk_ctls)

        name = self.naming(f"fk0_orient", "loc", _s="ctl")
        m = matrix.set_matrix_position(look_at_m, start_pos)
        self.fk_0_lock_orient_loc = matrix.transform(parent=root, name=name, m=m)

        name = self.naming("pelvis", "ref", _s="ctl")
        refs = [self.create_ref(context=context, name=name, anchor=True, m=self.pelvis_loc)]

        for i in range(division + 1):
            anchor = False if i < division else True
            name = self.naming(f"fk{i}", "ref", _s="ctl")
            m = self.fk_locs[i]
            refs.append(self.create_ref(context=context, name=name, anchor=anchor, m=m))

        parent = None
        for i, r in enumerate(refs):
            m = r.getMatrix(worldSpace=True)
            name = self.naming("pelvis", _s="jnt") if i == 0 else self.naming(f"spine{i - 1}", _s="jnt")
            parent = self.create_jnt(context=context,
                                     parent=parent,
                                     name=name,
                                     description=str(i),
                                     ref=r,
                                     m=m,
                                     leaf=False,
                                     uni_scale=uni_scale)

    def attributes(self, context):
        super(Spine01Rig, self).attributes(context)
        host = self.create_host(context)
        data = self.data(Spine01Data.SELF)

        self.position = attribute.add(host,
                                      f"position",
                                      "double",
                                      keyable=True,
                                      minValue=0,
                                      maxValue=1,
                                      defaultValue=data["position"])
        self.stretch_squash = attribute.add(host,
                                            f"stretch_squash_enable",
                                            "double",
                                            keyable=True,
                                            minValue=0,
                                            maxValue=1,
                                            defaultValue=1)
        self.max_stretch = attribute.add(host,
                                         f"max_stretch",
                                         "double",
                                         keyable=True,
                                         minValue=1,
                                         defaultValue=data["max_stretch"])
        self.max_squash = attribute.add(host,
                                        f"max_squash",
                                        "double",
                                        keyable=True,
                                        minValue=0.001,
                                        maxValue=1,
                                        defaultValue=data["max_squash"])
        self.front_bend = attribute.add(host,
                                        f"front_bend",
                                        "double",
                                        keyable=True,
                                        minValue=0,
                                        maxValue=2,
                                        defaultValue=0.5)
        self.side_bend = attribute.add(host,
                                       f"side_bend",
                                       "double",
                                       keyable=True,
                                       minValue=0,
                                       maxValue=2,
                                       defaultValue=0.5)
        self.tangent0 = attribute.add(host,
                                      f"tangent0",
                                      "double",
                                      keyable=True,
                                      minValue=0,
                                      defaultValue=1)
        self.tangent1 = attribute.add(host,
                                      f"tangent1",
                                      "double",
                                      keyable=True,
                                      minValue=0,
                                      defaultValue=1)
        self.lock_orient_0 = attribute.add(host,
                                           f"lock_orient_0",
                                           "double",
                                           keyable=True,
                                           minValue=0,
                                           maxValue=1,
                                           defaultValue=1)
        self.lock_orient_1 = attribute.add(host,
                                           f"lock_orient_1",
                                           "double",
                                           keyable=True,
                                           minValue=0,
                                           maxValue=1,
                                           defaultValue=1)
        self.volume = attribute.add(host,
                                    f"volume",
                                    "double",
                                    keyable=True,
                                    minValue=0,
                                    maxValue=1,
                                    defaultValue=1)
        self.stretch_attrs = []
        self.squash_attrs = []
        stretch_volume_fcurve = self.root.attr("stretch_volume_fcurve").inputs()[0]
        squash_volume_fcurve = self.root.attr("squash_volume_fcurve").inputs()[0]
        stretch_values = fcurve.get_fcurve_values(stretch_volume_fcurve, data["division"])
        for i, value in enumerate(stretch_values):
            self.stretch_attrs.append(attribute.add(self.root,
                                                    f"stretch_volume_value{i}",
                                                    "double",
                                                    keyable=False,
                                                    defaultValue=value))
        squash_values = fcurve.get_fcurve_values(squash_volume_fcurve, data["division"])
        for i, value in enumerate(squash_values):
            self.squash_attrs.append(attribute.add(self.root,
                                                   f"squash_volume_value{i}",
                                                   "double",
                                                   keyable=False,
                                                   defaultValue=value))
        self.fk_vis = attribute.add(host,
                                    f"fk_vis",
                                    "bool",
                                    keyable=True,
                                    defaultValue=False)

    def operators(self, context):
        super(Spine01Rig, self).operators(context)
        data = self.data(Spine01Data.SELF)

        # fk vis
        for ctl in self.fk_ctls:
            shapes = ctl.getShapes()
            for shape in shapes:
                pm.connectAttr(self.fk_vis, shape.attr("v"))

        # direction
        md = pm.createNode("multiplyDivide")
        pm.connectAttr(self.sc_chain[0].attr("rz"), md.attr("input1X"))
        pm.connectAttr(self.front_bend, md.attr("input2X"))
        front_bend = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(self.sc_chain[0].attr("ry"), md.attr("input1X"))
        pm.connectAttr(self.side_bend, md.attr("input2X"))
        side_bend = md.attr("outputX")

        pm.connectAttr(front_bend, self.ik1_auto_rotate.attr("rz"))
        pm.connectAttr(side_bend, self.ik1_auto_rotate.attr("ry"))

        # spline ik handle
        self.sp_ik_h.attr("dTwistControlEnable").set(True)
        self.sp_ik_h.attr("dWorldUpType").set(4)
        if self.ddata.negate:
            self.sp_ik_h.attr("dForwardAxis").set(1)
            self.sp_ik_h.attr("dWorldUpAxis").set(1)
        pm.connectAttr(self.ik0_loc.attr("worldMatrix")[0], self.sp_ik_h.attr("dWorldUpMatrix"))
        pm.connectAttr(self.ik1_loc.attr("worldMatrix")[0], self.sp_ik_h.attr("dWorldUpMatrixEnd"))

        # curve info
        original_crv_shape = self.spline_original_crv.getShape()
        curve_info = pm.arclen(original_crv_shape, ch=1)
        original_curve_length = curve_info.attr("arcLength")

        deform_crv_shape = self.spline_deform_crv.getShape()
        curve_info = pm.arclen(deform_crv_shape, ch=1)
        deform_curve_length = curve_info.attr("arcLength")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(2)
        pm.connectAttr(deform_curve_length, md.attr("input1X"))
        pm.connectAttr(original_curve_length, md.attr("input2X"))
        curve_ratio = md.attr("outputX")

        # stretch & squash
        condition = pm.createNode("condition")
        pm.connectAttr(curve_ratio, condition.attr("firstTerm"))
        pm.connectAttr(self.max_stretch, condition.attr("secondTerm"))
        condition.attr("operation").set(2)
        pm.connectAttr(self.max_stretch, condition.attr("colorIfTrueR"))
        pm.connectAttr(curve_ratio, condition.attr("colorIfFalseR"))
        max_stretch_multiple = condition.attr("outColorR")

        condition = pm.createNode("condition")
        pm.connectAttr(curve_ratio, condition.attr("firstTerm"))
        pm.connectAttr(self.max_squash, condition.attr("secondTerm"))
        condition.attr("operation").set(5)
        pm.connectAttr(self.max_squash, condition.attr("colorIfTrueR"))
        pm.connectAttr(curve_ratio, condition.attr("colorIfFalseR"))
        max_squash_multiple = condition.attr("outColorR")

        condition = pm.createNode("condition")
        pm.connectAttr(curve_ratio, condition.attr("firstTerm"))
        condition.attr("secondTerm").set(1)
        condition.attr("operation").set(3)
        pm.connectAttr(max_stretch_multiple, condition.attr("colorIfTrueR"))
        pm.connectAttr(max_squash_multiple, condition.attr("colorIfFalseR"))
        stretch_squash_multiple = condition.attr("outColorR")

        bta = pm.createNode("blendTwoAttr")
        bta.attr("input")[0].set(1)
        pm.connectAttr(stretch_squash_multiple, bta.attr("input")[1])
        pm.connectAttr(self.stretch_squash, bta.attr("attributesBlender"))
        stretch_squash_switch = bta.attr("output")

        for j in self.sp_chain:
            md = pm.createNode("multiplyDivide")
            pm.connectAttr(stretch_squash_switch, md.attr("input1X"))
            md.attr("input2X").set(j.attr("tx").get())
            pm.connectAttr(md.attr("outputX"), j.attr("tx"))

        # spline offset(ik solver offset) position
        condition = pm.createNode("condition")
        pm.connectAttr(deform_curve_length, condition.attr("firstTerm"))
        pm.connectAttr(original_curve_length, condition.attr("secondTerm"))
        condition.attr("operation").set(3)
        pm.connectAttr(stretch_squash_switch, condition.attr("colorIfTrueR"))
        condition.attr("colorIfFalseR").set(1)
        max_stretch_multiple_condition = condition.attr("outColorR")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(max_stretch_multiple_condition, md.attr("input1X"))
        pm.connectAttr(original_curve_length, md.attr("input2X"))
        stretched_original_curve_length = md.attr("outputX")

        pma = pm.createNode("plusMinusAverage")
        pma.attr("operation").set(2)
        pm.connectAttr(deform_curve_length, pma.attr("input1D")[0])
        pm.connectAttr(stretched_original_curve_length, pma.attr("input1D")[1])

        condition = pm.createNode("condition")
        condition.attr("operation").set(5)
        pm.connectAttr(pma.attr("output1D"), condition.attr("firstTerm"))
        pm.connectAttr(pma.attr("output1D"), condition.attr("colorIfFalseR"))
        offset_position_length_value = condition.attr("outColorR")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(2)
        pm.connectAttr(offset_position_length_value, md.attr("input1X"))
        pm.connectAttr(deform_curve_length, md.attr("input2X"))
        offset_position_u_value = md.attr("outputX")

        mp = pm.createNode("motionPath")
        mp.attr("fractionMode").set(True)
        pm.connectAttr(deform_crv_shape.attr("worldSpace")[0], mp.attr("geometryPath"))
        pm.connectAttr(offset_position_u_value, mp.attr("uValue"))

        npoc = pm.createNode("nearestPointOnCurve")
        pm.connectAttr(deform_crv_shape.attr("worldSpace")[0], npoc.attr("inputCurve"))
        pm.connectAttr(mp.attr("allCoordinates"), npoc.attr("inPosition"))
        position_offset_value = npoc.attr("result.parameter")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(position_offset_value, md.attr("input1X"))
        pm.connectAttr(self.position, md.attr("input2X"))
        ik_offset_value = md.attr("outputX")

        pm.connectAttr(ik_offset_value, self.sp_ik_h.attr("offset"))

        # volume
        volume_crv_shape = self.spline_volume_crv.getShape()
        curve_info = pm.arclen(volume_crv_shape, ch=1)
        volume_curve_length = curve_info.attr("arcLength")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(2)
        pm.connectAttr(volume_curve_length, md.attr("input1X"))
        pm.connectAttr(original_curve_length, md.attr("input2X"))
        volume_curve_ratio = md.attr("outputX")

        pma = pm.createNode("plusMinusAverage")
        pma.attr("operation").set(2)
        pm.connectAttr(volume_curve_ratio, pma.attr("input1D")[0])
        pma.attr("input1D")[1].set(1)

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(3)
        pm.connectAttr(pma.attr("output1D"), md.attr("input1X"))
        md.attr("input2X").set(2)
        pow_value = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(3)
        pm.connectAttr(pow_value, md.attr("input1X"))
        md.attr("input2X").set(0.5)
        abs_value = md.attr("outputX")

        for i in range(data["division"]):
            condition = pm.createNode("condition")
            condition.attr("operation").set(3)
            pm.connectAttr(stretch_squash_switch, condition.attr("firstTerm"))
            condition.attr("secondTerm").set(1)
            pm.connectAttr(self.stretch_attrs[i], condition.attr("colorIfTrueR"))
            pm.connectAttr(self.squash_attrs[i], condition.attr("colorIfFalseR"))

            md = pm.createNode("multiplyDivide")
            pm.connectAttr(condition.attr("outColorR"), md.attr("input1X"))
            pm.connectAttr(self.volume, md.attr("input2X"))
            volume_multiple = md.attr("outputX")

            md = pm.createNode("multiplyDivide")
            pm.connectAttr(abs_value, md.attr("input1X"))
            pm.connectAttr(volume_multiple, md.attr("input2X"))

            pma = pm.createNode("plusMinusAverage")
            pma.attr("input3D")[0].set((1, 1, 1))
            pm.connectAttr(md.attr("outputX"), pma.attr("input3D[1].input3Dx"))
            pm.connectAttr(md.attr("outputX"), pma.attr("input3D[1].input3Dy"))
            pm.connectAttr(md.attr("outputX"), pma.attr("input3D[1].input3Dz"))

            attribute.unlock(self.fk_locs[i], ["sx", "sy", "sz"])
            pm.connectAttr(pma.attr("output3D"), self.fk_locs[i].attr("s"))

        # lock orient
        for i, npo in enumerate([x.getParent() for x in self.fk_ctls]):
            if i == len(self.fk_ctls) - 1:
                pb = pm.createNode("pairBlend")
                pb.attr("rotInterpolation").set(1)
                pm.connectAttr(self.lock_orient_1, pb.attr("weight"))

                target = self.sp_chain[-1]
                target_parent = target.getParent()

                m = self.ik1_loc.getMatrix(worldSpace=True)
                target_parent_m = target_parent.getMatrix(worldSpace=True)
                offset_m = m * target_parent_m.inverse()

                mult_m = pm.createNode("multMatrix")
                mult_m.attr("matrixIn")[0].set(offset_m)
                pm.connectAttr(self.ik1_loc.attr("worldMatrix")[0], mult_m.attr("matrixIn")[1])
                pm.connectAttr(target_parent.attr("worldInverseMatrix")[0], mult_m.attr("matrixIn")[2])

                decom_m = pm.createNode("decomposeMatrix")
                pm.connectAttr(mult_m.attr("matrixSum"), decom_m.attr("inputMatrix"))
                lock_orient = decom_m.attr("outputRotate")

                pm.connectAttr(lock_orient, pb.attr("inRotate2"))
                pm.connectAttr(pb.attr("outRotate"), self.sp_chain[-1].attr("r"))
            pm.connectAttr(self.sp_chain[i].attr("dagLocalMatrix"), npo.attr("offsetParentMatrix"))

        pm.connectAttr(self.sp_chain[0].attr("t"), self.fk_0_lock_orient_loc.attr("t"))
        pm.connectAttr(self.sp_chain[0].attr("s"), self.fk_0_lock_orient_loc.attr("s"))

        decom_m = pm.createNode("decomposeMatrix")
        pm.connectAttr(self.sp_chain[0].attr("matrix"), decom_m.attr("inputMatrix"))
        follow_orient = decom_m.attr("outputRotate")

        root = self.fk_0_lock_orient_loc.getParent()
        mult_m = pm.createNode("multMatrix")
        pm.connectAttr(self.ik0_loc.attr("worldMatrix")[0], mult_m.attr("matrixIn")[0])
        pm.connectAttr(root.attr("worldInverseMatrix")[0], mult_m.attr("matrixIn")[1])

        decom_m = pm.createNode("decomposeMatrix")
        pm.connectAttr(mult_m.attr("matrixSum"), decom_m.attr("inputMatrix"))
        lock_orient = decom_m.attr("outputRotate")

        pb = pm.createNode("pairBlend")
        pb.attr("rotInterpolation").set(1)
        pm.connectAttr(follow_orient, pb.attr("inRotate1"))
        pm.connectAttr(lock_orient, pb.attr("inRotate2"))

        pm.connectAttr(self.lock_orient_0, pb.attr("weight"))
        pm.connectAttr(pb.attr("outRotate"), self.fk_0_lock_orient_loc.attr("r"))

        # pelvis
        pelvis_npo = self.pelvis_ctl.getParent()
        pm.parentConstraint(self.fk_0_lock_orient_loc, pelvis_npo, maintainOffset=True)
        pm.scaleConstraint(self.fk_0_lock_orient_loc, pelvis_npo, maintainOffset=True)

        # tangent ctl
        tan_npo = self.ik_tan_ctl.getParent()
        pm.connectAttr(self.ik_tan_ctl.attr("t"), self.ik0_tan_offset.attr("t"))
        pm.connectAttr(self.ik_tan_ctl.attr("t"), self.ik1_tan_offset.attr("t"))

        pm.pointConstraint(self.ik0_tan_npo, self.ik1_tan_npo, tan_npo, maintainOffset=True)
        pm.orientConstraint(self.ik0_tan_npo, self.ik1_tan_npo, tan_npo, maintainOffset=True)

        distance = pm.createNode("distanceBetween")
        decom = pm.createNode("decomposeMatrix")
        pm.connectAttr(self.ik0_loc.attr("worldMatrix")[0], decom.attr("inputMatrix"))
        pm.connectAttr(decom.attr("outputTranslate"), distance.attr("point1"))
        decom = pm.createNode("decomposeMatrix")
        pm.connectAttr(self.ik1_loc.attr("worldMatrix")[0], decom.attr("inputMatrix"))
        pm.connectAttr(decom.attr("outputTranslate"), distance.attr("point2"))
        distance = distance.attr("distance")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(2)
        pm.connectAttr(original_curve_length, md.attr("input1X"))
        md.attr("input2X").set(original_curve_length.get())
        original_crv_ratio = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(original_crv_ratio, md.attr("input1X"))
        md.attr("input2X").set(distance.get())
        scaled_distance = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(2)
        pm.connectAttr(distance, md.attr("input1X"))
        pm.connectAttr(scaled_distance, md.attr("input2X"))
        normalize_distance = md.attr("outputX")

        opm = self.ik0_tan_npo.attr("offsetParentMatrix").get()
        md = pm.createNode("multiplyDivide")
        pm.connectAttr(normalize_distance, md.attr("input1X"))
        md.attr("input2X").set(opm.translate.x)
        scaled_offset_value = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(self.tangent0, md.attr("input1X"))
        pm.connectAttr(scaled_offset_value, md.attr("input2X"))
        tan0_value = md.attr("outputX")

        pm.connectAttr(tan0_value, self.ik0_tan_npo.attr("tx"))

        opm.translate = (0, 0, 0)
        self.ik0_tan_npo.attr("offsetParentMatrix").set(opm)

        opm = self.ik1_tan_npo.attr("offsetParentMatrix").get()
        md = pm.createNode("multiplyDivide")
        pm.connectAttr(normalize_distance, md.attr("input1X"))
        md.attr("input2X").set(opm.translate.x)
        scaled_offset_value = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(self.tangent1, md.attr("input1X"))
        pm.connectAttr(scaled_offset_value, md.attr("input2X"))
        tan0_value = md.attr("outputX")

        pm.connectAttr(tan0_value, self.ik1_tan_npo.attr("tx"))

        opm.translate = (0, 0, 0)
        self.ik1_tan_npo.attr("offsetParentMatrix").set(opm)

    def connections(self, context):
        super(Spine01Rig, self).connections(context)


class Spine01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Spine01Data(node=node, data=data)
        self._guide = Spine01Guide(self._ddata)
        self._rig = Spine01Rig(self._ddata)
