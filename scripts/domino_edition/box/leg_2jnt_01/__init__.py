# domino
from domino.api import (matrix,
                        joint,
                        icon,
                        nurbs,
                        attribute,
                        controller,
                        operators,
                        callback,
                        fcurve,
                        vector)
from domino_edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Leg2jnt01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "leg"
    side = "C"
    index = 0
    description = "사람의 다리입니다. foot_01과 연결 될 수 있습니다."


class Leg2jnt01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))
    _m2 = matrix.get_matrix_from_pos((0, -2, 0.01))
    _m3 = matrix.get_matrix_from_pos((0, -4, 0))
    _m4 = matrix.get_matrix_from_pos((0, -4, 1))

    def __init__(self, node=None, data=None):
        self._identifier = Leg2jnt01Identifier(self)
        super(Leg2jnt01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Leg2jnt01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1, self._m2, self._m3, self._m4],
                        "multi": True},
            "offset_pole_vec": {"typ": "double",
                                "value": 1,
                                "channelBox": True},
            "offset_pole_vec_matrix": {"typ": "matrix",
                                       "value": dt.Matrix()},
            "upper_division": {"typ": "long",
                               "value": 3},
            "lower_division": {"typ": "long",
                               "value": 3},
            "fk_ik": {"typ": "double",
                      "value": 0},
            "max_stretch": {"typ": "double",
                            "value": 1.5},
            "ik_space_switch_array": {"typ": "string",
                                      "value": ""},
            "pv_space_switch_array": {"typ": "string",
                                      "value": ""},
            "pin_space_switch_array": {"typ": "string",
                                       "value": ""},
            "guide_orient_ankle": {"typ": "bool",
                                   "value": False},
            "support_knee_jnt": {"typ": "bool",
                                 "value": False},
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
                                                "weightedTangents": [False]}},
        })
        return preset


class Leg2jnt01Guide(piece.Guide):

    def guide(self):
        data = self.data(Leg2jnt01Data.SELF)
        root = super(Leg2jnt01Guide, self).guide()
        pos = self.create_position(root, data["anchors"][1])
        pos1 = self.create_position(pos, data["anchors"][2])
        pos2 = self.create_position(pos1, data["anchors"][3])
        pv = self.create_pv_locator(root, [root, pos, pos1])
        self.create_display_crv(root, [root, pos, pos1, pos2])
        self.create_display_crv(root, [pos, pv], thickness=1)


class Leg2jnt01Rig(piece.Rig):

    def objects(self, context):
        super(Leg2jnt01Rig, self).objects(context)

        data = self.data(Leg2jnt01Data.SELF)
        assembly_data = self.data(Leg2jnt01Data.ASSEMBLY)

        m0 = dt.Matrix(data["anchors"][0])
        m1 = dt.Matrix(data["anchors"][1])
        m2 = dt.Matrix(data["anchors"][2])
        m3 = dt.Matrix(data["anchors"][3])

        positions = [dt.Vector(x.translate) for x in [m0, m1, m2, m3]]
        normal = vector.getPlaneNormal(*positions[:-1])

        upper_jnt_v_values = [0]
        lower_jnt_v_values = [0, 1]

        root = self.create_root(context, positions[0])
        fk_color = self.get_fk_ctl_color()
        ik_color = self.get_ik_ctl_color()

        # fk ctls
        fk0_m = matrix.get_matrix_look_at(positions[0], positions[1], normal, "xz", self.ddata.negate)
        name = self.naming("fk0", "", _s="ctl")
        offset = ((positions[1] - positions[0]) / 2.0).length()
        po = offset * -1 if self.ddata.negate else offset
        self.fk0_ctl, self.fk0_loc = self.create_ctl(context=context, parent=None, name=name, parent_ctl=None,
                                                     color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro"], m=fk0_m,
                                                     shape="cube", cns=False, width=offset * 2, po=(po, 0, 0))
        m = matrix.set_matrix_position(fk0_m, positions[1])
        name = self.naming("fk0", "length", _s="ctl")
        self.fk0_length_obj = matrix.transform(self.fk0_loc, name, m)

        fk1_m = matrix.get_matrix_look_at(positions[1], positions[2], normal, "xz", self.ddata.negate)
        name = self.naming("fk1", "", _s="ctl")
        offset = ((positions[2] - positions[1]) / 2.0).length()
        po = offset * -1 if self.ddata.negate else offset
        self.fk1_ctl, self.fk1_loc = self.create_ctl(context=context, parent=self.fk0_length_obj, name=name,
                                                     parent_ctl=self.fk0_ctl, color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rz"], m=fk1_m, shape="cube",
                                                     cns=False, width=offset * 2, po=(po, 0, 0))
        m = matrix.set_matrix_position(fk1_m, positions[2])
        name = self.naming("fk1", "length", _s="ctl")
        self.fk1_length_obj = matrix.transform(self.fk1_loc, name, m)

        fk2_m = matrix.get_matrix_look_at(positions[2], positions[3], normal, "xz", self.ddata.negate)
        if data["guide_orient_ankle"]:
            fk2_m = matrix.set_matrix_rotation(fk2_m, m2)
            fk2_m.scale = (1, 1, 1)
        name = self.naming("fk2", "", _s="ctl")
        offset = ((positions[3] - positions[2]) / 2.0).length()
        po = offset * -1 if self.ddata.negate and not data["guide_orient_ankle"] else offset
        self.fk2_ctl, self.fk2_loc = self.create_ctl(context=context, parent=self.fk1_length_obj, name=name,
                                                     parent_ctl=self.fk1_ctl, color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx",
                                                                    "sy", "sz"], m=fk2_m, shape="cube", cns=False,
                                                     width=offset * 2, po=(po, 0, 0))
        # ik ctls
        m = matrix.get_matrix_from_pos(positions[2])
        if self.ddata.negate:
            m = matrix.get_mirror_matrix(m)
            m = matrix.set_matrix_position(m, positions[2])
        name = self.naming("ik", "", _s="ctl")
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context, parent=None, name=name, parent_ctl=None,
                                                   color=ik_color,
                                                   keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy",
                                                                  "sz"], m=m, shape="cube", cns=True)

        name = self.naming("ikLocal", "", _s="ctl")
        self.ik_local_ctl, self.ik_local_loc = self.create_ctl(context=context, parent=self.ik_loc, name=name,
                                                               parent_ctl=self.ik_ctl, color=ik_color,
                                                               keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro",
                                                                              "sx", "sy", "sz"], m=fk2_m, shape="cube",
                                                               cns=False, width=0.8, height=0.8, depth=0.8)

        pole_vec_pos = dt.Matrix(data["offset_pole_vec_matrix"]).translate
        pole_vec_m = matrix.set_matrix_position(fk1_m, pole_vec_pos)
        name = self.naming("pv", "", _s="ctl")
        self.pole_vec_ctl, self.pole_vec_loc = self.create_ctl(context=context, parent=None, name=name,
                                                               parent_ctl=self.ik_local_ctl, color=ik_color,
                                                               keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro"],
                                                               m=pole_vec_m, shape="x", cns=True)

        # ik jnts
        name = self.naming("ik%s", _s="jnt")
        self.ik_jnts = joint.add_chain(root, name, positions[:-1], normal, last_orient=fk2_m, negate=self.ddata.negate)

        name = self.naming("RP", "ikh", _s="jnt")
        self.ik_ikh = joint.ikh(self.ik_local_loc, name, self.ik_jnts, pole_vector=self.pole_vec_loc)
        pm.orientConstraint(self.ik_ikh, self.ik_jnts[-1], maintainOffset=True)
        pm.scaleConstraint(self.ik_ikh, self.ik_jnts[-1], maintainOffset=True)

        # knee - pole vector display curve
        name = self.naming("display", "crv", _s="ctl")
        self.display_curve = matrix.transform(root, name, dt.Matrix())
        icon.generate(self.display_curve,
                      [(0, 0, 0), (0, 0, 0)],
                      1,
                      dt.Color(0.55, 0.55, 0.55, 0.55),
                      thickness=1)
        nurbs.constraint(self.display_curve, [self.ik_jnts[1], self.pole_vec_loc])
        self.display_curve.getShape().attr("overrideDisplayType").set(2)
        self.display_curve.attr("inheritsTransform").set(0)
        self.display_curve.attr("translate").set((0, 0, 0))
        self.display_curve.attr("rotate").set((0, 0, 0))

        # blend objs
        self.blend_objs = []
        parent = root
        for i, jnt in enumerate(self.ik_jnts):
            name = self.naming(f"fkik{i}", "blend", _s="jnt")
            parent = pm.createNode("transform", name=name, parent=parent)
            parent.attr("offsetParentMatrix").set(jnt.getMatrix(worldSpace=False))
            self.blend_objs.append(parent)
        name = self.naming("fk_blend0", "offset", _s="ctl")
        self.fk0_blend_offset = pm.createNode("transform", name=name, parent=self.blend_objs[0])
        pm.parent(self.blend_objs[1], self.fk0_blend_offset)
        name = self.naming("fk_blend1", "offset", _s="ctl")
        self.fk1_blend_offset = pm.createNode("transform", name=name, parent=self.blend_objs[1])
        pm.parent(self.blend_objs[2], self.fk1_blend_offset)

        orig_m = dt.Matrix()
        name = self.naming("origUpper", "crv", _s="ctl")
        self.orig_upper_crv = nurbs.create(root,
                                           name,
                                           1,
                                           positions[:2],
                                           orig_m,
                                           vis=False,
                                           display_type=1)
        name = self.naming("deformUpper", "crv", _s="ctl")
        self.deform_upper_crv = nurbs.create(root,
                                             name,
                                             1,
                                             positions[:2],
                                             orig_m,
                                             vis=False,
                                             display_type=1)
        self.deform_upper_crv.attr("inheritsTransform").set(0)
        nurbs.constraint(self.deform_upper_crv, self.blend_objs[:2])
        name = self.naming("origLower", "crv", _s="ctl")
        self.orig_lower_crv = nurbs.create(root,
                                           name,
                                           1,
                                           positions[1:3],
                                           orig_m,
                                           vis=False,
                                           display_type=1)
        name = self.naming("lowerDeform", "crv", _s="ctl")
        self.deform_lower_crv = nurbs.create(root,
                                             name,
                                             1,
                                             positions[1:3],
                                             orig_m,
                                             vis=False,
                                             display_type=1)
        self.deform_lower_crv.attr("inheritsTransform").set(0)
        nurbs.constraint(self.deform_lower_crv, self.blend_objs[1:])

        # pin ctl
        name = self.naming("pin", _s="ctl")
        pin_m = matrix.get_matrix_look_at(positions[0], positions[2], normal, "xz", self.ddata.negate)
        pin_m = matrix.set_matrix_position(pin_m, positions[1])
        self.pin_ctl, self.pin_loc = self.create_ctl(context=context, parent=None, name=name, parent_ctl=self.ik_ctl,
                                                     color=ik_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx"],
                                                     m=pin_m, shape="angle", cns=True,
                                                     ro=(90, 0, 225) if self.ddata.negate else (90, 0, 45))
        # support knee ctl
        self.knee_loc = self.pin_loc
        if data["support_knee_jnt"] and data["upper_division"] > 1 and data["lower_division"] > 1:
            upper_jnt_v_values.append(0.99)
            lower_jnt_v_values.append(0.01)
            knee_m = matrix.get_matrix_look_at(positions[0], positions[2], normal, "xz", False)
            knee_m = matrix.set_matrix_position(knee_m, positions[1])
            name = self.naming("kneeThickness", _s="ctl")
            self.thickness_knee_ctl, self.thickness_knee_loc = self.create_ctl(context=context, parent=self.pin_loc,
                                                                               name=name, parent_ctl=self.pin_ctl,
                                                                               color=ik_color, keyable_attrs=["tx"],
                                                                               m=knee_m, shape="arrow", cns=False)
            self.knee_loc = self.thickness_knee_loc

        # lookAt jnts
        name = self.naming("lookAt%s", "jnt", _s="jnt")
        self.look_at_jnts = joint.add_chain(root,
                                            name,
                                            [positions[0], positions[2]],
                                            normal,
                                            negate=self.ddata.negate)
        name = self.naming("stretch", "jnt", _s="jnt")
        self.stretch_value_jnt = joint.add(self.look_at_jnts[0],
                                           name,
                                           self.look_at_jnts[1].getMatrix(worldSpace=True),
                                           vis=False)
        self.stretch_value_attr = self.stretch_value_jnt.attr("tx")

        name = self.naming("lookAt", "ikh", _s="ctl")
        self.look_at_sc_ikh = joint.ikh(root, name, self.look_at_jnts, "ikSCsolver")
        pm.pointConstraint(self.ik_jnts[0], self.look_at_jnts[0])
        pm.pointConstraint(self.ik_local_loc, self.look_at_sc_ikh)
        pm.pointConstraint(self.ik_local_loc, self.stretch_value_jnt)

        # SC jnts
        name = self.naming("upperSC", "offset", _s="ctl")
        self.upper_sc_offset = matrix.transform(parent=root,
                                                name=name,
                                                m=self.blend_objs[0].getMatrix(worldSpace=True))

        name = self.naming("upperFixSC%s", _s="jnt")
        self.upper_fix_sc_jnts = joint.add_chain(self.upper_sc_offset,
                                                 name,
                                                 positions[:2],
                                                 normal,
                                                 negate=self.ddata.negate)
        pm.connectAttr(self.blend_objs[0].attr("t"), self.upper_fix_sc_jnts[0].attr("t"))
        name = self.naming("upperRotSC%s", _s="jnt")
        self.upper_rot_sc_jnts = joint.add_chain(self.upper_sc_offset,
                                                 name,
                                                 positions[:2],
                                                 normal,
                                                 negate=self.ddata.negate)
        pm.connectAttr(self.blend_objs[0].attr("t"), self.upper_rot_sc_jnts[0].attr("t"))
        name = self.naming("upperFixSC", "ikh", _s="ctl")
        self.upper_fix_sc_ikh = joint.ikh(root, name, self.upper_fix_sc_jnts, "ikSCsolver")
        pm.pointConstraint(self.pin_loc, self.upper_fix_sc_ikh)
        name = self.naming("upperRotSC", "ikh", _s="ctl")
        self.upper_rot_sc_ikh = joint.ikh(root, name, self.upper_rot_sc_jnts, "ikSCsolver")
        pm.pointConstraint(self.pin_loc, self.upper_rot_sc_ikh)
        pm.orientConstraint(self.blend_objs[0], self.upper_rot_sc_ikh, maintainOffset=True)

        name = self.naming("upperStart", "bind", _s="jnt")
        self.upper_start_bind = joint.add(self.upper_fix_sc_jnts[0],
                                          name,
                                          self.upper_fix_sc_jnts[0].getMatrix(worldSpace=True),
                                          vis=False)
        name = self.naming("upperEnd", "bind", _s="jnt")
        self.upper_end_bind = joint.add(self.upper_rot_sc_jnts[1],
                                        name,
                                        self.upper_rot_sc_jnts[1].getMatrix(worldSpace=True),
                                        vis=False)
        pm.pointConstraint(self.pin_loc, self.upper_end_bind)

        name = self.naming("lowerFixSC%s", _s="jnt")
        self.lower_fix_sc_jnts = joint.add_chain(root, name, positions[1:3], normal, negate=self.ddata.negate)
        pm.pointConstraint(self.knee_loc, self.lower_fix_sc_jnts[0])

        name = self.naming("lowerFixSC", "ikh", _s="ctl")
        self.lower_fix_sc_ikh = joint.ikh(root, name, self.lower_fix_sc_jnts, "ikSCsolver")
        pm.pointConstraint(self.blend_objs[-1], self.lower_fix_sc_ikh)
        pm.orientConstraint(self.upper_end_bind, self.lower_fix_sc_ikh, maintainOffset=True)

        name = self.naming("lowerRotSC%s", _s="jnt")
        self.lower_rot_sc_jnts = joint.add_chain(root, name, positions[1:3], normal, negate=self.ddata.negate)
        pm.pointConstraint(self.knee_loc, self.lower_rot_sc_jnts[0])

        name = self.naming("lowerRotSC", "ikh", _s="ctl")
        self.lower_rot_sc_ikh = joint.ikh(root, name, self.lower_rot_sc_jnts, "ikSCsolver")
        pm.pointConstraint(self.blend_objs[-1], self.lower_rot_sc_ikh)
        pm.orientConstraint(self.blend_objs[-1], self.lower_rot_sc_ikh, maintainOffset=True)

        name = self.naming("lowerStart", "bind", _s="jnt")
        self.lower_start_bind = joint.add(self.lower_fix_sc_jnts[0],
                                          name,
                                          self.lower_fix_sc_jnts[0].getMatrix(worldSpace=True),
                                          vis=False)
        name = self.naming("lowerEnd", "bind", _s="jnt")
        self.lower_end_bind = joint.add(self.lower_rot_sc_jnts[1],
                                        name,
                                        self.lower_rot_sc_jnts[1].getMatrix(worldSpace=True),
                                        vis=False)
        pm.pointConstraint(self.blend_objs[-1], self.lower_end_bind)

        # ribbon bind jnts
        upper_bind_jnts = [self.upper_start_bind, self.upper_end_bind]
        lower_bind_jnts = [self.lower_start_bind, self.lower_end_bind]

        # mid ctl
        if data["upper_division"] > 1:
            uniform_value = 1.0 / data["upper_division"]
            upper_jnt_v_values.extend([uniform_value * i for i in range(1, data["upper_division"])])

            name = self.naming("mid0", _s="ctl")
            m = self.upper_fix_sc_jnts[0].getMatrix(worldSpace=True)
            self.mid0_ctl, self.mid0_loc = self.create_ctl(context=context, parent=self.upper_sc_offset, name=name,
                                                           parent_ctl=self.pin_ctl, color=ik_color,
                                                           keyable_attrs=["tx", "ty", "tz",
                                                                          "rx", "ry", "rz",
                                                                          "sx", "sy", "sz"], m=m, shape="circle3",
                                                           cns=False)
            name = self.naming("upperMid", "bind", _s="jnt")
            self.upper_mid_bind = joint.add(self.mid0_loc,
                                            name,
                                            m,
                                            vis=False)
            upper_bind_jnts.append(self.upper_mid_bind)
            mid0_npo = self.mid0_ctl.getParent()
            pm.pointConstraint([self.upper_start_bind, self.upper_end_bind], mid0_npo)
            cons = pm.orientConstraint([self.upper_start_bind, self.upper_end_bind], mid0_npo)
            cons.attr("interpType").set(2)
        else:
            pm.parent(self.upper_start_bind, self.blend_objs[0])

        if data["lower_division"] > 1:
            uniform_value = 1.0 / data["lower_division"]
            lower_jnt_v_values.extend([uniform_value * i for i in range(1, data["lower_division"])])

            name = self.naming("mid1", _s="ctl")
            m = self.lower_fix_sc_jnts[0].getMatrix(worldSpace=True)
            self.mid1_ctl, self.mid1_loc = self.create_ctl(context=context, parent=root, name=name,
                                                           parent_ctl=self.pin_ctl, color=ik_color,
                                                           keyable_attrs=["tx", "ty", "tz",
                                                                          "rx", "ry", "rz",
                                                                          "sx", "sy", "sz"], m=m, shape="circle3",
                                                           cns=False)
            name = self.naming("lowerMid", "bind", _s="jnt")
            self.lower_mid_bind = joint.add(self.mid1_loc,
                                            name,
                                            m,
                                            vis=False)
            lower_bind_jnts.append(self.lower_mid_bind)
            mid1_npo = self.mid1_ctl.getParent()
            pm.pointConstraint([self.lower_start_bind, self.lower_end_bind], mid1_npo)
            cons = pm.orientConstraint([self.lower_start_bind, self.lower_end_bind], mid1_npo)
            cons.attr("interpType").set(2)

        # ribbon
        self.leg_output_objs = []
        m = root.getMatrix(worldSpace=True)
        for i in range(len(upper_jnt_v_values)):
            name = self.naming(str(i), "space", _s="ctl")
            self.leg_output_objs.append(matrix.transform(root, name, m))
        for i in range(len(lower_jnt_v_values) - 1):
            name = self.naming(str(i + len(upper_jnt_v_values)), "space", _s="ctl")
            self.leg_output_objs.append(matrix.transform(root, name, m))
        name = self.naming(f"{len(self.leg_output_objs)}", "space", _s="ctl")
        obj = matrix.transform(root, name, fk2_m)
        self.leg_output_objs.append(obj)
        if data["upper_division"] > 1:
            mid0_uniform_attr = attribute.add(self.mid0_ctl,
                                              longName="uniform",
                                              typ="double",
                                              defaultValue=1,
                                              minValue=0,
                                              maxValue=1,
                                              keyable=True)
            name = self.naming("upper", "{}", _s="ctl")
            uvpin1 = nurbs.ribbon(root,
                                  name,
                                  positions[:2],
                                  normal,
                                  sorted(upper_jnt_v_values),
                                  upper_bind_jnts,
                                  mid0_uniform_attr,
                                  self.leg_output_objs[:len(lower_jnt_v_values) * -1],
                                  negate=self.ddata.negate)
            if not (data["support_knee_jnt"] and data["upper_division"] > 1 and data["lower_division"] > 1):
                index = len(upper_jnt_v_values) - 1
                aim_m = self.leg_output_objs[index].attr("offsetParentMatrix").inputs(type="aimMatrix")[0]
                aim_m.attr("primaryInputAxisX").set(-1 if self.ddata.negate else 1)
                pm.connectAttr(self.leg_output_objs[index + 1].attr("dagLocalMatrix"),
                               aim_m.attr("primaryTargetMatrix"),
                               force=True)
        else:
            pm.parentConstraint(self.upper_start_bind, self.leg_output_objs[0])
        if data["support_knee_jnt"] and data["upper_division"] > 1 and data["lower_division"] > 1:
            mid_index = len(upper_jnt_v_values)
            cons = pm.orientConstraint([self.leg_output_objs[mid_index - 1], self.leg_output_objs[mid_index + 1]],
                                       self.leg_output_objs[mid_index])
            cons.attr("interpType").set(2)
        if data["lower_division"] > 1:
            mid1_uniform_attr = attribute.add(self.mid1_ctl,
                                              longName="uniform",
                                              typ="double",
                                              defaultValue=1,
                                              minValue=0,
                                              maxValue=1,
                                              keyable=True)
            name = self.naming("lower", "{}", _s="ctl")
            uvpin2 = nurbs.ribbon(root,
                                  name,
                                  positions[1:3],
                                  normal,
                                  sorted(lower_jnt_v_values)[:-1],
                                  lower_bind_jnts,
                                  mid1_uniform_attr,
                                  self.leg_output_objs[len(upper_jnt_v_values):],
                                  negate=self.ddata.negate)
            aim_m = self.leg_output_objs[-2].attr("offsetParentMatrix").inputs(type="aimMatrix")[0]
            aim_m.attr("primaryInputAxisX").set(-1 if self.ddata.negate else 1)
            pm.connectAttr(self.leg_output_objs[-1].attr("matrix"), aim_m.attr("primaryTargetMatrix"), force=True)
        else:
            pm.parentConstraint(self.lower_start_bind, self.leg_output_objs[1])

        pm.parentConstraint(self.blend_objs[-1], obj, maintainOffset=True)
        pm.scaleConstraint(self.blend_objs[-1], obj, maintainOffset=True)

        self.volume_inputs = upper_jnt_v_values + [x + 1 for x in lower_jnt_v_values]
        self.volume_inputs = sorted([x / 2.0 for x in self.volume_inputs])

        # refs
        self.refs = []
        for i, obj in enumerate(self.leg_output_objs):
            name = self.naming(f"{i}", "ref", _s="ctl")
            if i == 0 or i == len(self.leg_output_objs) - 1 or i == len(upper_jnt_v_values):
                anchor = True
            else:
                anchor = False
            self.refs.append(self.create_ref(context=context,
                                             name=name,
                                             anchor=anchor,
                                             m=obj))
        # jnts
        uni_scale = False
        if assembly_data["force_uni_scale"]:
            uni_scale = True

        jnt = None
        twist_index = 0
        for i, ref in enumerate(self.refs):
            if i == 0:
                name = self.naming("thigh", _s="jnt")
            elif i == len(upper_jnt_v_values):
                name = self.naming("knee", _s="jnt")
                twist_index = 0
            elif i == len(self.refs) - 1:
                name = self.naming("ankle", _s="jnt")
            elif i < len(upper_jnt_v_values):
                name = self.naming(f"upperTwist{twist_index}", _s="jnt")
            else:
                name = self.naming(f"lowerTwist{twist_index}", _s="jnt")
            m = ref.getMatrix(worldSpace=True)
            jnt = self.create_jnt(context=context,
                                  parent=jnt,
                                  name=name,
                                  description=f"{i}",
                                  ref=ref,
                                  m=m,
                                  leaf=False,
                                  uni_scale=uni_scale)
            twist_index += 1

    def attributes(self, context):
        super(Leg2jnt01Rig, self).attributes(context)
        host = self.create_host(context)

        data = self.data(Leg2jnt01Data.SELF)
        self.fk0_length_attr = attribute.add(self.fk0_ctl,
                                             "length",
                                             "double",
                                             value=1,
                                             minValue=0,
                                             defaultValue=1,
                                             keyable=True)
        self.fk1_length_attr = attribute.add(self.fk1_ctl,
                                             "length",
                                             "double",
                                             value=1,
                                             minValue=0,
                                             defaultValue=1,
                                             keyable=True)
        self.fk_ik_attr = attribute.add(host,
                                        f"fk_ik",
                                        "double",
                                        keyable=True,
                                        minValue=0,
                                        maxValue=1,
                                        defaultValue=data["fk_ik"])
        self.roll_attr = attribute.add(host,
                                       f"roll",
                                       "double",
                                       keyable=True,
                                       defaultValue=0)
        self.armpit_roll_attr = attribute.add(host,
                                              f"armpit_roll",
                                              "double",
                                              keyable=True,
                                              defaultValue=0)
        self.scale_attr = attribute.add(host,
                                        f"scale_",
                                        "double",
                                        keyable=True,
                                        minValue=0.01,
                                        maxValue=999,
                                        defaultValue=1)
        self.slide_attr = attribute.add(host,
                                        f"slide",
                                        "double",
                                        keyable=True,
                                        minValue=0,
                                        maxValue=1,
                                        defaultValue=0.5)
        self.max_stretch_attr = attribute.add(host,
                                              f"max_stretch",
                                              "double",
                                              keyable=True,
                                              minValue=1,
                                              maxValue=999,
                                              defaultValue=data["max_stretch"])
        self.volume_attr = attribute.add(host,
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
        stretch_values = fcurve.get_fcurve_values(stretch_volume_fcurve, division=0, inputs=self.volume_inputs)
        for i, value in enumerate(stretch_values):
            self.stretch_attrs.append(attribute.add(self.root,
                                                    f"stretch_volume_value{i}",
                                                    "double",
                                                    keyable=False,
                                                    minValue=-1,
                                                    maxValue=0,
                                                    defaultValue=value))
        squash_values = fcurve.get_fcurve_values(squash_volume_fcurve, division=0, inputs=self.volume_inputs)
        for i, value in enumerate(squash_values):
            self.squash_attrs.append(attribute.add(self.root,
                                                   f"squash_volume_value{i}",
                                                   "double",
                                                   keyable=False,
                                                   minValue=0,
                                                   maxValue=1,
                                                   defaultValue=value))
        if data["support_knee_jnt"] and data["upper_division"] > 1 and data["lower_division"] > 1:
            self.auto_knee_thickness_attr = attribute.add(host,
                                                          f"auto_knee_thickness",
                                                          "double",
                                                          keyable=True,
                                                          minValue=0,
                                                          maxValue=2,
                                                          defaultValue=1)
        if data["upper_division"] > 1:
            self.upper_uniform_attr = attribute.add(self.mid0_ctl,
                                                    longName="uniform",
                                                    typ="double",
                                                    defaultValue=1,
                                                    minValue=0,
                                                    maxValue=1,
                                                    keyable=True)
        if data["lower_division"] > 1:
            self.lower_uniform_attr = attribute.add(self.mid1_ctl,
                                                    longName="uniform",
                                                    typ="double",
                                                    defaultValue=1,
                                                    minValue=0,
                                                    maxValue=1,
                                                    keyable=True)

    def operators(self, context):
        super(Leg2jnt01Rig, self).operators(context)
        data = self.data(Leg2jnt01Data.SELF)
        host = self.host()

        # fk ik blend
        operators.set_fk_ik_blend_matrix(self.blend_objs,
                                         [self.fk0_ctl, self.fk1_ctl, self.fk2_ctl],
                                         self.ik_jnts,
                                         self.fk_ik_attr)
        rev = pm.createNode("reverse")
        pm.connectAttr(self.fk_ik_attr, rev.attr("inputX"))

        ik_npo = self.ik_ctl.getParent()
        if pm.controller(ik_npo, query=True):
            ik_npo = ik_npo.getParent()
        pv_npo = self.pole_vec_ctl.getParent()
        if pm.controller(pv_npo, query=True):
            pv_npo = pv_npo.getParent()
        fk_npo = self.fk0_ctl.getParent()
        if pm.controller(fk_npo, query=True):
            fk_npo = fk_npo.getParent()

        pm.connectAttr(self.fk_ik_attr, ik_npo.attr("v"))
        pm.connectAttr(self.fk_ik_attr, pv_npo.attr("v"))
        pm.connectAttr(rev.attr("outputX"), fk_npo.attr("v"))
        pm.connectAttr(self.fk_ik_attr, self.display_curve.attr("v"))

        # fk ctl length
        fk0_length = self.fk0_length_obj.attr("tx").get()
        fk1_length = self.fk1_length_obj.attr("tx").get()
        md = pm.createNode("multiplyDivide")
        md.attr("input1X").set(fk0_length)
        md.attr("input1Y").set(fk1_length)
        pm.connectAttr(self.fk0_length_attr, md.attr("input2X"))
        pm.connectAttr(self.fk1_length_attr, md.attr("input2Y"))
        self.fk0_length_attr = md.attr("outputX")
        self.fk1_length_attr = md.attr("outputY")
        pm.connectAttr(self.fk0_length_attr, self.fk0_length_obj.attr("tx"))
        pm.connectAttr(self.fk1_length_attr, self.fk1_length_obj.attr("tx"))

        pma = pm.createNode("plusMinusAverage")
        pm.connectAttr(self.fk0_length_attr, pma.attr("input1D")[0])
        pma.attr("input1D")[1].set(self.fk0_length_attr.get() * -1)
        self.fk0_length_attr = pma.attr("output1D")
        pma = pm.createNode("plusMinusAverage")
        pm.connectAttr(self.fk1_length_attr, pma.attr("input1D")[0])
        pma.attr("input1D")[1].set(self.fk1_length_attr.get() * -1)
        self.fk1_length_attr = pma.attr("output1D")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(self.fk0_length_attr, md.attr("input1X"))
        pm.connectAttr(self.fk1_length_attr, md.attr("input1Y"))
        pm.connectAttr(rev.attr("outputX"), md.attr("input2X"))
        pm.connectAttr(rev.attr("outputX"), md.attr("input2Y"))
        pm.connectAttr(md.attr("outputX"), self.fk0_blend_offset.attr("tx"))
        pm.connectAttr(md.attr("outputY"), self.fk1_blend_offset.attr("tx"))

        # pin ctl
        pin_npo = self.pin_ctl.getParent()
        if pm.controller(pin_npo, query=True):
            pin_npo = pin_npo.getParent()
        pm.pointConstraint(self.blend_objs[1], pin_npo)
        cons = pm.orientConstraint([self.blend_objs[0], self.blend_objs[1]], pin_npo, maintainOffset=True)
        cons.attr("interpType").set(2)

        # roll
        pm.connectAttr(self.roll_attr, self.ik_ikh.attr("twist"))

        # armpit roll
        pm.connectAttr(self.armpit_roll_attr, self.upper_start_bind.attr("rx"))

        # scale, slide, stretch
        operators.ik_2jnt(self.ik_jnts[1],
                          self.ik_jnts[2],
                          self.scale_attr,
                          self.slide_attr,
                          self.stretch_value_attr,
                          self.max_stretch_attr,
                          self.ddata.negate)

        # volume
        pma = pm.createNode("plusMinusAverage")
        orig_upper_length = nurbs.length(self.orig_upper_crv)
        orig_lower_length = nurbs.length(self.orig_lower_crv)
        pm.connectAttr(orig_upper_length, pma.attr("input1D")[0])
        pm.connectAttr(orig_lower_length, pma.attr("input1D")[1])
        orig_distance_attr = pma.attr("output1D")

        pma = pm.createNode("plusMinusAverage")
        pm.connectAttr(nurbs.length(self.deform_upper_crv), pma.attr("input1D")[0])
        pm.connectAttr(nurbs.length(self.deform_lower_crv), pma.attr("input1D")[1])

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(orig_upper_length, md.attr("input1X"))
        pm.connectAttr(orig_lower_length, md.attr("input1Y"))
        md.attr("input2X").set(-1)
        md.attr("input2Y").set(-1)

        pma1 = pm.createNode("plusMinusAverage")
        pm.connectAttr(md.attr("outputX"), pma1.attr("input1D")[0])
        pm.connectAttr(md.attr("outputY"), pma1.attr("input1D")[1])
        pm.connectAttr(pma1.attr("output1D"), pma.attr("input1D")[2])

        delta_distance_attr = pma.attr("output1D")
        operators.volume(orig_distance_attr,
                         delta_distance_attr,
                         self.squash_attrs,
                         self.stretch_attrs,
                         self.volume_attr,
                         self.leg_output_objs[:-1])

        # auto knee thickness
        if data["support_knee_jnt"] and data["upper_division"] > 1 and data["lower_division"] > 1:
            distance1 = self.ik_jnts[1].attr("tx").get()
            distance2 = self.ik_jnts[2].attr("tx").get()
            if distance1 < 0:
                distance1 *= -1
            if distance2 < 0:
                distance2 *= -1
            length = distance1 + distance2
            md = pm.createNode("multiplyDivide")
            pm.connectAttr(self.auto_knee_thickness_attr, md.attr("input1X"))
            pm.setDrivenKeyframe(md.attr("input2X"),
                                 currentDriver=self.blend_objs[1].attr("rz"),
                                 driverValue=0,
                                 value=0,
                                 inTangentType="linear",
                                 outTangentType="linear")
            pm.setDrivenKeyframe(md.attr("input2X"),
                                 currentDriver=self.blend_objs[1].attr("rz"),
                                 driverValue=-180,
                                 value=length / float(distance2) / 5,
                                 inTangentType="linear",
                                 outTangentType="linear")

            npo = self.thickness_knee_ctl.getParent()
            pm.connectAttr(md.attr("outputX"), npo.attr("tx"))

        # space switch
        if data["ik_space_switch_array"]:
            source_ctls = self.find_ctls(data["ik_space_switch_array"])
            operators.space_switch(source_ctls, self.ik_ctl, host, attr_name="ik_space_switch")
            script_node = callback.space_switch(source_ctls, self.ik_ctl, host, switch_attr_name="ik_space_switch")
            if script_node:
                context["callbacks"].append(script_node)
        if data["pv_space_switch_array"]:
            source_ctls = self.find_ctls(data["pv_space_switch_array"])
            operators.space_switch(source_ctls,
                                   self.pole_vec_ctl,
                                   host,
                                   attr_name="pv_space_switch")
            script_node = callback.space_switch(source_ctls, self.pole_vec_ctl, host,
                                                switch_attr_name="pv_space_switch")
            if script_node:
                context["callbacks"].append(script_node)
        if data["pin_space_switch_array"]:
            name = self.naming("pin", "spaceSwitch", _s="ctl")
            controller.npo(self.pin_ctl.getParent(), name=name)
            source_ctls = self.find_ctls(data["pin_space_switch_array"])
            operators.space_switch(source_ctls, self.pin_ctl, host, attr_name="pin_space_switch")
            script_node = callback.space_switch(source_ctls, self.pin_ctl, host, switch_attr_name="pin_space_switch")
            if script_node:
                context["callbacks"].append(script_node)

    def connections(self, context):
        super(Leg2jnt01Rig, self).connections(context)

        if "leg_2jnt_01" not in context:
            context["leg_2jnt_01"] = {}
        context["leg_2jnt_01"][str(self.ddata.identifier)] = [self.ik_local_loc,
                                                              self.ik_ikh,
                                                              self.refs[-1],
                                                              self.fk_ik_attr]


class Leg2jnt01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Leg2jnt01Data(node=node, data=data)
        self._guide = Leg2jnt01Guide(self._ddata)
        self._rig = Leg2jnt01Rig(self._ddata)
