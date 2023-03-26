# domino
from domino.core import matrix, attribute, vector, operators, joint, fcurve, nurbs, callback
from domino.edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Leg3jnt01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "leg"
    side = "C"
    index = 0
    description = "quadruped 다리 입니다."


class Leg3jnt01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))
    _m2 = matrix.get_matrix_from_pos((0, -2, 0.1))
    _m3 = matrix.get_matrix_from_pos((0, -4, 0))
    _m4 = matrix.get_matrix_from_pos((0, -6, 0.1))
    _m5 = matrix.get_matrix_from_pos((0, -6, 1))

    def __init__(self, node=None, data=None):
        self._identifier = Leg3jnt01Identifier(self)
        super(Leg3jnt01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Leg3jnt01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1, self._m2, self._m3, self._m4, self._m5],
                        "multi": True},
            "offset_pole_vec": {"typ": "double",
                                "value": 1,
                                "channelBox": True},
            "offset_pole_vec_matrix": {"typ": "matrix",
                                       "value": dt.Matrix()},
            "fk_ik": {"typ": "double",
                      "value": 1},
            "spring_solver": {"typ": "bool",
                              "value": True},
            "division1": {"typ": "long",
                          "value": 3},
            "division2": {"typ": "long",
                          "value": 3},
            "division3": {"typ": "long",
                          "value": 3},
            "max_stretch": {"typ": "double",
                            "value": 1.2},
            "ik_space_switch_array": {"typ": "string",
                                      "value": ""},
            "pv_space_switch_array": {"typ": "string",
                                      "value": ""},
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


class Leg3jnt01Guide(piece.Guide):

    def guide(self):
        data = self.data(Leg3jnt01Data.SELF)
        root = super(Leg3jnt01Guide, self).guide()
        pos = self.create_position(root, data["anchors"][1])
        pos1 = self.create_position(pos, data["anchors"][2])
        pos2 = self.create_position(pos1, data["anchors"][3])
        pos3 = self.create_position(pos2, data["anchors"][4])
        self.create_display_crv(root, [root, pos, pos1, pos2, pos3])
        attribute.lock(pos, ["tx", "ry", "rz"])
        attribute.lock(pos1, ["tx", "ry", "rz"])
        attribute.lock(pos2, ["tx"])
        pv = self.create_pv_locator(root, [root, pos, pos1])
        self.create_display_crv(root, [pos, pv], thickness=1)


class Leg3jnt01Rig(piece.Rig):

    def objects(self, context):
        super(Leg3jnt01Rig, self).objects(context)

        data = self.data(Leg3jnt01Data.SELF)
        assembly_data = self.data(Leg3jnt01Data.ASSEMBLY)

        m0, m1, m2, m3, m4 = [dt.Matrix(x) for x in data["anchors"]]

        positions = [dt.Vector(x.translate) for x in [m0, m1, m2, m3, m4]]
        normal = vector.getPlaneNormal(*positions[:3])

        root = self.create_root(context, positions[0])
        fk_color = self.get_fk_ctl_color()
        ik_color = self.get_ik_ctl_color()

        total_length = 0
        div_length = 0
        for i, p in enumerate(positions[:-1]):
            if i == len(positions[:-1]) - 1:
                break
            l = vector.get_distance(p, positions[i + 1])
            total_length += l
            if i == 0 or i == 2:
                div_length += l

        # fk ctls
        fk0_m = matrix.get_matrix_look_at(positions[0], positions[1], normal, "xz", self.ddata.negate)
        name = self.naming("fk0", "", _s="ctl")
        offset = ((positions[1] - positions[0]) / 2.0).length()
        po = offset * -1 if self.ddata.negate else offset
        self.fk0_ctl, self.fk0_loc = self.create_ctl(context=context,
                                                     parent=None,
                                                     name=name,
                                                     parent_ctl=None,
                                                     color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro"],
                                                     m=fk0_m,
                                                     shape="cube",
                                                     cns=False,
                                                     width=offset * 2,
                                                     height=div_length / total_length,
                                                     depth=div_length / total_length,
                                                     po=(po, 0, 0))

        fk1_m = matrix.get_matrix_look_at(positions[1], positions[2], normal, "xz", self.ddata.negate)
        name = self.naming("fk1", "", _s="ctl")
        offset = ((positions[2] - positions[1]) / 2.0).length()
        po = offset * -1 if self.ddata.negate else offset
        self.fk1_ctl, self.fk1_loc = self.create_ctl(context=context,
                                                     parent=self.fk0_loc,
                                                     name=name,
                                                     parent_ctl=self.fk0_ctl,
                                                     color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro"],
                                                     m=fk1_m,
                                                     shape="cube",
                                                     cns=False,
                                                     width=offset * 2,
                                                     height=div_length / total_length,
                                                     depth=div_length / total_length,
                                                     po=(po, 0, 0))

        fk2_m = matrix.get_matrix_look_at(positions[2], positions[3], normal, "xz", self.ddata.negate)
        name = self.naming("fk2", "", _s="ctl")
        offset = ((positions[3] - positions[2]) / 2.0).length()
        po = offset * -1 if self.ddata.negate else offset
        self.fk2_ctl, self.fk2_loc = self.create_ctl(context=context,
                                                     parent=self.fk1_loc,
                                                     name=name,
                                                     parent_ctl=self.fk1_ctl,
                                                     color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro"],
                                                     m=fk2_m,
                                                     shape="cube",
                                                     cns=False,
                                                     width=offset * 2,
                                                     height=div_length / total_length,
                                                     depth=div_length / total_length,
                                                     po=(po, 0, 0))

        fk3_m = matrix.get_matrix_look_at(positions[3], positions[4], normal, "xz", self.ddata.negate)
        name = self.naming("fk3", "", _s="ctl")
        offset = ((positions[4] - positions[3]) / 2.0).length()
        po = offset * -1 if self.ddata.negate else offset
        self.fk3_ctl, self.fk3_loc = self.create_ctl(context=context,
                                                     parent=self.fk2_loc,
                                                     name=name,
                                                     parent_ctl=self.fk2_ctl,
                                                     color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro"],
                                                     m=fk3_m,
                                                     shape="cube",
                                                     cns=False,
                                                     width=offset * 2,
                                                     height=div_length / total_length,
                                                     depth=div_length / total_length,
                                                     po=(po, 0, 0))

        # ik ctl
        m = matrix.get_matrix_from_pos(positions[3])
        if self.ddata.negate:
            m = matrix.get_mirror_matrix(m)
            m = matrix.set_matrix_position(m, positions[3])
        name = self.naming("ik", "", _s="ctl")
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context,
                                                   parent=None,
                                                   name=name,
                                                   parent_ctl=None,
                                                   color=ik_color,
                                                   keyable_attrs=["tx", "ty", "tz",
                                                                  "rx", "ry", "rz", "ro"],
                                                   m=m,
                                                   shape="cube",
                                                   width=div_length / total_length,
                                                   height=div_length / total_length,
                                                   depth=div_length / total_length,
                                                   cns=True)

        third_rot_m = matrix.get_matrix_look_at(positions[3], positions[2], normal, "xz", self.ddata.negate)
        name = self.naming("thirdRot", "", _s="ctl")
        self.third_rot_ctl, self.third_rot_loc = self.create_ctl(context=context,
                                                                 parent=self.ik_loc,
                                                                 name=name,
                                                                 parent_ctl=self.ik_ctl,
                                                                 color=ik_color,
                                                                 keyable_attrs=["rx", "ry", "rz"],
                                                                 m=third_rot_m,
                                                                 shape="arrow4",
                                                                 cns=False,
                                                                 width=div_length / total_length,
                                                                 height=div_length / total_length,
                                                                 depth=div_length / total_length,
                                                                 ro=(0, 0, 90))
        name = self.naming("chain2Ikh", "source", _s="ctl")
        self.chain2_ikh_source = matrix.transform(self.third_rot_loc, name, third_rot_m)
        offset = vector.get_distance(positions[-2], positions[-3]) * (-1 if self.ddata.negate else 1)
        self.chain2_ikh_source.attr("tx").set(offset)

        # pin ctl
        name = self.naming("pin1", _s="ctl")
        pin1_m = matrix.get_matrix_look_at(positions[0], positions[2], normal, "xz", self.ddata.negate)
        pin1_m = matrix.set_matrix_position(pin1_m, positions[1])
        self.pin1_ctl, self.pin1_loc = self.create_ctl(context=context,
                                                       parent=None,
                                                       name=name,
                                                       parent_ctl=self.ik_ctl,
                                                       color=ik_color,
                                                       keyable_attrs=["tx", "ty", "tz"],
                                                       m=pin1_m,
                                                       shape="angle",
                                                       cns=True,
                                                       width=div_length / total_length,
                                                       height=div_length / total_length,
                                                       ro=(90, 0, 225) if self.ddata.negate else (90, 0, 45))

        name = self.naming("pin2", _s="ctl")
        pin2_m = matrix.get_matrix_look_at(positions[1], positions[3], normal, "xz", self.ddata.negate)
        pin2_m = matrix.set_matrix_position(pin2_m, positions[2])
        self.pin2_ctl, self.pin2_loc = self.create_ctl(context=context,
                                                       parent=None,
                                                       name=name,
                                                       parent_ctl=self.pin1_ctl,
                                                       color=ik_color,
                                                       keyable_attrs=["tx", "ty", "tz"],
                                                       m=pin2_m,
                                                       shape="angle",
                                                       cns=True,
                                                       width=div_length / total_length,
                                                       height=div_length / total_length,
                                                       ro=(90, 0, 225) if self.ddata.negate else (90, 0, 45))

        # pole vec ctl
        pole_vec_pos = dt.Matrix(data["offset_pole_vec_matrix"]).translate
        pole_vec_m = matrix.set_matrix_position(fk1_m, pole_vec_pos)
        name = self.naming("pv", "", _s="ctl")
        self.pole_vec_ctl, self.pole_vec_loc = self.create_ctl(context=context,
                                                               parent=None,
                                                               name=name,
                                                               parent_ctl=self.ik_ctl,
                                                               color=ik_color,
                                                               keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro"],
                                                               m=pole_vec_m,
                                                               shape="x",
                                                               cns=True)

        # 3 joint chain (spring solver or rp solver)
        is_spring = data["spring_solver"]
        if is_spring:
            pm.mel.eval("ikSpringSolver;")
        n = "chain3Spring%s" if is_spring else "chain3RP%s"
        name = self.naming(n, _s="jnt")
        self.chain3_ik_jnts = joint.add_chain(root,
                                              name,
                                              positions[:-1],
                                              normal,
                                              last_orient=fk3_m,
                                              negate=self.ddata.negate,
                                              vis=False)
        name = self.naming("thirdRot", "auto", _s="ctl")
        self.third_rot_auto_obj = matrix.transform(self.chain3_ik_jnts[-1], name, third_rot_m)
        name = self.naming("thirdRot", "fix", _s="ctl")
        self.third_rot_fix_obj = matrix.transform(self.ik_loc, name, third_rot_m)

        name = self.naming("chain3", "aim", _s="ctl")
        self.chain3_aim_obj = matrix.transform(root, name, matrix.get_matrix_from_pos(positions[0]))
        pm.aimConstraint(self.third_rot_loc, self.chain3_aim_obj, aimVector=(1, 0, 0))

        name = self.naming("stretchValue", "grp", _s="ctl")
        self.stretch_value_grp = matrix.transform(root, name, matrix.get_matrix_from_pos(positions[0]))
        pm.pointConstraint(self.chain3_ik_jnts[0], self.stretch_value_grp)
        pm.aimConstraint(self.ik_loc, self.stretch_value_grp, aimVector=(1, 0, 0))

        name = self.naming("stretchValue", "pos", _s="ctl")
        self.stretch_value_obj = matrix.transform(self.stretch_value_grp, name,
                                                  matrix.get_matrix_from_pos(positions[0]))
        pm.pointConstraint(self.ik_loc, self.stretch_value_obj)
        self.stretch_value_attr = self.stretch_value_obj.attr("tx")

        name = self.naming("chain3", "pos", _s="ctl")
        self.chain3_pos_obj = matrix.transform(root, name, matrix.get_matrix_from_pos(positions[-2]))
        pm.parentConstraint(self.ik_loc, self.chain3_pos_obj)

        n = "chain3Spring" if is_spring else "chain3RP"
        s = "ikSpringSolver" if is_spring else "ikRPsolver"
        name = self.naming(n, "ikh", _s="ctl")
        self.chain3_ik_ikh = joint.ikh(self.chain3_pos_obj,
                                       name,
                                       self.chain3_ik_jnts,
                                       solver=s,
                                       pole_vector=self.pole_vec_loc)
        if round(positions[1], 6) != round(self.chain3_ik_jnts[1].getTranslation(worldSpace=True), 6):
            self.chain3_ik_ikh.attr("twist").set(180)

        # ik jnts
        name = self.naming("ik%s", _s="jnt")
        self.ik_jnts = joint.add_chain(root,
                                       name,
                                       positions[:-1],
                                       normal,
                                       last_orient=fk3_m,
                                       negate=self.ddata.negate,
                                       vis=False)
        pm.orientConstraint(self.chain3_ik_ikh, self.ik_jnts[-1], maintainOffset=True)
        name = self.naming("chain2", "aim", _s="ctl")
        self.chain2_aim_obj = matrix.transform(root, name, matrix.get_matrix_from_pos(positions[0]))
        pm.aimConstraint(self.ik_jnts[-2], self.chain2_aim_obj, aimVector=(1, 0, 0))

        name = self.naming("chain2", "pos", _s="ctl")
        self.chain2_pos_obj = matrix.transform(root, name, matrix.get_matrix_from_pos(positions[-3]))
        pm.pointConstraint(self.chain2_ikh_source, self.chain2_pos_obj)

        name = self.naming("chain2RP", "ikh", _s="ctl")
        self.chain2_ik_ikh = joint.ikh(self.chain2_pos_obj, name, self.ik_jnts[:-1], pole_vector=self.pole_vec_loc)

        pm.aimConstraint(self.third_rot_auto_obj,
                         self.ik_jnts[-2],
                         worldUpType="object",
                         worldUpObject=self.third_rot_auto_obj,
                         maintainOffset=True,
                         aimVector=(-1 if self.ddata.negate else 1, 0, 0))

        name = self.naming("display", "crv", _s="ctl")
        self.display_curve = nurbs.create(root,
                                          name,
                                          1,
                                          ((0, 0, 0), (0, 0, 0)),
                                          vis=True,
                                          inherits=False,
                                          display_type=2)
        nurbs.constraint(self.display_curve, [self.chain3_ik_jnts[1], self.pole_vec_loc])

        # blend objs
        self.blend_objs = []
        parent = root
        for i, jnt in enumerate(self.ik_jnts):
            name = self.naming(f"fkik{i}", "blend", _s="jnt")
            parent = pm.createNode("transform", name=name, parent=parent)
            parent.attr("offsetParentMatrix").set(jnt.getMatrix(worldSpace=False))
            self.blend_objs.append(parent)

        # curve for volume
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

        name = self.naming("origMid", "crv", _s="ctl")
        self.orig_mid_crv = nurbs.create(root,
                                         name,
                                         1,
                                         positions[1:3],
                                         orig_m,
                                         vis=False,
                                         display_type=1)
        name = self.naming("deformMid", "crv", _s="ctl")
        self.deform_mid_crv = nurbs.create(root,
                                           name,
                                           1,
                                           positions[1:3],
                                           orig_m,
                                           vis=False,
                                           display_type=1)
        self.deform_mid_crv.attr("inheritsTransform").set(0)
        nurbs.constraint(self.deform_mid_crv, self.blend_objs[1:3])

        name = self.naming("origLower", "crv", _s="ctl")
        self.orig_lower_crv = nurbs.create(root,
                                           name,
                                           1,
                                           positions[2:4],
                                           orig_m,
                                           vis=False,
                                           display_type=1)
        name = self.naming("deformLower", "crv", _s="ctl")
        self.deform_lower_crv = nurbs.create(root,
                                             name,
                                             1,
                                             positions[2:4],
                                             orig_m,
                                             vis=False,
                                             display_type=1)
        self.deform_lower_crv.attr("inheritsTransform").set(0)
        nurbs.constraint(self.deform_lower_crv, self.blend_objs[2:4])

        # SC jnts
        # upper
        name = self.naming("upperSC", "offset", _s="ctl")
        self.upper_sc_offset = matrix.transform(parent=root, name=name, m=fk0_m)

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
        pm.pointConstraint(self.pin1_loc, self.upper_fix_sc_ikh)
        name = self.naming("upperRotSC", "ikh", _s="ctl")
        self.upper_rot_sc_ikh = joint.ikh(root, name, self.upper_rot_sc_jnts, "ikSCsolver")
        pm.pointConstraint(self.pin1_loc, self.upper_rot_sc_ikh)
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
        pm.pointConstraint(self.pin1_loc, self.upper_end_bind)

        # mid
        name = self.naming("midFixSC%s", _s="jnt")
        self.mid_fix_sc_jnts = joint.add_chain(root, name, positions[1:3], normal, negate=self.ddata.negate)
        pm.pointConstraint(self.pin1_loc, self.mid_fix_sc_jnts[0])

        name = self.naming("midFixSC", "ikh", _s="ctl")
        self.mid_fix_sc_ikh = joint.ikh(root, name, self.mid_fix_sc_jnts, "ikSCsolver")
        pm.pointConstraint(self.blend_objs[-2], self.mid_fix_sc_ikh)
        pm.orientConstraint(self.upper_end_bind, self.mid_fix_sc_ikh, maintainOffset=True)

        name = self.naming("midRotSC%s", _s="jnt")
        self.mid_rot_sc_jnts = joint.add_chain(root, name, positions[1:3], normal, negate=self.ddata.negate)
        pm.pointConstraint(self.pin1_loc, self.mid_rot_sc_jnts[0])

        name = self.naming("midRotSC", "ikh", _s="ctl")
        self.mid_rot_sc_ikh = joint.ikh(root, name, self.mid_rot_sc_jnts, "ikSCsolver")
        pm.pointConstraint(self.blend_objs[-2], self.mid_rot_sc_ikh)
        pm.orientConstraint(self.blend_objs[-2], self.mid_rot_sc_ikh, maintainOffset=True)

        name = self.naming("midStart", "bind", _s="jnt")
        self.mid_start_bind = joint.add(self.mid_fix_sc_jnts[0],
                                        name,
                                        self.mid_fix_sc_jnts[0].getMatrix(worldSpace=True),
                                        vis=False)
        name = self.naming("midEnd", "bind", _s="jnt")
        self.mid_end_bind = joint.add(self.mid_rot_sc_jnts[1],
                                      name,
                                      self.mid_rot_sc_jnts[1].getMatrix(worldSpace=True),
                                      vis=False)
        pm.pointConstraint(self.pin2_loc, self.mid_end_bind)

        # lower
        name = self.naming("lowerFixSC%s", _s="jnt")
        self.lower_fix_sc_jnts = joint.add_chain(root, name, positions[1:3], normal, negate=self.ddata.negate)
        pm.pointConstraint(self.pin2_loc, self.lower_fix_sc_jnts[0])

        name = self.naming("lowerFixSC", "ikh", _s="ctl")
        self.lower_fix_sc_ikh = joint.ikh(root, name, self.lower_fix_sc_jnts, "ikSCsolver")
        pm.pointConstraint(self.blend_objs[-1], self.lower_fix_sc_ikh)
        pm.orientConstraint(self.upper_end_bind, self.lower_fix_sc_ikh, maintainOffset=True)

        name = self.naming("lowerRotSC%s", _s="jnt")
        self.lower_rot_sc_jnts = joint.add_chain(root, name, positions[1:3], normal, negate=self.ddata.negate)
        pm.pointConstraint(self.pin2_loc, self.lower_rot_sc_jnts[0])

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
        mid_bind_jnts = [self.mid_start_bind, self.mid_end_bind]
        lower_bind_jnts = [self.lower_start_bind, self.lower_end_bind]

        division1_v_values = [0]
        division2_v_values = [0]
        division3_v_values = [0, 1]
        # flexible ctl
        if data["division1"] > 1:
            uniform_value = 1.0 / data["division1"]
            division1_v_values.extend([uniform_value * i for i in range(1, data["division1"])])

            name = self.naming("flexible0", _s="ctl")
            m = self.upper_fix_sc_jnts[0].getMatrix(worldSpace=True)
            self.flexible0_ctl, self.flexible0_loc = self.create_ctl(context=context,
                                                                     parent=self.upper_sc_offset,
                                                                     name=name,
                                                                     parent_ctl=self.pin1_ctl,
                                                                     color=ik_color,
                                                                     keyable_attrs=["tx", "ty", "tz",
                                                                                    "rx", "ry", "rz",
                                                                                    "sx", "sy", "sz"],
                                                                     m=m,
                                                                     shape="circle3",
                                                                     cns=False,
                                                                     width=div_length / total_length,
                                                                     height=div_length / total_length,
                                                                     depth=div_length / total_length)
            name = self.naming("upperMid", "bind", _s="jnt")
            self.upper_flexible_bind = joint.add(self.flexible0_loc, name, m, vis=False)
            upper_bind_jnts.append(self.upper_flexible_bind)
            flexible0_npo = self.flexible0_ctl.getParent()
            pm.pointConstraint([self.upper_start_bind, self.upper_end_bind], flexible0_npo)
            cons = pm.orientConstraint([self.upper_start_bind, self.upper_end_bind], flexible0_npo)
            cons.attr("interpType").set(2)
        else:
            pm.parent(self.upper_start_bind, self.blend_objs[0])

        if data["division2"] > 1:
            uniform_value = 1.0 / data["division2"]
            division2_v_values.extend([uniform_value * i for i in range(1, data["division2"])])

            name = self.naming("flexible1", _s="ctl")
            m = self.lower_fix_sc_jnts[0].getMatrix(worldSpace=True)
            self.flexible1_ctl, self.flexible1_loc = self.create_ctl(context=context,
                                                                     parent=root,
                                                                     name=name,
                                                                     parent_ctl=self.pin1_ctl,
                                                                     color=ik_color,
                                                                     keyable_attrs=["tx", "ty", "tz",
                                                                                    "rx", "ry", "rz",
                                                                                    "sx", "sy", "sz"],
                                                                     m=m,
                                                                     shape="circle3",
                                                                     cns=False,
                                                                     width=div_length / total_length,
                                                                     height=div_length / total_length,
                                                                     depth=div_length / total_length)
            name = self.naming("midMid", "bind", _s="jnt")
            self.mid_flexible_bind = joint.add(self.flexible1_loc, name, m, vis=False)
            mid_bind_jnts.append(self.mid_flexible_bind)
            flexible1_npo = self.flexible1_ctl.getParent()
            pm.pointConstraint([self.mid_start_bind, self.mid_end_bind], flexible1_npo)
            cons = pm.orientConstraint([self.mid_start_bind, self.mid_end_bind], flexible1_npo)
            cons.attr("interpType").set(2)
        else:
            pm.parent(self.mid_start_bind, self.blend_objs[1])

        if data["division3"] > 1:
            uniform_value = 1.0 / data["division3"]
            division3_v_values.extend([uniform_value * i for i in range(1, data["division3"])])

            name = self.naming("flexible2", _s="ctl")
            m = self.lower_fix_sc_jnts[0].getMatrix(worldSpace=True)
            self.flexible2_ctl, self.flexible2_loc = self.create_ctl(context=context,
                                                                     parent=root,
                                                                     name=name,
                                                                     parent_ctl=self.pin2_ctl,
                                                                     color=ik_color,
                                                                     keyable_attrs=["tx", "ty", "tz",
                                                                                    "rx", "ry", "rz",
                                                                                    "sx", "sy", "sz"],
                                                                     m=m,
                                                                     shape="circle3",
                                                                     cns=False,
                                                                     width=div_length / total_length,
                                                                     height=div_length / total_length,
                                                                     depth=div_length / total_length)
            name = self.naming("lowerMid", "bind", _s="jnt")
            self.lower_flexible_bind = joint.add(self.flexible2_loc, name, m, vis=False)
            lower_bind_jnts.append(self.lower_flexible_bind)
            flexible2_npo = self.flexible2_ctl.getParent()
            pm.pointConstraint([self.lower_start_bind, self.lower_end_bind], flexible2_npo)
            cons = pm.orientConstraint([self.lower_start_bind, self.lower_end_bind], flexible2_npo)
            cons.attr("interpType").set(2)

        # ribbon
        self.leg_output_objs = []
        m = root.getMatrix(worldSpace=True)
        for i in range(len(division1_v_values)):
            name = self.naming(str(i), "space", _s="ctl")
            self.leg_output_objs.append(matrix.transform(root, name, m))
        for i in range(len(division2_v_values)):
            name = self.naming(str(i + len(division1_v_values)), "space", _s="ctl")
            self.leg_output_objs.append(matrix.transform(root, name, m))
        for i in range(len(division3_v_values) - 1):
            name = self.naming(str(i + len(division1_v_values) + len(division2_v_values)), "space", _s="ctl")
            self.leg_output_objs.append(matrix.transform(root, name, m))
        name = self.naming(f"{len(self.leg_output_objs)}", "space", _s="ctl")
        obj = matrix.transform(root, name, fk3_m)
        self.leg_output_objs.append(obj)
        if data["division1"] > 1:
            flexible0_uniform_attr = attribute.add(self.flexible0_ctl,
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
                                  sorted(division1_v_values),
                                  upper_bind_jnts,
                                  flexible0_uniform_attr,
                                  self.leg_output_objs[:(len(division2_v_values) + len(division3_v_values) - 1) * -1],
                                  negate=self.ddata.negate)
            index = len(division1_v_values) - 1
            aim_m = self.leg_output_objs[index].attr("offsetParentMatrix").inputs(type="aimMatrix")[0]
            aim_m.attr("primaryInputAxisX").set(-1 if self.ddata.negate else 1)
            pm.connectAttr(self.leg_output_objs[index + 1].attr("dagLocalMatrix"),
                           aim_m.attr("primaryTargetMatrix"),
                           force=True)
        else:
            pm.parentConstraint(self.upper_start_bind, self.leg_output_objs[0])
        if data["division2"] > 1:
            flexible1_uniform_attr = attribute.add(self.flexible1_ctl,
                                                   longName="uniform",
                                                   typ="double",
                                                   defaultValue=1,
                                                   minValue=0,
                                                   maxValue=1,
                                                   keyable=True)
            name = self.naming("flexible", "{}", _s="ctl")
            index_range = (len(division1_v_values), len(division1_v_values) + len(division2_v_values))
            uvpin2 = nurbs.ribbon(root,
                                  name,
                                  positions[1:3],
                                  normal,
                                  sorted(division2_v_values),
                                  mid_bind_jnts,
                                  flexible1_uniform_attr,
                                  self.leg_output_objs[index_range[0]:index_range[1]],
                                  negate=self.ddata.negate)
            index = len(division1_v_values) + len(division2_v_values) - 1
            aim_m = self.leg_output_objs[index].attr("offsetParentMatrix").inputs(type="aimMatrix")[0]
            aim_m.attr("primaryInputAxisX").set(-1 if self.ddata.negate else 1)
            pm.connectAttr(self.leg_output_objs[index + 1].attr("dagLocalMatrix"),
                           aim_m.attr("primaryTargetMatrix"),
                           force=True)
        else:
            pm.parentConstraint(self.mid_start_bind, self.leg_output_objs[1])
        if data["division3"] > 1:
            flexible2_uniform_attr = attribute.add(self.flexible2_ctl,
                                                   longName="uniform",
                                                   typ="double",
                                                   defaultValue=1,
                                                   minValue=0,
                                                   maxValue=1,
                                                   keyable=True)
            name = self.naming("lower", "{}", _s="ctl")
            uvpin2 = nurbs.ribbon(root,
                                  name,
                                  positions[2:4],
                                  normal,
                                  sorted(division3_v_values)[:-1],
                                  lower_bind_jnts,
                                  flexible2_uniform_attr,
                                  self.leg_output_objs[len(division1_v_values) + len(division2_v_values):],
                                  negate=self.ddata.negate)
            aim_m = self.leg_output_objs[-2].attr("offsetParentMatrix").inputs(type="aimMatrix")[0]
            aim_m.attr("primaryInputAxisX").set(-1 if self.ddata.negate else 1)
            pm.connectAttr(self.leg_output_objs[-1].attr("matrix"), aim_m.attr("primaryTargetMatrix"), force=True)
        else:
            pm.parentConstraint(self.lower_start_bind, self.leg_output_objs[2])

        pm.parentConstraint(self.blend_objs[-1], obj, maintainOffset=True)
        pm.scaleConstraint(self.blend_objs[-1], obj, maintainOffset=True)

        self.volume_inputs = division1_v_values + \
                             [x + 1 for x in division2_v_values] + \
                             [x + 2 for x in division3_v_values]
        self.volume_inputs = sorted([x / 3.0 for x in self.volume_inputs])

        # refs
        self.refs = []
        for i, obj in enumerate(self.leg_output_objs):
            name = self.naming(f"{i}", "ref", _s="ctl")
            if i == 0 \
                    or i == len(self.leg_output_objs) - 1 \
                    or i == len(division1_v_values) \
                    or i == len(division2_v_values):
                anchor = True
            else:
                anchor = False
            self.refs.append(self.create_ref(context=context,
                                             name=name,
                                             anchor=anchor,
                                             m=obj))
        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            jnt = None
            twist_index = 0
            for i, ref in enumerate(self.refs):
                if i == 0:
                    name = self.naming("1", _s="jnt")
                elif i == len(division1_v_values):
                    name = self.naming("2", _s="jnt")
                    twist_index = 0
                elif i == len(division1_v_values) + len(division2_v_values):
                    name = self.naming("3", _s="jnt")
                    twist_index = 0
                elif i == len(self.refs) - 1:
                    name = self.naming("4", _s="jnt")
                elif i < len(division1_v_values):
                    name = self.naming(f"upper{twist_index}", _s="jnt")
                elif len(division1_v_values) < i < len(division1_v_values) + len(division2_v_values):
                    name = self.naming(f"mid{twist_index}", _s="jnt")
                else:
                    name = self.naming(f"lower{twist_index}", _s="jnt")
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
        super(Leg3jnt01Rig, self).attributes(context)
        host = self.create_host(context)
        data = self.data(Leg3jnt01Data.SELF)

        self.fk_ik_attr = attribute.add(host,
                                        "fk_ik",
                                        typ="double",
                                        keyable=True,
                                        minValue=0,
                                        maxValue=1,
                                        defaultValue=data["fk_ik"])
        self.auto_rot_attr = attribute.add(host,
                                           "auto_rot",
                                           typ="double",
                                           keyable=True,
                                           minValue=0,
                                           maxValue=1,
                                           defaultValue=1)
        if data["spring_solver"]:
            self.spring_bias0_attr = attribute.add(host,
                                                   "spring_angle_bias0",
                                                   typ="double",
                                                   keyable=True,
                                                   minValue=0,
                                                   maxValue=1,
                                                   defaultValue=0.5)
            self.spring_bias1_attr = attribute.add(host,
                                                   "spring_angle_bias1",
                                                   typ="double",
                                                   keyable=True,
                                                   minValue=0,
                                                   maxValue=1,
                                                   defaultValue=0.5)
        self.upper_twist_attr = attribute.add(host, "upper_twist", typ="double", defaultValue=0, keyable=True)
        self.upper_roll_attr = attribute.add(host, "upper_roll", typ="double", defaultValue=0, keyable=True)
        self.roll_attr = attribute.add(host, "roll", typ="double", defaultValue=0, keyable=True)
        self.max_stretch_attr = attribute.add(host,
                                              "max_stretch",
                                              "double",
                                              keyable=True,
                                              minValue=1,
                                              maxValue=999,
                                              defaultValue=data["max_stretch"])
        self.volume_attr = attribute.add(host,
                                         "volume",
                                         "double",
                                         keyable=True,
                                         minValue=0,
                                         maxValue=1,
                                         defaultValue=1)
        self.first_length_attr = attribute.add(self.root,
                                               "first_length",
                                               "double",
                                               keyable=False,
                                               value=self.chain3_ik_jnts[1].attr("tx").get())
        self.first_length_mult_attr = attribute.add(host,
                                                    "first_length_mult",
                                                    "double",
                                                    keyable=True,
                                                    minValue=1)
        self.second_length_attr = attribute.add(self.root,
                                                "second_length",
                                                "double",
                                                keyable=False,
                                                defaultValue=self.chain3_ik_jnts[2].attr("tx").get())
        self.second_length_mult_attr = attribute.add(host,
                                                     "second_length_mult",
                                                     "double",
                                                     keyable=True,
                                                     minValue=1)
        self.third_length_attr = attribute.add(self.root,
                                               "third_length",
                                               "double",
                                               keyable=False,
                                               defaultValue=self.chain3_ik_jnts[3].attr("tx").get())
        self.third_length_mult_attr = attribute.add(host,
                                                    "third_length_mult",
                                                    "double",
                                                    keyable=True,
                                                    minValue=1)
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
        if data["division1"] > 1:
            self.upper_uniform_attr = attribute.add(host,
                                                    longName="uniform",
                                                    typ="double",
                                                    defaultValue=1,
                                                    minValue=0,
                                                    maxValue=1,
                                                    keyable=True)
        if data["division2"] > 1:
            self.lower_uniform_attr = attribute.add(host,
                                                    longName="uniform",
                                                    typ="double",
                                                    defaultValue=1,
                                                    minValue=0,
                                                    maxValue=1,
                                                    keyable=True)
        if data["division3"] > 1:
            self.metacarpals_uniform_attr = attribute.add(host,
                                                          longName="uniform",
                                                          typ="double",
                                                          defaultValue=1,
                                                          minValue=0,
                                                          maxValue=1,
                                                          keyable=True)

    def operators(self, context):
        super(Leg3jnt01Rig, self).operators(context)
        host = self.host()
        data = self.data(Leg3jnt01Data.SELF)

        # fk ik blend
        operators.set_fk_ik_blend_matrix(self.blend_objs,
                                         [self.fk0_ctl, self.fk1_ctl, self.fk2_ctl, self.fk3_ctl],
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

        # spring solver
        if data["spring_solver"]:
            pm.connectAttr(self.spring_bias0_attr,
                           self.chain3_ik_ikh.attr("springAngleBias[0].springAngleBias_FloatValue"))
            pm.connectAttr(self.spring_bias1_attr,
                           self.chain3_ik_ikh.attr("springAngleBias[1].springAngleBias_FloatValue"))

        # third roll
        pm.pointConstraint(self.chain3_ik_jnts[-1], self.third_rot_fix_obj)
        cons = pm.parentConstraint([self.third_rot_fix_obj, self.third_rot_auto_obj], self.third_rot_ctl.getParent())
        rev = pm.createNode("reverse")
        pm.connectAttr(self.auto_rot_attr, rev.attr("inputX"))
        pm.connectAttr(rev.attr("outputX"), cons.attr("target[0].targetWeight"), force=True)
        pm.connectAttr(self.auto_rot_attr, cons.attr("target[1].targetWeight"), force=True)

        # length multiple, stretch
        operators.ik_3jnt(self.chain3_ik_jnts[1],
                          self.chain3_ik_jnts[2],
                          self.chain3_ik_jnts[3],
                          self.first_length_mult_attr,
                          self.second_length_mult_attr,
                          self.third_length_mult_attr,
                          self.stretch_value_attr,
                          self.max_stretch_attr,
                          self.ddata.negate)
        pm.connectAttr(self.chain3_ik_jnts[1].attr("tx"), self.ik_jnts[1].attr("tx"))
        pm.connectAttr(self.chain3_ik_jnts[2].attr("tx"), self.ik_jnts[2].attr("tx"))
        pm.connectAttr(self.chain3_ik_jnts[3].attr("tx"), self.ik_jnts[3].attr("tx"))
        pm.connectAttr(self.chain3_ik_jnts[3].attr("tx"), self.chain2_ikh_source.attr("tx"))

        # pin ctl
        for i, pin_ctl in enumerate([self.pin1_ctl, self.pin2_ctl]):
            pin_npo = pin_ctl
            if pm.controller(pin_npo, query=True):
                pin_npo = pin_npo.getParent()
            pm.pointConstraint(self.blend_objs[i + 1], pin_npo)
            cons = pm.orientConstraint([self.blend_objs[i], self.blend_objs[i + 1]], pin_npo, maintainOffset=True)
            cons.attr("interpType").set(2)

        # roll
        if self.chain3_ik_ikh.attr("twist").get() != 0:
            pma = pm.createNode("plusMinusAverage")
            pma.attr("input1D")[0].set(180)
            pm.connectAttr(self.roll_attr, pma.attr("input1D")[1])
            pm.connectAttr(pma.attr("output1D"), self.chain3_ik_ikh.attr("twist"))
        else:
            pm.connectAttr(self.roll_attr, self.chain3_ik_ikh.attr("twist"))
        pma = pm.createNode("plusMinusAverage")
        pm.connectAttr(self.roll_attr, pma.attr("input1D")[0])
        pm.connectAttr(self.upper_roll_attr, pma.attr("input1D")[1])
        pm.connectAttr(pma.attr("output1D"), self.chain2_ik_ikh.attr("twist"))

        # upper twist
        pm.connectAttr(self.upper_twist_attr, self.upper_start_bind.attr("rx"))

        # volume
        pma = pm.createNode("plusMinusAverage")
        orig_upper_length = nurbs.length(self.orig_upper_crv)
        orig_mid_length = nurbs.length(self.orig_mid_crv)
        orig_lower_length = nurbs.length(self.orig_lower_crv)
        pm.connectAttr(orig_upper_length, pma.attr("input1D")[0])
        pm.connectAttr(orig_mid_length, pma.attr("input1D")[1])
        pm.connectAttr(orig_lower_length, pma.attr("input1D")[2])
        orig_distance_attr = pma.attr("output1D")

        pma = pm.createNode("plusMinusAverage")
        pm.connectAttr(nurbs.length(self.deform_upper_crv), pma.attr("input1D")[0])
        pm.connectAttr(nurbs.length(self.deform_mid_crv), pma.attr("input1D")[1])
        pm.connectAttr(nurbs.length(self.deform_lower_crv), pma.attr("input1D")[2])

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(orig_upper_length, md.attr("input1X"))
        pm.connectAttr(orig_mid_length, md.attr("input1Y"))
        pm.connectAttr(orig_lower_length, md.attr("input1Z"))
        md.attr("input2X").set(-1)
        md.attr("input2Y").set(-1)
        md.attr("input2Z").set(-1)

        pma1 = pm.createNode("plusMinusAverage")
        pm.connectAttr(md.attr("outputX"), pma1.attr("input1D")[0])
        pm.connectAttr(md.attr("outputY"), pma1.attr("input1D")[1])
        pm.connectAttr(md.attr("outputZ"), pma1.attr("input1D")[2])
        pm.connectAttr(pma1.attr("output1D"), pma.attr("input1D")[3])

        delta_distance_attr = pma.attr("output1D")
        operators.volume(orig_distance_attr,
                         delta_distance_attr,
                         self.squash_attrs,
                         self.stretch_attrs,
                         self.volume_attr,
                         self.leg_output_objs[:-1])

        # space switch
        if data["ik_space_switch_array"]:
            source_ctls = self.find_ctls(data["ik_space_switch_array"])
            operators.space_switch(source_ctls, self.ik_ctl, host, attr_name="ik_space_switch")
            script_node = callback.space_switch(source_ctls,
                                                self.ik_ctl,
                                                host,
                                                switch_attr_name="ik_space_switch")
            context["callbacks"].append(script_node)
        if data["pv_space_switch_array"]:
            source_ctls = self.find_ctls(data["pv_space_switch_array"])
            operators.space_switch(source_ctls, self.pole_vec_ctl, host, attr_name="pv_space_switch")
            script_node = callback.space_switch(source_ctls,
                                                self.pole_vec_ctl,
                                                host,
                                                switch_attr_name="pv_space_switch")
            context["callbacks"].append(script_node)

    def connections(self, context):
        super(Leg3jnt01Rig, self).connections(context)

        if "leg_3jnt_01" not in context:
            context["leg_3jnt_01"] = {}
        context["leg_3jnt_01"][str(self.ddata.identifier)] = [self.ik_loc,
                                                              self.chain3_ik_ikh,
                                                              self.refs[-1],
                                                              self.fk_ik_attr]


class Leg3jnt01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Leg3jnt01Data(node=node, data=data)
        self._guide = Leg3jnt01Guide(self._ddata)
        self._rig = Leg3jnt01Rig(self._ddata)
