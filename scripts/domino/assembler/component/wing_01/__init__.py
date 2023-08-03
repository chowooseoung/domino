# domino
from domino.lib import matrix, vector, hierarchy, attribute
from domino.lib.rigging import joint, nurbs, operators
from domino.lib.animation import fcurve
from domino import assembler

# built-ins
import os
import uuid

# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2
from maya.internal.nodes.proximitywrap import node_interface as ifc


class Author:
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "wing"
    side = "C"
    index = 0
    description = ("새의 날개입니다. feather_01과 연결 될 수 있습니다. 각 쌍의 curve는 깃털이 놓일 mesh를 생성하는데 사용됩니다. "
                   "깃털의 구역은 https://youtu.be/GFCgwglikcY 를 참고해주세요.")


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset_pole_vec": {"type": "double", "minValue": 0},
        "offset_pole_vec_matrix": {"type": "matrix"},
        "stretch_volume_fcurve": {"type": "double"},
        "squash_volume_fcurve": {"type": "double"},
        "primary_curve1": {"type": "nurbsCurve"},
        "primary_curve2": {"type": "nurbsCurve"},
        "primary_coverts_curve1": {"type": "nurbsCurve"},
        "primary_coverts_curve2": {"type": "nurbsCurve"},
        "primary_under_coverts_curve1": {"type": "nurbsCurve"},
        "primary_under_coverts_curve2": {"type": "nurbsCurve"},
        "secondary_curve1": {"type": "nurbsCurve"},
        "secondary_curve2": {"type": "nurbsCurve"},
        "secondary_coverts_curve1": {"type": "nurbsCurve"},
        "secondary_coverts_curve2": {"type": "nurbsCurve"},
        "secondary_under_coverts_curve1": {"type": "nurbsCurve"},
        "secondary_under_coverts_curve2": {"type": "nurbsCurve"},
        "tertiary_curve1": {"type": "nurbsCurve"},
        "tertiary_curve2": {"type": "nurbsCurve"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))
        m2 = matrix.set_matrix_translate(m, (1.5, 0, 0.5))
        m3 = matrix.set_matrix_translate(m, (3, 0, 0))
        m4 = matrix.set_matrix_translate(m, (3.3, 0, 0.05))
        m5 = matrix.set_matrix_translate(m, (4, 0, 0.3))
        m6 = matrix.set_matrix_translate(m, (5, 0, 0.7))

        # guideA
        m7 = matrix.set_matrix_translate(m, (0, 0, 1))
        m8 = matrix.set_matrix_translate(m, (0, 0, 2))
        m9 = matrix.set_matrix_translate(m, (0, 0, 3))
        m10 = matrix.set_matrix_translate(m, (0, 0, 4))

        # guideB
        m11 = matrix.set_matrix_translate(m, (1.5, 0, 1))
        m12 = matrix.set_matrix_translate(m, (1.5, 0, 2))
        m13 = matrix.set_matrix_translate(m, (1.5, 0, 3))
        m14 = matrix.set_matrix_translate(m, (1.5, 0, 4))

        # guideC
        m15 = matrix.set_matrix_translate(m, (3, 0, 1))
        m16 = matrix.set_matrix_translate(m, (3, 0, 2))
        m17 = matrix.set_matrix_translate(m, (3, 0, 3))
        m18 = matrix.set_matrix_translate(m, (3, 0, 4))

        # guideD
        m19 = matrix.set_matrix_translate(m, (4, 0, 1))
        m20 = matrix.set_matrix_translate(m, (4, 0, 2))
        m21 = matrix.set_matrix_translate(m, (4, 0, 3))
        m22 = matrix.set_matrix_translate(m, (4, 0, 4))

        # guideE
        m23 = matrix.set_matrix_translate(m, (5, 0, 1))
        m24 = matrix.set_matrix_translate(m, (5, 0, 2))
        m25 = matrix.set_matrix_translate(m, (5, 0, 3))
        m26 = matrix.set_matrix_translate(m, (5, 0, 4))
        return m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, \
            m23, m24, m25, m26

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "offset_pole_vec": 5,
        "offset_pole_vec_matrix": list(om2.MMatrix()),
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
    common_preset["nurbs_curve"].update({
        "primary_curve1": None,
        "primary_curve2": None,
        "primary_coverts_curve1": None,
        "primary_coverts_curve2": None,
        "primary_under_coverts_curve1": None,
        "primary_under_coverts_curve2": None,
        "secondary_curve1": None,
        "secondary_curve2": None,
        "secondary_coverts_curve1": None,
        "secondary_coverts_curve2": None,
        "secondary_under_coverts_curve1": None,
        "secondary_under_coverts_curve2": None,
        "tertiary_curve1": None,
        "tertiary_curve2": None,
    })
    return common_preset


def guide_recipe():
    recipe = {
        "root": "humerus",
        "position": [
            (0, "elbow"),
            (1, "carpus"),
            (2, "metacarpus"),
            (3, "phalanges"),
            (4, "tip"),
            (0, "guideA0"),
            (6, "guideA1"),
            (7, "guideA2"),
            (8, "guideA3"),
            (1, "guideB0"),
            (10, "guideB1"),
            (11, "guideB2"),
            (12, "guideB3"),
            (2, "guideC0"),
            (14, "guideC1"),
            (15, "guideC2"),
            (16, "guideC3"),
            (4, "guideD0"),
            (18, "guideD1"),
            (19, "guideD2"),
            (20, "guideD3"),
            (5, "guideE0"),
            (22, "guideE1"),
            (23, "guideE2"),
            (24, "guideE3"),
        ],
        "pole_vec": ((0, 1, 2), "poleVec"),  # source node indexes, extension
        "display_curve": [
            ((0, 1, 2, 3, 4, 5), "dpCrv"),
            ((0, 6, 7, 8, 9), "dpGuide0Crv"),
            ((1, 10, 11, 12, 13), "dpGuide2Crv"),
            ((2, 14, 15, 16, 17), "dpGuide4Crv"),
            ((4, 18, 19, 20, 21), "dpGuide6Crv"),
            ((5, 22, 23, 24, 25), "dpGuide8Crv"),
        ],
        "lock_attrs": [
            (),
        ]
    }
    for i in range(len(recipe["position"])):
        recipe["lock_attrs"].append(("ty", "rx", "rz"))
    return recipe


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]
        nurbs_curve_data = self.component.data["nurbs_curve"]

        matrices = [om2.MMatrix(m) for m in data["anchors"][0:6]]
        guide_a_matrices = [om2.MMatrix(m) for m in data["anchors"][6:10]]
        guide_b_matrices = [om2.MMatrix(m) for m in data["anchors"][10:14]]
        guide_c_matrices = [om2.MMatrix(m) for m in data["anchors"][14:18]]
        guide_d_matrices = [om2.MMatrix(m) for m in data["anchors"][18:22]]
        guide_e_matrices = [om2.MMatrix(m) for m in data["anchors"][22:]]
        guide7_matrices = [om2.MMatrix(m) for m in data["anchors"][34:38]]
        guide5_matrices = [om2.MMatrix(m) for m in data["anchors"][26:30]]
        guide3_matrices = [om2.MMatrix(m) for m in data["anchors"][18:22]]
        guide1_matrices = [om2.MMatrix(m) for m in data["anchors"][10:14]]

        positions = [om2.MVector(list(x)[12:-1]) for x in matrices]
        guide_a_positions = [positions[0]] + [om2.MVector(list(m)[12:-1]) for m in guide_a_matrices]
        guide_b_positions = [positions[1]] + [om2.MVector(list(m)[12:-1]) for m in guide_b_matrices]
        guide_c_positions = [positions[2]] + [om2.MVector(list(m)[12:-1]) for m in guide_c_matrices]
        guide_d_positions = [positions[4]] + [om2.MVector(list(m)[12:-1]) for m in guide_d_matrices]
        guide_e_positions = [positions[5]] + [om2.MVector(list(m)[12:-1]) for m in guide_e_matrices]
        guide7_positions = [(positions[4] + positions[5]) / 2] + [om2.MVector(list(m)[12:-1]) for m in guide7_matrices]
        guide5_positions = [(positions[2] + positions[4]) / 2] + [om2.MVector(list(m)[12:-1]) for m in guide5_matrices]
        guide3_positions = [(positions[1] + positions[2]) / 2] + [om2.MVector(list(m)[12:-1]) for m in guide3_matrices]
        guide1_positions = [(positions[0] + positions[1]) / 2] + [om2.MVector(list(m)[12:-1]) for m in guide1_matrices]

        upper_jnt_v_values = [0]
        lower_jnt_v_values = [0, 1]

        normal = vector.get_plane_normal(*positions[:3])
        negate = self.component.negate

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
                                                     parent=self.fk0_loc,
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
        offset = ((positions[3] - positions[2]) / 2.0).length()
        po = offset * -1 if negate else offset
        self.fk2_ctl, self.fk2_loc = self.create_ctl(context=context,
                                                     parent=self.fk1_loc,
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
        ik_m = matrix.set_matrix_translate(om2.MMatrix(), positions[2])
        if negate:
            ik_m = matrix.set_matrix_translate(ik_m, positions[2])
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context,
                                                   parent=None,
                                                   name=self.generate_name("ik", "", "ctl"),
                                                   parent_ctl=None,
                                                   attrs=["tx", "ty", "tz",
                                                          "rx", "ry", "rz",
                                                          "sx", "sy", "sz"],
                                                   m=ik_m,
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
        self.ik_match_source.append(matrix.transform(self.fk2_loc, self.generate_name("carpus", "match", "ctl"), ik_m))

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

        m = om2.MMatrix()
        # ik jnts
        self.fk_match_source = self.ik_jnts = joint.add_chain_joint(root,
                                                                    self.generate_name("ik%s", "", "ctl"),
                                                                    positions[:3],
                                                                    normal,
                                                                    last_orient=fk2_m,
                                                                    negate=negate)

        self.ik_ikh = joint.ikh(self.ik_local_loc,
                                self.generate_name("RP", "ikh", "ctl"),
                                self.ik_jnts,
                                pole_vector=self.pole_vec_loc)
        mc.orientConstraint(self.ik_ikh, self.ik_jnts[-1], maintainOffset=True)
        mc.scaleConstraint(self.ik_ikh, self.ik_jnts[-1], maintainOffset=True)

        # elbow - pole vector display curve
        self.display_curve = nurbs.create(parent=root,
                                          name=self.generate_name("display", "crv", "ctl"),
                                          degree=1,
                                          positions=((0, 0, 0), (0, 0, 0)),
                                          m=m,
                                          inherits=False,
                                          display_type=2)
        nurbs.constraint(self.display_curve, [self.ik_jnts[1], self.pole_vec_loc])

        # blend objs
        self.blend_nodes = []
        parent = root
        for i, jnt in enumerate(self.ik_jnts):
            parent = matrix.transform(parent=parent,
                                      name=self.generate_name("fkik" + str(i), "blend", "ctl"),
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

        self.orig_upper_crv = nurbs.create(root,
                                           self.generate_name("origUpper", "crv", "ctl"),
                                           1,
                                           positions[:2],
                                           m,
                                           vis=False,
                                           display_type=1)
        self.deform_upper_crv = nurbs.create(root,
                                             self.generate_name("deformUpper", "crv", "ctl"),
                                             1,
                                             positions[:2],
                                             m,
                                             vis=False,
                                             display_type=1)
        mc.setAttr(self.deform_upper_crv + ".inheritsTransform", 0)
        nurbs.constraint(self.deform_upper_crv, self.blend_nodes[:2])
        self.orig_lower_crv = nurbs.create(root,
                                           self.generate_name("origLower", "crv", "ctl"),
                                           1,
                                           positions[1:3],
                                           m,
                                           vis=False,
                                           display_type=1)
        self.deform_lower_crv = nurbs.create(root,
                                             self.generate_name("deformLower", "crv", "ctl"),
                                             1,
                                             positions[1:3],
                                             m,
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
                                                         "ro": (90, 0, -315) if negate else (90, 0, 225)
                                                     },
                                                     mirror_ctl_name=self.generate_name("pin", "", "ctl", True))

        # lookAt jnts
        self.look_at_jnts = joint.add_chain_joint(root,
                                                  self.generate_name("lookAt%s", "", "ctl"),
                                                  [positions[0], positions[2]],
                                                  normal,
                                                  negate=negate)
        self.stretch_value_jnt = joint.add_joint(self.look_at_jnts[0],
                                                 self.generate_name("stretch", "", "ctl"),
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
                                                       self.generate_name("upperFixSC%s", "", "ctl"),
                                                       positions[:2],
                                                       normal,
                                                       negate=negate)
        mc.connectAttr(self.blend_nodes[0] + ".t", self.upper_fix_sc_jnts[0] + ".t")
        self.upper_rot_sc_jnts = joint.add_chain_joint(self.upper_sc_offset,
                                                       self.generate_name("upperRotSC%s", "", "ctl"),
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
                                                self.generate_name("upperStart", "bind", "ctl"),
                                                matrix.get_matrix(self.upper_fix_sc_jnts[0], world_space=True),
                                                vis=False)
        self.upper_end_bind = joint.add_joint(self.upper_rot_sc_jnts[1],
                                              self.generate_name("upperEnd", "bind", "ctl"),
                                              matrix.get_matrix(self.upper_rot_sc_jnts[1], world_space=True),
                                              vis=False)
        mc.pointConstraint(self.pin_loc, self.upper_end_bind)
        mc.connectAttr(self.pin_ctl + ".rx", self.upper_end_bind + ".rx")

        self.lower_fix_sc_jnts = joint.add_chain_joint(root,
                                                       self.generate_name("lowerFixSC%s", "", "ctl"),
                                                       positions[1:3],
                                                       normal,
                                                       negate=negate)
        mc.pointConstraint(self.pin_loc, self.lower_fix_sc_jnts[0])

        self.lower_fix_sc_ikh = joint.ikh(root,
                                          self.generate_name("lowerFixSC", "ikh", "ctl"),
                                          self.lower_fix_sc_jnts,
                                          "ikSCsolver")
        mc.pointConstraint(self.blend_nodes[-1], self.lower_fix_sc_ikh)
        mc.orientConstraint(self.upper_end_bind, self.lower_fix_sc_ikh, maintainOffset=True)

        self.lower_rot_sc_jnts = joint.add_chain_joint(root,
                                                       self.generate_name("lowerRotSC%s", "", "ctl"),
                                                       positions[1:3],
                                                       normal,
                                                       negate=negate)
        mc.pointConstraint(self.pin_loc, self.lower_rot_sc_jnts[0])

        self.lower_rot_sc_ikh = joint.ikh(root,
                                          self.generate_name("lowerRotSC", "ikh", "ctl"),
                                          self.lower_rot_sc_jnts,
                                          "ikSCsolver")
        mc.pointConstraint(self.blend_nodes[-1], self.lower_rot_sc_ikh)
        mc.orientConstraint(self.blend_nodes[-1], self.lower_rot_sc_ikh, maintainOffset=True)

        self.lower_start_bind = joint.add_joint(self.lower_fix_sc_jnts[0],
                                                self.generate_name("lowerStart", "bind", "ctl"),
                                                matrix.get_matrix(self.lower_fix_sc_jnts[0], world_space=True),
                                                vis=False)
        self.lower_end_bind = joint.add_joint(self.lower_rot_sc_jnts[1],
                                              self.generate_name("lowerEnd", "bind", "ctl"),
                                              matrix.get_matrix(self.lower_rot_sc_jnts[1], world_space=True),
                                              vis=False)
        mc.pointConstraint(self.blend_nodes[-1], self.lower_end_bind)

        # ribbon bind jnts
        upper_bind_jnts = [self.upper_start_bind, self.upper_end_bind]
        lower_bind_jnts = [self.lower_start_bind, self.lower_end_bind]

        # flexible ctl
        upper_division = 3
        uniform_value = 1.0 / upper_division
        upper_jnt_v_values.extend([uniform_value * i for i in range(1, upper_division)])

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
                                                   self.generate_name("upperMid", "bind", "ctl"),
                                                   m,
                                                   vis=False)
        upper_bind_jnts.append(self.upper_flexible_bind)
        flexible0_npo = hierarchy.get_parent(self.flexible0_ctl)
        mc.pointConstraint([self.upper_start_bind, self.upper_end_bind], flexible0_npo)
        cons = mc.orientConstraint([self.upper_start_bind, self.upper_end_bind], flexible0_npo)[0]
        mc.setAttr(cons + ".interpType", 2)

        lower_division = 3
        uniform_value = 1.0 / lower_division
        lower_jnt_v_values.extend([uniform_value * i for i in range(1, lower_division)])

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
                                                   self.generate_name("lowerMid", "bind", "ctl"),
                                                   m,
                                                   vis=False)
        lower_bind_jnts.append(self.lower_flexible_bind)
        flexible1_npo = hierarchy.get_parent(self.flexible1_ctl)
        mc.pointConstraint([self.lower_start_bind, self.lower_end_bind], flexible1_npo)
        cons = mc.orientConstraint([self.lower_start_bind, self.lower_end_bind], flexible1_npo)[0]
        mc.setAttr(cons + ".interpType", 2)

        # ribbon
        self.arm_output_nodes = []
        m = matrix.get_matrix(root, world_space=True)
        for i in range(len(upper_jnt_v_values)):
            self.arm_output_nodes.append(matrix.transform(root, self.generate_name(str(i), "space", "ctl"), m))
        for i in range(len(lower_jnt_v_values) - 1):
            self.arm_output_nodes.append(matrix.transform(root,
                                                          self.generate_name(str(i + len(upper_jnt_v_values)),
                                                                             "space",
                                                                             "ctl"),
                                                          m))
        node = matrix.transform(root, self.generate_name(str(len(self.arm_output_nodes)), "space", "ctl"), fk2_m)
        self.arm_output_nodes.append(node)

        # upper
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
                              self.arm_output_nodes[:len(lower_jnt_v_values) * -1],
                              negate=negate)
        # upper last aim fix
        pick_m = mc.listConnections(self.arm_output_nodes[len(upper_jnt_v_values) - 1] + ".offsetParentMatrix",
                                    source=True,
                                    destination=False)[0]
        aim_m = mc.listConnections(pick_m + ".inputMatrix", source=True, destination=False)[0]
        mc.setAttr(aim_m + ".primaryInputAxisX", -1 if negate else 1)
        mc.connectAttr(self.arm_output_nodes[len(upper_jnt_v_values)] + ".offsetParentMatrix",
                       aim_m + ".primaryTargetMatrix",
                       force=True)

        # lower
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
                              self.arm_output_nodes[len(upper_jnt_v_values):],
                              negate=negate)

        # last-1 aim reverse
        pick_m = mc.listConnections(self.arm_output_nodes[-2] + ".offsetParentMatrix",
                                    source=True,
                                    destination=False)[0]
        aim_m = mc.listConnections(pick_m + ".inputMatrix", source=True, destination=False)[0]
        mc.setAttr(aim_m + ".primaryInputAxisX", -1 if negate else 1)
        mc.connectAttr(self.arm_output_nodes[-1] + ".matrix", aim_m + ".primaryTargetMatrix", force=True)

        mc.parentConstraint(self.blend_nodes[-1], node, maintainOffset=False)
        mc.scaleConstraint(self.blend_nodes[-1], node, maintainOffset=False)

        self.volume_inputs = upper_jnt_v_values + [x + 1 for x in lower_jnt_v_values]
        self.volume_inputs = sorted([x / 2.0 for x in self.volume_inputs])

        fk3_m = matrix.get_look_at_matrix(positions[3], positions[4], normal, "xz", negate)
        offset = ((positions[4] - positions[3]) / 2.0).length()
        po = offset * -1 if negate else offset
        self.fk3_ctl, self.fk3_loc = self.create_ctl(context=context,
                                                     parent=self.arm_output_nodes[-1],
                                                     name=self.generate_name("fk3", "", "ctl"),
                                                     parent_ctl=self.fk2_ctl,
                                                     attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz",
                                                            "sx", "sy", "sz"],
                                                     m=fk3_m,
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
                                                     mirror_ctl_name=self.generate_name("fk3", "", "ctl", True))

        fk4_m = matrix.get_look_at_matrix(positions[4], positions[5], normal, "xz", negate)
        offset = ((positions[5] - positions[4]) / 2.0).length()
        po = offset * -1 if negate else offset
        self.fk4_ctl, self.fk4_loc = self.create_ctl(context=context,
                                                     parent=self.fk3_loc,
                                                     name=self.generate_name("fk4", "", "ctl"),
                                                     parent_ctl=self.fk3_ctl,
                                                     attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz",
                                                            "sx", "sy", "sz"],
                                                     m=fk4_m,
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
                                                     mirror_ctl_name=self.generate_name("fk4", "", "ctl", True))
        xxx_curve_grp = mc.createNode("transform", parent=context["xxx"], name=self.generate_name("crv", "grp", "ctl"))
        xxx_mesh_grp = mc.createNode("transform", parent=context["xxx"], name=self.generate_name("mesh", "grp", "ctl"))
        xxx_split_output_grp = mc.createNode("transform",
                                             parent=root,
                                             name=self.generate_name("splitOutput", "grp", "ctl"))
        xxx_split_skin_grp = mc.createNode("transform",
                                           parent=xxx_mesh_grp,
                                           name=self.generate_name("splitSkin", "grp", "ctl"))
        mc.hide(xxx_split_skin_grp)

        # create mesh
        self.primary1_crv = nurbs.build(curve_data=nurbs_curve_data["primary_curve1"]["0"],
                                        name=self.generate_name("primary1", "crv", "ctl"),
                                        match=True,
                                        parent=xxx_curve_grp)
        mc.connectAttr(self.primary1_crv + ".worldSpace[0]", self.root + ".primary_curve1")
        self.primary2_crv = nurbs.build(curve_data=nurbs_curve_data["primary_curve2"]["0"],
                                        name=self.generate_name("primary2", "crv", "ctl"),
                                        match=True,
                                        parent=xxx_curve_grp)
        mc.connectAttr(self.primary2_crv + ".worldSpace[0]", self.root + ".primary_curve2")
        self.primary_output_mesh = nurbs.loft(xxx_split_output_grp,
                                              self.primary1_crv,
                                              self.primary2_crv,
                                              self.generate_name("primary", "mesh", "ctl"),
                                              100)
        self.primary_skin_mesh = nurbs.loft(xxx_split_skin_grp,
                                            self.primary1_crv,
                                            self.primary2_crv,
                                            self.generate_name("primarySkin", "mesh", "ctl"),
                                            100)
        self.primary_coverts1_crv = nurbs.build(curve_data=nurbs_curve_data["primary_coverts_curve1"]["0"],
                                                name=self.generate_name("primaryCoverts1", "crv", "ctl"),
                                                match=True,
                                                parent=xxx_curve_grp)
        mc.connectAttr(self.primary_coverts1_crv + ".worldSpace[0]", self.root + ".primary_coverts_curve1")
        self.primary_coverts2_crv = nurbs.build(curve_data=nurbs_curve_data["primary_coverts_curve2"]["0"],
                                                name=self.generate_name("primaryCoverts2", "crv", "ctl"),
                                                match=True,
                                                parent=xxx_curve_grp)
        mc.connectAttr(self.primary_coverts2_crv + ".worldSpace[0]", self.root + ".primary_coverts_curve2")
        self.primary_converts_output_mesh = nurbs.loft(xxx_split_output_grp,
                                                       self.primary_coverts1_crv,
                                                       self.primary_coverts2_crv,
                                                       self.generate_name("primaryCoverts", "mesh", "ctl"),
                                                       100)
        self.primary_converts_skin_mesh = nurbs.loft(xxx_split_skin_grp,
                                                     self.primary_coverts1_crv,
                                                     self.primary_coverts2_crv,
                                                     self.generate_name("primaryCovertsSkin", "mesh", "ctl"),
                                                     100)
        self.primary_under1_crv = nurbs.build(curve_data=nurbs_curve_data["primary_under_coverts_curve1"]["0"],
                                              name=self.generate_name("primaryUnder1", "crv", "ctl"),
                                              match=True,
                                              parent=xxx_curve_grp)
        mc.connectAttr(self.primary_under1_crv + ".worldSpace[0]", self.root + ".primary_under_coverts_curve1")
        self.primary_under2_crv = nurbs.build(curve_data=nurbs_curve_data["primary_under_coverts_curve2"]["0"],
                                              name=self.generate_name("primaryUnder2", "crv", "ctl"),
                                              match=True,
                                              parent=xxx_curve_grp)
        mc.connectAttr(self.primary_under2_crv + ".worldSpace[0]", self.root + ".primary_under_coverts_curve2")
        self.primary_under_output_mesh = nurbs.loft(xxx_split_output_grp,
                                                    self.primary_under1_crv,
                                                    self.primary_under2_crv,
                                                    self.generate_name("primaryUnder", "mesh", "ctl"),
                                                    100)
        self.primary_under_skin_mesh = nurbs.loft(xxx_split_skin_grp,
                                                  self.primary_under1_crv,
                                                  self.primary_under2_crv,
                                                  self.generate_name("primaryUnderSkin", "mesh", "ctl"),
                                                  100)
        self.secondary1_crv = nurbs.build(curve_data=nurbs_curve_data["secondary_curve1"]["0"],
                                          name=self.generate_name("secondary1", "crv", "ctl"),
                                          match=True,
                                          parent=xxx_curve_grp)
        mc.connectAttr(self.secondary1_crv + ".worldSpace[0]", self.root + ".secondary_curve1")
        self.secondary2_crv = nurbs.build(curve_data=nurbs_curve_data["secondary_curve2"]["0"],
                                          name=self.generate_name("secondary2", "crv", "ctl"),
                                          match=True,
                                          parent=xxx_curve_grp)
        mc.connectAttr(self.secondary2_crv + ".worldSpace[0]", self.root + ".secondary_curve2")
        self.secondary_output_mesh = nurbs.loft(xxx_split_output_grp,
                                                self.secondary1_crv,
                                                self.secondary2_crv,
                                                self.generate_name("secondary", "mesh", "ctl"),
                                                100)
        self.secondary_skin_mesh = nurbs.loft(xxx_split_skin_grp,
                                              self.secondary1_crv,
                                              self.secondary2_crv,
                                              self.generate_name("secondarySkin", "mesh", "ctl"),
                                              100)
        self.secondary_coverts1_crv = nurbs.build(curve_data=nurbs_curve_data["secondary_coverts_curve1"]["0"],
                                                  name=self.generate_name("secondaryCoverts1", "crv", "ctl"),
                                                  match=True,
                                                  parent=xxx_curve_grp)
        mc.connectAttr(self.secondary_coverts1_crv + ".worldSpace[0]", self.root + ".secondary_coverts_curve1")
        self.secondary_coverts2_crv = nurbs.build(curve_data=nurbs_curve_data["secondary_coverts_curve2"]["0"],
                                                  name=self.generate_name("secondaryCoverts2", "crv", "ctl"),
                                                  match=True,
                                                  parent=xxx_curve_grp)
        mc.connectAttr(self.secondary_coverts2_crv + ".worldSpace[0]", self.root + ".secondary_coverts_curve2")
        self.secondary_converts_output_mesh = nurbs.loft(xxx_split_output_grp,
                                                         self.secondary_coverts1_crv,
                                                         self.secondary_coverts2_crv,
                                                         self.generate_name("secondaryCoverts", "mesh", "ctl"),
                                                         100)
        self.secondary_converts_skin_mesh = nurbs.loft(xxx_split_skin_grp,
                                                       self.secondary_coverts1_crv,
                                                       self.secondary_coverts2_crv,
                                                       self.generate_name("secondaryCovertsSkin", "mesh", "ctl"),
                                                       100)
        self.secondary_under1_crv = nurbs.build(curve_data=nurbs_curve_data["secondary_under_coverts_curve1"]["0"],
                                                name=self.generate_name("secondaryUnder1", "crv", "ctl"),
                                                match=True,
                                                parent=xxx_curve_grp)
        mc.connectAttr(self.secondary_under1_crv + ".worldSpace[0]", self.root + ".secondary_under_coverts_curve1")
        self.secondary_under2_crv = nurbs.build(curve_data=nurbs_curve_data["secondary_under_coverts_curve2"]["0"],
                                                name=self.generate_name("secondaryUnder2", "crv", "ctl"),
                                                match=True,
                                                parent=xxx_curve_grp)
        mc.connectAttr(self.secondary_under2_crv + ".worldSpace[0]", self.root + ".secondary_under_coverts_curve2")
        self.secondary_under_output_mesh = nurbs.loft(xxx_split_output_grp,
                                                      self.secondary_under1_crv,
                                                      self.secondary_under2_crv,
                                                      self.generate_name("secondaryUnder", "mesh", "ctl"),
                                                      100)
        self.secondary_under_skin_mesh = nurbs.loft(xxx_split_skin_grp,
                                                    self.secondary_under1_crv,
                                                    self.secondary_under2_crv,
                                                    self.generate_name("secondaryUnderSkin", "mesh", "ctl"),
                                                    100)
        self.tertiary1_crv = nurbs.build(curve_data=nurbs_curve_data["tertiary_curve1"]["0"],
                                         name=self.generate_name("tertiary1", "crv", "ctl"),
                                         match=True,
                                         parent=xxx_curve_grp)
        mc.connectAttr(self.tertiary1_crv + ".worldSpace[0]", self.root + ".tertiary_curve1")
        self.tertiary2_crv = nurbs.build(curve_data=nurbs_curve_data["tertiary_curve2"]["0"],
                                         name=self.generate_name("tertiary2", "crv", "ctl"),
                                         match=True,
                                         parent=xxx_curve_grp)
        mc.connectAttr(self.tertiary2_crv + ".worldSpace[0]", self.root + ".tertiary_curve2")
        self.tertiary_output_mesh = nurbs.loft(xxx_split_output_grp,
                                               self.tertiary1_crv,
                                               self.tertiary2_crv,
                                               self.generate_name("tertiary", "mesh", "ctl"),
                                               100)
        self.tertiary_skin_mesh = nurbs.loft(xxx_split_skin_grp,
                                             self.tertiary1_crv,
                                             self.tertiary2_crv,
                                             self.generate_name("tertiarySkin", "mesh", "ctl"),
                                             100)
        mc.hide([self.primary1_crv,
                 self.primary2_crv,
                 self.primary_coverts1_crv,
                 self.primary_coverts2_crv,
                 self.primary_under1_crv,
                 self.primary_under2_crv,
                 self.secondary1_crv,
                 self.secondary2_crv,
                 self.secondary_coverts1_crv,
                 self.secondary_coverts2_crv,
                 self.secondary_under1_crv,
                 self.secondary_under2_crv,
                 self.tertiary1_crv,
                 self.tertiary2_crv])
        self.split_meshes = [self.primary_output_mesh,
                             self.primary_converts_output_mesh,
                             self.primary_under_output_mesh,
                             self.secondary_output_mesh,
                             self.secondary_converts_output_mesh,
                             self.secondary_under_output_mesh,
                             self.tertiary_output_mesh]
        if not negate:
            for grp in [xxx_split_output_grp, xxx_split_skin_grp]:
                for child in mc.listRelatives(grp, children=True):
                    mc.polyNormal(child, normalMode=0, userNormalMode=0, ch=0)

        dup_meshes = []
        indexes = []
        for mesh in self.split_meshes:
            dup_meshes.append(mc.duplicate(mesh, name=str(uuid.uuid4()))[0])
            for i in range(len(self.split_meshes)):
                mc.setAttr(mesh + ".componentTags[{0}].componentTagName".format(i),
                           self.identifier + "_{0}".format(i),
                           type="string")
                if mesh == self.split_meshes[i]:
                    mc.setAttr(mesh + ".componentTags[{0}].componentTagContents".format(i),
                               1,
                               "vtx[*]",
                               type="componentList")
            indexes.append(mc.polyEvaluate(mesh, vertex=True))

        mc.blendShape(xxx_split_skin_grp,
                      xxx_split_output_grp,
                      name=self.generate_name("splitMesh", "bs", "ctl"),
                      weight=(0, 1))

        self.combine_mesh = mc.polyUnite(dup_meshes,
                                         constructionHistory=False,
                                         name=self.generate_name("combine", "mesh", "ctl"))[0]
        self.combine_mesh = mc.parent(self.combine_mesh, xxx_mesh_grp)[0]
        previous_index = 0
        for i, mesh in enumerate(self.split_meshes):
            mc.setAttr(self.combine_mesh + ".componentTags[{0}].componentTagName".format(i),
                       self.identifier + "_{0}".format(i),
                       type="string")
            mc.setAttr(self.combine_mesh + ".componentTags[{0}].componentTagContents".format(i),
                       1,
                       "vtx[{0}:{1}]".format(previous_index, previous_index + indexes[i] - 1),
                       type="componentList")
            previous_index += indexes[i]

        self.combine_skin_mesh = mc.polyPlane(name=self.generate_name("combineSkin", "mesh", "ctl"),
                                              constructionHistory=0,
                                              subdivisionsHeight=4,
                                              subdivisionsWidth=4)[0]
        self.combine_skin_mesh = mc.parent(self.combine_skin_mesh, xxx_mesh_grp)[0]
        for i, _pos in enumerate([guide_a_positions,
                                  guide_b_positions,
                                  guide_c_positions,
                                  guide_d_positions,
                                  guide_e_positions]):
            for j in range(5):
                index = i + j * 5
                mc.xform(self.combine_skin_mesh + ".vtx[{0}]".format(index),
                         translation=_pos[4 - j],
                         worldSpace=True)
        edges_indexes = []
        edges_indexes.append([0, 2, 4, 6])
        edges_indexes.append([8, 17, 26, 35, 47])
        edges_indexes.append([36, 37, 38, 39, 56])
        edges_indexes.append([1, 10, 19, 28, 40, 60])
        for indexes in edges_indexes:
            edges = []
            for i in indexes:
                edges.append(self.combine_skin_mesh + ".e[{0}]".format(i))
            mc.polyExtrudeEdge(edges,
                               constructionHistory=0,
                               keepFacesTogether=1,
                               offset=2)

        # guide aim
        self.fix_aim0_node = matrix.transform(parent=root,
                                              name=self.generate_name("fixAim0", "pos", "ctl"),
                                              m=matrix.set_matrix_translate(m, guide_a_positions[-1]))
        self.move_aim0_node = matrix.transform(parent=self.arm_output_nodes[0],
                                               name=self.generate_name("moveAim0", "pos", "ctl"),
                                               m=matrix.set_matrix_translate(m, guide_a_positions[-1]))
        self.blend_aim0_source_node = self.arm_output_nodes[0]
        self.blend_aim0_target_node = matrix.transform(parent=root,
                                                       name=self.generate_name("blendAim0", "pos", "ctl"),
                                                       m=matrix.set_matrix_translate(m, guide_a_positions[-1]))
        mc.pointConstraint(self.arm_output_nodes[0], self.fix_aim0_node, maintainOffset=True)
        self.guide_a_cons = mc.pointConstraint(self.fix_aim0_node,
                                               self.move_aim0_node,
                                               self.blend_aim0_target_node)[0]

        self.fix_aim1_node = matrix.transform(parent=self.arm_output_nodes[0],
                                              name=self.generate_name("fixAim1", "pos", "ctl"),
                                              m=matrix.set_matrix_translate(m, guide_b_positions[-1]))
        self.move_aim1_node = matrix.transform(parent=self.arm_output_nodes[int(len(self.arm_output_nodes) / 2)],
                                               name=self.generate_name("moveAim1", "pos", "ctl"),
                                               m=matrix.set_matrix_translate(m, guide_b_positions[-1]))
        self.blend_aim1_source_node = self.arm_output_nodes[int(len(self.arm_output_nodes) / 2)]
        self.blend_aim1_target_node = matrix.transform(parent=root,
                                                       name=self.generate_name("blendAim1", "pos", "ctl"),
                                                       m=matrix.set_matrix_translate(m, guide_b_positions[-1]))
        self.guide_b_cons = mc.pointConstraint(self.fix_aim1_node, self.move_aim1_node, self.blend_aim1_target_node)[0]

        self.fix_aim2_node = matrix.transform(parent=self.arm_output_nodes[int(len(self.arm_output_nodes) / 2)],
                                              name=self.generate_name("fixAim2", "pos", "ctl"),
                                              m=matrix.set_matrix_translate(m, guide_c_positions[-1]))
        self.move_aim2_node = matrix.transform(parent=self.fk3_loc,
                                               name=self.generate_name("moveAim2", "pos", "ctl"),
                                               m=matrix.set_matrix_translate(m, guide_c_positions[-1]))
        self.blend_aim2_source_node = self.arm_output_nodes[-1]
        self.blend_aim2_target_node = matrix.transform(parent=root,
                                                       name=self.generate_name("blendAim2", "pos", "ctl"),
                                                       m=matrix.set_matrix_translate(m, guide_c_positions[-1]))
        self.guide_c_cons = mc.pointConstraint(self.fix_aim2_node, self.move_aim2_node, self.blend_aim2_target_node)[0]

        self.fix_aim3_node = matrix.transform(parent=self.fk3_loc,
                                              name=self.generate_name("fixAim3", "pos", "ctl"),
                                              m=matrix.set_matrix_translate(m, guide_d_positions[-1]))
        self.move_aim3_node = matrix.transform(parent=self.fk4_loc,
                                               name=self.generate_name("moveAim3", "pos", "ctl"),
                                               m=matrix.set_matrix_translate(m, guide_d_positions[-1]))
        self.blend_aim3_source_node = self.fk4_loc
        self.blend_aim3_target_node = matrix.transform(parent=root,
                                                       name=self.generate_name("blendAim3", "pos", "ctl"),
                                                       m=matrix.set_matrix_translate(m, guide_d_positions[-1]))
        self.guide_d_cons = mc.pointConstraint(self.fix_aim3_node, self.move_aim3_node, self.blend_aim3_target_node)[0]

        self.aim4_target_node = matrix.transform(parent=self.fk4_loc,
                                                 name=self.generate_name("aim4", "pos", "ctl"),
                                                 m=matrix.set_matrix_translate(m, guide_e_positions[-1]))
        self.aim4_source_node = matrix.transform(parent=self.fk4_loc,
                                                 name=self.generate_name("src4", "pos", "ctl"),
                                                 m=matrix.set_matrix_translate(m, positions[-1]))

        self.guide_a_ctls = []
        self.guide_a_locs = []
        parent = root
        parent_ctl = self.fk0_ctl
        guide_a_matrices = matrix.get_chain_matrix(guide_a_positions, normal, negate)
        for i, _m in enumerate(guide_a_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("guideA" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
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
                                       mirror_ctl_name=self.generate_name("guideA" + str(i), "", "ctl", True))
            self.guide_a_ctls.append(ctl)
            self.guide_a_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.guide_a_up_move = matrix.transform(parent=self.arm_output_nodes[0],
                                                name=self.generate_name("guideA", "upMove", "ctl"),
                                                m=matrix.get_matrix(self.guide_a_ctls[0]))
        mc.setAttr(self.guide_a_up_move + ".tz", 1)
        self.guide_a_up_fix = matrix.transform(parent=root,
                                               name=self.generate_name("guideA", "upFix", "ctl"),
                                               m=matrix.get_matrix(self.guide_a_up_move))
        mc.pointConstraint(self.arm_output_nodes[0], self.guide_a_up_fix, maintainOffset=True)
        self.guide_a_up = matrix.transform(parent=root,
                                           name=self.generate_name("guideA", "up", "ctl"),
                                           m=matrix.get_matrix(self.guide_a_up_move))
        mc.pointConstraint(self.guide_a_up_fix, self.guide_a_up_move, self.guide_a_up)
        npo = hierarchy.get_parent(self.guide_a_ctls[0])
        mc.pointConstraint(self.blend_aim0_source_node, npo)
        mc.aimConstraint(self.blend_aim0_target_node,
                         npo,
                         aimVector=(1, 0, 0),
                         upVector=(0, 0, 1),
                         worldUpType="object",
                         worldUpObject=self.guide_a_up,
                         maintainOffset=True)
        self.guide_a_jnts = joint.add_chain_joint(npo,
                                                  self.generate_name("guideA%s", "jnt", "ctl"),
                                                  guide_a_positions[:-1],
                                                  normal,
                                                  negate=negate,
                                                  vis=True)
        mc.setAttr(self.guide_a_jnts[0] + ".overrideEnabled", 1)
        mc.setAttr(self.guide_a_jnts[0] + ".overrideDisplayType", 2)
        for ctl, jnt in zip(self.guide_a_ctls, self.guide_a_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.guide_b_ctls = []
        self.guide_b_locs = []
        parent = root
        parent_ctl = self.fk1_ctl
        guide_b_matrices = matrix.get_chain_matrix(guide_b_positions, normal, negate)
        for i, _m in enumerate(guide_b_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("guideB" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
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
                                       mirror_ctl_name=self.generate_name("guideB" + str(i), "", "ctl", True))
            self.guide_b_ctls.append(ctl)
            self.guide_b_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.guide_b_up = matrix.transform(parent=self.arm_output_nodes[int(len(self.arm_output_nodes) / 2)],
                                           name=self.generate_name("guideB", "up", "ctl"),
                                           m=matrix.get_matrix(self.guide_b_ctls[0]))
        mc.setAttr(self.guide_b_up + ".tz", 1)
        npo = hierarchy.get_parent(self.guide_b_ctls[0])
        mc.pointConstraint(self.blend_aim1_source_node, npo)
        mc.aimConstraint(self.blend_aim1_target_node,
                         npo,
                         aimVector=(1, 0, 0),
                         upVector=(0, 0, 1),
                         worldUpType="object",
                         worldUpObject=self.guide_b_up,
                         maintainOffset=True)
        self.guide_b_jnts = joint.add_chain_joint(npo,
                                                  self.generate_name("guideB%s", "jnt", "ctl"),
                                                  guide_b_positions[:-1],
                                                  normal,
                                                  negate=negate,
                                                  vis=True)
        mc.setAttr(self.guide_b_jnts[0] + ".overrideEnabled", 1)
        mc.setAttr(self.guide_b_jnts[0] + ".overrideDisplayType", 2)
        for ctl, jnt in zip(self.guide_b_ctls, self.guide_b_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.guide_c_ctls = []
        self.guide_c_locs = []
        parent = root
        parent_ctl = self.fk2_ctl
        guide_c_matrices = matrix.get_chain_matrix(guide_c_positions, normal, negate)
        for i, _m in enumerate(guide_c_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("guideC" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
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
                                       mirror_ctl_name=self.generate_name("guideC" + str(i), "", "ctl", True))
            self.guide_c_ctls.append(ctl)
            self.guide_c_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.guide_c_up = matrix.transform(parent=self.arm_output_nodes[-1],
                                           name=self.generate_name("guideC", "up", "ctl"),
                                           m=matrix.get_matrix(self.guide_c_ctls[0]))
        mc.setAttr(self.guide_c_up + ".tz", 1)
        npo = hierarchy.get_parent(self.guide_c_ctls[0])
        mc.pointConstraint(self.blend_aim2_source_node, npo)
        mc.aimConstraint(self.blend_aim2_target_node,
                         npo,
                         aimVector=(1, 0, 0),
                         upVector=(0, 0, 1),
                         worldUpType="object",
                         worldUpObject=self.guide_c_up,
                         maintainOffset=True)
        self.guide_c_jnts = joint.add_chain_joint(npo,
                                                  self.generate_name("guideC%s", "jnt", "ctl"),
                                                  guide_c_positions[:-1],
                                                  normal,
                                                  negate=negate,
                                                  vis=True)
        mc.setAttr(self.guide_c_jnts[0] + ".overrideEnabled", 1)
        mc.setAttr(self.guide_c_jnts[0] + ".overrideDisplayType", 2)
        for ctl, jnt in zip(self.guide_c_ctls, self.guide_c_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.guide_d_ctls = []
        self.guide_d_locs = []
        parent = root
        parent_ctl = self.fk4_ctl
        guide_d_matrices = matrix.get_chain_matrix(guide_d_positions, normal, negate)
        for i, _m in enumerate(guide_d_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("guideD" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
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
                                       mirror_ctl_name=self.generate_name("guideD" + str(i), "", "ctl", True))
            self.guide_d_ctls.append(ctl)
            self.guide_d_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.guide_d_up = matrix.transform(parent=self.fk4_loc,
                                           name=self.generate_name("guideD", "up", "ctl"),
                                           m=matrix.get_matrix(self.guide_d_ctls[0]))
        mc.setAttr(self.guide_d_up + ".tz", 1)
        npo = hierarchy.get_parent(self.guide_d_ctls[0])
        mc.pointConstraint(self.blend_aim3_source_node, npo)
        mc.aimConstraint(self.blend_aim3_target_node,
                         npo,
                         aimVector=(1, 0, 0),
                         upVector=(0, 0, 1),
                         worldUpType="object",
                         worldUpObject=self.guide_d_up,
                         maintainOffset=True)
        self.guide_d_jnts = joint.add_chain_joint(npo,
                                                  self.generate_name("guideD%s", "jnt", "ctl"),
                                                  guide_d_positions[:-1],
                                                  normal,
                                                  negate=negate,
                                                  vis=True)
        mc.setAttr(self.guide_d_jnts[0] + ".overrideEnabled", 1)
        mc.setAttr(self.guide_d_jnts[0] + ".overrideDisplayType", 2)
        for ctl, jnt in zip(self.guide_d_ctls, self.guide_d_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.guide_e_ctls = []
        self.guide_e_locs = []
        parent = root
        parent_ctl = self.fk4_ctl
        guide_e_matrices = matrix.get_chain_matrix(guide_e_positions, normal, negate)
        for i, _m in enumerate(guide_e_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("guideE" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
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
                                       mirror_ctl_name=self.generate_name("guideE" + str(i), "", "ctl", True))
            self.guide_e_ctls.append(ctl)
            self.guide_e_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.guide_e_up = matrix.transform(parent=self.fk4_loc,
                                           name=self.generate_name("guideE", "up", "ctl"),
                                           m=matrix.get_matrix(self.guide_e_ctls[0]))
        mc.setAttr(self.guide_e_up + ".tz", 1)
        npo = hierarchy.get_parent(self.guide_e_ctls[0])
        mc.pointConstraint(self.aim4_source_node, npo)
        mc.aimConstraint(self.aim4_target_node,
                         npo,
                         aimVector=(1, 0, 0),
                         upVector=(0, 0, 1),
                         worldUpType="object",
                         worldUpObject=self.guide_e_up,
                         maintainOffset=True)
        self.guide_e_jnts = joint.add_chain_joint(npo,
                                                  self.generate_name("guideE%s", "jnt", "ctl"),
                                                  guide_e_positions[:-1],
                                                  normal,
                                                  negate=negate,
                                                  vis=True)
        mc.setAttr(self.guide_e_jnts[0] + ".overrideEnabled", 1)
        mc.setAttr(self.guide_e_jnts[0] + ".overrideDisplayType", 2)
        for ctl, jnt in zip(self.guide_e_ctls, self.guide_e_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.fix_skin_jnt = joint.add_joint(parent=context["xxx"],
                                            name=self.generate_name("fix", "jnt", "ctl"))

        self.tertiary_in_ctls = []
        self.tertiary_in_locs = []
        parent = root
        parent_ctl = self.guide_a_ctls[-1]
        guide_a_matrices = matrix.get_chain_matrix(guide_a_positions, normal, negate)
        for i, _m in enumerate(guide_a_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("tertiaryIn" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": 20,
                                           "height": div_length / total_length,
                                           "depth": div_length / total_length,
                                           "width": offset * 2,
                                           "po": (po, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("tertiaryIn" + str(i), "", "ctl", True))
            self.tertiary_in_ctls.append(ctl)
            self.tertiary_in_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.tertiary_in_jnts = joint.add_chain_joint(context["xxx"],
                                                      self.generate_name("tertiaryIn%s", "jnt", "ctl"),
                                                      guide_a_positions[:-1],
                                                      normal,
                                                      negate=negate)
        for ctl, split_ctl in zip(self.guide_a_ctls, self.tertiary_in_ctls):
            mult_m = mc.createNode("multMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(ctl + ".matrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".matrix", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            split_npo = hierarchy.get_parent(split_ctl)
            mc.connectAttr(decom_m + ".outputTranslate", split_npo + ".t")
            mc.connectAttr(decom_m + ".outputRotate", split_npo + ".r")
        for ctl, jnt in zip(self.tertiary_in_ctls, self.tertiary_in_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.tertiary_out_ctls = []
        self.tertiary_out_locs = []
        parent = root
        parent_ctl = self.guide_b_ctls[-1]
        guide_b_matrices = matrix.get_chain_matrix(guide_b_positions, normal, negate)
        for i, _m in enumerate(guide_b_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("tertiaryOut" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": 20,
                                           "height": div_length / total_length,
                                           "depth": div_length / total_length,
                                           "width": offset * 2,
                                           "po": (po, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("tertiaryOut" + str(i), "", "ctl", True))
            self.tertiary_out_ctls.append(ctl)
            self.tertiary_out_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.tertiary_out_jnts = joint.add_chain_joint(context["xxx"],
                                                       self.generate_name("tertiaryOut%s", "jnt", "ctl"),
                                                       guide_b_positions[:-1],
                                                       normal,
                                                       negate=negate)
        for ctl, split_ctl in zip(self.guide_b_ctls, self.tertiary_out_ctls):
            mult_m = mc.createNode("multMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(ctl + ".matrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".matrix", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            split_npo = hierarchy.get_parent(split_ctl)
            mc.connectAttr(decom_m + ".outputTranslate", split_npo + ".t")
            mc.connectAttr(decom_m + ".outputRotate", split_npo + ".r")
        for ctl, jnt in zip(self.tertiary_out_ctls, self.tertiary_out_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.secondary_in_ctls = []
        self.secondary_in_locs = []
        parent = root
        parent_ctl = self.guide_a_ctls[-1]
        guide_a_matrices = matrix.get_chain_matrix(guide_a_positions, normal, negate)
        for i, _m in enumerate(guide_a_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("secondaryIn" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": 18,
                                           "height": div_length / total_length,
                                           "depth": div_length / total_length,
                                           "width": offset * 2,
                                           "po": (po, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("secondaryIn" + str(i), "", "ctl", True))
            self.secondary_in_ctls.append(ctl)
            self.secondary_in_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.secondary_in_jnts = joint.add_chain_joint(context["xxx"],
                                                       self.generate_name("secondaryIn%s", "jnt", "ctl"),
                                                       guide_a_positions[:-1],
                                                       normal,
                                                       negate=negate)
        for ctl, split_ctl in zip(self.guide_a_ctls, self.secondary_in_ctls):
            mult_m = mc.createNode("multMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(ctl + ".matrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".matrix", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            split_npo = hierarchy.get_parent(split_ctl)
            mc.connectAttr(decom_m + ".outputTranslate", split_npo + ".t")
            mc.connectAttr(decom_m + ".outputRotate", split_npo + ".r")
        for ctl, jnt in zip(self.secondary_in_ctls, self.secondary_in_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.secondary_mid_ctls = []
        self.secondary_mid_locs = []
        parent = root
        parent_ctl = self.guide_b_ctls[-1]
        guide_b_matrices = matrix.get_chain_matrix(guide_b_positions, normal, negate)
        for i, _m in enumerate(guide_b_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("secondaryMid" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": 18,
                                           "height": div_length / total_length,
                                           "depth": div_length / total_length,
                                           "width": offset * 2,
                                           "po": (po, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("secondaryMid" + str(i), "", "ctl", True))
            self.secondary_mid_ctls.append(ctl)
            self.secondary_mid_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.secondary_mid_jnts = joint.add_chain_joint(context["xxx"],
                                                        self.generate_name("secondaryMid%s", "jnt", "ctl"),
                                                        guide_b_positions[:-1],
                                                        normal,
                                                        negate=negate)
        for ctl, split_ctl in zip(self.guide_b_ctls, self.secondary_mid_ctls):
            mult_m = mc.createNode("multMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(ctl + ".matrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".matrix", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            split_npo = hierarchy.get_parent(split_ctl)
            mc.connectAttr(decom_m + ".outputTranslate", split_npo + ".t")
            mc.connectAttr(decom_m + ".outputRotate", split_npo + ".r")
        for ctl, jnt in zip(self.secondary_mid_ctls, self.secondary_mid_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.secondary_out_ctls = []
        self.secondary_out_locs = []
        parent = root
        parent_ctl = self.guide_c_ctls[-1]
        guide_c_matrices = matrix.get_chain_matrix(guide_c_positions, normal, negate)
        for i, _m in enumerate(guide_c_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("secondaryOut" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": 18,
                                           "height": div_length / total_length,
                                           "depth": div_length / total_length,
                                           "width": offset * 2,
                                           "po": (po, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("secondaryOut" + str(i), "", "ctl", True))
            self.secondary_out_ctls.append(ctl)
            self.secondary_out_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.secondary_out_jnts = joint.add_chain_joint(context["xxx"],
                                                        self.generate_name("secondaryOut%s", "jnt", "ctl"),
                                                        guide_c_positions[:-1],
                                                        normal,
                                                        negate=negate)
        for ctl, split_ctl in zip(self.guide_c_ctls, self.secondary_out_ctls):
            mult_m = mc.createNode("multMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(ctl + ".matrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".matrix", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            split_npo = hierarchy.get_parent(split_ctl)
            mc.connectAttr(decom_m + ".outputTranslate", split_npo + ".t")
            mc.connectAttr(decom_m + ".outputRotate", split_npo + ".r")
        for ctl, jnt in zip(self.secondary_out_ctls, self.secondary_out_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.primary_in_ctls = []
        self.primary_in_locs = []
        parent = root
        parent_ctl = self.guide_c_ctls[-1]
        guide_c_matrices = matrix.get_chain_matrix(guide_c_positions, normal, negate)
        for i, _m in enumerate(guide_c_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("primaryIn" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": 17,
                                           "height": div_length / total_length,
                                           "depth": div_length / total_length,
                                           "width": offset * 2,
                                           "po": (po, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("primaryIn" + str(i), "", "ctl", True))
            self.primary_in_ctls.append(ctl)
            self.primary_in_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.primary_in_jnts = joint.add_chain_joint(context["xxx"],
                                                     self.generate_name("primaryIn%s", "jnt", "ctl"),
                                                     guide_c_positions[:-1],
                                                     normal,
                                                     negate=negate)
        for ctl, split_ctl in zip(self.guide_c_ctls, self.primary_in_ctls):
            mult_m = mc.createNode("multMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(ctl + ".matrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".matrix", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            split_npo = hierarchy.get_parent(split_ctl)
            mc.connectAttr(decom_m + ".outputTranslate", split_npo + ".t")
            mc.connectAttr(decom_m + ".outputRotate", split_npo + ".r")
        for ctl, jnt in zip(self.primary_in_ctls, self.primary_in_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.primary_mid_ctls = []
        self.primary_mid_locs = []
        parent = root
        parent_ctl = self.guide_d_ctls[-1]
        guide_d_matrices = matrix.get_chain_matrix(guide_d_positions, normal, negate)
        for i, _m in enumerate(guide_d_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("primaryMid" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": 17,
                                           "height": div_length / total_length,
                                           "depth": div_length / total_length,
                                           "width": offset * 2,
                                           "po": (po, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("primaryMid" + str(i), "", "ctl", True))
            self.primary_mid_ctls.append(ctl)
            self.primary_mid_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.primary_mid_jnts = joint.add_chain_joint(context["xxx"],
                                                      self.generate_name("primaryMid%s", "jnt", "ctl"),
                                                      guide_d_positions[:-1],
                                                      normal,
                                                      negate=negate)
        for ctl, split_ctl in zip(self.guide_d_ctls, self.primary_mid_ctls):
            mult_m = mc.createNode("multMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(ctl + ".matrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".matrix", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            split_npo = hierarchy.get_parent(split_ctl)
            mc.connectAttr(decom_m + ".outputTranslate", split_npo + ".t")
            mc.connectAttr(decom_m + ".outputRotate", split_npo + ".r")
        for ctl, jnt in zip(self.primary_mid_ctls, self.primary_mid_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        self.primary_out_ctls = []
        self.primary_out_locs = []
        parent = root
        parent_ctl = self.guide_e_ctls[-1]
        guide_e_matrices = matrix.get_chain_matrix(guide_e_positions, normal, negate)
        for i, _m in enumerate(guide_e_matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("primaryOut" + str(i), "", "ctl"),
                                       parent_ctl=parent_ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=_m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": 17,
                                           "height": div_length / total_length,
                                           "depth": div_length / total_length,
                                           "width": offset * 2,
                                           "po": (po, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("primaryOut" + str(i), "", "ctl", True))
            self.primary_out_ctls.append(ctl)
            self.primary_out_locs.append(loc)
            parent = loc
            parent_ctl = ctl
        self.primary_out_jnts = joint.add_chain_joint(context["xxx"],
                                                      self.generate_name("primaryOut%s", "jnt", "ctl"),
                                                      guide_e_positions[:-1],
                                                      normal,
                                                      negate=negate)
        for ctl, split_ctl in zip(self.guide_e_ctls, self.primary_out_ctls):
            mult_m = mc.createNode("multMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(ctl + ".matrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".matrix", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            split_npo = hierarchy.get_parent(split_ctl)
            mc.connectAttr(decom_m + ".outputTranslate", split_npo + ".t")
            mc.connectAttr(decom_m + ".outputRotate", split_npo + ".r")
        for ctl, jnt in zip(self.primary_out_ctls, self.primary_out_jnts):
            mc.connectAttr(ctl + ".r", jnt + ".r")

        # add context
        context[self.identifier]["combine_mesh"] = self.combine_mesh
        context[self.identifier]["combine_skin_mesh"] = self.combine_skin_mesh

        self.bind_jnts = []
        self.bind_jnts += self.guide_a_jnts
        self.bind_jnts += self.guide_b_jnts
        self.bind_jnts += self.guide_c_jnts
        self.bind_jnts += self.guide_d_jnts
        self.bind_jnts += self.guide_e_jnts

        # refs
        self.refs = []
        twist_index = 0
        for i, node in enumerate(self.arm_output_nodes + [self.fk3_loc, self.fk4_loc]):
            if i == 0:
                anchor = True
                name = self.generate_name("humerus", "ref", "ctl")
            elif i == len(upper_jnt_v_values):
                anchor = True
                name = self.generate_name("elbow", "ref", "ctl")
                twist_index = 0
            elif i == len(self.arm_output_nodes) - 1:
                anchor = True
                name = self.generate_name("carpus", "ref", "ctl")
            elif i == len(self.arm_output_nodes):
                anchor = True
                name = self.generate_name("metacarpus", "ref", "ctl")
            elif i == len(self.arm_output_nodes) + 1:
                anchor = True
                name = self.generate_name("phalanges", "ref", "ctl")
            else:
                anchor = False
                name = self.generate_name(
                    "upper" + str(twist_index) if i < len(upper_jnt_v_values) else "lower" + str(twist_index),
                    "ref",
                    "ctl")
            self.refs.append(self.create_ref(context=context, name=name, anchor=anchor, m=node))
            twist_index += 1

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            jnt = None
            twist_index = 0
            for i, ref in enumerate(self.refs):
                bind = True
                if i == 0:
                    name = self.generate_name("humerus", "", "jnt")
                elif i == len(upper_jnt_v_values):
                    name = self.generate_name("elbow", "", "jnt")
                    twist_index = 0
                elif i == len(self.arm_output_nodes) - 1:
                    name = self.generate_name("carpus", "", "jnt")
                elif i == len(self.arm_output_nodes):
                    name = self.generate_name("metacarpus", "", "jnt")
                elif i == len(self.arm_output_nodes) + 1:
                    name = self.generate_name("phalanges", "", "jnt")
                elif i < len(upper_jnt_v_values):
                    bind = False
                    name = self.generate_name("upper" + str(twist_index), "", "jnt")
                else:
                    bind = False
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
                if bind:
                    self.bind_jnts.append(jnt)
                twist_index += 1
        context[self.identifier]["bind_jnts"] = self.bind_jnts

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
                                             defaultValue=0)
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
                                                   defaultValue=1.1)
        self.volume_attr = attribute.add_attr(host,
                                              longName="volume",
                                              type="double",
                                              keyable=True,
                                              minValue=0,
                                              maxValue=1,
                                              defaultValue=1)
        self.guide_ctls_vis_attr = attribute.add_attr(host,
                                                      longName="guide_ctls_vis",
                                                      type="float",
                                                      keyable=True,
                                                      minValue=0,
                                                      maxValue=1,
                                                      defaultValue=0)
        self.guide_a_blend_attr = attribute.add_attr(host,
                                                     longName="guide_a_blend",
                                                     type="float",
                                                     keyable=True,
                                                     minValue=0,
                                                     maxValue=1,
                                                     defaultValue=0.5)
        self.guide_b_blend_attr = attribute.add_attr(host,
                                                     longName="guide_b_blend",
                                                     type="float",
                                                     keyable=True,
                                                     minValue=0,
                                                     maxValue=1,
                                                     defaultValue=0.5)
        self.guide_c_blend_attr = attribute.add_attr(host,
                                                     longName="guide_c_blend",
                                                     type="float",
                                                     keyable=True,
                                                     minValue=0,
                                                     maxValue=1,
                                                     defaultValue=0.5)
        self.guide_d_blend_attr = attribute.add_attr(host,
                                                     longName="guide_d_blend",
                                                     type="float",
                                                     keyable=True,
                                                     minValue=0,
                                                     maxValue=1,
                                                     defaultValue=0.5)
        self.primary_ctls_vis_attr = attribute.add_attr(host,
                                                        longName="primary_ctls_vis",
                                                        type="float",
                                                        keyable=True,
                                                        minValue=0,
                                                        maxValue=1,
                                                        defaultValue=0)
        self.secondary_ctls_vis_attr = attribute.add_attr(host,
                                                          longName="secondary_ctls_vis",
                                                          type="float",
                                                          keyable=True,
                                                          minValue=0,
                                                          maxValue=1,
                                                          defaultValue=0)
        self.tertiary_ctls_vis_attr = attribute.add_attr(host,
                                                         longName="tertiary_ctls_vis",
                                                         type="float",
                                                         keyable=True,
                                                         minValue=0,
                                                         maxValue=1,
                                                         defaultValue=0)
        self.feather_plane_vis_attr = attribute.add_attr(host,
                                                         longName="feather_plane_vis",
                                                         type="enum",
                                                         enumName="none:plane:feather",
                                                         keyable=True,
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
        self.upper_uniform_attr = attribute.add_attr(self.flexible0_ctl,
                                                     longName="uniform",
                                                     type="double",
                                                     defaultValue=1,
                                                     minValue=0,
                                                     maxValue=1,
                                                     keyable=True)
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
            mc.connectAttr(node + ".message", self.ik_match_source_attr + "[{0}]".format(i))
        self.fk_match_source_attr = attribute.add_attr(host,
                                                       longName="fk_match_source",
                                                       type="message",
                                                       multi=True)
        for i, node in enumerate(self.fk_match_source):
            mc.connectAttr(node + ".message", self.fk_match_source_attr + "[{0}]".format(i))
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
                         self.arm_output_nodes[:-1])

        # guide blend
        cons = [self.guide_a_cons, self.guide_b_cons, self.guide_c_cons, self.guide_d_cons]
        attrs = [self.guide_a_blend_attr, self.guide_b_blend_attr, self.guide_c_blend_attr, self.guide_d_blend_attr]
        for c, attr in zip(cons, attrs):
            fix_attr, move_attr = mc.pointConstraint(c, query=True, weightAliasList=True)
            rev = mc.createNode("reverse")
            mc.connectAttr(attr, rev + ".inputX")
            mc.connectAttr(attr, c + "." + fix_attr)
            mc.connectAttr(rev + ".outputX", c + "." + move_attr)

        # guide vis
        for npo in map(hierarchy.get_parent, [self.guide_a_ctls[0],
                                              self.guide_b_ctls[0],
                                              self.guide_c_ctls[0],
                                              self.guide_d_ctls[0],
                                              self.guide_e_ctls[0]]):
            mc.connectAttr(self.guide_ctls_vis_attr, npo + ".v")
        for npo in map(hierarchy.get_parent, [self.tertiary_in_ctls[0],
                                              self.tertiary_out_ctls[0]]):
            mc.connectAttr(self.tertiary_ctls_vis_attr, npo + ".v")
        for npo in map(hierarchy.get_parent, [self.secondary_in_ctls[0],
                                              self.secondary_mid_ctls[0],
                                              self.secondary_out_ctls[0]]):
            mc.connectAttr(self.secondary_ctls_vis_attr, npo + ".v")
        for npo in map(hierarchy.get_parent, [self.primary_in_ctls[0],
                                              self.primary_mid_ctls[0],
                                              self.primary_out_ctls[0]]):
            mc.connectAttr(self.primary_ctls_vis_attr, npo + ".v")

        plane_choice = mc.createNode("choice")
        mc.setAttr(plane_choice + ".input[0]", 0)
        mc.setAttr(plane_choice + ".input[1]", 1)
        mc.setAttr(plane_choice + ".input[2]", 0)
        mc.connectAttr(self.feather_plane_vis_attr, plane_choice + ".selector")
        for mesh in [self.primary_output_mesh,
                     self.secondary_output_mesh,
                     self.primary_converts_output_mesh,
                     self.secondary_converts_output_mesh,
                     self.primary_under_output_mesh,
                     self.secondary_under_output_mesh,
                     self.tertiary_output_mesh]:
            mc.connectAttr(plane_choice + ".output", mesh + ".v")

        combine_sc = mc.skinCluster(self.bind_jnts,
                                    self.combine_skin_mesh,
                                    name=self.generate_name("combine", "sc", "ctl"),
                                    toSelectedBones=True,
                                    bindMethod=1,
                                    normalizeWeights=1,
                                    weightDistribution=1,
                                    removeUnusedInfluence=False)[0]
        mc.polySmooth(self.combine_skin_mesh,
                      name=self.generate_name("combine", "smooth", "ctl"),
                      keepBorder=0,
                      continuity=1,
                      constructionHistory=1)

        wing_skin_sets = mc.sets([self.combine_skin_mesh,
                                  self.primary_skin_mesh,
                                  self.primary_converts_skin_mesh,
                                  self.primary_under_skin_mesh,
                                  self.secondary_skin_mesh,
                                  self.secondary_converts_skin_mesh,
                                  self.secondary_under_skin_mesh,
                                  self.tertiary_skin_mesh], name=self.identifier + "_skin_mesh")
        if "specific_sets" not in context:
            context["specific_sets"] = []
        context["specific_sets"].append(wing_skin_sets)

        mc.select(self.combine_mesh, self.combine_skin_mesh)
        mc.CreateWrap()
        mc.hide([self.combine_skin_mesh, self.combine_mesh])

        p_wrap = mc.deformer(self.split_meshes,
                             type="proximityWrap",
                             name=self.generate_name("split", "pWrap", "ctl"))[0]
        p_wrap_ifc = ifc.NodeInterface(p_wrap)
        p_wrap_ifc.addDriver(mc.listRelatives(self.combine_mesh, shapes=True, fullPath=True)[0])
        mc.setAttr(p_wrap + ".useBindTags", 1)
        mc.setAttr(p_wrap + ".bindTagsFilter", self.identifier + "*", type="string")

        bind_jnts = [self.fix_skin_jnt] + self.primary_in_jnts + self.primary_mid_jnts + self.primary_out_jnts
        primary_sc = mc.skinCluster(bind_jnts,
                                    self.primary_skin_mesh,
                                    name=self.generate_name("primarySkin", "sc", "ctl"),
                                    toSelectedBones=True,
                                    bindMethod=0,
                                    dropoffRate=4,
                                    maximumInfluences=6,
                                    normalizeWeights=1,
                                    weightDistribution=1,
                                    removeUnusedInfluence=False)[0]
        primary_coverts_sc = mc.skinCluster(bind_jnts,
                                            self.primary_converts_skin_mesh,
                                            name=self.generate_name("primaryCovertsSkin", "sc", "ctl"),
                                            toSelectedBones=True,
                                            bindMethod=0,
                                            dropoffRate=4,
                                            maximumInfluences=6,
                                            normalizeWeights=1,
                                            weightDistribution=1,
                                            removeUnusedInfluence=False)[0]
        primary_under_sc = mc.skinCluster(bind_jnts,
                                          self.primary_under_skin_mesh,
                                          name=self.generate_name("primaryUnderSkin", "sc", "ctl"),
                                          toSelectedBones=True,
                                          bindMethod=0,
                                          dropoffRate=4,
                                          maximumInfluences=6,
                                          normalizeWeights=1,
                                          weightDistribution=1,
                                          removeUnusedInfluence=False)[0]
        bind_jnts = [self.fix_skin_jnt] + self.secondary_in_jnts + self.secondary_mid_jnts + self.secondary_out_jnts
        secondary_sc = mc.skinCluster(bind_jnts,
                                      self.secondary_skin_mesh,
                                      name=self.generate_name("secondarySkin", "sc", "ctl"),
                                      toSelectedBones=True,
                                      bindMethod=0,
                                      dropoffRate=4,
                                      maximumInfluences=6,
                                      normalizeWeights=1,
                                      weightDistribution=1,
                                      removeUnusedInfluence=False)[0]
        secondary_coverts_sc = mc.skinCluster(bind_jnts,
                                              self.secondary_converts_skin_mesh,
                                              name=self.generate_name("secondaryCovertsSkin", "sc", "ctl"),
                                              toSelectedBones=True,
                                              bindMethod=0,
                                              dropoffRate=4,
                                              maximumInfluences=6,
                                              normalizeWeights=1,
                                              weightDistribution=1,
                                              removeUnusedInfluence=False)[0]
        secondary_under_sc = mc.skinCluster(bind_jnts,
                                            self.secondary_under_skin_mesh,
                                            name=self.generate_name("secondaryUnderSkin", "sc", "ctl"),
                                            toSelectedBones=True,
                                            bindMethod=0,
                                            dropoffRate=4,
                                            maximumInfluences=6,
                                            normalizeWeights=1,
                                            weightDistribution=1,
                                            removeUnusedInfluence=False)[0]
        bind_jnts = [self.fix_skin_jnt] + self.tertiary_in_jnts + self.tertiary_out_jnts
        tertiary_sc = mc.skinCluster(bind_jnts,
                                     self.tertiary_skin_mesh,
                                     name=self.generate_name("tertiarySkin", "sc", "ctl"),
                                     toSelectedBones=True,
                                     bindMethod=0,
                                     dropoffRate=4,
                                     maximumInfluences=6,
                                     normalizeWeights=1,
                                     weightDistribution=1,
                                     removeUnusedInfluence=False)[0]

    def connections(self, context):
        super().connections(context)

        data = self.component.data["value"]
