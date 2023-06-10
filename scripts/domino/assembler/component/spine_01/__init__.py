# domino
from domino.lib import attribute, icon, matrix, vector, hierarchy
from domino.lib.rigging import nurbs, controller, joint
from domino.lib.animation import fcurve
from domino import assembler

# built-ins
import os
import uuid
import math

# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2


class Author:
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "spine"
    side = "C"
    index = 0
    description = "maya의 spline ik를 사용한 spine setting입니다. 사용 방법은 mgear의 spine과 거의 같습니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset": {"type": "doubleAngle"},
        "offset_matrix": {"type": "matrix"},
        "division": {"type": "long"},
        "position": {"type": "double"},
        "max_stretch": {"type": "double"},
        "max_squash": {"type": "double"},
        "hip_position": {"type": "double", "minValue": 0, "maxValue": 1},
        "stretch_volume_fcurve": {"type": "double"},
        "squash_volume_fcurve": {"type": "double"},
    })

    def _anchors():
        m = om2.MMatrix()
        t_m = om2.MTransformationMatrix()
        t_m.setRotation(om2.MEulerRotation([math.radians(x) for x in (0, 0, 90)]))
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))
        m1 = matrix.set_matrix_rotate(m1, t_m)
        m2 = matrix.set_matrix_translate(m, (0, 3, 0))
        return m1, m2

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "offset": 0,
        "offset_matrix": list(om2.MMatrix()),
        "division": 3,
        "position": 0,
        "max_stretch": 1.1,
        "max_squash": 0.95,
        "hip_position": 0.5,
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
        "root": "start",
        "position": [
            (0, "end"),
        ],
        "orientation": (1, "ori"),  # target node index, extension
        "display_curve": [
            ((0, 1), "dpCrv"),  # source node indexes, extension
        ],
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        ik_color = self.generate_color("ik")
        fk_color = self.generate_color("fk")

        orient_xyz = vector.OrientXYZ(data["offset_matrix"])
        normal = orient_xyz.y

        start_pos, end_pos = [om2.MVector(x[12:-1]) for x in data["anchors"]]

        negate = self.component.negate

        division = data["division"] - 1
        positions = []
        for i in range(division):
            positions.append((end_pos - start_pos) * ((i + 1) / division) + start_pos)

        look_at_m = matrix.get_look_at_matrix(start_pos, end_pos, normal, "xz", negate)
        if negate:
            look_at_ik_m = matrix.get_look_at_matrix(start_pos, end_pos, normal, "x-z", negate)
        else:
            look_at_ik_m = matrix.get_look_at_matrix(start_pos, end_pos, normal, "xz", negate)
        root = self.create_root(context)

        m = matrix.set_matrix_translate(look_at_m, (end_pos - start_pos) * data["hip_position"] + start_pos)
        self.hip_ctl, self.hip_loc = self.create_ctl(context=context,
                                                     parent=None,
                                                     name=self.generate_name("hip", "", "ctl"),
                                                     parent_ctl=None,
                                                     attrs=["rx", "ry", "rz"],
                                                     m=m,
                                                     cns=False,
                                                     mirror_config=(0,0,0, 0, 1, 1, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "circle",
                                                         "width": 2,
                                                         "height": 3.2,
                                                         "depth": 3.2,
                                                         "ro": (0, 0, 90),
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("hip", "", "ctl", True))
        m = matrix.set_matrix_translate(look_at_ik_m, start_pos)
        self.ik0_ctl, self.ik0_loc = self.create_ctl(context=context,
                                                     parent=self.hip_loc,
                                                     name=self.generate_name("ik0", "", "ctl"),
                                                     parent_ctl=self.hip_ctl,
                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                     m=m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "arrow4",
                                                         "width": 5,
                                                         "ro": (0, 0, 90),
                                                         "color": ik_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("ik0", "", "ctl", True))

        m = matrix.set_matrix_translate(look_at_ik_m, (end_pos - start_pos) * 0.5 + start_pos)
        self.ik_tan_ctl, self.ik_tan_loc = self.create_ctl(context=context,
                                                           parent=None,
                                                           name=self.generate_name("ikTan", "", "ctl"),
                                                           parent_ctl=self.ik0_ctl,
                                                           attrs=["tx", "ty", "tz"],
                                                           m=m,
                                                           cns=False,
                                                           mirror_config=(1,1, 1, 0, 0, 0, 0, 0, 0),
                                                           shape_args={
                                                               "shape": "circle3",
                                                               "width": 0.4,
                                                               "color": ik_color
                                                           },
                                                           mirror_ctl_name=self.generate_name("ikTan", "", "ctl", True))

        m = matrix.set_matrix_translate(look_at_m, start_pos - ((end_pos - start_pos) * 0.01))
        self.pelvis_ctl, self.pelvis_loc = self.create_ctl(context=context,
                                                           parent=None,
                                                           name=self.generate_name("pelvis", "", "ctl"),
                                                           parent_ctl=self.ik0_ctl,
                                                           attrs=["rx", "ry", "rz"],
                                                           m=m,
                                                           cns=False,
                                                           mirror_config=(0, 0, 0, 0, 1, 1, 0, 0, 0),
                                                           shape_args={
                                                               "shape": "cube",
                                                               "width": 1,
                                                               "height": 2.2,
                                                               "depth": 2.2,
                                                               "color": fk_color
                                                           },
                                                           mirror_ctl_name=self.generate_name("pelvis", "", "ctl",
                                                                                              True))

        m = matrix.set_matrix_translate(look_at_ik_m, end_pos)
        self.direction_ctl, self.direction_loc = \
            self.create_ctl(context=context,
                            parent=None,
                            name=self.generate_name("direction", "", "ctl"),
                            parent_ctl=self.hip_ctl,
                            attrs=["tx", "ty", "tz", "rx"],
                            m=m,
                            cns=False,
                            mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                            shape_args={
                                "shape": "circle3",
                                "width": 0.5,
                                "color": ik_color
                            },
                            mirror_ctl_name=self.generate_name("direction", "", "ctl", True))

        name = self.generate_name("display", "crv", "ctl")
        self.display_curve = matrix.transform(root, name, om2.MMatrix())
        icon.generate(self.display_curve,
                      [(0, 0, 0), (0, 0, 0)],
                      1,
                      om2.MColor((0.55, 0.55, 0.55, 0.55)),
                      thickness=1)
        nurbs.constraint(self.display_curve, [self.pelvis_loc, self.direction_loc])
        shape = mc.listRelatives(self.display_curve, shapes=True, fullPath=True)[0]
        mc.setAttr(shape + ".overrideDisplayType", 2)
        mc.setAttr(self.display_curve + ".inheritsTransform", 0)
        mc.setAttr(self.display_curve + ".translate", 0, 0, 0)
        mc.setAttr(self.display_curve + ".rotate", 0, 0, 0)

        name = self.generate_name("SC%s", "", "jnt")
        sc_normal = orient_xyz.y * -1
        self.sc_chain = joint.add_chain_joint(root, name, [start_pos, end_pos], sc_normal, negate=negate)
        name = self.generate_name("SC", "ikh", "ctl")
        joint.ikh(self.direction_loc, name, self.sc_chain, solver="ikSCsolver")

        name = self.generate_name("ik1", "autoRot", "ctl")
        m = matrix.get_look_at_matrix(end_pos, start_pos, sc_normal, "-xz", False)
        self.ik1_auto_rotate = matrix.transform(self.sc_chain[-1], name, m, offset_parent_matrix=True)

        m = matrix.set_matrix_translate(look_at_ik_m, end_pos)
        self.ik1_ctl, self.ik1_loc = self.create_ctl(context=context,
                                                     parent=self.ik1_auto_rotate,
                                                     name=self.generate_name("ik1", "", "ctl"),
                                                     parent_ctl=self.direction_ctl,
                                                     attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz"],
                                                     m=m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "arrow4",
                                                         "width": 5,
                                                         "ro": (0, 0, 90),
                                                         "color": ik_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("ik1", "", "ctl", True))

        m = matrix.set_matrix_translate(look_at_ik_m, (end_pos - start_pos) * 0.4 + start_pos)
        name = self.generate_name("ik0Tan", "offset", "ctl")
        self.ik0_tan_offset = matrix.transform(parent=self.ik0_loc, name=name, m=m)
        self.ik0_tan_ctl, self.ik0_tan_loc = \
            self.create_ctl(context=context,
                            parent=self.ik0_tan_offset,
                            name=self.generate_name("ik0Tan", "", "ctl"),
                            parent_ctl=self.ik_tan_ctl,
                            attrs=["tx", "ty", "tz"],
                            m=m,
                            cns=False,
                            mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                            shape_args={
                                "shape": "circle3",
                                "width": 0.2,
                                "color": ik_color
                            },
                            mirror_ctl_name=self.generate_name("ik0Tan", "", "ctl", True))

        curve_points = [start_pos, list(m)[12:-1]]
        self.ik0_tan_npo = hierarchy.get_parent(self.ik0_tan_ctl)

        m = matrix.set_matrix_translate(look_at_ik_m, (end_pos - start_pos) * 0.6 + start_pos)
        name = self.generate_name("ik1Tan", "offset", "ctl")
        self.ik1_tan_offset = matrix.transform(parent=self.ik1_loc, name=name, m=m)
        self.ik1_tan_ctl, self.ik1_tan_loc = \
            self.create_ctl(context=context,
                            parent=self.ik1_tan_offset,
                            name=self.generate_name("ik1Tan", "", "ctl"),
                            parent_ctl=self.ik1_ctl,
                            attrs=["tx", "ty", "tz"],
                            m=m,
                            cns=False,
                            mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                            shape_args={
                                "shape": "circle3",
                                "width": 0.2,
                                "color": ik_color
                            },
                            mirror_ctl_name=self.generate_name("ik1Tan", "", "ctl", True))
        curve_points.append(list(m)[12:-1])
        curve_points.append(end_pos)
        self.ik1_tan_npo = hierarchy.get_parent(self.ik1_tan_ctl)

        name = self.generate_name("original", "crv", "ctl")
        self.spline_original_crv = nurbs.create(root,
                                                name,
                                                degree=3,
                                                positions=curve_points,
                                                bezier=False,
                                                vis=False,
                                                inherits=True,
                                                display_type=1)
        name = self.generate_name("deform", "crv", "ctl")
        self.spline_deform_crv = nurbs.create(root,
                                              name,
                                              degree=3,
                                              positions=curve_points,
                                              m=matrix.get_matrix(root),
                                              bezier=False,
                                              vis=False,
                                              inherits=False,
                                              display_type=1)
        nurbs.constraint(self.spline_deform_crv, [self.ik0_loc, self.ik0_tan_loc, self.ik1_tan_loc, self.ik1_loc])

        fk_offset = (end_pos - start_pos) / division
        name = self.generate_name("SP%s", "", "jnt")
        self.sp_chain = joint.add_chain_joint(root,
                                              name,
                                              [start_pos + fk_offset * i for i in range(division + 1)],
                                              normal,
                                              negate=negate)
        name = self.generate_name("SP0", "loc", "ctl")
        self.sp0_loc = mc.createNode("transform", name=name, parent=self.root)
        mc.connectAttr(self.sp_chain[0] + ".matrix", self.sp0_loc + ".offsetParentMatrix")

        name = self.generate_name("SP", "ikh", "ctl")
        self.sp_ik_h = joint.sp_ikh(root, name, self.sp_chain, self.spline_deform_crv)

        parent_ctl = self.ik0_ctl
        parent = root
        self.fk_ctls = []
        self.fk_locs = []
        for i, m in enumerate(range(division + 1)):
            m = matrix.set_matrix_translate(look_at_m, start_pos + fk_offset * i)
            fk_ctl, fk_loc = self.create_ctl(context=context,
                                             parent=parent,
                                             name=self.generate_name("fk" + str(i), "", "ctl"),
                                             parent_ctl=parent_ctl,
                                             attrs=["tx", "ty", "tz",
                                                    "rx", "ry", "rz",
                                                    "sx", "sy", "sz"],
                                             m=m,
                                             cns=False,
                                             mirror_config=(1, 1, 1, 0, 1, 1, 0, 0, 0),
                                             shape_args={
                                                 "shape": "cube",
                                                 "width": 0.1,
                                                 "height": 3,
                                                 "depth": 3,
                                                 "color": fk_color
                                             },
                                             mirror_ctl_name=self.generate_name("fk" + str(i), "", "ctl", True))
            parent_ctl = fk_ctl
            parent = fk_ctl
            self.fk_ctls.append(fk_ctl)
            self.fk_locs.append(fk_loc)

        name = self.generate_name("volume", "crv", "ctl")
        self.spline_volume_crv = nurbs.create(root,
                                              name,
                                              degree=1,
                                              positions=[om2.MVector((0, 0, 0)) for _ in self.fk_ctls],
                                              m=matrix.get_matrix(root),
                                              bezier=False,
                                              vis=False,
                                              inherits=False,
                                              display_type=1)
        self.non_scale_fk_pos = []
        parent = root
        for i, ctl in enumerate(self.fk_ctls):
            name = self.generate_name(f"fk{i}NonScale", "pos", "ctl")
            parent = matrix.transform(parent, name, om2.MMatrix())
            self.non_scale_fk_pos.append(parent)
            mc.connectAttr(ctl + ".translate", parent + ".translate")
            mc.connectAttr(ctl + ".rotate", parent + ".rotate")
        nurbs.constraint(self.spline_volume_crv, self.non_scale_fk_pos)

        name = self.generate_name("fk0Orient", "loc", "ctl")
        m = matrix.set_matrix_translate(look_at_m, start_pos)
        self.fk_0_lock_orient_loc = matrix.transform(parent=root, name=name, m=m)

        # refs
        name = self.generate_name("pelvis", "ref", "ctl")
        refs = [self.create_ref(context=context, name=name, anchor=True, m=self.pelvis_loc)]

        for i in range(division + 1):
            anchor = False if i < division else True
            name = self.generate_name(f"fk{i}", "ref", "ctl")
            m = self.fk_locs[i]
            refs.append(self.create_ref(context=context, name=name, anchor=anchor, m=m))

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            parent = None
            for i, r in enumerate(refs):
                m = matrix.get_matrix(r)
                name = self.generate_name("pelvis", "", "jnt") if i == 0 else self.generate_name(f"spine{i - 1}", "",
                                                                                                 "jnt")
                parent = self.create_jnt(context=context,
                                         parent=parent,
                                         name=name,
                                         description=str(i),
                                         ref=r,
                                         m=m,
                                         leaf=False,
                                         uni_scale=uni_scale)

    def attributes(self, context):
        super().attributes(context)
        host = self.host
        data = self.component.data["value"]

        self.position = attribute.add_attr(host,
                                           longName="position",
                                           type="double",
                                           keyable=True,
                                           minValue=0,
                                           maxValue=1,
                                           defaultValue=data["position"])
        self.stretch_squash = attribute.add_attr(host,
                                                 longName="stretch_squash_enable",
                                                 type="double",
                                                 keyable=True,
                                                 minValue=0,
                                                 maxValue=1,
                                                 defaultValue=1)
        self.max_stretch = attribute.add_attr(host,
                                              longName="max_stretch",
                                              type="double",
                                              keyable=True,
                                              minValue=1,
                                              defaultValue=data["max_stretch"])
        self.max_squash = attribute.add_attr(host,
                                             longName="max_squash",
                                             type="double",
                                             keyable=True,
                                             minValue=0.001,
                                             maxValue=1,
                                             defaultValue=data["max_squash"])
        self.front_bend = attribute.add_attr(host,
                                             longName="front_bend",
                                             type="double",
                                             keyable=True,
                                             minValue=0,
                                             maxValue=2,
                                             defaultValue=0.5)
        self.side_bend = attribute.add_attr(host,
                                            longName="side_bend",
                                            type="double",
                                            keyable=True,
                                            minValue=0,
                                            maxValue=2,
                                            defaultValue=0.5)
        self.tangent0 = attribute.add_attr(host,
                                           longName="tangent0",
                                           type="double",
                                           keyable=True,
                                           minValue=0,
                                           defaultValue=1)
        self.tangent1 = attribute.add_attr(host,
                                           longName="tangent1",
                                           type="double",
                                           keyable=True,
                                           minValue=0,
                                           defaultValue=1)
        self.lock_orient_0 = attribute.add_attr(host,
                                                longName="lock_orient_0",
                                                type="double",
                                                keyable=True,
                                                minValue=0,
                                                maxValue=1,
                                                defaultValue=1)
        self.lock_orient_1 = attribute.add_attr(host,
                                                longName="lock_orient_1",
                                                type="double",
                                                keyable=True,
                                                minValue=0,
                                                maxValue=1,
                                                defaultValue=1)
        self.volume = attribute.add_attr(host,
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
        stretch_values = fcurve.get_fcurve_values(stretch_volume_fcurve, data["division"])
        for i, value in enumerate(stretch_values):
            self.stretch_attrs.append(attribute.add_attr(self.root,
                                                         longName=f"stretch_volume_value{i}",
                                                         type="double",
                                                         keyable=False,
                                                         defaultValue=value))
        squash_values = fcurve.get_fcurve_values(squash_volume_fcurve, data["division"])
        for i, value in enumerate(squash_values):
            self.squash_attrs.append(attribute.add_attr(self.root,
                                                        longName=f"squash_volume_value{i}",
                                                        type="double",
                                                        keyable=False,
                                                        defaultValue=value))
        self.fk_vis = attribute.add_attr(host,
                                         longName="fk_vis",
                                         type="bool",
                                         keyable=True,
                                         defaultValue=False)

    def operators(self, context):
        super().operators(context)
        data = self.component.data["value"]

        negate = self.component.negate

        # fk vis
        for ctl in self.fk_ctls:
            for shape in mc.listRelatives(ctl, shapes=True, fullPath=True):
                mc.connectAttr(self.fk_vis, shape + ".v")

        # direction
        md = mc.createNode("multiplyDivide")
        mc.connectAttr(self.sc_chain[0] + ".rz", md + ".input1X")
        mc.connectAttr(self.front_bend, md + ".input2X")
        front_bend = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(self.sc_chain[0] + ".ry", md + ".input1X")
        mc.connectAttr(self.side_bend, md + ".input2X")
        side_bend = md + ".outputX"

        if negate:
            md = mc.createNode("multiplyDivide")
            mc.connectAttr(side_bend, md + ".input1X")
            mc.setAttr(md + ".input2X", -1)
            side_bend = md + ".outputX"

        mc.connectAttr(front_bend, self.ik1_auto_rotate + ".rz")
        mc.connectAttr(side_bend, self.ik1_auto_rotate + ".ry")

        # spline ik handle
        mc.setAttr(self.sp_ik_h + ".dTwistControlEnable", True)
        mc.setAttr(self.sp_ik_h + ".dWorldUpType", 4)
        if negate:
            mc.setAttr(self.sp_ik_h + ".dForwardAxis", 1)
            mc.setAttr(self.sp_ik_h + ".dWorldUpAxis", 1)
        mc.connectAttr(self.ik0_loc + ".worldMatrix[0]", self.sp_ik_h + ".dWorldUpMatrix")
        mc.connectAttr(self.ik1_loc + ".worldMatrix[0]", self.sp_ik_h + ".dWorldUpMatrixEnd")

        # curve info
        original_crv_shape = mc.listRelatives(self.spline_original_crv, shapes=True, fullPath=True)[0]
        curve_info = mc.arclen(original_crv_shape, ch=1)
        original_curve_length = curve_info + ".arcLength"

        deform_crv_shape = mc.listRelatives(self.spline_deform_crv, shapes=True, fullPath=True)[0]
        curve_info = mc.arclen(deform_crv_shape, ch=1)
        deform_curve_length = curve_info + ".arcLength"

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".operation", 2)
        mc.connectAttr(deform_curve_length, md + ".input1X")
        mc.connectAttr(original_curve_length, md + ".input2X")
        curve_ratio = md + ".outputX"

        # stretch & squash
        condition = mc.createNode("condition")
        mc.connectAttr(curve_ratio, condition + ".firstTerm")
        mc.connectAttr(self.max_stretch, condition + ".secondTerm")
        mc.setAttr(condition + ".operation", 2)
        mc.connectAttr(self.max_stretch, condition + ".colorIfTrueR")
        mc.connectAttr(curve_ratio, condition + ".colorIfFalseR")
        max_stretch_multiple = condition + ".outColorR"

        condition = mc.createNode("condition")
        mc.connectAttr(curve_ratio, condition + ".firstTerm")
        mc.connectAttr(self.max_squash, condition + ".secondTerm")
        mc.setAttr(condition + ".operation", 5)
        mc.connectAttr(self.max_squash, condition + ".colorIfTrueR")
        mc.connectAttr(curve_ratio, condition + ".colorIfFalseR")
        max_squash_multiple = condition + ".outColorR"

        condition = mc.createNode("condition")
        mc.connectAttr(curve_ratio, condition + ".firstTerm")
        mc.setAttr(condition + ".secondTerm", 1)
        mc.setAttr(condition + ".operation", 3)
        mc.connectAttr(max_stretch_multiple, condition + ".colorIfTrueR")
        mc.connectAttr(max_squash_multiple, condition + ".colorIfFalseR")
        stretch_squash_multiple = condition + ".outColorR"

        bta = mc.createNode("blendTwoAttr")
        mc.setAttr(bta + ".input[0]", 1)
        mc.connectAttr(stretch_squash_multiple, bta + ".input[1]")
        mc.connectAttr(self.stretch_squash, bta + ".attributesBlender")
        stretch_squash_switch = bta + ".output"

        for j in self.sp_chain:
            md = mc.createNode("multiplyDivide")
            mc.connectAttr(stretch_squash_switch, md + ".input1X")
            mc.setAttr(md + ".input2X", mc.getAttr(j + ".tx"))
            mc.connectAttr(md + ".outputX", j + ".tx")

        # spline offset(ik solver offset) position
        condition = mc.createNode("condition")
        mc.connectAttr(deform_curve_length, condition + ".firstTerm")
        mc.connectAttr(original_curve_length, condition + ".secondTerm")
        mc.setAttr(condition + ".operation", 3)
        mc.connectAttr(stretch_squash_switch, condition + ".colorIfTrueR")
        mc.setAttr(condition + ".colorIfFalseR", 1)
        max_stretch_multiple_condition = condition + ".outColorR"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(max_stretch_multiple_condition, md + ".input1X")
        mc.connectAttr(original_curve_length, md + ".input2X")
        stretched_original_curve_length = md + ".outputX"

        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".operation", 2)
        mc.connectAttr(deform_curve_length, pma + ".input1D[0]")
        mc.connectAttr(stretched_original_curve_length, pma + ".input1D[1]")

        condition = mc.createNode("condition")
        mc.setAttr(condition + ".operation", 5)
        mc.connectAttr(pma + ".output1D", condition + ".firstTerm")
        mc.connectAttr(pma + ".output1D", condition + ".colorIfFalseR")
        offset_position_length_value = condition + ".outColorR"

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".operation", 2)
        mc.connectAttr(offset_position_length_value, md + ".input1X")
        mc.connectAttr(deform_curve_length, md + ".input2X")
        offset_position_u_value = md + ".outputX"

        mp = mc.createNode("motionPath")
        mc.setAttr(mp + ".fractionMode", True)
        mc.connectAttr(deform_crv_shape + ".worldSpace[0]", mp + ".geometryPath")
        mc.connectAttr(offset_position_u_value, mp + ".uValue")

        npoc = mc.createNode("nearestPointOnCurve")
        mc.connectAttr(deform_crv_shape + ".worldSpace[0]", npoc + ".inputCurve")
        mc.connectAttr(mp + ".allCoordinates", npoc + ".inPosition")
        position_offset_value = npoc + ".result.parameter"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(position_offset_value, md + ".input1X")
        mc.connectAttr(self.position, md + ".input2X")
        ik_offset_value = md + ".outputX"

        mc.connectAttr(ik_offset_value, self.sp_ik_h + ".offset")

        # volume
        volume_crv_shape = mc.listRelatives(self.spline_volume_crv, shapes=True, fullPath=True)[0]
        curve_info = mc.arclen(volume_crv_shape, ch=1)
        volume_curve_length = curve_info + ".arcLength"

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".operation", 2)
        mc.connectAttr(volume_curve_length, md + ".input1X")
        mc.connectAttr(original_curve_length, md + ".input2X")
        volume_curve_ratio = md + ".outputX"

        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".operation", 2)
        mc.connectAttr(volume_curve_ratio, pma + ".input1D[0]")
        mc.setAttr(pma + ".input1D[1]", 1)

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".operation", 3)
        mc.connectAttr(pma + ".output1D", md + ".input1X")
        mc.setAttr(md + ".input2X", 2)
        pow_value = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".operation", 3)
        mc.connectAttr(pow_value, md + ".input1X")
        mc.setAttr(md + ".input2X", 0.5)
        abs_value = md + ".outputX"

        for i in range(data["division"]):
            condition = mc.createNode("condition")
            mc.setAttr(condition + ".operation", 3)
            mc.connectAttr(stretch_squash_switch, condition + ".firstTerm")
            mc.setAttr(condition + ".secondTerm", 1)
            mc.connectAttr(self.stretch_attrs[i], condition + ".colorIfTrueR")
            mc.connectAttr(self.squash_attrs[i], condition + ".colorIfFalseR")

            md = mc.createNode("multiplyDivide")
            mc.connectAttr(condition + ".outColorR", md + ".input1X")
            mc.connectAttr(self.volume, md + ".input2X")
            volume_multiple = md + ".outputX"

            md = mc.createNode("multiplyDivide")
            mc.connectAttr(abs_value, md + ".input1X")
            mc.connectAttr(volume_multiple, md + ".input2X")

            pma = mc.createNode("plusMinusAverage")
            mc.setAttr(pma + ".input3D[0]", 1, 1, 1)
            mc.connectAttr(md + ".outputX", pma + ".input3D[1].input3Dx")
            mc.connectAttr(md + ".outputX", pma + ".input3D[1].input3Dy")
            mc.connectAttr(md + ".outputX", pma + ".input3D[1].input3Dz")

            [mc.setAttr(self.fk_locs[i] + "." + attr, lock=False) for attr in ["sx", "sy", "sz"]]
            mc.connectAttr(pma + ".output3D", self.fk_locs[i] + ".s")

        # lock orient
        for i, npo in enumerate([hierarchy.get_parent(x) for x in self.fk_ctls]):
            if i == len(self.fk_ctls) - 1:
                pb = mc.createNode("pairBlend")
                mc.setAttr(pb + ".rotInterpolation", 1)
                mc.connectAttr(self.lock_orient_1, pb + ".weight")

                target = self.sp_chain[-1]
                target_parent = hierarchy.get_parent(target)

                m = matrix.get_matrix(self.ik1_loc)
                target_parent_m = matrix.get_matrix(target_parent)
                offset_m = m * target_parent_m.inverse()

                mult_m = mc.createNode("multMatrix")
                mc.setAttr(mult_m + ".matrixIn[0]", offset_m, type="matrix")
                mc.connectAttr(self.ik1_loc + ".worldMatrix[0]", mult_m + ".matrixIn[1]")
                mc.connectAttr(target_parent + ".worldInverseMatrix[0]", mult_m + ".matrixIn[2]")

                decom_m = mc.createNode("decomposeMatrix")
                mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
                lock_orient = decom_m + ".outputRotate"

                mc.connectAttr(lock_orient, pb + ".inRotate2")
                mc.connectAttr(pb + ".outRotate", self.sp_chain[-1] + ".r")
            mc.connectAttr(self.sp_chain[i] + ".matrix", npo + ".offsetParentMatrix")
            mc.connectAttr(self.sp_chain[i] + ".matrix", self.non_scale_fk_pos[i] + ".offsetParentMatrix")

        mc.connectAttr(self.sp_chain[0] + ".t", self.fk_0_lock_orient_loc + ".t")
        mc.connectAttr(self.sp_chain[0] + ".s", self.fk_0_lock_orient_loc + ".s")

        decom_m = mc.createNode("decomposeMatrix")
        mc.connectAttr(self.sp_chain[0] + ".matrix", decom_m + ".inputMatrix")
        follow_orient = decom_m + ".outputRotate"

        root = hierarchy.get_parent(self.fk_0_lock_orient_loc)
        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.ik0_loc + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
        mc.connectAttr(root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

        decom_m = mc.createNode("decomposeMatrix")
        mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
        lock_orient = decom_m + ".outputRotate"

        pb = mc.createNode("pairBlend")
        mc.setAttr(pb + ".rotInterpolation", 1)
        mc.connectAttr(follow_orient, pb + ".inRotate1")
        mc.connectAttr(lock_orient, pb + ".inRotate2")

        mc.connectAttr(self.lock_orient_0, pb + ".weight")
        mc.connectAttr(pb + ".outRotate", self.fk_0_lock_orient_loc + ". r")

        # pelvis
        pelvis_npo = hierarchy.get_parent(self.pelvis_ctl)
        mc.parentConstraint(self.fk_0_lock_orient_loc, pelvis_npo, maintainOffset=True)
        mc.scaleConstraint(self.fk_0_lock_orient_loc, pelvis_npo, maintainOffset=True)

        # tangent ctl
        tan_npo = hierarchy.get_parent(self.ik_tan_ctl)
        mc.connectAttr(self.ik_tan_ctl + ".t", self.ik0_tan_npo + ".t")
        mc.connectAttr(self.ik_tan_ctl + ".t", self.ik1_tan_npo + ".t")

        mc.pointConstraint(self.ik0_tan_offset, self.ik1_tan_offset, tan_npo, maintainOffset=True)
        mc.orientConstraint(self.ik0_tan_offset, self.ik1_tan_offset, tan_npo, maintainOffset=True)

        distance = mc.createNode("distanceBetween")
        decom = mc.createNode("decomposeMatrix")
        mc.connectAttr(self.ik0_loc + ".worldMatrix[0]", decom + ".inputMatrix")
        mc.connectAttr(decom + ".outputTranslate", distance + ".point1")
        decom = mc.createNode("decomposeMatrix")
        mc.connectAttr(self.ik1_loc + ".worldMatrix[0]", decom + ".inputMatrix")
        mc.connectAttr(decom + ".outputTranslate", distance + ".point2")
        distance = distance + ".distance"

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".operation", 2)
        mc.connectAttr(original_curve_length, md + ".input1X")
        mc.setAttr(md + ".input2X", mc.getAttr(original_curve_length))
        original_crv_ratio = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(original_crv_ratio, md + ".input1X")
        mc.setAttr(md + ".input2X", mc.getAttr(distance))
        scaled_distance = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".operation", 2)
        mc.connectAttr(distance, md + ".input1X")
        mc.connectAttr(scaled_distance, md + ".input2X")
        normalize_distance = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(normalize_distance, md + ".input1X")
        mc.setAttr(md + ".input2X", mc.getAttr(self.ik0_tan_offset + ".tx"))
        scaled_offset_value = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(self.tangent0, md + ".input1X")
        mc.connectAttr(scaled_offset_value, md + ".input2X")
        tan0_value = md + ".outputX"

        mc.connectAttr(tan0_value, self.ik0_tan_offset + ".tx")

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(normalize_distance, md + ".input1X")
        mc.setAttr(md + ".input2X", mc.getAttr(self.ik1_tan_offset + ".tx"))
        scaled_offset_value = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(self.tangent1, md + ".input1X")
        mc.connectAttr(scaled_offset_value, md + ".input2X")
        tan0_value = md + ".outputX"

        mc.connectAttr(tan0_value, self.ik1_tan_offset + ".tx")

    def connections(self, context):
        super().connections(context)
