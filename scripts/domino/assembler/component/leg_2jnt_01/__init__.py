# built-ins
import os
import uuid
import math

# maya
from maya.api import OpenMaya as om2
from maya import cmds as mc

# domino
from domino.lib import attribute, icon, matrix, vector, hierarchy
from domino.lib.rigging import nurbs, controller, joint, operators, callback
from domino.lib.animation import fcurve
from domino import assembler


class Author:
    madeBy = "Chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "leg"
    side = "C"
    index = 0
    description = "사람의 다리입니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset_pole_vec": {"type": "double", "minValue": 0},
        "offset_pole_vec_matrix": {"type": "matrix"},
        "upper_division": {"type": "long"},
        "lower_division": {"type": "long"},
        "fk_ik": {"type": "double"},
        "max_stretch": {"type": "double"},
        "ik_space_switch_array": {"type": "string"},
        "pv_space_switch_array": {"type": "string"},
        "pin_space_switch_array": {"type": "string"},
        "guide_orient_ankle": {"type": "bool"},
        "support_knee_jnt": {"type": "bool"},
        "stretch_volume_fcurve": {"type": "double"},
        "squash_volume_fcurve": {"type": "double"},
        "connector": {"type": "string"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))
        m2 = matrix.set_matrix_translate(m, (0, -2, 0.01))
        m3 = matrix.set_matrix_translate(m, (0, -4, 0))
        m4 = matrix.set_matrix_translate(m, (0, -4, 1))
        return m1, m2, m3, m4

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
        "upper_division": 3,
        "lower_division": 3,
        "fk_ik": 0,
        "max_stretch": 1.5,
        "guide_orient_ankle": False,
        "support_knee_jnt": False,
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
        "root": "thigh",
        "position": [
            (0, "knee"),
            (1, "ankle"),  # parent node index, extension
            (2, "foot")
        ],
        "pole_vec": ((0, 1, 2), "poleVec"),  # source node indexes, extension
        "display_curve": [
            ((0, 1, 2, 3), "dpCrv"),  # source node indexes, extension
        ],
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        negate = self.component.negate

        m0 = om2.MMatrix(data["anchors"][0])
        m1 = om2.MMatrix(data["anchors"][1])
        m2 = om2.MMatrix(data["anchors"][2])
        m3 = om2.MMatrix(data["anchors"][3])

        positions = [om2.MVector(list(x)[12:-1]) for x in [m0, m1, m2, m3]]
        normal = vector.get_plane_normal(*positions[:-1])

        upper_jnt_v_values = [0]
        lower_jnt_v_values = [0, 1]

        root = self.create_root(context)
        fk_color = self.generate_color("fk")
        ik_color = self.generate_color("ik")

        div_length = vector.get_distance(positions[0], positions[1])
        total_length = div_length + vector.get_distance(positions[1], positions[2])

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
                                                         "color": fk_color,
                                                         "width": offset * 2,
                                                         "height": div_length / total_length,
                                                         "depth": div_length / total_length,
                                                         "po": (po, 0, 0)
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk0", "", "ctl", True))
        m = matrix.set_matrix_translate(fk0_m, positions[1])
        self.fk0_length_node = matrix.transform(self.fk0_loc, self.generate_name("fk0", "length", "ctl"), m)

        fk1_m = matrix.get_look_at_matrix(positions[1], positions[2], normal, "xz", negate)
        offset = ((positions[2] - positions[1]) / 2.0).length()
        po = offset * -1 if negate else offset
        self.fk1_ctl, self.fk1_loc = self.create_ctl(context=context,
                                                     parent=self.fk0_length_node,
                                                     name=self.generate_name("fk1", "", "ctl"),
                                                     parent_ctl=self.fk0_ctl,
                                                     attrs=["tx", "ty", "tz", "rz"],
                                                     m=fk1_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "color": fk_color,
                                                         "width": offset * 2,
                                                         "height": div_length / total_length,
                                                         "depth": div_length / total_length,
                                                         "po": (po, 0, 0)
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk1", "", "ctl", True))

        m = matrix.set_matrix_translate(fk1_m, positions[2])
        self.fk1_length_node = matrix.transform(self.fk1_loc, self.generate_name("fk1", "length", "ctl"), m)

        fk2_m = matrix.get_look_at_matrix(positions[2], positions[3], normal, "xz", negate)
        if data["guide_orient_ankle"]:
            fk2_m = m2
            if negate:
                fk2_m = matrix.set_matrix_scale(m2, (1, 1, 1))
                fk2_m = om2.MTransformationMatrix(fk2_m).rotateBy(om2.MEulerRotation(0, 0, math.radians(180)),
                                                                  om2.MSpace.kObject).asMatrix()
        offset = ((positions[3] - positions[2]) / 2.0).length()
        po = offset * -1 if negate or data["guide_orient_ankle"] else offset
        self.fk2_ctl, self.fk2_loc = self.create_ctl(context=context,
                                                     parent=self.fk1_length_node,
                                                     name=self.generate_name("fk2", "", "ctl"),
                                                     parent_ctl=self.fk1_ctl,
                                                     attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz",
                                                            "sx", "sy", "sz"],
                                                     m=fk2_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "color": fk_color,
                                                         "height": div_length / total_length,
                                                         "depth": div_length / total_length,
                                                         "width": offset * 2,
                                                         "po": (po, 0, 0)
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk2", "", "ctl", True))

        # ik ctls
        m = matrix.set_matrix_translate(om2.MMatrix(), positions[2])
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context,
                                                   parent=None,
                                                   name=self.generate_name("ik", "", "ctl"),
                                                   parent_ctl=None,
                                                   attrs=["tx", "ty", "tz",
                                                          "rx", "ry", "rz",
                                                          "sx", "sy", "sz"],
                                                   m=m,
                                                   cns=True,
                                                   mirror_config=(1, 0, 0, 0, 1, 1, 0, 0, 0),
                                                   shape_args={
                                                       "shape": "cube",
                                                       "color": ik_color,
                                                       "width": div_length / total_length * 2,
                                                       "height": div_length / total_length * 2,
                                                       "depth": div_length / total_length * 2
                                                   },
                                                   mirror_ctl_name=self.generate_name("ik", "", "ctl", True))
        self.ik_match_source = [self.fk0_ctl, self.fk1_ctl]
        self.ik_match_source.append(matrix.transform(self.fk2_loc, self.generate_name("ankle", "match", "ctl"), m))

        self.ik_local_ctl, self.ik_local_loc = \
            self.create_ctl(context=context,
                            parent=self.ik_loc,
                            name=self.generate_name("ikLocal", "", "ctl"),
                            parent_ctl=self.ik_ctl,
                            attrs=["tx", "ty", "tz",
                                   "rx", "ry", "rz",
                                   "sx", "sy", "sz"],
                            m=fk2_m,
                            cns=False,
                            mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                            shape_args={
                                "shape": "cube",
                                "color": ik_color,
                                "width": div_length / total_length * 1.6,
                                "height": div_length / total_length * 1.6,
                                "depth": div_length / total_length * 1.6
                            },
                            mirror_ctl_name=self.generate_name("ikLocal", "", "ctl", True))

        pole_vec_pos = data["offset_pole_vec_matrix"][12:-1]
        pole_vec_m = matrix.set_matrix_translate(fk1_m, pole_vec_pos)
        self.pole_vec_ctl, self.pole_vec_loc = \
            self.create_ctl(context=context,
                            parent=None,
                            name=self.generate_name("pv", "", "ctl"),
                            parent_ctl=self.ik_local_ctl,
                            attrs=["tx", "ty", "tz"],
                            m=pole_vec_m,
                            cns=True,
                            mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                            shape_args={
                                "shape": "x",
                                "color": ik_color,
                                "width": 1,
                                "height": 1,
                                "depth": 1
                            },
                            mirror_ctl_name=self.generate_name("pv", "", "ctl", True))

        # ik jnts
        self.fk_match_source = self.ik_jnts = joint.add_chain_joint(root,
                                                                    self.generate_name("ik%s", "", "jnt"),
                                                                    positions[:-1],
                                                                    normal,
                                                                    last_orient=fk2_m,
                                                                    negate=negate)

        self.ik_ikh = joint.ikh(self.ik_local_loc,
                                self.generate_name("RP", "ikh", "ctl"),
                                self.ik_jnts,
                                pole_vector=self.pole_vec_loc)
        mc.orientConstraint(self.ik_ikh, self.ik_jnts[-1], maintainOffset=True)
        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.ik_ikh + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
        mc.connectAttr(self.ik_jnts[-1] + ".parentInverseMatrix[0]", mult_m + ".matrixIn[1]")
        decom_m = mc.createNode("decomposeMatrix")
        mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
        mc.connectAttr(decom_m + ".outputScale", self.ik_jnts[-1] + ".s")

        # knee - pole vector display curve
        self.display_curve = matrix.transform(root, self.generate_name("display", "crv", "ctl"), om2.MMatrix())
        icon.generate(self.display_curve,
                      [(0, 0, 0), (0, 0, 0)],
                      1,
                      om2.MColor((0.55, 0.55, 0.55, 0.55)),
                      thickness=1)
        nurbs.constraint(self.display_curve, [self.ik_jnts[1], self.pole_vec_loc])
        mc.setAttr(self.display_curve + ".inheritsTransform", 0)
        mc.setAttr(self.display_curve + ".translate", 0, 0, 0)
        mc.setAttr(self.display_curve + ".rotate", 0, 0, 0)
        for shape in mc.listRelatives(self.display_curve, shapes=True, fullPath=True):
            mc.setAttr(shape + ".overrideDisplayType", 2)

        # blend objs
        self.blend_nodes = []
        parent = root
        for i, jnt in enumerate(self.ik_jnts):
            parent = matrix.transform(parent=parent,
                                      name=self.generate_name("fkik" + str(i), "blend", "jnt"),
                                      m=matrix.get_matrix(jnt, world_space=True),
                                      offset_parent_matrix=True)
            self.blend_nodes.append(parent)
        sel_list = om2.MSelectionList()
        [sel_list.add(x) for x in self.blend_nodes]
        self.fk_blend0_offset = mc.createNode("transform",
                                              name=self.generate_name("fk_blend0", "offset", "ctl"),
                                              parent=self.blend_nodes[0])
        self.fk_blend1_offset = mc.createNode("transform",
                                              name=self.generate_name("fk_blend1", "offset", "ctl"),
                                              parent=self.blend_nodes[1])
        sel_list.add(self.fk_blend1_offset)
        mc.parent(self.blend_nodes[2], self.fk_blend1_offset)
        mc.parent(self.blend_nodes[1], self.fk_blend0_offset)
        self.blend_nodes = [sel_list.getDagPath(i).fullPathName() for i in range(len(self.blend_nodes))]
        self.fk_blend1_offset = sel_list.getDagPath(len(self.blend_nodes)).fullPathName()

        orig_m = om2.MMatrix()
        self.orig_upper_crv = nurbs.create(root,
                                           self.generate_name("origUpper", "crv", "ctl"),
                                           1,
                                           positions[:2],
                                           orig_m,
                                           vis=False,
                                           display_type=1)
        self.deform_upper_crv = nurbs.create(root,
                                             self.generate_name("deformUpper", "crv", "ctl"),
                                             1,
                                             positions[:2],
                                             orig_m,
                                             vis=False,
                                             display_type=1)
        mc.setAttr(self.deform_upper_crv + ".inheritsTransform", 0)
        nurbs.constraint(self.deform_upper_crv, self.blend_nodes[:2])
        self.orig_lower_crv = nurbs.create(root,
                                           self.generate_name("origLower", "crv", "ctl"),
                                           1,
                                           positions[1:3],
                                           orig_m,
                                           vis=False,
                                           display_type=1)
        self.deform_lower_crv = nurbs.create(root,
                                             self.generate_name("deformLower", "crv", "ctl"),
                                             1,
                                             positions[1:3],
                                             orig_m,
                                             vis=False,
                                             display_type=1)
        mc.setAttr(self.deform_lower_crv + ".inheritsTransform", 0)
        nurbs.constraint(self.deform_lower_crv, self.blend_nodes[1:])

        # pin ctl
        pin_m = matrix.get_look_at_matrix(positions[0], positions[2], normal, "xz", negate)
        pin_m = matrix.set_matrix_translate(pin_m, positions[1])
        self.pin_ctl, self.pin_loc = self.create_ctl(context=context,
                                                     parent=None,
                                                     name=self.generate_name("pin", "", "ctl"),
                                                     parent_ctl=self.fk2_ctl,
                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx"],
                                                     m=pin_m,
                                                     cns=True,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "angle",
                                                         "color": ik_color,
                                                         "width": div_length / total_length,
                                                         "height": div_length / total_length,
                                                         "depth": div_length / total_length,
                                                         "ro": (90, 0, 225) if negate else (90, 0, 45)
                                                     },
                                                     mirror_ctl_name=self.generate_name("pin", "", "ctl", True))
        # support knee ctl
        self.knee_loc = self.pin_loc
        if data["support_knee_jnt"] and data["upper_division"] > 1 and data["lower_division"] > 1:
            upper_jnt_v_values.insert(-1, 0.99)
            lower_jnt_v_values.insert(1, 0.01)
            knee_m = matrix.get_look_at_matrix(positions[0], positions[2], normal, "xz", False)
            knee_m = matrix.set_matrix_translate(knee_m, positions[1])
            self.thickness_knee_ctl, self.thickness_knee_loc = \
                self.create_ctl(context=context,
                                parent=self.pin_loc,
                                name=self.generate_name("kneeThickness", "", "ctl"),
                                parent_ctl=self.pin_ctl,
                                attrs=["tx"],
                                m=knee_m,
                                cns=False,
                                mirror_config=(0, 0, 0, 0, 0, 0, 0, 0, 0),
                                shape_args={
                                    "shape": "arrow",
                                    "color": ik_color,
                                    "width": div_length / total_length,
                                    "height": div_length / total_length,
                                    "depth": div_length / total_length,
                                    "ro": (0, 180, 0) if negate else (0, 0, 0)
                                },
                                mirror_ctl_name=self.generate_name("kneeThickness", "", "ctl", True))
            self.knee_loc = self.thickness_knee_loc

        # lookAt jnts
        self.look_at_jnts = joint.add_chain_joint(root,
                                                  self.generate_name("lookAt%s", "", "jnt"),
                                                  [positions[0], positions[2]],
                                                  normal,
                                                  negate=negate)
        self.stretch_value_jnt = joint.add_joint(self.look_at_jnts[0],
                                                 self.generate_name("stretch", "", "jnt"),
                                                 matrix.get_matrix(self.look_at_jnts[1], world_space=True),
                                                 vis=False)
        self.stretch_value_attr = self.stretch_value_jnt + ".tx"

        self.look_at_sc_ikh = joint.ikh(root,
                                        self.generate_name("lookAt", "ikh", "ctl"),
                                        self.look_at_jnts,
                                        "ikSCsolver")
        mc.pointConstraint(self.ik_jnts[0], self.look_at_jnts[0])
        mc.pointConstraint(self.ik_local_loc, self.look_at_sc_ikh)
        mc.pointConstraint(self.ik_local_loc, self.stretch_value_jnt)

        # SC jnts
        self.upper_sc_offset = matrix.transform(parent=root,
                                                name=self.generate_name("upperSC", "offset", "ctl"),
                                                m=matrix.get_matrix(self.blend_nodes[0], world_space=True))

        self.upper_fix_sc_jnts = joint.add_chain_joint(self.upper_sc_offset,
                                                       self.generate_name("upperFixSC%s", "", "jnt"),
                                                       positions[:2],
                                                       normal,
                                                       negate=negate)
        mc.connectAttr(self.blend_nodes[0] + ".t", self.upper_fix_sc_jnts[0] + ".t")
        self.upper_rot_sc_jnts = joint.add_chain_joint(self.upper_sc_offset,
                                                       self.generate_name("upperRotSC%s", "", "jnt"),
                                                       positions[:2],
                                                       normal,
                                                       negate=negate)
        mc.connectAttr(self.blend_nodes[0] + ".t", self.upper_rot_sc_jnts[0] + ".t")
        self.upper_fix_sc_ikh = joint.ikh(root,
                                          self.generate_name("upperFixSC", "ikh", "ctl"),
                                          self.upper_fix_sc_jnts,
                                          "ikSCsolver")
        mc.pointConstraint(self.pin_loc, self.upper_fix_sc_ikh)
        self.upper_rot_sc_ikh = joint.ikh(root,
                                          self.generate_name("upperRotSC", "ikh", "ctl"),
                                          self.upper_rot_sc_jnts,
                                          "ikSCsolver")
        mc.pointConstraint(self.pin_loc, self.upper_rot_sc_ikh)
        mc.orientConstraint(self.blend_nodes[0], self.upper_rot_sc_ikh, maintainOffset=True)

        self.upper_start_bind = joint.add_joint(self.upper_fix_sc_jnts[0],
                                                self.generate_name("upperStart", "bind", "jnt"),
                                                matrix.get_matrix(self.upper_fix_sc_jnts[0], world_space=True),
                                                vis=False)
        self.upper_end_bind = joint.add_joint(self.upper_rot_sc_jnts[1],
                                              self.generate_name("upperEnd", "bind", "jnt"),
                                              matrix.get_matrix(self.upper_rot_sc_jnts[1], world_space=True),
                                              vis=False)
        mc.pointConstraint(self.pin_loc, self.upper_end_bind)
        mc.connectAttr(self.pin_ctl + ".rx", self.upper_end_bind + ".rx")

        self.lower_fix_sc_jnts = joint.add_chain_joint(root,
                                                       self.generate_name("lowerFixSC%s", "", "jnt"),
                                                       positions[1:3],
                                                       normal,
                                                       negate=negate)
        mc.pointConstraint(self.knee_loc, self.lower_fix_sc_jnts[0])

        self.lower_fix_sc_ikh = joint.ikh(root,
                                          self.generate_name("lowerFixSC", "ikh", "ctl"),
                                          self.lower_fix_sc_jnts,
                                          "ikSCsolver")
        mc.pointConstraint(self.blend_nodes[-1], self.lower_fix_sc_ikh)
        mc.orientConstraint(self.upper_end_bind, self.lower_fix_sc_ikh, maintainOffset=True)

        self.lower_rot_sc_jnts = joint.add_chain_joint(root,
                                                       self.generate_name("lowerRotSC%s", "", "jnt"),
                                                       positions[1:3],
                                                       normal,
                                                       negate=negate)
        mc.pointConstraint(self.knee_loc, self.lower_rot_sc_jnts[0])

        self.lower_rot_sc_ikh = joint.ikh(root,
                                          self.generate_name("lowerRotSC", "ikh", "ctl"),
                                          self.lower_rot_sc_jnts,
                                          "ikSCsolver")
        mc.pointConstraint(self.blend_nodes[-1], self.lower_rot_sc_ikh)
        mc.orientConstraint(self.blend_nodes[-1], self.lower_rot_sc_ikh, maintainOffset=True)

        self.lower_start_bind = joint.add_joint(self.lower_fix_sc_jnts[0],
                                                self.generate_name("lowerStart", "bind", "jnt"),
                                                matrix.get_matrix(self.lower_fix_sc_jnts[0], world_space=True),
                                                vis=False)
        self.lower_end_bind = joint.add_joint(self.lower_rot_sc_jnts[1],
                                              self.generate_name("lowerEnd", "bind", "jnt"),
                                              matrix.get_matrix(self.lower_rot_sc_jnts[1], world_space=True),
                                              vis=False)
        mc.pointConstraint(self.blend_nodes[-1], self.lower_end_bind)

        # ribbon bind jnts
        upper_bind_jnts = [self.upper_start_bind, self.upper_end_bind]
        lower_bind_jnts = [self.lower_start_bind, self.lower_end_bind]

        # flexible ctl
        if data["upper_division"] > 1:
            uniform_value = 1.0 / data["upper_division"]
            upper_jnt_v_values.extend([uniform_value * i for i in range(1, data["upper_division"])])

            m = matrix.get_matrix(self.upper_fix_sc_jnts[0], world_space=True)
            self.flexible0_ctl, self.flexible0_loc = \
                self.create_ctl(context=context,
                                parent=self.upper_sc_offset,
                                name=self.generate_name("flexible0", "", "ctl"),
                                parent_ctl=self.pin_ctl,
                                attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                m=m,
                                cns=False,
                                mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                shape_args={
                                    "shape": "circle3",
                                    "color": ik_color,
                                    "width": div_length / total_length,
                                    "height": div_length / total_length,
                                    "depth": div_length / total_length,
                                },
                                mirror_ctl_name=self.generate_name("flexible0", "", "ctl", True))
            self.upper_flexible_bind = joint.add_joint(self.flexible0_loc,
                                                       self.generate_name("upperMid", "bind", "jnt"),
                                                       m,
                                                       vis=False)
            upper_bind_jnts.append(self.upper_flexible_bind)
            flexible0_npo = hierarchy.get_parent(self.flexible0_ctl)
            mc.pointConstraint([self.upper_start_bind, self.upper_end_bind], flexible0_npo)
            cons = mc.orientConstraint([self.upper_start_bind, self.upper_end_bind], flexible0_npo)[0]
            mc.setAttr(cons + ".interpType", 2)
        else:
            self.upper_start_bind = mc.parent(self.upper_start_bind, self.blend_nodes[0])[0]

        if data["lower_division"] > 1:
            uniform_value = 1.0 / data["lower_division"]
            lower_jnt_v_values.extend([uniform_value * i for i in range(1, data["lower_division"])])

            m = matrix.get_matrix(self.lower_fix_sc_jnts[0], world_space=True)
            self.flexible1_ctl, self.flexible1_loc = \
                self.create_ctl(context=context,
                                parent=root,
                                name=self.generate_name("flexible1", "", "ctl"),
                                parent_ctl=self.pin_ctl,
                                attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                m=m,
                                cns=False,
                                mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                shape_args={
                                    "shape": "circle3",
                                    "color": ik_color,
                                    "width": div_length / total_length,
                                    "height": div_length / total_length,
                                    "depth": div_length / total_length,
                                },
                                mirror_ctl_name=self.generate_name("flexible1", "", "ctl", True))
            self.lower_flexible_bind = joint.add_joint(self.flexible1_loc,
                                                       self.generate_name("lowerMid", "bind", "jnt"),
                                                       m,
                                                       vis=False)
            lower_bind_jnts.append(self.lower_flexible_bind)
            flexible1_npo = hierarchy.get_parent(self.flexible1_ctl)
            mc.pointConstraint([self.lower_start_bind, self.lower_end_bind], flexible1_npo)
            cons = mc.orientConstraint([self.lower_start_bind, self.lower_end_bind], flexible1_npo)[0]
            mc.setAttr(cons + ".interpType", 2)

        # ribbon
        self.leg_output_nodes = []
        m = matrix.get_matrix(root, world_space=True)
        for i in range(len(upper_jnt_v_values)):
            self.leg_output_nodes.append(matrix.transform(root, self.generate_name(str(i), "space", "ctl"), m))
        for i in range(len(lower_jnt_v_values) - 1):
            self.leg_output_nodes.append(matrix.transform(root,
                                                          self.generate_name(str(i + len(upper_jnt_v_values)),
                                                                             "space",
                                                                             "ctl"),
                                                          m))
        node = matrix.transform(root, self.generate_name(str(len(self.leg_output_nodes)), "space", "ctl"), fk2_m)
        self.leg_output_nodes.append(node)
        if data["upper_division"] > 1:
            flexible0_uniform_attr = attribute.add_attr(self.flexible0_ctl,
                                                        longName="uniform",
                                                        type="double",
                                                        defaultValue=1,
                                                        minValue=0,
                                                        maxValue=1,
                                                        keyable=True)
            uvpin1 = nurbs.ribbon(root,
                                  self.generate_name("upper", "{}", "ctl"),
                                  positions[:2],
                                  normal,
                                  sorted(upper_jnt_v_values),
                                  upper_bind_jnts,
                                  flexible0_uniform_attr,
                                  self.leg_output_nodes[:len(lower_jnt_v_values) * -1],
                                  negate=negate)
            # upper last aim fix
            pick_m = mc.listConnections(self.leg_output_nodes[len(upper_jnt_v_values) - 1] + ".offsetParentMatrix",
                                        source=True,
                                        destination=False)[0]
            aim_m = mc.listConnections(pick_m + ".inputMatrix", source=True, destination=False)[0]
            mc.setAttr(aim_m + ".primaryInputAxisX", -1 if negate else 1)
            mc.connectAttr(self.leg_output_nodes[len(upper_jnt_v_values)] + ".offsetParentMatrix",
                           aim_m + ".primaryTargetMatrix",
                           force=True)
        else:
            # thigh setup
            mc.parentConstraint(self.upper_start_bind, self.leg_output_nodes[0])

            # twist setup
            mc.orientConstraint(self.fk0_loc, self.upper_fix_sc_ikh, maintainOffset=True, skip=("y", "z"))
        if data["lower_division"] > 1:
            flexible1_uniform_attr = attribute.add_attr(self.flexible1_ctl,
                                                        longName="uniform",
                                                        type="double",
                                                        defaultValue=1,
                                                        minValue=0,
                                                        maxValue=1,
                                                        keyable=True)
            uvpin2 = nurbs.ribbon(root,
                                  self.generate_name("lower", "{}", "ctl"),
                                  positions[1:3],
                                  normal,
                                  sorted(lower_jnt_v_values)[:-1],
                                  lower_bind_jnts,
                                  flexible1_uniform_attr,
                                  self.leg_output_nodes[len(upper_jnt_v_values):],
                                  negate=negate)
            # knee aim setup
            if data["upper_division"] > 1 and data["support_knee_jnt"]:
                # support option
                support_index = len(upper_jnt_v_values)
                mc.orientConstraint(
                    [
                        self.leg_output_nodes[support_index - 1],
                        self.leg_output_nodes[support_index + 1]
                    ],
                    self.leg_output_nodes[support_index],
                    maintainOffset=True)
            # last-1 aim reverse
            pick_m = mc.listConnections(self.leg_output_nodes[-2] + ".offsetParentMatrix",
                                        source=True,
                                        destination=False)[0]
            aim_m = mc.listConnections(pick_m + ".inputMatrix", source=True, destination=False)[0]
            mc.setAttr(aim_m + ".primaryInputAxisX", -1 if negate else 1)
            mc.connectAttr(self.leg_output_nodes[-1] + ".matrix", aim_m + ".primaryTargetMatrix", force=True)
        else:
            # knee setup
            mc.parentConstraint(self.lower_start_bind, self.leg_output_nodes[-2])

        mc.parentConstraint(self.blend_nodes[-1], node, maintainOffset=False)
        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.blend_nodes[-1] + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
        mc.connectAttr(node + ".parentInverseMatrix[0]", mult_m + ".matrixIn[1]")
        decom_m = mc.createNode("decomposeMatrix")
        mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
        mc.connectAttr(decom_m + ".outputScale", node + ".s")

        self.volume_inputs = upper_jnt_v_values + [x + 1 for x in lower_jnt_v_values]
        self.volume_inputs = sorted([x / 2.0 for x in self.volume_inputs])

        # refs
        self.refs = []
        for i, node in enumerate(self.leg_output_nodes):
            if i == 0 or i == len(self.leg_output_nodes) - 1 or i == len(upper_jnt_v_values):
                anchor = True
            else:
                anchor = False
            name = self.generate_name(str(i), "ref", "ctl")
            self.refs.append(self.create_ref(context=context, name=name, anchor=anchor, m=node))

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            jnt = None
            twist_index = 0
            for i, ref in enumerate(self.refs):
                if i == 0:
                    name = self.generate_name("thigh", "", "jnt")
                elif i == len(upper_jnt_v_values):
                    name = self.generate_name("knee", "", "jnt")
                    twist_index = 0
                elif i == len(self.refs) - 1:
                    name = self.generate_name("ankle", "", "jnt")
                elif i < len(upper_jnt_v_values):
                    name = self.generate_name("upper" + str(twist_index), "", "jnt")
                else:
                    name = self.generate_name("lower" + str(twist_index), "", "jnt")
                m = matrix.get_matrix(ref, world_space=True)
                jnt = self.create_jnt(context=context,
                                      parent=jnt,
                                      name=name,
                                      description=str(i),
                                      ref=ref,
                                      m=m,
                                      leaf=False,
                                      uni_scale=uni_scale)
                twist_index += 1

    def attributes(self, context):
        super().attributes(context)
        host = self.host

        data = self.component.data["value"]
        self.fk0_length_attr = attribute.add_attr(self.fk0_ctl,
                                                  longName="length",
                                                  type="double",
                                                  minValue=0,
                                                  defaultValue=1,
                                                  keyable=True)
        self.fk1_length_attr = attribute.add_attr(self.fk1_ctl,
                                                  longName="length",
                                                  type="double",
                                                  minValue=0,
                                                  defaultValue=1,
                                                  keyable=True)
        self.fk_ik_attr = attribute.add_attr(host,
                                             longName="fk_ik",
                                             type="double",
                                             keyable=True,
                                             minValue=0,
                                             maxValue=1,
                                             defaultValue=data["fk_ik"])
        self.roll_attr = attribute.add_attr(host,
                                            longName="roll",
                                            type="double",
                                            keyable=True,
                                            defaultValue=0)
        self.armpit_roll_attr = attribute.add_attr(host,
                                                   longName="armpit_roll",
                                                   type="double",
                                                   keyable=True,
                                                   defaultValue=0)
        self.scale_attr = attribute.add_attr(host,
                                             longName="scale_",
                                             type="double",
                                             keyable=True,
                                             minValue=0.01,
                                             maxValue=999,
                                             defaultValue=1)
        self.slide_attr = attribute.add_attr(host,
                                             longName="slide",
                                             type="double",
                                             keyable=True,
                                             minValue=0,
                                             maxValue=1,
                                             defaultValue=0.5)
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
                                                         longName="stretch_volume_value" + str(i),
                                                         type="double",
                                                         keyable=False,
                                                         minValue=-1,
                                                         maxValue=0,
                                                         defaultValue=value))
        squash_values = fcurve.get_fcurve_values(squash_volume_fcurve, division=0, inputs=self.volume_inputs)
        for i, value in enumerate(squash_values):
            self.squash_attrs.append(attribute.add_attr(self.root,
                                                        longName="squash_volume_value" + str(i),
                                                        type="double",
                                                        keyable=False,
                                                        minValue=0,
                                                        maxValue=1,
                                                        defaultValue=value))
        if data["support_knee_jnt"] and data["upper_division"] > 1 and data["lower_division"] > 1:
            self.auto_knee_thickness_attr = attribute.add_attr(host,
                                                               longName="auto_knee_thickness",
                                                               type="double",
                                                               keyable=True,
                                                               minValue=0,
                                                               maxValue=2,
                                                               defaultValue=1)
        if data["upper_division"] > 1:
            self.upper_uniform_attr = attribute.add_attr(self.flexible0_ctl,
                                                         longName="uniform",
                                                         type="double",
                                                         defaultValue=1,
                                                         minValue=0,
                                                         maxValue=1,
                                                         keyable=True)
        if data["lower_division"] > 1:
            self.lower_uniform_attr = attribute.add_attr(self.flexible1_ctl,
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

    def operators(self, context):
        super().operators(context)
        data = self.component.data["value"]
        host = self.host

        negate = self.component.negate

        # fk ik blend
        operators.set_fk_ik_blend_matrix(self.blend_nodes,
                                         [self.fk0_ctl, self.fk1_ctl, self.fk2_ctl],
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

        # fk ctl length
        fk0_length = mc.getAttr(self.fk0_length_node + ".tx")
        fk1_length = mc.getAttr(self.fk1_length_node + ".tx")
        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".input1X", fk0_length)
        mc.setAttr(md + ".input1Y", fk1_length)
        mc.connectAttr(self.fk0_length_attr, md + ".input2X")
        mc.connectAttr(self.fk1_length_attr, md + ".input2Y")
        self.fk0_length_attr = md + ".outputX"
        self.fk1_length_attr = md + ".outputY"
        mc.connectAttr(self.fk0_length_attr, self.fk0_length_node + ".tx")
        mc.connectAttr(self.fk1_length_attr, self.fk1_length_node + ".tx")

        pma = mc.createNode("plusMinusAverage")
        mc.connectAttr(self.fk0_length_attr, pma + ".input1D[0]")
        mc.setAttr(pma + ".input1D[1]", mc.getAttr(self.fk0_length_attr) * -1)
        self.fk0_length_attr = pma + ".output1D"
        pma = mc.createNode("plusMinusAverage")
        mc.connectAttr(self.fk1_length_attr, pma + ".input1D[0]")
        mc.setAttr(pma + ".input1D[1]", mc.getAttr(self.fk1_length_attr) * -1)
        self.fk1_length_attr = pma + ".output1D"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(self.fk0_length_attr, md + ".input1X")
        mc.connectAttr(self.fk1_length_attr, md + ".input1Y")
        mc.connectAttr(rev + ".outputX", md + ".input2X")
        mc.connectAttr(rev + ".outputX", md + ".input2Y")
        mc.connectAttr(md + ".outputX", self.fk_blend0_offset + ".tx")
        mc.connectAttr(md + ".outputY", self.fk_blend1_offset + ".tx")

        # pin ctl
        pin_npo = hierarchy.get_parent(self.pin_ctl)
        if mc.controller(pin_npo, query=True):
            pin_npo = hierarchy.get_parent(pin_npo)
        mc.pointConstraint(self.blend_nodes[1], pin_npo)
        cons = mc.orientConstraint([self.blend_nodes[0], self.blend_nodes[1]], pin_npo, maintainOffset=True)[0]
        mc.setAttr(cons + ".interpType", 2)

        # roll
        mc.connectAttr(self.roll_attr, self.ik_ikh + ".twist")

        # armpit roll
        mc.connectAttr(self.armpit_roll_attr, self.upper_start_bind + ".rx")

        # scale, slide, stretch
        operators.ik_2jnt(self.ik_jnts[1],
                          self.ik_jnts[2],
                          self.scale_attr,
                          self.slide_attr,
                          self.stretch_value_attr,
                          self.max_stretch_attr,
                          negate)

        # volume
        pma = mc.createNode("plusMinusAverage")
        orig_upper_length_attr = nurbs.get_length_attr(self.orig_upper_crv, local=False)
        orig_lower_length_attr = nurbs.get_length_attr(self.orig_lower_crv, local=False)
        mc.connectAttr(orig_upper_length_attr, pma + ".input1D[0]")
        mc.connectAttr(orig_lower_length_attr, pma + ".input1D[1]")
        orig_distance_attr = pma + ".output1D"

        pma = mc.createNode("plusMinusAverage")
        mc.connectAttr(nurbs.get_length_attr(self.deform_upper_crv), pma + ".input1D[0]")
        mc.connectAttr(nurbs.get_length_attr(self.deform_lower_crv), pma + ".input1D[1]")

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(orig_upper_length_attr, md + ".input1X")
        mc.connectAttr(orig_lower_length_attr, md + ".input1Y")
        mc.setAttr(md + ".input2X", -1)
        mc.setAttr(md + ".input2Y", -1)

        pma1 = mc.createNode("plusMinusAverage")
        mc.connectAttr(md + ".outputX", pma1 + ".input1D[0]")
        mc.connectAttr(md + ".outputY", pma1 + ".input1D[1]")
        mc.connectAttr(pma1 + ".output1D", pma + ".input1D[2]")

        delta_distance_attr = pma + ".output1D"
        operators.volume(orig_distance_attr,
                         delta_distance_attr,
                         self.squash_attrs,
                         self.stretch_attrs,
                         self.volume_attr,
                         self.leg_output_nodes[:-1])

        # auto knee thickness
        if data["support_knee_jnt"] and data["upper_division"] > 1 and data["lower_division"] > 1:
            distance1 = mc.getAttr(self.ik_jnts[1] + ".tx")
            distance2 = mc.getAttr(self.ik_jnts[2] + ".tx")
            if distance1 < 0:
                distance1 *= -1
            if distance2 < 0:
                distance2 *= -1
            length = distance1 + distance2
            md = mc.createNode("multiplyDivide")
            mc.connectAttr(self.auto_knee_thickness_attr, md + ".input1X")
            mc.setDrivenKeyframe(md + ".input2X",
                                 currentDriver=self.blend_nodes[1] + ".rz",
                                 driverValue=0,
                                 value=0,
                                 inTangentType="linear",
                                 outTangentType="linear")
            mc.setDrivenKeyframe(md + ".input2X",
                                 currentDriver=self.blend_nodes[1] + ".rz",
                                 driverValue=-180,
                                 value=length / float(distance2) / 5,
                                 inTangentType="linear",
                                 outTangentType="linear")

            npo = hierarchy.get_parent(self.thickness_knee_ctl)
            mc.connectAttr(md + ".outputX", npo + ".tx")

        # space switch
        if data["ik_space_switch_array"]:
            source_ctls = self.find_ctls(context, data["ik_space_switch_array"])
            self.ik_ctl_cons = operators.space_switch(source_ctls, self.ik_ctl, host, attr_name="ik_space_switch")
            self.ik_ctl_script_node = callback.space_switch(source_ctls,
                                                            self.ik_ctl,
                                                            host,
                                                            switch_attr_name="ik_space_switch")
            context["callbacks"].append(self.ik_ctl_script_node)
        source_ctls = [self.look_at_jnts[0]]
        if data["pv_space_switch_array"]:
            source_ctls += self.find_ctls(context, data["pv_space_switch_array"])
        self.pv_ctl_cons = operators.space_switch(source_ctls, self.pole_vec_ctl, host, attr_name="pv_space_switch")
        self.pv_ctl_script_node = callback.space_switch(source_ctls,
                                                        self.pole_vec_ctl,
                                                        host,
                                                        switch_attr_name="pv_space_switch")
        context["callbacks"].append(self.pv_ctl_script_node)
        if data["pin_space_switch_array"]:
            selection_list = om2.MSelectionList()
            selection_list.add(self.pin_ctl)
            dag_path = selection_list.getDagPath(0)
            controller.add_npo(hierarchy.get_parent(self.pin_ctl), name=self.generate_name("pin", "spaceSwitch", "ctl"))
            self.pin_ctl = dag_path.fullPathName()
            source_ctls = self.find_ctls(context, data["pin_space_switch_array"])
            operators.space_switch(source_ctls, self.pin_ctl, host, attr_name="pin_space_switch")
            script_node = callback.space_switch(source_ctls, self.pin_ctl, host, switch_attr_name="pin_space_switch")
            context["callbacks"].append(script_node)

    def connections(self, context):
        super().connections(context)

        if "leg_2jnt_01" not in context:
            context["leg_2jnt_01"] = {}
        context["leg_2jnt_01"][str(self.identifier)] = [self.ik_local_loc,
                                                        self.ik_ikh,
                                                        self.refs[-1],
                                                        self.fk_ik_attr]
