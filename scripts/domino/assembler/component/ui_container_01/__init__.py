# domino
from domino.lib import matrix
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
    name = "uiContainer"
    side = "C"
    index = 0
    description = "control ui interface 입니다. ui_slider_01 의 value 는 ui_container_01 에 연결됩니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "left_str": {"type": "string"},
        "right_str": {"type": "string"},
        "center_str": {"type": "string"}
    })

    def _anchors():
        t_m = om2.MTransformationMatrix()

        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0.5, -0.5, 0))
        m2 = matrix.set_matrix_translate(m, (0.5, 0.5, 0))
        t_m.setRotation(om2.MEulerRotation([math.radians(x) for x in (0, 0, 90)]))
        m2 = matrix.set_matrix_rotate(m2, t_m)
        m3 = matrix.set_matrix_translate(m, (-0.5, 0.5, 0))
        t_m.setRotation(om2.MEulerRotation([math.radians(x) for x in (0, 0, 180)]))
        m3 = matrix.set_matrix_rotate(m3, t_m)
        m4 = matrix.set_matrix_translate(m, (-0.5, -0.5, 0))
        t_m.setRotation(om2.MEulerRotation([math.radians(x) for x in (0, 0, 270)]))
        m4 = matrix.set_matrix_rotate(m4, t_m)
        return m, m1, m2, m3, m4

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "left_str": "l",
        "right_str": "r",
    })
    return common_preset


def guide_recipe():
    script = """import maya.cmds as mc
import maya.api.OpenMaya as om2
from domino.lib import icon

root = icon.square(None, "TEMP", (1, 0, 0), om2.MMatrix(), width=0.1, height=0.1, up="z")
icon.replace(root, "{0}")
mc.delete(root)"""
    return {
        "position": [
            (0, "pos0", "bracket"),
            (0, "pos1", "bracket"),
            (0, "pos2", "bracket"),
            (0, "pos3", "bracket"),
        ],
        "lock_attrs": (
            (),
            ("tz", "rx", "ry", "rz", "sx", "sy", "sz"),
            ("tz", "rx", "ry", "rz", "sx", "sy", "sz"),
            ("tz", "rx", "ry", "rz", "sx", "sy", "sz"),
            ("tz", "rx", "ry", "rz", "sx", "sy", "sz"),
        ),
        "post": {
            "script": script,
            "indexes": [0]
        }
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)
        self.create_root(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]
        positions = [om2.MVector(x[12:-1]) for x in data["anchors"][1:]]

        self.ctl, self.loc = self.create_ctl(context=context,
                                             parent=self.root,
                                             name=self.generate_name("frame", "", "ctl"),
                                             parent_ctl=None,
                                             attrs=[],
                                             m=data["anchors"][0],
                                             cns=False,
                                             mirror_config=(1, 1, 1, 0, 1, 1, 0, 0, 0),
                                             shape_args={
                                                 "shape": "square",
                                                 "thickness": 2,
                                                 "width": 1,
                                                 "height": 1,
                                                 "up": "z",
                                                 "color": (1, 1, 0)
                                             },
                                             mirror_ctl_name=self.generate_name("frame", "", "ctl", True))
        mc.move(*positions[0], self.ctl + ".cv[0]", worldSpace=True, absolute=True)
        mc.move(*positions[1], self.ctl + ".cv[1]", worldSpace=True, absolute=True)
        mc.move(*positions[2], self.ctl + ".cv[2]", worldSpace=True, absolute=True)
        mc.move(*positions[3], self.ctl + ".cv[3]", worldSpace=True, absolute=True)

        name = self.generate_name("frame", "ref", "ctl")
        ref = self.create_ref(context=context, name=name, anchor=True, m=self.loc)

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            self.jnt = self.create_jnt(context=context,
                                       parent=None,
                                       name=self.generate_name("", "", "jnt"),
                                       description="",
                                       ref=ref,
                                       m=matrix.get_matrix(ref),
                                       leaf=False,
                                       uni_scale=uni_scale)

        context[self.identifier]["ui_container"] = [data["left_str"],
                                                    data["right_str"],
                                                    data["center_str"],
                                                    self.jnt if data["create_jnt"] else self.ctl]

    def attributes(self, context):
        super().attributes(context)

    def operators(self, context):
        super().operators(context)

    def connections(self, context):
        super().connections(context)
