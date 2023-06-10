# domino
from domino.lib import matrix, attribute, vector, hierarchy
from domino.lib.rigging import operators, joint, nurbs, callback
from domino.lib.animation import fcurve
from domino import assembler

# built-ins
import os
import uuid

# maya
from maya import cmds as mc
from maya import mel
from maya.api import OpenMaya as om2


class Author:
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "leg"
    side = "C"
    index = 0
    description = "quadruped 다리 입니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset_pole_vec": {"type": "double", "minValue": 0},
        "offset_pole_vec_matrix": {"type": "matrix"},
        "fk_ik": {"type": "double"},
        "spring_solver": {"type": "bool"},
        "division1": {"type": "long", "minValue": 1},
        "division2": {"type": "long", "minValue": 1},
        "division3": {"type": "long", "minValue": 1},
        "max_stretch": {"type": "double"},
        "ik_space_switch_array": {"type": "string"},
        "pv_space_switch_array": {"type": "string"},
        "stretch_volume_fcurve": {"type": "double"},
        "squash_volume_fcurve": {"type": "double"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))
        m2 = matrix.set_matrix_translate(m, (0, -2, 0.1))
        m3 = matrix.set_matrix_translate(m, (0, -4, 0))
        m4 = matrix.set_matrix_translate(m, (0, -6, 0.1))
        m5 = matrix.set_matrix_translate(m, (0, -6, 1))
        return m1, m2, m3, m4, m5

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "offset_pole_vec": 1,
        "offset_pole_vec_matrix": list(om2.MMatrix()),
        "fk_ik": 1,
        "spring_solver": True,
        "division1": 3,
        "division2": 3,
        "division3": 3,
        "max_stretch": 1.2,
    })
    common_preset["anim"].update({
        "stretch_volume_fcurve": {"name": "stretch_volume_fcurve_UU",
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
                                  "weightedTangents": [False]},
        "squash_volume_fcurve": {"name": "squash_volume_fcurve_UU",
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
                                 "weightedTangents": [False]},
    })
    return common_preset


def guide_recipe():
    return {
        "position": [
            (0, "pos1"),
            (1, "pos2"),  # parent node index, extension
            (2, "pos3"),
            (3, "pos4"),
        ],
        "pole_vec": ((0, 1, 2), "poleVec"),  # source node indexes, extension
        "display_curve": [
            ((0, 1, 2, 3, 4), "dpCrv"),  # source node indexes, extension
        ],
        "lock_attrs": (
            (),
            ("tx", "ry", "rz"),
            ("tx", "ry", "rz"),
            ("tx", "rz"),
        )
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        m0, m1, m2, m3, m4 = [om2.MMatrix(x) for x in data["anchors"]]

        positions = [om2.MVector(list(x)[12:-1]) for x in [m0, m1, m2, m3, m4]]
        normal = vector.get_plane_normal(*positions[:3])

        root = self.create_root(context)
        fk_color = self.generate_color("fk")
        ik_color = self.generate_color("ik")

        orig_m = om2.MMatrix()
        negate = self.component.negate

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
        fk0_m = matrix.get_look_at_matrix(positions[0], positions[1], normal, "xz", negate)
        offset = ((positions[1] - positions[0]) / 2.0).length()
        po = offset * -1 if negate else offset
        self.fk0_ctl, self.fk0_loc = self.create_ctl(context=context,
                                                     parent=None,
                                                     name=self.generate_name("fk0", "", "ctl"),
                                                     parent_ctl=None,
                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                     m=fk0_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "width": offset * 2,
                                                         "height": div_length / total_length,
                                                         "depth": div_length / total_length,
                                                         "po": (po, 0, 0),
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk0", "", "ctl", True))

        fk1_m = matrix.get_look_at_matrix(positions[1], positions[2], normal, "xz", negate)
        offset = ((positions[2] - positions[1]) / 2.0).length()
        po = offset * -1 if negate else offset
        self.fk1_ctl, self.fk1_loc = self.create_ctl(context=context,
                                                     parent=self.fk0_loc,
                                                     name=self.generate_name("fk1", "", "ctl"),
                                                     parent_ctl=self.fk0_ctl,
                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                     m=fk1_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "width": offset * 2,
                                                         "height": div_length / total_length,
                                                         "depth": div_length / total_length,
                                                         "po": (po, 0, 0),
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk1", "", "ctl", True))

        fk2_m = matrix.get_look_at_matrix(positions[2], positions[3], normal, "xz", negate)
        offset = ((positions[3] - positions[2]) / 2.0).length()
        po = offset * -1 if negate else offset
        self.fk2_ctl, self.fk2_loc = self.create_ctl(context=context,
                                                     parent=self.fk1_loc,
                                                     name=self.generate_name("fk2", "", "ctl"),
                                                     parent_ctl=self.fk1_ctl,
                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                     m=fk2_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "width": offset * 2,
                                                         "height": div_length / total_length,
                                                         "depth": div_length / total_length,
                                                         "po": (po, 0, 0),
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk2", "", "ctl", True))

        fk3_m = matrix.get_look_at_matrix(positions[3], positions[4], normal, "xz", negate)
        offset = ((positions[4] - positions[3]) / 2.0).length()
        po = offset * -1 if negate else offset
        self.fk3_ctl, self.fk3_loc = self.create_ctl(context=context,
                                                     parent=self.fk2_loc,
                                                     name=self.generate_name("fk3", "", "ctl"),
                                                     parent_ctl=self.fk2_ctl,
                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                     m=fk3_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "width": offset * 2,
                                                         "height": div_length / total_length,
                                                         "depth": div_length / total_length,
                                                         "po": (po, 0, 0),
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk3", "", "ctl", True))

        # ik ctl
        m = matrix.set_matrix_translate(orig_m, positions[3])
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context,
                                                   parent=None,
                                                   name=self.generate_name("ik", "", "ctl"),
                                                   parent_ctl=None,
                                                   color=ik_color,
                                                   attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                   m=m,
                                                   cns=True,
                                                   mirror_config=(1, 0, 0, 0, 1, 1, 0, 0, 0),
                                                   shape_args={
                                                       "shape": "cube",
                                                       "width": div_length / total_length,
                                                       "height": div_length / total_length,
                                                       "depth": div_length / total_length,
                                                       "color": ik_color
                                                   },
                                                   mirror_ctl_name=self.generate_name("ik", "", "ctl", True))
        self.ik_match_source = [self.fk0_ctl, self.fk1_ctl, self.fk2_ctl]
        self.ik_match_source.append(matrix.transform(self.fk3_loc, self.generate_name("ik", "match", "ctl"), m))

        third_rot_m = matrix.get_look_at_matrix(positions[3], positions[2], normal, "xz", negate)
        self.third_rot_ctl, self.third_rot_loc = \
            self.create_ctl(context=context,
                            parent=self.ik_loc,
                            name=self.generate_name("thirdRot", "", "ctl"),
                            parent_ctl=self.ik_ctl,
                            attrs=["rx", "ry", "rz"],
                            m=third_rot_m,
                            cns=False,
                            mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                            shape_args={
                                "shape": "arrow4",
                                "width": div_length / total_length,
                                "height": div_length / total_length,
                                "depth": div_length / total_length,
                                "color": ik_color
                            },
                            mirror_ctl_name=self.generate_name("thirdRot", "", "ctl", True))

        name = self.generate_name("chain2Ikh", "source", "ctl")
        self.chain2_ikh_source = matrix.transform(self.third_rot_loc, name, third_rot_m)
        offset = vector.get_distance(positions[-2], positions[-3]) * (-1 if negate else 1)
        mc.setAttr(self.chain2_ikh_source + ".tx", offset)

        # pin ctl
        pin1_m = matrix.get_look_at_matrix(positions[0], positions[2], normal, "xz", negate)
        pin1_m = matrix.set_matrix_translate(pin1_m, positions[1])
        self.pin1_ctl, self.pin1_loc = self.create_ctl(context=context,
                                                       parent=None,
                                                       name=self.generate_name("pin1", "", "ctl"),
                                                       parent_ctl=self.third_rot_ctl,
                                                       attrs=["tx", "ty", "tz", "rx"],
                                                       m=pin1_m,
                                                       cns=True,
                                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                       shape_args={
                                                           "shape": "angle",
                                                           "width": div_length / total_length,
                                                           "height": div_length / total_length,
                                                           "color": ik_color,
                                                           "ro": (90, 0, 225) if negate else (90, 0, 45)
                                                       },
                                                       mirror_ctl_name=self.generate_name("pin1", "", "ctl", True))

        pin2_m = matrix.get_look_at_matrix(positions[1], positions[3], normal, "xz", negate)
        pin2_m = matrix.set_matrix_translate(pin2_m, positions[2])
        self.pin2_ctl, self.pin2_loc = self.create_ctl(context=context,
                                                       parent=None,
                                                       name=self.generate_name("pin2", "", "ctl"),
                                                       parent_ctl=self.pin1_ctl,
                                                       color=ik_color,
                                                       attrs=["tx", "ty", "tz", "rx"],
                                                       m=pin2_m,
                                                       cns=True,
                                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                       shape_args={
                                                           "shape": "angle",
                                                           "width": div_length / total_length,
                                                           "height": div_length / total_length,
                                                           "color": ik_color,
                                                           "ro": (90, 0, 225) if negate else (90, 0, 45)
                                                       },
                                                       mirror_ctl_name=self.generate_name("pin2", "", "ctl", True))

        # pole vec ctl
        pole_vec_pos = om2.MVector(data["offset_pole_vec_matrix"][12:-1])
        pole_vec_m = matrix.set_matrix_translate(fk1_m, pole_vec_pos)
        self.pole_vec_ctl, self.pole_vec_loc = \
            self.create_ctl(context=context,
                            parent=None,
                            name=self.generate_name("pv", "", "ctl"),
                            parent_ctl=self.ik_ctl,
                            attrs=["tx", "ty", "tz"],
                            m=pole_vec_m,
                            shape="x",
                            cns=True,
                            mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                            shape_args={
                                "shape": "x",
                                "width": 1,
                                "height": 1,
                                "depth": 1,
                                "color": ik_color,
                            },
                            mirror_ctl_name=self.generate_name("pv", "", "ctl", True))

        # 3 joint chain (spring solver or rp solver)
        is_spring = data["spring_solver"]
        if is_spring:
            mel.eval("ikSpringSolver;")
        n = "chain3Spring%s" if is_spring else "chain3RP%s"
        name = self.generate_name(n, "", "jnt")
        self.chain3_ik_jnts = joint.add_chain_joint(root,
                                                    name,
                                                    positions[:-1],
                                                    normal,
                                                    last_orient=fk3_m,
                                                    negate=negate,
                                                    vis=False)
        name = self.generate_name("thirdRot", "auto", "ctl")
        self.third_rot_auto_obj = matrix.transform(self.chain3_ik_jnts[-1], name, third_rot_m)
        name = self.generate_name("thirdRot", "fix", "ctl")
        self.third_rot_fix_obj = matrix.transform(self.ik_loc, name, third_rot_m)

        name = self.generate_name("chain3", "aim", "ctl")
        self.chain3_aim_obj = matrix.transform(root, name, matrix.set_matrix_translate(orig_m, positions[0]))
        mc.aimConstraint(self.third_rot_loc, self.chain3_aim_obj, aimVector=(1, 0, 0))

        name = self.generate_name("stretchValue", "grp", "ctl")
        self.stretch_value_grp = matrix.transform(root, name, matrix.set_matrix_translate(orig_m, positions[0]))
        mc.pointConstraint(self.chain3_ik_jnts[0], self.stretch_value_grp)
        mc.aimConstraint(self.ik_loc,
                         self.stretch_value_grp,
                         aimVector=(-1, 0, 0) if negate else (1, 0, 0),
                         upVector=(0, 1, 0),
                         worldUpVector=(-1, 0, 0) if negate else (1, 0, 0),
                         worldUpType="objectrotation",
                         worldUpObject=self.root)

        name = self.generate_name("stretchValue", "pos", "ctl")
        self.stretch_value_obj = matrix.transform(self.stretch_value_grp, name,
                                                  matrix.set_matrix_translate(orig_m, positions[0]))
        mc.pointConstraint(self.ik_loc, self.stretch_value_obj)
        self.stretch_value_attr = self.stretch_value_obj + ".tx"

        name = self.generate_name("chain3", "pos", "ctl")
        self.chain3_pos_obj = matrix.transform(root, name, matrix.set_matrix_translate(orig_m, positions[-2]))
        mc.parentConstraint(self.ik_loc, self.chain3_pos_obj)

        n = "chain3Spring" if is_spring else "chain3RP"
        s = "ikSpringSolver" if is_spring else "ikRPsolver"
        name = self.generate_name(n, "ikh", "ctl")
        orig_pos = vector.get_position(self.chain3_ik_jnts[1])
        self.chain3_ik_ikh = joint.ikh(self.chain3_pos_obj,
                                       name,
                                       self.chain3_ik_jnts,
                                       solver=s,
                                       pole_vector=self.pole_vec_loc)
        new_pos = vector.get_position(self.chain3_ik_jnts[1])

        # spring solver bug.
        if [round(x, 4) for x in orig_pos] != [round(x, 4) for x in new_pos]:
            mc.setAttr(self.chain3_ik_ikh + ".twist", 180)
        if is_spring:
            pick_m = mc.createNode("pickMatrix")
            mc.connectAttr(self.root + ".worldInverseMatrix[0]", pick_m + ".inputMatrix")
            mc.setAttr(pick_m + ".useTranslate", False)
            mc.setAttr(pick_m + ".useScale", False)
            mc.connectAttr(pick_m + ".outputMatrix", self.chain3_ik_jnts[0] + ".offsetParentMatrix")

        # ik jnts
        name = self.generate_name("ik%s", "", "jnt")
        self.fk_match_source = self.ik_jnts = joint.add_chain_joint(root,
                                                                    name,
                                                                    positions[:-1],
                                                                    normal,
                                                                    last_orient=fk3_m,
                                                                    negate=negate,
                                                                    vis=False)
        mc.orientConstraint(self.chain3_ik_ikh, self.ik_jnts[-1], maintainOffset=True)
        name = self.generate_name("chain2", "aim", "ctl")
        self.chain2_aim_obj = matrix.transform(root, name, matrix.set_matrix_translate(orig_m, positions[0]))
        mc.aimConstraint(self.ik_jnts[-2], self.chain2_aim_obj, aimVector=(1, 0, 0))

        name = self.generate_name("chain2", "pos", "ctl")
        self.chain2_pos_obj = matrix.transform(root, name, matrix.set_matrix_translate(orig_m, positions[-3]))
        mc.pointConstraint(self.chain2_ikh_source, self.chain2_pos_obj)

        name = self.generate_name("chain2RP", "ikh", "ctl")
        self.chain2_ik_ikh = joint.ikh(self.chain2_pos_obj, name, self.ik_jnts[:-1], pole_vector=self.pole_vec_loc)

        mc.aimConstraint(self.third_rot_auto_obj,
                         self.ik_jnts[-2],
                         worldUpType="objectrotation",
                         worldUpObject=self.third_rot_auto_obj,
                         maintainOffset=True,
                         aimVector=(-1 if negate else 1, 0, 0),
                         upVector=(0, 0, 1),
                         worldUpVector=(0, 0, 1))

        name = self.generate_name("display", "crv", "ctl")
        self.display_curve = nurbs.create(root,
                                          name,
                                          1,
                                          ((0, 0, 0), (0, 0, 0)),
                                          vis=True,
                                          inherits=False,
                                          display_type=2)
        nurbs.constraint(self.display_curve, [self.chain3_ik_jnts[1], self.pole_vec_loc])

        # blend objs
        self.blend_nodes = []
        parent = root
        for i, jnt in enumerate(self.ik_jnts):
            name = self.generate_name(f"fkik{i}", "blend", "jnt")
            m = mc.xform(jnt, query=True, matrix=True, worldSpace=True)
            parent = matrix.transform(parent=parent, name=name, m=m, offset_parent_matrix=True)
            self.blend_nodes.append(parent)

        # curve for volume
        name = self.generate_name("origUpper", "crv", "ctl")
        self.orig_upper_crv = nurbs.create(root,
                                           name,
                                           1,
                                           positions[:2],
                                           orig_m,
                                           vis=False,
                                           display_type=1)
        name = self.generate_name("deformUpper", "crv", "ctl")
        self.deform_upper_crv = nurbs.create(root,
                                             name,
                                             1,
                                             positions[:2],
                                             orig_m,
                                             vis=False,
                                             display_type=1)
        mc.setAttr(self.deform_upper_crv + ".inheritsTransform", 0)
        nurbs.constraint(self.deform_upper_crv, self.blend_nodes[:2])

        name = self.generate_name("origMid", "crv", "ctl")
        self.orig_mid_crv = nurbs.create(root,
                                         name,
                                         1,
                                         positions[1:3],
                                         orig_m,
                                         vis=False,
                                         display_type=1)
        name = self.generate_name("deformMid", "crv", "ctl")
        self.deform_mid_crv = nurbs.create(root,
                                           name,
                                           1,
                                           positions[1:3],
                                           orig_m,
                                           vis=False,
                                           display_type=1)
        mc.setAttr(self.deform_mid_crv + ".inheritsTransform", 0)
        nurbs.constraint(self.deform_mid_crv, self.blend_nodes[1:3])

        name = self.generate_name("origLower", "crv", "ctl")
        self.orig_lower_crv = nurbs.create(root,
                                           name,
                                           1,
                                           positions[2:4],
                                           orig_m,
                                           vis=False,
                                           display_type=1)
        name = self.generate_name("deformLower", "crv", "ctl")
        self.deform_lower_crv = nurbs.create(root,
                                             name,
                                             1,
                                             positions[2:4],
                                             orig_m,
                                             vis=False,
                                             display_type=1)
        mc.setAttr(self.deform_lower_crv + ".inheritsTransform", 0)
        nurbs.constraint(self.deform_lower_crv, self.blend_nodes[2:4])

        # SC jnts
        # upper
        name = self.generate_name("upperSC", "offset", "ctl")
        self.upper_sc_offset = matrix.transform(parent=root, name=name, m=fk0_m)

        name = self.generate_name("upperFixSC%s", "", "jnt")
        self.upper_fix_sc_jnts = joint.add_chain_joint(self.upper_sc_offset,
                                                       name,
                                                       positions[:2],
                                                       normal,
                                                       negate=negate)
        mc.connectAttr(self.blend_nodes[0] + ".t", self.upper_fix_sc_jnts[0] + ".t")
        name = self.generate_name("upperRotSC%s", "", "jnt")
        self.upper_rot_sc_jnts = joint.add_chain_joint(self.upper_sc_offset,
                                                       name,
                                                       positions[:2],
                                                       normal,
                                                       negate=negate)
        mc.connectAttr(self.blend_nodes[0] + ".t", self.upper_rot_sc_jnts[0] + ".t")

        name = self.generate_name("upperFixSC", "ikh", "ctl")
        self.upper_fix_sc_ikh = joint.ikh(root, name, self.upper_fix_sc_jnts, "ikSCsolver")
        mc.pointConstraint(self.pin1_loc, self.upper_fix_sc_ikh)
        name = self.generate_name("upperRotSC", "ikh", "ctl")
        self.upper_rot_sc_ikh = joint.ikh(root, name, self.upper_rot_sc_jnts, "ikSCsolver")
        mc.pointConstraint(self.pin1_loc, self.upper_rot_sc_ikh)
        mc.orientConstraint(self.blend_nodes[0], self.upper_rot_sc_ikh, maintainOffset=True)

        name = self.generate_name("upperStart", "bind", "jnt")
        self.upper_start_bind = joint.add_joint(self.upper_fix_sc_jnts[0],
                                                name,
                                                matrix.get_matrix(self.upper_fix_sc_jnts[0]),
                                                vis=False)
        name = self.generate_name("upperEnd", "bind", "jnt")
        self.upper_end_bind = joint.add_joint(self.upper_rot_sc_jnts[1],
                                              name,
                                              matrix.get_matrix(self.upper_rot_sc_jnts[1]),
                                              vis=False)
        mc.pointConstraint(self.pin1_loc, self.upper_end_bind)
        mc.connectAttr(self.pin1_ctl + ".rx", self.upper_end_bind + ".rx")

        # mid
        name = self.generate_name("midFixSC%s", "", "jnt")
        self.mid_fix_sc_jnts = joint.add_chain_joint(root, name, positions[1:3], normal, negate=negate)
        mc.pointConstraint(self.pin1_loc, self.mid_fix_sc_jnts[0])

        name = self.generate_name("midFixSC", "ikh", "ctl")
        self.mid_fix_sc_ikh = joint.ikh(root, name, self.mid_fix_sc_jnts, "ikSCsolver")
        mc.pointConstraint(self.blend_nodes[-2], self.mid_fix_sc_ikh)
        mc.orientConstraint(self.upper_end_bind, self.mid_fix_sc_ikh, maintainOffset=True)

        name = self.generate_name("midRotSC%s", "", "jnt")
        self.mid_rot_sc_jnts = joint.add_chain_joint(root, name, positions[1:3], normal, negate=negate)
        mc.pointConstraint(self.pin1_loc, self.mid_rot_sc_jnts[0])

        name = self.generate_name("midRotSC", "ikh", "ctl")
        self.mid_rot_sc_ikh = joint.ikh(root, name, self.mid_rot_sc_jnts, "ikSCsolver")
        mc.pointConstraint(self.blend_nodes[-2], self.mid_rot_sc_ikh)
        mc.orientConstraint(self.blend_nodes[-3], self.mid_rot_sc_ikh, maintainOffset=True)

        name = self.generate_name("midStart", "bind", "jnt")
        self.mid_start_bind = joint.add_joint(self.mid_fix_sc_jnts[0],
                                              name,
                                              matrix.get_matrix(self.mid_fix_sc_jnts[0]),
                                              vis=False)
        name = self.generate_name("midEnd", "bind", "jnt")
        self.mid_end_bind = joint.add_joint(self.mid_rot_sc_jnts[1],
                                            name,
                                            matrix.get_matrix(self.mid_rot_sc_jnts[1]),
                                            vis=False)
        mc.pointConstraint(self.pin2_loc, self.mid_end_bind)
        mc.connectAttr(self.pin2_ctl + ".rx", self.mid_end_bind + ".rx")

        # lower
        name = self.generate_name("lowerFixSC%s", "", "jnt")
        self.lower_fix_sc_jnts = joint.add_chain_joint(root, name, positions[1:3], normal, negate=negate)
        mc.pointConstraint(self.pin2_loc, self.lower_fix_sc_jnts[0])

        name = self.generate_name("lowerFixSC", "ikh", "ctl")
        self.lower_fix_sc_ikh = joint.ikh(root, name, self.lower_fix_sc_jnts, "ikSCsolver")
        mc.pointConstraint(self.blend_nodes[-1], self.lower_fix_sc_ikh)
        mc.orientConstraint(self.mid_end_bind, self.lower_fix_sc_ikh, maintainOffset=True)

        name = self.generate_name("lowerRotSC%s", "", "jnt")
        self.lower_rot_sc_jnts = joint.add_chain_joint(root, name, positions[1:3], normal, negate=negate)
        mc.pointConstraint(self.pin2_loc, self.lower_rot_sc_jnts[0])

        name = self.generate_name("lowerRotSC", "ikh", "ctl")
        self.lower_rot_sc_ikh = joint.ikh(root, name, self.lower_rot_sc_jnts, "ikSCsolver")
        mc.pointConstraint(self.blend_nodes[-1], self.lower_rot_sc_ikh)
        mc.orientConstraint(self.blend_nodes[-1], self.lower_rot_sc_ikh, maintainOffset=True)

        name = self.generate_name("lowerStart", "bind", "jnt")
        self.lower_start_bind = joint.add_joint(self.lower_fix_sc_jnts[0],
                                                name,
                                                matrix.get_matrix(self.lower_fix_sc_jnts[0]),
                                                vis=False)
        name = self.generate_name("lowerEnd", "bind", "jnt")
        self.lower_end_bind = joint.add_joint(self.lower_rot_sc_jnts[1],
                                              name,
                                              matrix.get_matrix(self.lower_rot_sc_jnts[1]),
                                              vis=False)
        mc.pointConstraint(self.blend_nodes[-1], self.lower_end_bind)

        # ribbon bind jnts
        upper_bind_jnts = [self.upper_start_bind, self.upper_end_bind]
        mid_bind_jnts = [self.mid_start_bind, self.mid_end_bind]
        lower_bind_jnts = [self.lower_start_bind, self.lower_end_bind]

        division1_v_values = [0, 1]
        division2_v_values = [1]
        division3_v_values = [1]
        # flexible ctl
        if data["division1"] > 1:
            uniform_value = 1.0 / data["division1"]
            division1_v_values.extend([uniform_value * i for i in range(1, data["division1"])])

            m = matrix.get_matrix(self.upper_fix_sc_jnts[0])
            self.flexible0_ctl, self.flexible0_loc = \
                self.create_ctl(context=context,
                                parent=self.upper_sc_offset,
                                name=self.generate_name("flexible0", "", "ctl"),
                                parent_ctl=self.pin1_ctl,
                                attrs=["tx", "ty", "tz",
                                       "rx", "ry", "rz",
                                       "sx", "sy", "sz"],
                                m=m,
                                cns=False,
                                mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                shape_args={
                                    "shape": "circle3",
                                    "width": div_length / total_length,
                                    "height": div_length / total_length,
                                    "depth": div_length / total_length,
                                    "color": ik_color
                                },
                                mirror_ctl_name=self.generate_name("flexible0", "", "ctl", True))

            name = self.generate_name("upperMid", "bind", "jnt")
            self.upper_flexible_bind = joint.add_joint(self.flexible0_loc, name, m, vis=False)
            upper_bind_jnts.append(self.upper_flexible_bind)
            flexible0_npo = hierarchy.get_parent(self.flexible0_ctl)
            mc.pointConstraint([self.upper_start_bind, self.upper_end_bind], flexible0_npo)
            cons = mc.orientConstraint([self.upper_start_bind, self.upper_end_bind], flexible0_npo)[0]
            mc.setAttr(cons + ".interpType", 2)

        if data["division2"] > 1:
            uniform_value = 1.0 / data["division2"]
            division2_v_values.extend([uniform_value * i for i in range(1, data["division2"])])

            m = matrix.get_matrix(self.lower_fix_sc_jnts[0])
            self.flexible1_ctl, self.flexible1_loc = \
                self.create_ctl(context=context,
                                parent=root,
                                name=self.generate_name("flexible1", "", "ctl"),
                                parent_ctl=self.pin1_ctl,
                                color=ik_color,
                                attrs=["tx", "ty", "tz",
                                       "rx", "ry", "rz",
                                       "sx", "sy", "sz"],
                                m=m,
                                cns=False,
                                mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                shape_args={
                                    "shape": "circle3",
                                    "width": div_length / total_length,
                                    "height": div_length / total_length,
                                    "depth": div_length / total_length,
                                    "color": ik_color
                                },
                                mirror_ctl_name=self.generate_name("flexible1", "", "ctl", True))

            name = self.generate_name("midMid", "bind", "jnt")
            self.mid_flexible_bind = joint.add_joint(self.flexible1_loc, name, m, vis=False)
            mid_bind_jnts.append(self.mid_flexible_bind)
            flexible1_npo = hierarchy.get_parent(self.flexible1_ctl)
            mc.pointConstraint([self.mid_start_bind, self.mid_end_bind], flexible1_npo)
            cons = mc.orientConstraint([self.mid_start_bind, self.mid_end_bind], flexible1_npo)[0]
            mc.setAttr(cons + ".interpType", 2)

        if data["division3"] > 1:
            uniform_value = 1.0 / data["division3"]
            division3_v_values.extend([uniform_value * i for i in range(1, data["division3"])])

            m = matrix.get_matrix(self.lower_fix_sc_jnts[0])
            self.flexible2_ctl, self.flexible2_loc = \
                self.create_ctl(context=context,
                                parent=root,
                                name=self.generate_name("flexible2", "", "ctl"),
                                parent_ctl=self.pin2_ctl,
                                attrs=["tx", "ty", "tz",
                                       "rx", "ry", "rz",
                                       "sx", "sy", "sz"],
                                m=m,
                                cns=False,
                                mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                shape_args={
                                    "shape": "circle3",
                                    "width": div_length / total_length,
                                    "height": div_length / total_length,
                                    "depth": div_length / total_length,
                                    "color": ik_color
                                },
                                mirror_ctl_name=self.generate_name("flexible2", "", "ctl", True))
            name = self.generate_name("lowerMid", "bind", "jnt")
            self.lower_flexible_bind = joint.add_joint(self.flexible2_loc, name, m, vis=False)
            lower_bind_jnts.append(self.lower_flexible_bind)
            flexible2_npo = hierarchy.get_parent(self.flexible2_ctl)
            mc.pointConstraint([self.lower_start_bind, self.lower_end_bind], flexible2_npo)
            cons = mc.orientConstraint([self.lower_start_bind, self.lower_end_bind], flexible2_npo)[0]
            mc.setAttr(cons + ".interpType", 2)

        # ribbon
        self.leg_output_nodes = []
        m = matrix.get_matrix(root)
        for i in range(len(division1_v_values)):
            name = self.generate_name(str(i), "space", "ctl")
            self.leg_output_nodes.append(matrix.transform(root, name, m))
        for i in range(len(division2_v_values)):
            name = self.generate_name(str(i + len(division1_v_values)), "space", "ctl")
            self.leg_output_nodes.append(matrix.transform(root, name, m))
        for i in range(len(division3_v_values) - 1):
            name = self.generate_name(str(i + len(division1_v_values) + len(division2_v_values)), "space", "ctl")
            self.leg_output_nodes.append(matrix.transform(root, name, m))
        name = self.generate_name(f"{len(self.leg_output_nodes)}", "space", "ctl")
        node = matrix.transform(root, name, fk3_m)
        self.leg_output_nodes.append(node)
        if data["division1"] > 1:
            flexible0_uniform_attr = attribute.add_attr(self.flexible0_ctl,
                                                        longName="uniform",
                                                        type="double",
                                                        defaultValue=1,
                                                        minValue=0,
                                                        maxValue=1,
                                                        keyable=True)
            name = self.generate_name("upper", "{}", "ctl")
            uvpin1 = nurbs.ribbon(root,
                                  name,
                                  positions[:2],
                                  normal,
                                  sorted(division1_v_values),
                                  upper_bind_jnts,
                                  flexible0_uniform_attr,
                                  self.leg_output_nodes[:(len(division2_v_values) + len(division3_v_values)) * -1],
                                  negate=negate)
            index = len(division1_v_values) - 1
            pick_m = mc.listConnections(self.leg_output_nodes[index] + ".offsetParentMatrix",
                                        source=True,
                                        destination=False)[0]
            aim_m = mc.listConnections(pick_m + ".inputMatrix", source=True, destination=False)[0]
            mc.setAttr(aim_m + ".primaryInputAxisX", -1 if negate else 1)
            mc.connectAttr(self.leg_output_nodes[index + 1] + ".matrix",
                           aim_m + ".primaryTargetMatrix",
                           force=True)

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(uvpin1 + ".outputMatrix[{0}]".format(index), decom_m + ".inputMatrix")

            pma = mc.createNode("plusMinusAverage")
            mc.setAttr(pma + ".operation", 2)
            mc.connectAttr(decom_m + ".outputTranslate", pma + ".input3D[1]")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(uvpin1 + ".outputMatrix[{0}]".format(index), mult_m + ".matrixIn[0]")
            mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            name = self.generate_name("div1Offset", "tz", "ctl")
            offset_node = mc.createNode("transform", name=name, parent=self.root)
            mc.connectAttr(mult_m + ".matrixSum", offset_node + ".offsetParentMatrix")
            mc.setAttr(offset_node + ".tz", 1)

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(offset_node + ".worldMatrix[0]", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", pma + ".input3D[0]")

            cons = mc.aimConstraint(self.leg_output_nodes[index + 1],
                                    self.leg_output_nodes[index],
                                    aimVector=(-1, 0, 0) if negate else (1, 0, 0),
                                    upVector=(0, 0, 1),
                                    worldUpType="vector",
                                    worldUpVector=(0, 1, 0))[0]
            mc.connectAttr(pma + ".output3D", cons + ".worldUpVector")
        else:
            mc.parentConstraint(self.upper_start_bind, self.leg_output_nodes[0])
            mc.pointConstraint(self.mid_start_bind, self.leg_output_nodes[1])
            mc.aimConstraint(self.leg_output_nodes[2], self.leg_output_nodes[1],
                             aimVector=(-1, 0, 0) if negate else (1, 0, 0),
                             upVector=(0, 1, 0),
                             worldUpType="objectrotation",
                             worldUpObject=self.mid_start_bind)
            mc.orientConstraint(self.fk0_loc, self.upper_fix_sc_ikh, maintainOffset=True, skip=("y", "z"))
        if data["division2"] > 1:
            flexible1_uniform_attr = attribute.add_attr(self.flexible1_ctl,
                                                        longName="uniform",
                                                        type="double",
                                                        defaultValue=1,
                                                        minValue=0,
                                                        maxValue=1,
                                                        keyable=True)
            name = self.generate_name("flexible", "{}", "ctl")
            index_range = (len(division1_v_values), len(division1_v_values) + len(division2_v_values))
            uvpin2 = nurbs.ribbon(root,
                                  name,
                                  positions[1:3],
                                  normal,
                                  sorted(division2_v_values),
                                  mid_bind_jnts,
                                  flexible1_uniform_attr,
                                  self.leg_output_nodes[index_range[0]:index_range[1]],
                                  negate=negate)
            index = len(division1_v_values) + len(division2_v_values) - 1
            pick_m = mc.listConnections(self.leg_output_nodes[index] + ".offsetParentMatrix",
                                        source=True,
                                        destination=False)[0]
            aim_m = mc.listConnections(pick_m + ".inputMatrix", source=True, destination=False)[0]
            mc.setAttr(aim_m + ".primaryInputAxisX", -1 if negate else 1)
            mc.connectAttr(self.leg_output_nodes[index + 1] + ".matrix",
                           aim_m + ".primaryTargetMatrix",
                           force=True)
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(uvpin2 + ".outputMatrix[{0}]".format(len(division2_v_values) - 1),
                           decom_m + ".inputMatrix")

            pma = mc.createNode("plusMinusAverage")
            mc.setAttr(pma + ".operation", 2)
            mc.connectAttr(decom_m + ".outputTranslate", pma + ".input3D[1]")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(uvpin2 + ".outputMatrix[{0}]".format(len(division2_v_values) - 1),
                           mult_m + ".matrixIn[0]")
            mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            name = self.generate_name("div2Offset", "tz", "ctl")
            offset_node = mc.createNode("transform", name=name, parent=self.root)
            mc.connectAttr(mult_m + ".matrixSum", offset_node + ".offsetParentMatrix")
            mc.setAttr(offset_node + ".tz", 1)

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(offset_node + ".worldMatrix[0]", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", pma + ".input3D[0]")

            cons = mc.aimConstraint(self.leg_output_nodes[index + 1],
                                    self.leg_output_nodes[index],
                                    aimVector=(-1, 0, 0) if negate else (1, 0, 0),
                                    upVector=(0, 0, 1),
                                    worldUpType="vector",
                                    worldUpVector=(0, 1, 0))[0]
            mc.connectAttr(pma + ".output3D", cons + ".worldUpVector")
        else:
            mc.connectAttr(self.fk1_ctl + ".rx", self.upper_rot_sc_jnts[-1] + ".rx")
            mc.pointConstraint(self.lower_start_bind,
                               self.leg_output_nodes[len(division1_v_values) + len(division2_v_values) - 1])
            mc.aimConstraint(self.leg_output_nodes[len(division1_v_values) + len(division2_v_values)],
                             self.leg_output_nodes[len(division1_v_values) + len(division2_v_values) - 1],
                             aimVector=(-1, 0, 0) if negate else (1, 0, 0),
                             upVector=(0, 1, 0),
                             worldUpType="objectrotation",
                             worldUpObject=self.lower_start_bind)
        if data["division3"] > 1:
            flexible2_uniform_attr = attribute.add_attr(self.flexible2_ctl,
                                                        longName="uniform",
                                                        type="double",
                                                        defaultValue=1,
                                                        minValue=0,
                                                        maxValue=1,
                                                        keyable=True)
            name = self.generate_name("lower", "{}", "ctl")
            uvpin2 = nurbs.ribbon(root,
                                  name,
                                  positions[2:4],
                                  normal,
                                  sorted(division3_v_values),
                                  lower_bind_jnts,
                                  flexible2_uniform_attr,
                                  self.leg_output_nodes[len(division1_v_values) + len(division2_v_values):],
                                  negate=negate)
            index = len(division1_v_values) + len(division2_v_values) + len(division3_v_values) - 2
            pick_m = mc.listConnections(self.leg_output_nodes[-2] + ".offsetParentMatrix",
                                        source=True,
                                        destination=False)[0]
            aim_m = mc.listConnections(pick_m + ".inputMatrix", source=True, destination=False)[0]
            mc.setAttr(aim_m + ".primaryInputAxisX", -1 if negate else 1)
            mc.connectAttr(self.leg_output_nodes[-1] + ".matrix",
                           aim_m + ".primaryTargetMatrix",
                           force=True)
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(uvpin2 + ".outputMatrix[{0}]".format(len(division3_v_values) - 2),
                           decom_m + ".inputMatrix")

            pma = mc.createNode("plusMinusAverage")
            mc.setAttr(pma + ".operation", 2)
            mc.connectAttr(decom_m + ".outputTranslate", pma + ".input3D[1]")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(uvpin2 + ".outputMatrix[{0}]".format(len(division3_v_values) - 2),
                           mult_m + ".matrixIn[0]")
            mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            name = self.generate_name("div2Offset", "tz", "ctl")
            offset_node = mc.createNode("transform", name=name, parent=self.root)
            mc.connectAttr(mult_m + ".matrixSum", offset_node + ".offsetParentMatrix")
            mc.setAttr(offset_node + ".tz", 1)

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(offset_node + ".worldMatrix[0]", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", pma + ".input3D[0]")

            cons = mc.aimConstraint(self.leg_output_nodes[index + 1],
                                    self.leg_output_nodes[index],
                                    aimVector=(-1, 0, 0) if negate else (1, 0, 0),
                                    upVector=(0, 0, 1),
                                    worldUpType="vector",
                                    worldUpVector=(0, 1, 0))[0]
            mc.connectAttr(pma + ".output3D", cons + ".worldUpVector")
        else:
            mc.connectAttr(self.fk2_ctl + ".rx", self.lower_start_bind + ".rx")

        mc.parentConstraint(self.blend_nodes[-1], self.leg_output_nodes[-1])

        self.volume_inputs = division1_v_values + \
                             [x + 1 for x in division2_v_values] + \
                             [x + 2 for x in division3_v_values]
        self.volume_inputs = sorted([x / 3.0 for x in self.volume_inputs])

        # refs
        self.refs = []
        for i, node in enumerate(self.leg_output_nodes):
            name = self.generate_name(f"{i}", "ref", "ctl")
            if i == 0 \
                    or i == len(self.leg_output_nodes) - 1 \
                    or i == len(division1_v_values) - 1 \
                    or i == len(division2_v_values) + len(division1_v_values) - 1:
                anchor = True
            else:
                anchor = False
            self.refs.append(self.create_ref(context=context,
                                             name=name,
                                             anchor=anchor,
                                             m=node))
        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            jnt = None
            twist_index = 0
            for i, ref in enumerate(self.refs):
                if i == 0:
                    name = self.generate_name("1", "", "jnt")
                elif i == len(division1_v_values) - 1:
                    name = self.generate_name("2", "", "jnt")
                    twist_index = 0
                elif i == len(division1_v_values) + len(division2_v_values) - 1:
                    name = self.generate_name("3", "", "jnt")
                    twist_index = 0
                elif i == len(self.refs) - 1:
                    name = self.generate_name("4", "", "jnt")
                elif i < len(division1_v_values):
                    name = self.generate_name(f"upper{twist_index}", "", "jnt")
                elif len(division1_v_values) - 1 < i < len(division1_v_values) + len(division2_v_values):
                    name = self.generate_name(f"mid{twist_index}", "", "jnt")
                else:
                    name = self.generate_name(f"lower{twist_index}", "", "jnt")
                m = matrix.get_matrix(ref)
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
        super().attributes(context)
        host = self.host
        data = self.component.data["value"]

        self.fk_ik_attr = attribute.add_attr(host,
                                             longName="fk_ik",
                                             type="double",
                                             keyable=True,
                                             minValue=0,
                                             maxValue=1,
                                             defaultValue=data["fk_ik"])
        self.auto_rot_attr = attribute.add_attr(host,
                                                longName="auto_rot",
                                                type="double",
                                                keyable=True,
                                                minValue=0,
                                                maxValue=1,
                                                defaultValue=1)
        if data["spring_solver"]:
            self.spring_bias0_attr = attribute.add_attr(host,
                                                        longName="spring_angle_bias0",
                                                        type="double",
                                                        keyable=True,
                                                        minValue=0,
                                                        maxValue=1,
                                                        defaultValue=0.5)
            self.spring_bias1_attr = attribute.add_attr(host,
                                                        longName="spring_angle_bias1",
                                                        type="double",
                                                        keyable=True,
                                                        minValue=0,
                                                        maxValue=1,
                                                        defaultValue=0.5)
        self.upper_twist_attr = attribute.add_attr(host,
                                                   longName="upper_twist",
                                                   type="double",
                                                   defaultValue=0,
                                                   keyable=True)
        self.upper_roll_attr = attribute.add_attr(host,
                                                  longName="upper_roll",
                                                  type="double",
                                                  defaultValue=0,
                                                  keyable=True)
        self.roll_attr = attribute.add_attr(host,
                                            longName="roll",
                                            type="double",
                                            defaultValue=0,
                                            keyable=True)
        self.max_stretch_attr = attribute.add_attr(host,
                                                   longName="max_stretch",
                                                   type="double",
                                                   keyable=True,
                                                   minValue=1,
                                                   maxValue=999,
                                                   defaultValue=data["max_stretch"])
        self.volume_attr = attribute.add_attr(host,
                                              longName="volume",
                                              type="double",
                                              keyable=True,
                                              minValue=0,
                                              maxValue=1,
                                              defaultValue=1)
        self.first_length_attr = attribute.add_attr(self.root,
                                                    longName="first_length",
                                                    type="double",
                                                    keyable=False,
                                                    defaultValue=mc.getAttr(self.chain3_ik_jnts[1] + ".tx"))
        self.first_length_mult_attr = attribute.add_attr(host,
                                                         longName="first_length_mult",
                                                         type="double",
                                                         keyable=True,
                                                         minValue=1)
        self.second_length_attr = attribute.add_attr(self.root,
                                                     longName="second_length",
                                                     type="double",
                                                     keyable=False,
                                                     defaultValue=mc.getAttr(self.chain3_ik_jnts[2] + ".tx"))
        self.second_length_mult_attr = attribute.add_attr(host,
                                                          longName="second_length_mult",
                                                          type="double",
                                                          keyable=True,
                                                          minValue=1)
        self.third_length_attr = attribute.add_attr(self.root,
                                                    longName="third_length",
                                                    type="double",
                                                    keyable=False,
                                                    defaultValue=mc.getAttr(self.chain3_ik_jnts[3] + ".tx"))
        self.third_length_mult_attr = attribute.add_attr(host,
                                                         longName="third_length_mult",
                                                         type="double",
                                                         keyable=True,
                                                         minValue=1)
        self.stretch_attrs = []
        self.squash_attrs = []
        stretch_volume_fcurve = mc.listConnections(self.root + ".stretch_volume_fcurve",
                                                   source=True,
                                                   destination=False)[0]
        squash_volume_fcurve = mc.listConnections(self.root + ".squash_volume_fcurve",
                                                  source=True,
                                                  destination=False)[0]
        stretch_values = fcurve.get_fcurve_values(stretch_volume_fcurve, division=0, inputs=self.volume_inputs)
        for i, value in enumerate(stretch_values):
            self.stretch_attrs.append(attribute.add_attr(self.root,
                                                         longName=f"stretch_volume_value{i}",
                                                         type="double",
                                                         keyable=False,
                                                         minValue=-1,
                                                         maxValue=0,
                                                         defaultValue=value))
        squash_values = fcurve.get_fcurve_values(squash_volume_fcurve, division=0, inputs=self.volume_inputs)
        for i, value in enumerate(squash_values):
            self.squash_attrs.append(attribute.add_attr(self.root,
                                                        longName=f"squash_volume_value{i}",
                                                        type="double",
                                                        keyable=False,
                                                        minValue=0,
                                                        maxValue=1,
                                                        defaultValue=value))
        if data["division1"] > 1:
            self.upper_uniform_attr = attribute.add_attr(host,
                                                         longName="uniform",
                                                         type="double",
                                                         defaultValue=1,
                                                         minValue=0,
                                                         maxValue=1,
                                                         keyable=True)
        if data["division2"] > 1:
            self.lower_uniform_attr = attribute.add_attr(host,
                                                         longName="uniform",
                                                         type="double",
                                                         defaultValue=1,
                                                         minValue=0,
                                                         maxValue=1,
                                                         keyable=True)
        if data["division3"] > 1:
            self.metacarpals_uniform_attr = attribute.add_attr(host,
                                                               longName="uniform",
                                                               type="double",
                                                               defaultValue=1,
                                                               minValue=0,
                                                               maxValue=1,
                                                               keyable=True)
        self.ik_match_source_attr = attribute.add_attr(host,
                                                       longName="ik_match_source",
                                                       type="message",
                                                       multi=True)
        for i, node in enumerate(self.ik_match_source):
            mc.connectAttr(node + ".message", self.ik_match_source_attr + f"[{i}]")
        self.fk_match_source_attr = attribute.add_attr(host,
                                                       longName="fk_match_source",
                                                       type="message",
                                                       multi=True)
        for i, node in enumerate(self.fk_match_source):
            mc.connectAttr(node + ".message", self.fk_match_source_attr + f"[{i}]")
        self.ik_match_target_attr = attribute.add_attr(host,
                                                       longName="ik_match_target",
                                                       type="message",
                                                       multi=True)
        mc.connectAttr(self.ik_ctl + ".message", self.ik_match_target_attr + "[0]")
        mc.connectAttr(self.pole_vec_ctl + ".message", self.ik_match_target_attr + "[1]")
        self.fk_match_target_attr = attribute.add_attr(host,
                                                       longName="fk_match_target",
                                                       type="message",
                                                       multi=True)
        mc.connectAttr(self.fk0_ctl + ".message", self.fk_match_target_attr + "[0]")
        mc.connectAttr(self.fk1_ctl + ".message", self.fk_match_target_attr + "[1]")
        mc.connectAttr(self.fk2_ctl + ".message", self.fk_match_target_attr + "[2]")
        mc.connectAttr(self.fk3_ctl + ".message", self.fk_match_target_attr + "[3]")

    def operators(self, context):
        super().operators(context)
        host = self.host
        data = self.component.data["value"]

        negate = self.component.negate

        # fk ik blend
        operators.set_fk_ik_blend_matrix(self.blend_nodes,
                                         [self.fk0_ctl, self.fk1_ctl, self.fk2_ctl, self.fk3_ctl],
                                         self.ik_jnts,
                                         self.fk_ik_attr)
        rev = mc.createNode("reverse")
        mc.connectAttr(self.fk_ik_attr, rev + ".inputX")

        ik_npo = hierarchy.get_parent(self.ik_ctl)
        if mc.controller(ik_npo, query=True):
            ik_npo = hierarchy.get_parent(ik_npo)
        pv_npo = hierarchy.get_parent(self.pole_vec_ctl)
        if mc.controller(pv_npo, query=True):
            pv_npo = hierarchy.get_parent(pv_npo)
        fk_npo = hierarchy.get_parent(self.fk0_ctl)
        if mc.controller(fk_npo, query=True):
            fk_npo = hierarchy.get_parent(fk_npo)

        mc.connectAttr(self.fk_ik_attr, ik_npo + ".v")
        mc.connectAttr(self.fk_ik_attr, pv_npo + ".v")
        mc.connectAttr(rev + ".outputX", fk_npo + ".v")
        mc.connectAttr(self.fk_ik_attr, self.display_curve + ".v")

        # spring solver
        if data["spring_solver"]:
            mc.connectAttr(self.spring_bias0_attr,
                           self.chain3_ik_ikh + ".springAngleBias[0].springAngleBias_FloatValue")
            mc.connectAttr(self.spring_bias1_attr,
                           self.chain3_ik_ikh + ".springAngleBias[1].springAngleBias_FloatValue")

        # third roll
        mc.pointConstraint(self.chain3_ik_jnts[-1], self.third_rot_fix_obj)
        cons = mc.parentConstraint([self.third_rot_fix_obj, self.third_rot_auto_obj],
                                   hierarchy.get_parent(self.third_rot_ctl))[0]
        rev = mc.createNode("reverse")
        mc.connectAttr(self.auto_rot_attr, rev + ".inputX")
        mc.connectAttr(rev + ".outputX", cons + ".target[0].targetWeight", force=True)
        mc.connectAttr(self.auto_rot_attr, cons + ".target[1].targetWeight", force=True)

        # length multiple, stretch
        operators.ik_3jnt(self.chain3_ik_jnts[1],
                          self.chain3_ik_jnts[2],
                          self.chain3_ik_jnts[3],
                          self.first_length_mult_attr,
                          self.second_length_mult_attr,
                          self.third_length_mult_attr,
                          self.stretch_value_attr,
                          self.max_stretch_attr,
                          negate)
        mc.connectAttr(self.chain3_ik_jnts[1] + ".tx", self.ik_jnts[1] + ".tx")
        mc.connectAttr(self.chain3_ik_jnts[2] + ".tx", self.ik_jnts[2] + ".tx")
        mc.connectAttr(self.chain3_ik_jnts[3] + ".tx", self.ik_jnts[3] + ".tx")
        mc.connectAttr(self.chain3_ik_jnts[3] + ".tx", self.chain2_ikh_source + ".tx")

        # pin ctl
        for i, pin_ctl in enumerate([self.pin1_ctl, self.pin2_ctl]):
            pin_npo = pin_ctl
            if mc.controller(pin_npo, query=True):
                pin_npo = hierarchy.get_parent(pin_npo)
            mc.pointConstraint(self.blend_nodes[i + 1], pin_npo)
            cons = mc.orientConstraint([self.blend_nodes[i], self.blend_nodes[i + 1]], pin_npo, maintainOffset=True)[0]
            mc.setAttr(cons + ".interpType", 2)

        # roll
        if mc.getAttr(self.chain3_ik_ikh + ".twist") != 0:
            pma = mc.createNode("plusMinusAverage")
            mc.setAttr(pma + ".input1D[0]", mc.getAttr(self.chain3_ik_ikh + ".twist"))
            mc.connectAttr(self.roll_attr, pma + ".input1D[1]")
            mc.connectAttr(pma + ".output1D", self.chain3_ik_ikh + ".twist")
        else:
            mc.connectAttr(self.roll_attr, self.chain3_ik_ikh + ".twist")
        pma = mc.createNode("plusMinusAverage")
        mc.connectAttr(self.roll_attr, pma + ".input1D[0]")
        mc.connectAttr(self.upper_roll_attr, pma + ".input1D[1]")
        mc.connectAttr(pma + ".output1D", self.chain2_ik_ikh + ".twist")

        # upper twist
        mc.connectAttr(self.upper_twist_attr, self.upper_start_bind + ".rx")

        # volume
        pma = mc.createNode("plusMinusAverage")
        orig_upper_length = nurbs.get_length_attr(self.orig_upper_crv, local=False)
        orig_mid_length = nurbs.get_length_attr(self.orig_mid_crv, local=False)
        orig_lower_length = nurbs.get_length_attr(self.orig_lower_crv, local=False)
        mc.connectAttr(orig_upper_length, pma + ".input1D[0]")
        mc.connectAttr(orig_mid_length, pma + ".input1D[1]")
        mc.connectAttr(orig_lower_length, pma + ".input1D[2]")
        orig_distance_attr = pma + ".output1D"

        pma = mc.createNode("plusMinusAverage")
        mc.connectAttr(nurbs.get_length_attr(self.deform_upper_crv), pma + ".input1D[0]")
        mc.connectAttr(nurbs.get_length_attr(self.deform_mid_crv), pma + ".input1D[1]")
        mc.connectAttr(nurbs.get_length_attr(self.deform_lower_crv), pma + ".input1D[2]")

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(orig_upper_length, md + ".input1X")
        mc.connectAttr(orig_mid_length, md + ".input1Y")
        mc.connectAttr(orig_lower_length, md + ".input1Z")
        mc.setAttr(md + ".input2X", -1)
        mc.setAttr(md + ".input2Y", -1)
        mc.setAttr(md + ".input2Z", -1)

        pma1 = mc.createNode("plusMinusAverage")
        mc.connectAttr(md + ".outputX", pma1 + ".input1D[0]")
        mc.connectAttr(md + ".outputY", pma1 + ".input1D[1]")
        mc.connectAttr(md + ".outputZ", pma1 + ".input1D[2]")
        mc.connectAttr(pma1 + ".output1D", pma + ".input1D[3]")

        delta_distance_attr = pma + ".output1D"
        operators.volume(orig_distance_attr,
                         delta_distance_attr,
                         self.squash_attrs,
                         self.stretch_attrs,
                         self.volume_attr,
                         self.leg_output_nodes[:-1])

        # space switch
        if data["ik_space_switch_array"]:
            source_ctls = self.find_ctls(context, data["ik_space_switch_array"])
            operators.space_switch(source_ctls, self.ik_ctl, host, attr_name="ik_space_switch")
            script_node = callback.space_switch(source_ctls,
                                                self.ik_ctl,
                                                host,
                                                switch_attr_name="ik_space_switch")
            context["callbacks"].append(script_node)
        source_ctls = [self.stretch_value_grp]
        if data["pv_space_switch_array"]:
            source_ctls += self.find_ctls(context, data["pv_space_switch_array"])
        operators.space_switch(source_ctls, self.pole_vec_ctl, host, attr_name="pv_space_switch")
        script_node = callback.space_switch(source_ctls,
                                            self.pole_vec_ctl,
                                            host,
                                            switch_attr_name="pv_space_switch")
        context["callbacks"].append(script_node)

    def connections(self, context):
        super().connections(context)

        if "leg_3jnt_01" not in context:
            context["leg_3jnt_01"] = {}
        context["leg_3jnt_01"][str(self.identifier)] = [self.ik_loc,
                                                        self.chain3_ik_ikh,
                                                        self.refs[-1],
                                                        self.fk_ik_attr]
