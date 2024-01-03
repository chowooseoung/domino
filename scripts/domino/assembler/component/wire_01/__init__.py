# domino
from domino.lib import matrix, attribute, hierarchy
from domino.lib.rigging import nurbs, joint
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
    name = "wire"
    side = "C"
    index = 0
    description = ("wire component 입니다. head, tail을 고정시킬수있습니다. splineIK를 사용합니다."
                   "nurbsCurve를 등록. curve의 cvPoint에 컨트롤러가 생성됩니다."
                   "range숫자만큼의 앞, 뒤 컨트롤러를 다른 component에 parent할수있습니다."
                   "path 컨트롤러는 fk 구조를 가질수있습니다.")


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "division": {"type": "long", "minValue": 1},
        "wire_curve": {"type": "nurbsCurve"},
        "head_parent": {"type": "string"},
        "head_range": {"type": "long", "minValue": 1},
        "tail_parent": {"type": "string"},
        "tail_range": {"type": "long", "minValue": 1},
        "up_normal_x": {"type": "double"},
        "up_normal_y": {"type": "double"},
        "up_normal_z": {"type": "double"},
        "fk_path": {"type": "bool"},
        "turning_point": {"type": "double", "minValue": 0, "maxValue": 1}
    })

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(om2.MMatrix())],
        "division": 30,
        "head_range": 1,
        "tail_range": 1,
        "up_normal_y": 1,
    })
    common_preset["nurbs_curve"].update({
        "wire_curve": None
    })
    return common_preset


def guide_recipe():
    return {}


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        wire_curve = self.component.data["nurbs_curve"]["wire_curve"]["0"]

        ik_color = self.generate_color("ik")

        division = data["division"] - 1

        self.create_root(context)
        orig_m = om2.MMatrix()
        self.origin_space = matrix.transform(parent=self.root,
                                             name=self.generate_name("origin", "space", "ctl"),
                                             m=orig_m)

        self.wire_orig_curve = nurbs.build(wire_curve,
                                           name=self.generate_name("orig", "crv", "ctl"),
                                           parent=self.origin_space,
                                           match=True)
        mc.setAttr(self.wire_orig_curve + ".v", 0)
        self.path_deform_curve = nurbs.build(wire_curve,
                                             name=self.generate_name("deform", "crv", "ctl"),
                                             parent=self.origin_space,
                                             match=True,
                                             inherits=False)
        mc.setAttr(self.path_deform_curve + ".overrideEnabled", 1)
        mc.setAttr(self.path_deform_curve + ".overrideDisplayType", 2)

        normal = om2.MVector(data["up_normal_x"], data["up_normal_y"], data["up_normal_z"])
        self.path_up_curve, offset_curve = mc.offsetCurve(self.wire_orig_curve,
                                                          name=self.generate_name("up", "crv", "ctl"),
                                                          constructionHistory=True,
                                                          range=False,
                                                          connectBreaks=2,
                                                          stitch=True,
                                                          cutLoop=True,
                                                          cutRadius=0,
                                                          distance=0.2,
                                                          tolerance=0.01,
                                                          subdivisionDensity=0,
                                                          normal=normal,
                                                          useGivenNormal=True)
        mc.connectAttr(self.wire_orig_curve + ".local", offset_curve + ".inputCurve", force=True)
        mc.delete(offset_curve)
        self.path_up_curve = mc.parent(self.path_up_curve, self.origin_space)[0]
        mc.setAttr(self.path_up_curve + ".overrideEnabled", 1)
        mc.setAttr(self.path_up_curve + ".overrideDisplayType", 2)
        mc.setAttr(self.path_up_curve + ".inheritsTransform", 0)

        self.orig_curve_length_attr = nurbs.get_length_attr(self.wire_orig_curve, False)
        self.deform_curve_length_attr = nurbs.get_length_attr(self.path_deform_curve, False)

        fn_curve = nurbs.get_fn_curve(self.wire_orig_curve)
        positions = [om2.MVector(x.x, x.y, x.z) for x in fn_curve.cvPositions(om2.MSpace.kWorld)]

        self.path_ctls = []
        matrices = matrix.get_chain_matrix2(positions, normal)
        parent = self.origin_space
        for i, m in enumerate(matrices):
            ctl, loc = self.create_ctl(context=context,
                                       parent=parent,
                                       name=self.generate_name("path" + str(i), "", "ctl"),
                                       m=m,
                                       parent_ctl=None,
                                       attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                       mirror_config=(0, 1, 0, 1, 0, 1, 0, 0, 0),
                                       shape_args={
                                           "shape": "axis",
                                           "width": 0.2,
                                           "height": 0.2,
                                           "depth": 0.2,
                                           "color": ik_color
                                       },
                                       mirror_ctl_name=self.generate_name("path" + str(i), "", "ctl", True))
            mc.cluster([self.path_deform_curve + ".cv[{0}]".format(i),
                        self.path_up_curve + ".cv[{0}]".format(i)],
                       bindState=True,
                       weightedNode=(loc, loc))
            self.path_ctls.append(ctl)
            if data["fk_path"]:
                parent = loc

        self.wire_curve = nurbs.build(wire_curve,
                                      name=self.generate_name("wire", "crv", "ctl"),
                                      parent=self.origin_space,
                                      match=True,
                                      inherits=False)
        self.wire_up_curve = nurbs.build(wire_curve,
                                      name=self.generate_name("wireUp", "crv", "ctl"),
                                      parent=self.origin_space,
                                      match=True,
                                      inherits=False)
        mc.hide([self.wire_curve, self.wire_up_curve])

        orig_curve_length = mc.getAttr(self.orig_curve_length_attr)
        division_length = orig_curve_length / division

        m = om2.MMatrix()
        parent = self.origin_space
        self.wire_joints = []
        wire_decom_m = []
        for i in range(division + 1):
            parent = joint.add_joint(parent=parent,
                                     name=self.generate_name("wire" + str(i), "pos", "ctl"),
                                     m=m,
                                     vis=False)
            if i > 0:
                mc.setAttr(parent + ".tx", division_length)
            self.wire_joints.append(parent)

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(parent + ".worldMatrix[0]", decom_m + ".inputMatrix")
            wire_decom_m.append(decom_m)
        wire_ikh = joint.sp_ikh(self.origin_space,
                                self.generate_name("wire", "ikh", "ctl"),
                                self.wire_joints,
                                self.wire_curve)
        mc.delete(wire_ikh)
        mc.makeIdentity(self.wire_joints, apply=True, rotate=True)
        wire_ikh = joint.sp_ikh(self.origin_space,
                                self.generate_name("wire", "ikh", "ctl"),
                                self.wire_joints,
                                self.wire_curve)
        mc.setAttr(wire_ikh + ".offset", lock=True)

        parent = self.origin_space
        self.up_joints = []
        up_decom_m = []
        for i in range(division + 1):
            parent = joint.add_joint(parent=parent,
                                     name=self.generate_name("up" + str(i), "pos", "ctl"),
                                     m=m,
                                     vis=False)
            mc.setAttr(parent + ".tx", division_length)
            self.up_joints.append(parent)

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(parent + ".worldMatrix[0]", decom_m + ".inputMatrix")
            up_decom_m.append(decom_m)
        up_ikh = joint.sp_ikh(self.origin_space,
                              self.generate_name("up", "ikh", "ctl"),
                              self.up_joints,
                              self.wire_up_curve)
        mc.delete(up_ikh)
        mc.makeIdentity(self.up_joints, apply=True, rotate=True)
        up_ikh = joint.sp_ikh(self.origin_space,
                              self.generate_name("up", "ikh", "ctl"),
                              self.up_joints,
                              self.wire_up_curve)
        mc.setAttr(up_ikh + ".offset", lock=True)

        parent = self.origin_space
        parent_space = self.origin_space
        self.forward_ctls = []
        up_vec_attrs = []
        self.forward_choice_nodes = []
        com_m = mc.createNode("composeMatrix")
        length = mc.getAttr(self.wire_joints[1] + ".tx")
        for i in range(division + 1):
            if i == division:
                target = self.wire_joints[i - 1]
                aim_vector = (-1, 0, 0)
            else:
                target = self.wire_joints[i + 1]
                aim_vector = (1, 0, 0)

            pma = mc.createNode("plusMinusAverage")
            mc.setAttr(pma + ".operation", 2)
            mc.connectAttr(up_decom_m[i] + ".outputTranslate", pma + ".input3D[0]")
            mc.connectAttr(wire_decom_m[i] + ".outputTranslate", pma + ".input3D[1]")
            up_vec_attr = pma + ".output3D"
            up_vec_attrs.append(up_vec_attr)

            parent_space = matrix.transform(parent=parent_space,
                                            name=self.generate_name("forward" + str(i), "space", "ctl"),
                                            m=m)
            mc.connectAttr(self.wire_joints[i] + ".t", parent_space + ".t")
            aim_m = mc.createNode("aimMatrix")
            mc.setAttr(aim_m + ".primaryMode", 1)
            mc.setAttr(aim_m + ".primaryInputAxis", *aim_vector)
            mc.setAttr(aim_m + ".secondaryMode", 1)
            mc.connectAttr(self.wire_joints[i] + ".worldMatrix[0]", aim_m + ".inputMatrix")
            mc.connectAttr(target + ".worldMatrix[0]", aim_m + ".primaryTargetMatrix")
            mc.connectAttr(self.up_joints[i] + ".worldMatrix[0]", aim_m + ".secondaryTargetMatrix")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(aim_m + ".outputMatrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(parent_space + ".parentInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputRotate", parent_space + ".r")

            ctl, parent = self.create_ctl(context=context,
                                          parent=parent,
                                          name=self.generate_name("forward" + str(i), "", "ctl"),
                                          m=m,
                                          parent_ctl=None,
                                          attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                          mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                          shape_args={
                                              "shape": "cube",
                                              "width": length,
                                              "height": 1,
                                              "depth": 1,
                                              "color": 21,
                                              "po": (length / 2, 0, 0)
                                          },
                                          mirror_ctl_name=self.generate_name("forward" + str(i), "", "ctl", True))
            attribute.add_attr(ctl,
                               longName="turning_point",
                               type="double",
                               defaultValue=float(i) / division)

            npo = hierarchy.get_parent(ctl)
            mc.setAttr(npo + ".offsetParentMatrix", m, type="matrix")

            choice = mc.createNode("choice")
            mc.connectAttr(ctl + ".inverseMatrix", choice + ".input[0]")
            mc.connectAttr(com_m + ".outputMatrix", choice + ".input[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(choice + ".output", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", parent + ".t")
            mc.connectAttr(decom_m + ".outputRotate", parent + ".r")
            self.forward_choice_nodes.append(choice)

            mc.connectAttr(parent_space + ".t", npo + ".t")
            mc.connectAttr(parent_space + ".r", npo + ".r")
            self.forward_ctls.append(ctl)

        parent = self.origin_space
        parent_space = self.origin_space
        self.reverse_ctls = []
        up_vec_attrs.reverse()
        self.wire_joints.reverse()
        self.up_joints.reverse()
        self.reverse_choice_nodes = []
        for i in range(division + 1):
            if i == 0:
                target = self.wire_joints[i + 1]
                aim_vector = (-1, 0, 0)
            else:
                target = self.wire_joints[i - 1]
                aim_vector = (1, 0, 0)

            parent_space = matrix.transform(parent=parent_space,
                                            name=self.generate_name("reverse" + str(i), "space", "ctl"),
                                            m=m)
            mc.pointConstraint(self.wire_joints[i], parent_space)
            aim_m = mc.createNode("aimMatrix")
            mc.setAttr(aim_m + ".primaryMode", 1)
            mc.setAttr(aim_m + ".primaryInputAxis", *aim_vector)
            mc.setAttr(aim_m + ".secondaryMode", 1)
            mc.connectAttr(self.wire_joints[i] + ".worldMatrix[0]", aim_m + ".inputMatrix")
            mc.connectAttr(target + ".worldMatrix[0]", aim_m + ".primaryTargetMatrix")
            mc.connectAttr(self.up_joints[i] + ".worldMatrix[0]", aim_m + ".secondaryTargetMatrix")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(aim_m + ".outputMatrix", mult_m + ".matrixIn[0]")
            mc.connectAttr(parent_space + ".parentInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputRotate", parent_space + ".r")

            ctl, parent = self.create_ctl(context=context,
                                          parent=parent,
                                          name=self.generate_name("reverse" + str(i), "", "ctl"),
                                          m=m,
                                          parent_ctl=None,
                                          attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                          mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                          shape_args={
                                              "shape": "cube",
                                              "width": length,
                                              "height": 1,
                                              "depth": 1,
                                              "color": 28,
                                              "po": (length / -2, 0, 0)
                                          },
                                          mirror_ctl_name=self.generate_name("reverse" + str(i), "", "ctl", True))
            value = 1 - float(i + 1) / division
            attribute.add_attr(ctl,
                               longName="turning_point",
                               type="double",
                               defaultValue=value if value > 0 else 0)

            npo = hierarchy.get_parent(ctl)
            mc.setAttr(npo + ".offsetParentMatrix", m, type="matrix")

            choice = mc.createNode("choice")
            mc.connectAttr(ctl + ".inverseMatrix", choice + ".input[0]")
            mc.connectAttr(com_m + ".outputMatrix", choice + ".input[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(choice + ".output", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", parent + ".t")
            mc.connectAttr(decom_m + ".outputRotate", parent + ".r")
            self.reverse_choice_nodes.append(choice)

            mc.connectAttr(parent_space + ".t", npo + ".t")
            mc.connectAttr(parent_space + ".r", npo + ".r")
            self.reverse_ctls.append(ctl)
        self.wire_joints.reverse()

        # refs
        self.reverse_ctls.reverse()
        self.ref_point_cons = []
        self.ref_orient_cons = []
        self.ref_scale_condition = []
        spaces = []
        for i in range(division + 1):
            space = matrix.transform(parent=self.origin_space,
                                     name=self.generate_name("ref" + str(i), "space", "ctl"),
                                     m=m)
            forward_loc = mc.listRelatives(self.forward_ctls[i], children=True, fullPath=True, type="transform")[0]
            reverse_loc = mc.listRelatives(self.reverse_ctls[i], children=True, fullPath=True, type="transform")[0]
            point_cons = mc.pointConstraint([forward_loc, reverse_loc], space)[0]
            orient_cons = mc.orientConstraint([forward_loc, reverse_loc], space)[0]

            condition = mc.createNode("condition")
            mc.setAttr(condition + ".operation", 0)
            mc.setAttr(condition + ".secondTerm", 1)

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(forward_loc + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.origin_space + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputScale", condition + ".colorIfTrue")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(reverse_loc + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.origin_space + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputScale", condition + ".colorIfFalse")
            mc.connectAttr(condition + ".outColor", space + ".s")
            self.ref_point_cons.append(point_cons)
            self.ref_orient_cons.append(orient_cons)
            self.ref_scale_condition.append(condition)

            attr1, attr2 = mc.pointConstraint(point_cons, query=True, weightAliasList=True)
            mc.setAttr(point_cons + "." + attr1, 1)
            mc.setAttr(point_cons + "." + attr2, 0)
            attr1, attr2 = mc.orientConstraint(orient_cons, query=True, weightAliasList=True)
            mc.setAttr(orient_cons + "." + attr1, 1)
            mc.setAttr(orient_cons + "." + attr2, 0)
            spaces.append(space)
        self.reverse_ctls.reverse()

        self.refs = []
        for i, space in enumerate(spaces):
            ref = self.create_ref(context=context,
                                  name=self.generate_name(str(i), "ref", "ctl"),
                                  anchor=False,
                                  m=space)
            self.refs.append(ref)

        # wire curve setup
        md = mc.createNode("multiplyDivide")
        mc.connectAttr(self.deform_curve_length_attr, md + ".input1X")
        mc.connectAttr(self.orig_curve_length_attr, md + ".input2X")
        mc.setAttr(md + ".operation", 2)
        self.curve_ratio_attr = md + ".outputX"

        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".input1D[0]", 0)
        mc.setAttr(pma + ".input1D[1]", 1)
        self.offset_attr_destination = pma + ".input1D[0]"

        bta = mc.createNode("blendTwoAttr")
        mc.connectAttr(pma + ".output1D", bta + ".input[0]")
        mc.setAttr(bta + ".input[1]", 1)
        mc.setAttr(bta + ".attributesBlender", 0)
        end_length_u_value_attr = bta + ".output"
        self.stretch_attr_destination = bta + ".attributesBlender"

        mp = mc.createNode("motionPath")
        mc.setAttr(mp + ".fractionMode", True)
        mc.connectAttr(self.path_deform_curve + ".worldSpace[0]", mp + ".geometryPath")
        mc.setAttr(mp + ".uValue", 0)
        self.offset_attr_destination1 = mp + ".uValue"

        npoc = mc.createNode("nearestPointOnCurve")
        mc.connectAttr(self.path_deform_curve + ".worldSpace[0]", npoc + ".inputCurve")
        mc.connectAttr(mp + ".allCoordinates", npoc + ".inPosition")
        start_u_value_attr = npoc + ".parameter"

        mp = mc.createNode("motionPath")
        mc.setAttr(mp + ".fractionMode", True)
        mc.connectAttr(self.path_deform_curve + ".worldSpace[0]", mp + ".geometryPath")
        mc.connectAttr(end_length_u_value_attr, mp + ".uValue")

        npoc = mc.createNode("nearestPointOnCurve")
        mc.connectAttr(self.path_deform_curve + ".worldSpace[0]", npoc + ".inputCurve")
        mc.connectAttr(mp + ".allCoordinates", npoc + ".inPosition")
        end_u_value_attr = npoc + ".parameter"

        detach_curve = mc.createNode("detachCurve")
        mc.connectAttr(self.path_deform_curve + ".worldSpace[0]", detach_curve + ".inputCurve")
        mc.connectAttr(start_u_value_attr, detach_curve + ".parameter[0]")
        mc.connectAttr(end_u_value_attr, detach_curve + ".parameter[1]")
        mc.connectAttr(detach_curve + ".outputCurve[1]", self.wire_curve + ".create")

        detach_curve = mc.createNode("detachCurve")
        mc.connectAttr(self.path_up_curve + ".worldSpace[0]", detach_curve + ".inputCurve")
        mc.connectAttr(start_u_value_attr, detach_curve + ".parameter[0]")
        mc.connectAttr(end_u_value_attr, detach_curve + ".parameter[1]")
        mc.connectAttr(detach_curve + ".outputCurve[1]", self.wire_up_curve + ".create")

        # stretch
        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".operation", 2)
        mc.connectAttr(self.curve_ratio_attr, pma + ".input1D[0]")
        mc.setAttr(pma + ".input1D[1]", 1)

        condition = mc.createNode("condition")
        mc.setAttr(condition + ".operation", 2)
        mc.connectAttr(pma + ".output1D", condition + ".firstTerm")
        mc.setAttr(condition + ".secondTerm", 0)
        mc.connectAttr(pma + ".output1D", condition + ".colorIfTrueR")
        mc.setAttr(condition + ".colorIfFalseR", 0)

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(condition + ".outColorR", md + ".input1X")
        mc.setAttr(md + ".input2X", 0)
        stretch_attr = md + ".outputX"
        self.stretch_attr_destination1 = md + ".input2X"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(stretch_attr, md + ".input1X")
        mc.setAttr(md + ".input2X", mc.getAttr(self.wire_joints[1] + ".tx"))

        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".input1D[0]", mc.getAttr(self.wire_joints[1] + ".tx"))
        mc.connectAttr(md + ".outputX", pma + ".input1D[1]")
        stretch_value_attr = pma + ".output1D"

        for i in range(1, len(self.up_joints)):
            mc.connectAttr(stretch_value_attr, self.wire_joints[i] + ".tx")
            mc.connectAttr(stretch_value_attr, self.up_joints[i] + ".tx")

        # turning point
        self.turning_point_attr_destination = []
        for i in range(len(self.forward_ctls)):
            forward_ctl_shapes = mc.listRelatives(self.forward_ctls[i], shapes=True, fullPath=True)
            reverse_ctl_shapes = mc.listRelatives(self.reverse_ctls[i], shapes=True, fullPath=True)
            forward_ctl_position = mc.getAttr(self.forward_ctls[i] + ".turning_point")
            reverse_ctl_position = mc.getAttr(self.reverse_ctls[i] + ".turning_point")

            condition = mc.createNode("condition")
            mc.setAttr(condition + ".firstTerm", data["turning_point"])
            self.turning_point_attr_destination.append(condition + ".firstTerm")
            mc.setAttr(condition + ".secondTerm", forward_ctl_position)
            mc.setAttr(condition + ".operation", 5 if i == 0 else 4)
            mc.setAttr(condition + ".colorIfTrueR", 1)
            mc.setAttr(condition + ".colorIfFalseR", 0)
            forward_condition_attr = condition + ".outColorR"
            mc.connectAttr(forward_condition_attr, self.forward_choice_nodes[i] + ".selector")
            for shape in forward_ctl_shapes:
                mc.connectAttr(forward_condition_attr, shape + ".v")

            condition = mc.createNode("condition")
            mc.setAttr(condition + ".firstTerm", data["turning_point"])
            self.turning_point_attr_destination.append(condition + ".firstTerm")
            mc.setAttr(condition + ".secondTerm", reverse_ctl_position)
            mc.setAttr(condition + ".operation", 2 if i >= len(self.forward_ctls) - 2 else 3)
            mc.setAttr(condition + ".colorIfTrueR", 1)
            mc.setAttr(condition + ".colorIfFalseR", 0)
            reverse_condition_attr = condition + ".outColorR"
            mc.connectAttr(reverse_condition_attr, self.reverse_choice_nodes[i] + ".selector")
            for shape in reverse_ctl_shapes:
                mc.connectAttr(reverse_condition_attr, shape + ".v")

            rev = mc.createNode("reverse")
            mc.connectAttr(forward_condition_attr, rev + ".inputX")
            rev_attr = rev + ".outputX"
            attr1, attr2 = mc.pointConstraint(self.ref_point_cons[i], query=True, weightAliasList=True)
            mc.connectAttr(forward_condition_attr, self.ref_point_cons[i] + "." + attr1)
            mc.connectAttr(rev_attr, self.ref_point_cons[i] + "." + attr2)
            attr1, attr2 = mc.orientConstraint(self.ref_orient_cons[i], query=True, weightAliasList=True)
            mc.connectAttr(forward_condition_attr, self.ref_orient_cons[i] + "." + attr1)
            mc.connectAttr(rev_attr, self.ref_orient_cons[i] + "." + attr2)
            mc.connectAttr(forward_condition_attr, self.ref_scale_condition[i] + ".firstTerm")


        # remap scale setup
        remap = mc.createNode("remapValue")

        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".operation", 2)
        mc.setAttr(pma + ".input1D[0]", 0.5)
        mc.setAttr(pma + ".input1D[1]", 0.5)
        mc.connectAttr(pma + ".output1D", remap + ".value[0].value_Position")
        mc.setAttr(remap + ".value[0].value_FloatValue", 0)
        mc.setAttr(remap + ".value[0].value_Interp", 2)
        self.scale_position_attr_destination = pma + ".input1D[0]"
        self.scale_left_range_attr_destination = pma + ".input1D[1]"
        self.scale_left_value_attr_destination = remap + ".value[0].value_FloatValue"

        mc.setAttr(remap + ".value[1].value_Position", 0.5)
        self.scale_position_attr_destination1 = remap +".value[1].value_Position"
        mc.setAttr(remap + ".value[1].value_FloatValue", 0)
        mc.setAttr(remap + ".value[1].value_Interp", 2)
        self.scale_value_attr_destination = remap + ".value[1].value_FloatValue"

        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".input1D[0]", 0.5)
        self.scale_position_attr_destination2 = pma + ".input1D[0]"
        mc.setAttr(pma + ".input1D[1]", 0.5)
        self.scale_right_range_attr_destination = pma + ".input1D[1]"
        mc.connectAttr(pma + ".output1D", remap + ".value[2].value_Position")
        mc.setAttr(remap + ".value[2].value_FloatValue", 0)
        self.scale_right_value_attr_destination = remap + ".value[2].value_FloatValue"
        mc.setAttr(remap + ".value[2].value_Interp", 2)

        for i, ref in enumerate(self.refs):
            mc.setAttr(ref + ".s", lock=False)
            mc.setAttr(ref + ".sx", lock=False)
            mc.setAttr(ref + ".sy", lock=False)
            mc.setAttr(ref + ".sz", lock=False)

            rm = mc.createNode("remapValue")
            mc.setAttr(rm + ".inputValue", float(i) / len(self.refs))
            mc.setAttr(rm + ".inputMin", 0)
            mc.setAttr(rm + ".inputMax", 1)
            mc.setAttr(rm + ".outputMin", 1)
            mc.setAttr(rm + ".outputMax", 2)
            mc.connectAttr(remap + ".value", rm + ".value")

            mc.connectAttr(rm + ".outValue", ref + ".sy")
            mc.connectAttr(rm + ".outValue", ref + ".sz")

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            parent = None
            for i, r in enumerate(self.refs):
                m = matrix.get_matrix(r)
                name = self.generate_name(str(i), "", "jnt")
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

        data = self.component.data["value"]
        host = self.host

        self.offset_attr = attribute.add_attr(host,
                                              longName="offset",
                                              type="double",
                                              keyable=True,
                                              minValue=0,
                                              maxValue=0.9999)
        self.stretch_attr = attribute.add_attr(host,
                                               longName="stretch",
                                               type="double",
                                               keyable=True,
                                               minValue=0,
                                               maxValue=1)
        self.scale_left_range_attr = attribute.add_attr(host,
                                                        longName="scale_left_range",
                                                        type="double",
                                                        minValue=0.001,
                                                        maxValue=1,
                                                        defaultValue=0.5,
                                                        keyable=True)
        self.scale_left_value_attr = attribute.add_attr(host,
                                                        longName="scale_left_value",
                                                        type="double",
                                                        minValue=0,
                                                        defaultValue=0,
                                                        keyable=True)
        self.scale_position_attr = attribute.add_attr(host,
                                                      longName="scale_position",
                                                      type="double",
                                                      minValue=0,
                                                      maxValue=1,
                                                      defaultValue=0.5,
                                                      keyable=True)
        self.scale_value_attr = attribute.add_attr(host,
                                                   longName="scale_value",
                                                   type="double",
                                                   minValue=0,
                                                   defaultValue=0,
                                                   keyable=True)
        self.scale_right_range_attr = attribute.add_attr(host,
                                                         longName="scale_right_range",
                                                         type="double",
                                                         minValue=0.001,
                                                         maxValue=1,
                                                         defaultValue=0.5,
                                                         keyable=True)
        self.scale_right_value_attr = attribute.add_attr(host,
                                                         longName="scale_right_value",
                                                         type="double",
                                                         minValue=0,
                                                         maxValue=1,
                                                         defaultValue=0,
                                                         keyable=True)
        self.turning_point_attr = attribute.add_attr(host,
                                                     longName="turning_point",
                                                     type="double",
                                                     keyable=True,
                                                     minValue=0,
                                                     defaultValue=data["turning_point"])
        self.fk_vis_attr = attribute.add_attr(host,
                                              longName="fk_vis",
                                              type="enum",
                                              enumName="off:on",
                                              defaultValue=0,
                                              keyable=True)

    def operators(self, context):
        super().operators(context)

        # fk vis
        mc.connectAttr(self.fk_vis_attr, hierarchy.get_parent(self.forward_ctls[0]) + ".v")
        mc.connectAttr(self.fk_vis_attr, hierarchy.get_parent(self.reverse_ctls[0]) + ".v")

        # wire attribute setup
        mc.connectAttr(self.offset_attr, self.offset_attr_destination)
        mc.connectAttr(self.offset_attr, self.offset_attr_destination1)
        mc.connectAttr(self.stretch_attr, self.stretch_attr_destination)
        mc.connectAttr(self.stretch_attr, self.stretch_attr_destination1)
        for destination in self.turning_point_attr_destination:
            mc.connectAttr(self.turning_point_attr, destination)
        mc.connectAttr(self.scale_position_attr, self.scale_position_attr_destination)
        mc.connectAttr(self.scale_position_attr, self.scale_position_attr_destination1)
        mc.connectAttr(self.scale_position_attr, self.scale_position_attr_destination2)
        mc.connectAttr(self.scale_left_range_attr, self.scale_left_range_attr_destination)
        mc.connectAttr(self.scale_left_value_attr, self.scale_left_value_attr_destination)
        mc.connectAttr(self.scale_value_attr, self.scale_value_attr_destination)
        mc.connectAttr(self.scale_right_range_attr, self.scale_right_range_attr_destination)
        mc.connectAttr(self.scale_right_value_attr, self.scale_right_value_attr_destination)

    def connections(self, context):
        super().connections(context)

        data = self.component.data["value"]

        if not data["fk_path"] and data["head_parent"]:
            head_parent = context[data["head_parent"]]["root"]
            head_ctls = self.path_ctls[:data["head_range"]]
            for ctl in head_ctls:
                npo = hierarchy.get_parent(ctl)
                mc.parent(npo, head_parent)
        if not data["fk_path"] and data["tail_parent"]:
            tail_parent = context[data["tail_parent"]]["root"]
            tail_ctls = self.path_ctls[data["head_range"] * -1:]
            for ctl in tail_ctls:
                npo = hierarchy.get_parent(ctl)
                mc.parent(npo, tail_parent)
