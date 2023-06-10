# domino
from domino.lib import attribute, matrix, vector, hierarchy
from domino.lib.rigging import controller
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
    name = "foot"
    side = "C"
    index = 0
    description = ("발 입니다. 원하는 관절의 수를 지정할 수 있습니다. leg_2jnt_01과 연결될 수 있습니다."
                   "\n- 주의사항 : heel, tip, toe 는 일직선 위에 놓여 있어야 합니다. "
                   "in, out, toe 는 normal 을 구하는데 사용됩니다.\n"
                   "fk chain 또한 같은 평면 위에 있어야합니다.")


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset": {"type": "doubleAngle"},
        "offset_matrix": {"type": "matrix"},
        "roll_angle": {"type": "double"},
        "connector": {"type": "string"},
    })

    def _anchors():
        m = om2.MMatrix()
        t_m = om2.MTransformationMatrix()
        t_m.setRotation(om2.MEulerRotation([math.radians(x) for x in (0, -90, 0)]))
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))  # root
        m2 = matrix.set_matrix_translate(m, (0, -2, -1))  # heel
        m3 = matrix.set_matrix_translate(m, (-1, -2, 0))  # in
        m3 = matrix.set_matrix_rotate(m3, t_m)
        m4 = matrix.set_matrix_translate(m, (1, -2, 0))  # out
        m4 = matrix.set_matrix_rotate(m4, t_m)
        m5 = matrix.set_matrix_translate(m, (0, -2, 1))  # tip
        m6 = matrix.set_matrix_translate(m, (0, -2, 2))  # toe
        return m1, m2, m3, m4, m5, m6

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "offset": -90,
        "offset_matrix": list(om2.MMatrix()),
        "roll_angle": -20,
        "connector": "default",
    })
    return common_preset


def guide_recipe():
    return {
        "position": [
            (0, "heel"),
            (1, "in", "ori"),  # parent node index, extension
            (1, "out", "ori"),
            (1, "tip"),
            (4, "toe")
        ],
        "orientation": (6, "ori"),  # target node index, extension
        "display_curve": [
            ((0, 1, 4, 5), "dpCrv"),  # source node indexes, extension
            ((1, 2), "dpInCrv"),  # source node indexes, extension
            ((1, 3), "dpOutCrv"),  # source node indexes, extension
        ],
        "flexible_position": (7, "pos%s", (0, 0, 1))  # anchor min value, extension
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        root_pos = data["anchors"][0][12:-1]
        heel_pos = data["anchors"][1][12:-1]
        in_m = om2.MMatrix(data["anchors"][2])
        in_m = matrix.set_matrix_scale(in_m, (1, 1, 1))
        out_m = om2.MMatrix(data["anchors"][3])
        out_m = matrix.set_matrix_scale(out_m, (1, 1, 1))
        tip_pos = data["anchors"][4][12:-1]
        toe_pos = data["anchors"][5][12:-1]

        orient_xyz = vector.OrientXYZ(om2.MMatrix(data["offset_matrix"]))
        normal = orient_xyz.y * (1 if self.component.negate else -1)
        bi_normal = orient_xyz.z * (-1 if self.component.negate else 1)

        fk_positions = [x[12:-1] for x in data["anchors"][6:]]
        fk_matrices = matrix.get_chain_matrix(fk_positions, normal, self.component.negate)
        fk_matrices.append(matrix.set_matrix_translate(fk_matrices[-1], fk_positions[-1]))

        total_length = vector.get_distance(heel_pos, tip_pos)
        div_length = vector.get_distance(fk_positions[0], fk_positions[1])

        root = self.create_root(context)
        fk_color = self.generate_color("fk")
        ik_color = self.generate_color("ik")

        heel_m = matrix.get_look_at_matrix(heel_pos, toe_pos, normal, "xz", self.component.negate)
        tip_m = matrix.get_look_at_matrix(tip_pos, toe_pos, normal, "xz", self.component.negate)
        toe_m = matrix.set_matrix_translate(heel_m, toe_pos)

        m = matrix.set_matrix_translate(heel_m, root_pos)
        self.roll_ctl, self.roll_loc = self.create_ctl(context=context,
                                                       parent=root,
                                                       name=self.generate_name("roll", "", "ctl"),
                                                       parent_ctl=None,
                                                       attrs=["rx", "rz"],
                                                       m=m,
                                                       cns=False,
                                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                       shape_args={
                                                           "shape": "dodecahedron",
                                                           "color": ik_color,
                                                           "width": div_length / total_length,
                                                           "height": div_length / total_length,
                                                           "depth": div_length / total_length,
                                                           "ro": (0, 0, 90)
                                                       },
                                                       mirror_ctl_name=self.generate_name("roll", "", "ctl", True))
        mc.setAttr(self.roll_ctl + ".rotateOrder", 5)
        mc.setAttr(self.roll_ctl + ".rotateOrder", lock=True)

        self.in_ctl, self.in_loc = self.create_ctl(context=context,
                                                   parent=root,
                                                   name=self.generate_name("in", "", "ctl"),
                                                   parent_ctl=None,
                                                   attrs=["rx", "ry", "rz"],
                                                   m=in_m,
                                                   cns=False,
                                                   mirror_config=(0, 0, 0, 1, 1, 0, 0, 0, 0),
                                                   shape_args={
                                                       "shape": "halfmoon",
                                                       "color": ik_color,
                                                       "width": div_length / total_length,
                                                       "ro": (0, -90 if self.component.negate else 90, 0, 90)
                                                   },
                                                   mirror_ctl_name=self.generate_name("in", "", "ctl", True))
        self.out_ctl, self.out_loc = self.create_ctl(context=context,
                                                     parent=self.in_loc,
                                                     name=self.generate_name("out", "", "ctl"),
                                                     parent_ctl=self.in_ctl,
                                                     attrs=["rx", "ry", "rz"],
                                                     m=out_m,
                                                     cns=False,
                                                     mirror_config=(0, 0, 0, 1, 1, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "halfmoon",
                                                         "color": ik_color,
                                                         "width": div_length / total_length,
                                                         "ro": (0, 90 if self.component.negate else -90, 0)
                                                     },
                                                     mirror_ctl_name=self.generate_name("out", "", "ctl", True))
        self.heel_ctl, self.heel_loc = self.create_ctl(context=context,
                                                       parent=self.out_loc,
                                                       name=self.generate_name("heel", "", "ctl"),
                                                       parent_ctl=self.out_ctl,
                                                       attrs=["rx", "ry", "rz"],
                                                       m=heel_m,
                                                       cns=False,
                                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                       shape_args={
                                                           "shape": "halfmoon",
                                                           "color": ik_color,
                                                           "width": div_length / total_length,
                                                           "ro": (0, 180 if self.component.negate else 0, 0)
                                                       },
                                                       mirror_ctl_name=self.generate_name("heel", "", "ctl", True))
        self.tip_ctl, self.tip_loc = self.create_ctl(context=context,
                                                     parent=self.heel_loc,
                                                     name=self.generate_name("tip", "", "ctl"),
                                                     parent_ctl=self.heel_ctl,
                                                     attrs=["rx", "ry", "rz"],
                                                     m=tip_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "square",
                                                         "color": ik_color,
                                                         "width": div_length / total_length,
                                                         "height": div_length / total_length,
                                                         "up": "y"
                                                     },
                                                     mirror_ctl_name=self.generate_name("tip", "", "ctl", True))
        self.toe_ctl, self.toe_loc = self.create_ctl(context=context,
                                                     parent=self.tip_loc,
                                                     name=self.generate_name("toe", "", "ctl"),
                                                     parent_ctl=self.tip_ctl,
                                                     attrs=["rx", "ry", "rz"],
                                                     m=toe_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "halfmoon",
                                                         "color": ik_color,
                                                         "width": div_length / total_length,
                                                         "ro": (0, 0, 0 if self.component.negate else 180)
                                                     },
                                                     mirror_ctl_name=self.generate_name("toe", "", "ctl", True))

        self.rev_fk_ctls = []
        self.rev_fk_locs = []
        ctl = self.toe_ctl
        loc = self.toe_loc
        for i, m in enumerate(reversed(fk_matrices)):
            ctl, loc = self.create_ctl(context=context,
                                       parent=loc,
                                       name=self.generate_name(f"rev{i}", "", "ctl"),
                                       parent_ctl=ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "circle3",
                                           "color": ik_color,
                                           "width": div_length / total_length * 0.5,
                                       },
                                       mirror_ctl_name=self.generate_name(f"rev{i}", "", "ctl", True))
            if i == 0:
                mc.delete(mc.listRelatives(ctl, shapes=True, fullPath=True))
            self.rev_fk_ctls.append(ctl)
            self.rev_fk_locs.append(loc)

        name = self.generate_name("legRef", "space", "ctl")
        root_opm = matrix.get_matrix(root, offset_parent_matrix=True)
        self.leg_space = matrix.transform(self.rev_fk_locs[-1], name, root_opm, True)

        ctl = self.rev_fk_ctls[-1]
        self.fk_ctls = []
        self.fk_locs = []
        for i in range(len(fk_matrices) - 1):
            offset = vector.get_distance(fk_positions[i], fk_positions[i + 1]) / 2.0
            po = offset * -1 if self.component.negate else offset
            ctl, loc = self.create_ctl(context=context,
                                       parent=self.fk_locs[-1] if self.fk_locs else self.leg_space,
                                       name=self.generate_name("fk" + str(i), "", "ctl"),
                                       parent_ctl=ctl,
                                       attrs=["rx", "ry", "rz"],
                                       m=fk_matrices[i],
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": fk_color,
                                           "width": offset * 2,
                                           "height": div_length / total_length * 0.7,
                                           "depth": div_length / total_length * 0.7,
                                           "po": (po, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("fk" + str(i), "", "ctl", True))
            sel_list = om2.MSelectionList()
            sel_list.add(loc)
            npo, ctl = controller.add_npo(ctl, self.generate_name("rot" + str(i), "inv", "ctl"))
            self.fk_ctls.append(ctl)
            self.fk_locs.append(sel_list.getDagPath(0).fullPathName())

        self.refs = []
        ref = self.create_ref(context=context,
                              name=self.generate_name("0", "ref", "ctl"),
                              anchor=True,
                              m=self.leg_space)
        self.refs.append(ref)
        for i, loc in enumerate(self.fk_locs):
            ref = self.create_ref(context=context,
                                  name=self.generate_name(str(i + 1), "ref", "ctl"),
                                  anchor=True,
                                  m=loc)
            self.refs.append(ref)

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            self.jnts = []
            parent = None
            for i, ref in enumerate(self.refs[1:]):
                if i == 1:
                    mc.connectAttr(parent + ".message", root + ".jnts[1]")
                m = matrix.get_matrix(ref)
                parent = self.create_jnt(context=context,
                                         parent=parent,
                                         name=self.generate_name(str(i), "", "jnt"),
                                         description=f"{i}",
                                         ref=ref,
                                         m=m,
                                         leaf=False,
                                         uni_scale=uni_scale)
                self.jnts.append(parent)

    def attributes(self, context):
        super().attributes(context)
        host = self.host

        data = self.component.data["value"]
        self.roll_angle_attrs = []
        for i, ctl in enumerate(self.fk_ctls):
            attr = attribute.add_attr(host,
                                      longName=f"angle{i}",
                                      type="double",
                                      defaultValue=data["roll_angle"],
                                      keyable=True)
            mc.setAttr(host + f".angle{i}", data["roll_angle"])
            self.roll_angle_attrs.append(attr)

    def operators(self, context):
        super().operators(context)

        # roll - rev
        reversed_rev_fk_ctls = list(reversed(self.rev_fk_ctls))
        limit_value = self.roll_angle_attrs[0]
        input_value = self.roll_ctl + ".rz"
        for i, attr in enumerate(self.roll_angle_attrs):
            cmp = mc.createNode("clamp")
            mc.connectAttr(attr, cmp + ".minR")
            mc.connectAttr(input_value, cmp + ".inputR")

            npo = hierarchy.get_parent(reversed_rev_fk_ctls[i])
            mc.connectAttr(cmp + ".outputR", npo + ".rz")

            if i < len(self.roll_angle_attrs) - 1:
                md = mc.createNode("multiplyDivide")
                mc.setAttr(md + ".input1X", -1)
                mc.connectAttr(limit_value, md + ".input2X")

                adl = mc.createNode("addDoubleLinear")
                mc.connectAttr(md + ".outputX", adl + ".input1")
                mc.connectAttr(self.roll_ctl + ".rz", adl + ".input2")
                input_value = adl + ".output"

                adl = mc.createNode("addDoubleLinear")
                mc.connectAttr(limit_value, adl + ".input1")
                mc.connectAttr(self.roll_angle_attrs[i + 1], adl + ".input2")
                limit_value = adl + ".output"
        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".input1X", -1)
        mc.connectAttr(limit_value, md + ".input2X")

        adl = mc.createNode("addDoubleLinear")
        mc.connectAttr(md + ".outputX", adl + ".input1")
        mc.connectAttr(self.roll_ctl + ".rz", adl + ".input2")
        input_value = adl + ".output"

        cmp = mc.createNode("clamp")
        mc.setAttr(cmp + ".minR", -360)
        mc.connectAttr(input_value, cmp + ".inputR")

        # npo = hierarchy.get_parent(reversed_rev_fk_ctls[-1])
        npo = hierarchy.get_parent(self.toe_ctl)
        mc.connectAttr(cmp + ".outputR", npo + ".rz")

        # roll - heel
        cmp = mc.createNode("clamp")
        mc.setAttr(cmp + ".maxR", 360)
        mc.connectAttr(self.roll_ctl + ".rz", cmp + ".inputR")

        npo = hierarchy.get_parent(self.heel_ctl)
        mc.connectAttr(cmp + ".outputR", npo + ".rz")

        # roll - in, out
        cmp = mc.createNode("clamp")
        mc.setAttr(cmp + ".minR", -360)
        mc.connectAttr(self.roll_ctl + ".rx", cmp + ".inputR")

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".input1X", -1 if self.component.negate else 1)
        mc.setAttr(md + ".input1Y", -1 if self.component.negate else 1)
        mc.connectAttr(cmp + ".outputR", md + ".input2X")

        npo = hierarchy.get_parent(self.out_ctl)
        mc.connectAttr(md + ".outputX", npo + ".rx")

        cmp = mc.createNode("clamp")
        mc.setAttr(cmp + ".maxR", 360)
        mc.connectAttr(self.roll_ctl + ".rx", cmp + ".inputR")

        mc.connectAttr(cmp + ".outputR", md + ".input2Y")

        npo = hierarchy.get_parent(self.in_ctl)
        mc.connectAttr(md + ".outputY", npo + ".rx")

        # fk ctl
        fk_ctls_reverse = list(reversed(self.fk_ctls))
        for i, ctl in enumerate(fk_ctls_reverse):
            inv_rot = hierarchy.get_parent(ctl)
            npo = hierarchy.get_parent(inv_rot)
            rev_npo = hierarchy.get_parent(self.rev_fk_ctls[i + 1])

            inv_m = mc.createNode("inverseMatrix")
            mc.connectAttr(rev_npo + ".matrix", inv_m + ".inputMatrix")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(inv_m + ".outputMatrix", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputRotate", inv_rot + ".rotate")

            inv_m = mc.createNode("inverseMatrix")
            mc.connectAttr(self.rev_fk_ctls[i + 1] + ".matrix", inv_m + ".inputMatrix")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(inv_m + ".outputMatrix", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputRotate", npo + ".rotate")

    def connections(self, context):
        super().connections(context)

        data = self.component.data["value"]
        parent_component = self.component.parent
        parent_data = parent_component.data["value"]
        if (data["connector"] == "leg_2jnt_01" and parent_data["component"] == "leg_2jnt_01") \
                or (data["connector"] == "leg_3jnt_01" and parent_data["component"] == "leg_3jnt_01"):
            connector_data = context[data["connector"]][str(self.parent.identifier)]
            ik_local_loc, ikh, last_ref, fk_ik_attr = connector_data

            src_attr = mc.listConnections(self.root + ".offsetParentMatrix", source=True, destination=False, plugs=True)
            mc.disconnectAttr(src_attr[0], self.root + ".offsetParentMatrix")
            [mc.setAttr(self.root + "." + attr, lock=False) for attr in ["tx", "ty", "tz", "rx", "ry", "rz"]]
            cons = mc.parentConstraint(last_ref, self.root, maintainOffset=True)[0]
            mc.connectAttr(ik_local_loc + ".worldMatrix", self.root + ".offsetParentMatrix")
            mc.delete(cons)
            [mc.setAttr(self.root + "." + attr, lock=True) for attr in ["tx", "ty", "tz", "rx", "ry", "rz"]]

            mc.parent(ikh, self.rev_fk_locs[-1])

            mc.parentConstraint(last_ref, self.leg_space, maintainOffset=True)

            for i, ctl in enumerate(self.fk_ctls):
                inv_rot = hierarchy.get_parent(ctl)
                npo = hierarchy.get_parent(inv_rot)

                pb = mc.createNode("pairBlend")
                mc.setAttr(pb + ".rotInterpolation", 1)
                mc.connectAttr(fk_ik_attr, pb + ".weight")
                src_attr = mc.listConnections(inv_rot + ".rotate", source=True, destination=False, plugs=True)[0]
                mc.connectAttr(src_attr, pb + ".inRotate2")
                mc.disconnectAttr(src_attr, inv_rot + ".rotate")
                mc.connectAttr(pb + ".outRotate", inv_rot + ".rotate")

                pb = mc.createNode("pairBlend")
                mc.setAttr(pb + ".rotInterpolation", 1)
                mc.connectAttr(fk_ik_attr, pb + ".weight")
                src_attr = mc.listConnections(npo + ".rotate", source=True, destination=False, plugs=True)[0]
                mc.connectAttr(src_attr, pb + ".inRotate2")
                mc.disconnectAttr(src_attr, npo + ".rotate")
                mc.connectAttr(pb + ".outRotate", npo + ".rotate")

            vis_ctls = [self.roll_ctl,
                        self.in_ctl,
                        self.out_ctl,
                        self.heel_ctl,
                        self.tip_ctl,
                        self.toe_ctl] + self.rev_fk_ctls
            for ctl in vis_ctls:
                for shape in mc.listRelatives(ctl, shapes=True, fullPath=True) or []:
                    mc.connectAttr(fk_ik_attr, shape + ".v")
