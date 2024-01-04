# domino
from domino.lib import attribute, matrix, vector, hierarchy
from domino.lib.rigging import nurbs, joint
from domino.lib.animation import fcurve
from domino import assembler

# built-ins
import os
import uuid

# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2


class Author:
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "neck"
    side = "C"
    index = 0
    description = "목 입니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset": {"type": "doubleAngle"},
        "offset_matrix": {"type": "matrix"},
        "division": {"type": "long"},
        "max_stretch": {"type": "double"},
        "max_squash": {"type": "double"},
        "stretch_volume_fcurve": {"type": "double"},
        "squash_volume_fcurve": {"type": "double"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))  # root
        m2 = matrix.set_matrix_translate(m, (0, 0.5, 0))  # cv1
        m3 = matrix.set_matrix_translate(m, (0, 1.5, 0))  # neck
        m4 = matrix.set_matrix_translate(m, (0, 1, 0))  # cv2
        m5 = matrix.set_matrix_translate(m, (0, 1.6, 0))  # lookAt
        m6 = matrix.set_matrix_translate(m, (0, 1.2, -0.5))  # orbit
        return m1, m2, m3, m4, m5, m6

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
        "division": 2,
        "max_stretch": 1.1,
        "max_squash": 0.9,
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
            (0, "cv1"),
            (0, "end"),  # parent node index, extension
            (2, "cv2"),
            (2, "lookAt"),
            (0, "orbit"),
        ],
        "orientation": (1, "ori"),  # target node index, extension
        "display_curve": [
            ((0, 1, 3, 2), "dp0Crv", 3, 2),  # source node indexes, extension, degree, thickness
            ((0, 1, 3, 2), "dp1Crv"),  # source node indexes, extension
        ],
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        ik_color = self.generate_color("ik")
        fk_color = self.generate_color("fk")

        orient_xyz = vector.OrientXYZ(om2.MMatrix(data["offset_matrix"]))
        normal = orient_xyz.z

        pos0 = om2.MVector(data["anchors"][0][12:-1])  # root
        pos1 = om2.MVector(data["anchors"][1][12:-1])  # cv1
        pos2 = om2.MVector(data["anchors"][2][12:-1])  # neck
        pos3 = om2.MVector(data["anchors"][3][12:-1])  # cv2
        pos4 = om2.MVector(data["anchors"][4][12:-1])  # lookAt
        pos5 = om2.MVector(data["anchors"][5][12:-1])  # orbit

        negate = self.component.negate

        root = self.create_root(context)
        root_m = matrix.get_matrix(root)

        look_at_ik_m = matrix.get_look_at_matrix(pos2, pos4, normal, "xz", negate)
        m = matrix.set_matrix_translate(look_at_ik_m, pos5)
        self.orbit_ctl, self.orbit_loc = self.create_ctl(context=context,
                                                         parent=None,
                                                         name=self.generate_name("orbit", "", "ctl"),
                                                         parent_ctl=None,
                                                         attrs=["rx", "ry", "rz"],
                                                         m=m,
                                                         cns=False,
                                                         mirror_config=(0, 0, 0, 0, 1, 1, 0, 0, 0),
                                                         shape_args={
                                                             "shape": "circle3",
                                                             "width": 0.5,
                                                             "color": ik_color
                                                         },
                                                         mirror_ctl_name=self.generate_name("orbit", "", "ctl", True))

        m = matrix.set_matrix_translate(look_at_ik_m, pos2)
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context,
                                                   parent=self.orbit_loc,
                                                   name=self.generate_name("ik", "", "ctl"),
                                                   parent_ctl=self.orbit_ctl,
                                                   attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                   m=m,
                                                   cns=False,
                                                   mirror_config=(1, 0, 0, 0, 1, 1, 0, 0, 0),
                                                   shape_args={
                                                       "shape": "arrow4",
                                                       "width": 3,
                                                       "ro": (0, 0, 90),
                                                       "color": ik_color
                                                   },
                                                   mirror_ctl_name=self.generate_name("ik", "", "ctl", True))

        name = self.generate_name("lookAtStart", "grp", "ctl")
        m = matrix.get_look_at_matrix(pos0, pos1, normal, "xz", negate)
        self.look_at_start_grp = matrix.transform(root, name, m, True)

        name = self.generate_name("cv1", "pos", "ctl")
        m = matrix.set_matrix_translate(m, pos1)
        self.cv1_pos = matrix.transform(self.look_at_start_grp, name, m, False)
        self.cv1_ctl, self.cv1_loc = self.create_ctl(context=context,
                                                     parent=self.cv1_pos,
                                                     name=self.generate_name("cv1", "", "ctl"),
                                                     parent_ctl=self.ik_ctl,
                                                     attrs=["tx", "ty", "tz"],
                                                     m=m,
                                                     cns=False,
                                                     mirror_config=(1, 0, 0, 0, 1, 1, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "circle3",
                                                         "width": 0.3,
                                                         "color": ik_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("cv1", "", "ctl", True))

        name = self.generate_name("lookAtEnd", "grp", "ctl")
        m = matrix.get_look_at_matrix(pos2, pos3, normal, "-xz", negate)
        self.look_at_end_grp = matrix.transform(self.ik_loc, name, m, True)

        name = self.generate_name("cv2", "pos", "ctl")
        m = matrix.set_matrix_translate(m, pos3)
        self.cv2_pos = matrix.transform(self.look_at_end_grp, name, m, False)
        self.cv2_ctl, self.cv2_loc = self.create_ctl(context=context,
                                                     parent=self.cv2_pos,
                                                     name=self.generate_name("cv2", "", "ctl"),
                                                     parent_ctl=self.ik_ctl,
                                                     attrs=["tx", "ty", "tz"],
                                                     m=m,
                                                     cns=False,
                                                     mirror_config=(1, 0, 0, 0, 1, 1, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "circle3",
                                                         "width": 0.3,
                                                         "color": ik_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("cv2", "", "ctl", True))

        name = self.generate_name("original", "crv", "ctl")
        self.original_crv = nurbs.create(root,
                                         name,
                                         degree=3,
                                         positions=[pos0, pos1, pos3, pos2],
                                         bezier=False,
                                         vis=False,
                                         inherits=True,
                                         display_type=1)

        name = self.generate_name("deform", "crv", "ctl")
        self.deform_crv = nurbs.create(root,
                                       name,
                                       degree=3,
                                       positions=[pos0, pos1, pos3, pos2],
                                       bezier=False,
                                       vis=False,
                                       inherits=True,
                                       display_type=1)
        for i, obj in enumerate([self.look_at_start_grp, self.cv1_loc, self.cv2_loc, self.ik_loc]):
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(obj + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", self.deform_crv + ".cv[{0}]".format(i))

        neck_jnt_positions = nurbs.point_on_curve(self.deform_crv, data["division"])
        name = self.generate_name("SP%s", "jnt", "ctl")
        self.sp_chain = joint.add_chain_joint(root,
                                              name,
                                              neck_jnt_positions,
                                              normal,
                                              negate=negate)

        name = self.generate_name("SP", "ikh", "ctl")
        self.sp_ik_h = joint.sp_ikh(root, name, self.sp_chain, self.deform_crv)

        name = self.generate_name("startUp", "loc", "ctl")
        self.start_up_loc = matrix.transform(self.root, name, matrix.get_matrix(self.sp_chain[0]))

        name = self.generate_name("lockOrient", "loc", "ctl")
        self.lock_orient_loc = matrix.transform(self.ik_loc, name, matrix.get_matrix(self.sp_chain[-1]))

        parent_ctl = self.ik_ctl
        parent = root
        self.fk_ctls = []
        self.fk_locs = []
        for i, p in enumerate(neck_jnt_positions):
            if i < len(neck_jnt_positions) - 1:
                m = matrix.get_look_at_matrix(p, neck_jnt_positions[i + 1], normal, "xz", negate)
            else:
                m = matrix.set_matrix_translate(m, neck_jnt_positions[i])
            fk_ctl, fk_loc = self.create_ctl(context=context,
                                             parent=parent,
                                             name=self.generate_name("fk" + str(i), "", "ctl"),
                                             parent_ctl=parent_ctl,
                                             attrs=["tx", "ty", "tz",
                                                    "rx", "ry", "rz",
                                                    "sx", "sy", "sz"],
                                             m=m,
                                             cns=False,
                                             mirror_config=(1, 0, 0, 0, 1, 1, 0, 0, 0),
                                             shape_args={
                                                 "shape": "cube",
                                                 "width": 0.1,
                                                 "height": 1,
                                                 "depth": 1,
                                                 "color": fk_color
                                             },
                                             mirror_ctl_name=self.generate_name("fk" + str(i), "", "ctl", True))
            parent_ctl = fk_ctl
            parent = fk_ctl
            self.fk_ctls.append(fk_ctl)
            self.fk_locs.append(fk_loc)

        name = self.generate_name("volumeOrig", "crv", "ctl")
        positions = [vector.get_position(x) for x in self.fk_ctls]
        self.orig_volume_crv = nurbs.create(root,
                                            name,
                                            degree=1,
                                            positions=positions,
                                            bezier=False,
                                            vis=False,
                                            inherits=True,
                                            display_type=1)
        name = self.generate_name("volumeDeform", "crv", "ctl")
        self.deform_volume_crv = nurbs.create(root,
                                              name,
                                              degree=1,
                                              positions=positions,
                                              bezier=False,
                                              vis=False,
                                              inherits=False,
                                              display_type=1)
        self.non_scale_fk_pos = []
        parent = root
        for i, ctl in enumerate(self.fk_ctls):
            name = self.generate_name("fk" + str(i) + "NonScale", "pos", "ctl")
            parent = matrix.transform(parent, name, om2.MMatrix())
            self.non_scale_fk_pos.append(parent)
            mc.connectAttr(ctl + ".translate", parent + ".translate")
            mc.connectAttr(ctl + ".rotate", parent + ".rotate")
        nurbs.constraint(self.deform_volume_crv, self.non_scale_fk_pos)

        # refs
        refs = []
        for i in range(len(self.fk_ctls)):
            anchor = False if i < len(self.fk_ctls) - 1 else True
            name = self.generate_name(str(i), "ref", "ctl")
            m = self.fk_locs[i]
            refs.append(self.create_ref(context=context, name=name, anchor=anchor, m=m))

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            parent = None
            for i, r in enumerate(refs):
                name = self.generate_name(str(i), "", "jnt")
                parent = self.create_jnt(context=context,
                                         parent=parent,
                                         name=name,
                                         description=str(i),
                                         ref=r,
                                         m=matrix.get_matrix(r),
                                         leaf=False,
                                         uni_scale=uni_scale)

    def attributes(self, context):
        super().attributes(context)
        host = self.host
        data = self.component.data["value"]

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
                                                longName="lock_orient",
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
        volume_inputs = [x / float(data["division"]) for x in range(data["division"] + 1)]
        stretch_values = fcurve.get_fcurve_values(stretch_volume_fcurve, division=0, inputs=volume_inputs)
        for i, value in enumerate(stretch_values):
            self.stretch_attrs.append(attribute.add_attr(self.root,
                                                         longName=f"stretch_volume_value{i}",
                                                         type="double",
                                                         keyable=False,
                                                         defaultValue=value))
        squash_values = fcurve.get_fcurve_values(squash_volume_fcurve, division=0, inputs=volume_inputs)
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
        self.cv_vis = attribute.add_attr(host,
                                         longName="cv_vis",
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

        # cv vis
        for ctl in [self.cv1_ctl, self.cv2_ctl]:
            for shape in mc.listRelatives(ctl, shapes=True, fullPath=True):
                mc.connectAttr(self.cv_vis, shape + ".v")

        # spline ik handle
        mc.setAttr(self.sp_ik_h + ".dTwistControlEnable", True)
        mc.setAttr(self.sp_ik_h + ".dWorldUpType", 4)
        mc.setAttr(self.sp_ik_h + ".dWorldUpAxis", 3)
        mc.setAttr(self.sp_ik_h + ".dWorldUpVector", 0, 0, 1)
        mc.setAttr(self.sp_ik_h + ".dWorldUpVectorEnd", 0, 0, 1)
        if negate:
            mc.setAttr(self.sp_ik_h + ".dForwardAxis", 1)
        mc.connectAttr(self.start_up_loc + ".worldMatrix[0]", self.sp_ik_h + ".dWorldUpMatrix")
        mc.connectAttr(self.lock_orient_loc + ".worldMatrix[0]", self.sp_ik_h + ".dWorldUpMatrixEnd")

        # curve info
        original_crv_shape = mc.listRelatives(self.original_crv, shapes=True, fullPath=True)[0]
        curve_info = mc.arclen(original_crv_shape, ch=1)
        original_curve_length = curve_info + ".arcLength"

        deform_crv_shape = mc.listRelatives(self.deform_crv, shapes=True, fullPath=True)[0]
        curve_info = mc.arclen(deform_crv_shape, ch=1)
        deform_curve_length = curve_info + ".arcLength"

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".operation", 2)
        mc.connectAttr(deform_curve_length, md + ".input1X")
        mc.connectAttr(original_curve_length, md + ".input2X")
        deform_curve_ratio = md + ".outputX"

        # stretch & squash
        condition = mc.createNode("condition")
        mc.connectAttr(deform_curve_ratio, condition + ".firstTerm")
        mc.connectAttr(self.max_stretch, condition + ".secondTerm")
        mc.setAttr(condition + ".operation", 2)
        mc.connectAttr(self.max_stretch, condition + ".colorIfTrueR")
        mc.connectAttr(deform_curve_ratio, condition + ".colorIfFalseR")
        max_stretch_multiple = condition + ".outColorR"

        condition = mc.createNode("condition")
        mc.connectAttr(deform_curve_ratio, condition + ".firstTerm")
        mc.connectAttr(self.max_squash, condition + ".secondTerm")
        mc.setAttr(condition + ".operation", 5)
        mc.connectAttr(self.max_squash, condition + ".colorIfTrueR")
        mc.connectAttr(deform_curve_ratio, condition + ".colorIfFalseR")
        max_squash_multiple = condition + ".outColorR"

        condition = mc.createNode("condition")
        mc.connectAttr(deform_curve_ratio, condition + ".firstTerm")
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

        # volume
        orig_volume_crv_shape = mc.listRelatives(self.orig_volume_crv, shapes=True, fullPath=True)[0]
        curve_info = mc.arclen(orig_volume_crv_shape, ch=1)
        orig_volume_curve_length = curve_info + ".arcLength"

        deform_volume_crv_shape = mc.listRelatives(self.deform_volume_crv, shapes=True, fullPath=True)[0]
        curve_info = mc.arclen(deform_volume_crv_shape, ch=1)
        deform_volume_curve_length = curve_info + ".arcLength"

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".operation", 2)
        mc.connectAttr(deform_volume_curve_length, md + ".input1X")
        mc.connectAttr(orig_volume_curve_length, md + ".input2X")
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

        for i in range(data["division"] + 1):
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
                mc.connectAttr(self.lock_orient_0, pb + ".weight")

                target = self.sp_chain[-1]
                target_parent = hierarchy.get_parent(target)

                mult_m = mc.createNode("multMatrix")
                mc.connectAttr(self.lock_orient_loc + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
                mc.connectAttr(target_parent + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

                decom_m = mc.createNode("decomposeMatrix")
                mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
                lock_orient = decom_m + ".outputRotate"

                mc.connectAttr(lock_orient, pb + ".inRotate2")
                mc.connectAttr(pb + ".outRotate", self.sp_chain[-1] + ".r")
            mc.connectAttr(self.sp_chain[i] + ".matrix", npo + ".offsetParentMatrix")
            mc.connectAttr(self.sp_chain[i] + ".matrix", self.non_scale_fk_pos[i] + ".offsetParentMatrix")

        # tangent
        distance = mc.createNode("distanceBetween")
        decom = mc.createNode("decomposeMatrix")
        mc.connectAttr(self.look_at_start_grp + ".worldMatrix[0]", decom + ".inputMatrix")
        mc.connectAttr(decom + ".outputTranslate", distance + ".point1")
        decom = mc.createNode("decomposeMatrix")
        mc.connectAttr(self.ik_loc + ".worldMatrix[0]", decom + ".inputMatrix")
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

        cv1_tx = mc.getAttr(self.cv1_pos + ".tx")
        md = mc.createNode("multiplyDivide")
        mc.connectAttr(normalize_distance, md + ".input1X")
        mc.setAttr(md + ".input2X", cv1_tx)
        cv1_scaled_offset_value = md + ".outputX"

        cv2_tx = mc.getAttr(self.cv2_pos + ".tx")
        md = mc.createNode("multiplyDivide")
        mc.connectAttr(normalize_distance, md + ".input1X")
        mc.setAttr(md + ".input2X", cv2_tx)
        cv2_scaled_offset_value = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(self.tangent0, md + ".input1X")
        mc.connectAttr(self.tangent1, md + ".input1Y")
        mc.connectAttr(cv1_scaled_offset_value, md + ".input2X")
        mc.connectAttr(cv2_scaled_offset_value, md + ".input2Y")
        tan0_value = md + ".outputX"
        tan1_value = md + ".outputY"

        mc.connectAttr(tan0_value, self.cv1_pos + ".tx")
        mc.connectAttr(tan1_value, self.cv2_pos + ".tx")

    def connections(self, context):
        super().connections(context)
