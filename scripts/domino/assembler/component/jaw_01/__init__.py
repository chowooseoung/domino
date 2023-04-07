# domino
from domino.lib import attribute, matrix, vector, hierarchy
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
    name = "jaw"
    side = "C"
    index = 0
    description = "턱 입니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "sliding_angle": {"type": "double"},
        "sliding": {"type": "double", "minValue": 0, "maxValue": 2},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))  # root
        m2 = matrix.set_matrix_translate(m, (0, -1, 1))  # heel
        m3 = matrix.set_matrix_translate(m, (0, -2, 3))  # in
        return m1, m2, m3

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "sliding_angle": -3,
        "sliding": 0.1,
    })
    return common_preset


def guide_recipe():
    return {
        "position": [
            (0, "sliding"),
            (1, "aim"),  # parent node index, extension
        ],
        "display_curve": [
            ((0, 1, 2), "dpCrv"),  # source node indexes, extension
        ],
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        m0 = om2.MMatrix(data["anchors"][0])
        m1 = om2.MMatrix(data["anchors"][1])
        m2 = om2.MMatrix(data["anchors"][2])

        positions = [om2.MVector(list(x)[12:-1]) for x in [m0, m1, m2]]
        normal = vector.get_plane_normal(*positions) * -1

        root = self.create_root(context)
        fk_color = self.generate_color("fk")
        ik_color = self.generate_color("ik")

        aim_m = matrix.get_look_at_matrix(positions[-1], positions[1], normal, "xz", True)
        self.aim_ctl, self.aim_loc = self.create_ctl(context=context,
                                                     parent=root,
                                                     name=self.generate_name("aim", "", "ctl"),
                                                     parent_ctl=None,
                                                     attrs=["tx", "ty", "tz"],
                                                     m=aim_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "circle",
                                                         "width": 1,
                                                         "height": 1,
                                                         "depth": 1,
                                                         "ro": (0, 0, 90),
                                                         "color": ik_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("aim", "", "ctl", True))

        distance = vector.get_distance(positions[0], positions[-1])
        m = matrix.get_look_at_matrix(positions[0], positions[-1], normal, "-xz", True)
        self.jaw_ctl, self.jaw_loc = self.create_ctl(context=context,
                                                     parent=root,
                                                     name=self.generate_name("", "", "ctl"),
                                                     parent_ctl=self.aim_ctl,
                                                     attrs=["rx", "ry", "rz"],
                                                     m=m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "width": distance,
                                                         "height": distance / 2,
                                                         "depth": 1,
                                                         "po": (distance / 2, 0, 0),
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("", "", "ctl", True))
        name = self.generate_name("rot", "", "ctl")
        self.rot_obj = matrix.transform(root, name, m, True)

        sliding_m = matrix.get_look_at_matrix(positions[0], positions[1], normal, "-xz", True)
        name = self.generate_name("sliding", "space", "ctl")
        self.sliding_grp = matrix.transform(root, name, sliding_m, True)

        name = self.generate_name("sliding", "aim", "ctl")
        self.sliding_aim = matrix.transform(self.sliding_grp, name, m, True)

        # refs
        name = self.generate_name("", "ref", "ctl")
        ref = self.create_ref(context, name, True, self.sliding_aim)

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True
            name = self.generate_name("", "", "jnt")
            jnt = self.create_jnt(context=context,
                                  parent=None,
                                  name=name,
                                  description="",
                                  ref=ref,
                                  m=m,
                                  leaf=False,
                                  uni_scale=uni_scale)

    def attributes(self, context):
        super().attributes(context)
        host = self.host

        data = self.component.data["value"]
        self.sliding_attr = attribute.add_attr(host,
                                               longName="sliding",
                                               type="double",
                                               minValue=0,
                                               defaultValue=data["sliding"],
                                               keyable=True)
        self.sliding_angle_attr = attribute.add_attr(host,
                                                     longName="sliding_angle",
                                                     type="double",
                                                     defaultValue=data["sliding_angle"],
                                                     keyable=True)

    def operators(self, context):
        super().operators(context)

        jaw_npo = hierarchy.get_parent(self.jaw_ctl)
        mc.aimConstraint(self.aim_loc,
                         jaw_npo,
                         aimVector=(1, 0, 0),
                         upVector=(0, 0, 1),
                         worldUpType="object",
                         worldUpObject=self.root)
        mc.orientConstraint(self.jaw_loc, self.sliding_aim)
        mc.orientConstraint(self.jaw_loc, self.rot_obj)

        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".input1X", -1)
        mc.connectAttr(self.sliding_angle_attr, md + ".input2X")

        adl = mc.createNode("addDoubleLinear")
        mc.connectAttr(self.rot_obj + ".rz", adl + ".input1")
        mc.connectAttr(md + ".outputX", adl + ".input2")

        clamp = mc.createNode("clamp")
        mc.setAttr(clamp + ".minR", -360)
        mc.connectAttr(adl + ".output", clamp + ".inputR")

        data = self.component.data["value"]
        distance = vector.get_distance(data["anchors"][1][12:-1], data["anchors"][-1][12:-1])

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(clamp + ".outputR", md + ".input1X")
        mc.setAttr(md + ".input2X", distance / -300)
        sliding_value = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(sliding_value, md + ".input1X")
        mc.connectAttr(self.sliding_attr, md + ".input2X")

        mc.connectAttr(md + ".outputX", self.sliding_grp + ".tx")

    def connections(self, context):
        super().connections(context)
