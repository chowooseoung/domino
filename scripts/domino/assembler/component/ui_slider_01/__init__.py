# domino
from domino.lib import matrix, icon, vector, attribute
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
    name = "uiSlider"
    side = "C"
    index = 0
    description = "slider ui 입니다. +tx, -tx, +ty, -ty 로 작동하는 ui 를 생성합니다. ui_container_01 과 연결될수있습니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "frame": {"type": "bool"},
        "size": {"type": "float"},
        "plus_x": {"type": "bool"},
        "minus_x": {"type": "bool"},
        "plus_y": {"type": "bool"},
        "minus_y": {"type": "bool"},
        "plus_x_name": {"type": "string"},
        "minus_x_name": {"type": "string"},
        "plus_y_name": {"type": "string"},
        "minus_y_name": {"type": "string"}
    })

    def _anchors():
        t_m = om2.MTransformationMatrix()

        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (1, 0, 0))
        t_m.setRotation(om2.MEulerRotation([math.radians(x) for x in (0, 0, 180)]))
        m1 = matrix.set_matrix_rotate(m1, t_m)
        m2 = matrix.set_matrix_translate(m, (0, 1, 0))
        t_m.setRotation(om2.MEulerRotation([math.radians(x) for x in (0, 0, 270)]))
        m2 = matrix.set_matrix_rotate(m2, t_m)
        m3 = matrix.set_matrix_translate(m, (-1, 0, 0))
        m4 = matrix.set_matrix_translate(m, (0, -1, 0))
        t_m.setRotation(om2.MEulerRotation([math.radians(x) for x in (0, 0, 90)]))
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
        "frame": True,
        "size": 0.2,
        "plus_x": True,
        "minus_x": True,
        "plus_y": True,
        "minus_y": True
    })
    return common_preset


def guide_recipe():
    script = """import maya.cmds as mc
import maya.api.OpenMaya as om2
from domino.lib import icon

root = icon.square(None, "TEMP", (1, 0, 0), om2.MMatrix(), width=0.1, height=0.1, up="z")
icon.replace(root, "{0}")
mc.delete(root)
mc.setAttr("{1}.v", lock=False)
mc.setAttr("{2}.v", lock=False)
mc.setAttr("{3}.v", lock=False)
mc.setAttr("{4}.v", lock=False)
mc.connectAttr("{0}.plus_x", "{1}.v")
mc.connectAttr("{0}.minus_x", "{3}.v")
mc.connectAttr("{0}.plus_y", "{2}.v")
mc.connectAttr("{0}.minus_y", "{4}.v")
for pos in ["{1}", "{2}", "{3}", "{4}"]:
    shape = mc.listRelatives(pos, shapes=True, fullPath=True)[0]
    mc.setAttr(shape + ".overrideEnabled", 0)
    mc.setAttr(pos + ".overrideEnabled", 1)
    mc.setAttr(pos + ".overrideDisplayType", 2)
    mc.setAttr(pos + ".displayHandle", False)"""
    return {
        "position": [
            (0, "pos0", "slider"),
            (0, "pos1", "slider"),
            (0, "pos2", "slider"),
            (0, "pos3", "slider"),
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
            "indexes": [0, 1, 2, 3, 4]
        }
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)
        self.create_root(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        positions = [om2.MVector(x[12:-1]) for x in data["anchors"]]
        distance_x = vector.get_distance(positions[0], positions[1])
        distance_y = vector.get_distance(positions[0], positions[2])
        fk_color = self.generate_color("fk")

        root_m = matrix.get_matrix(self.root)

        if data["frame"]:
            frame_icon = icon.create(parent=self.root,
                                     name=self.generate_name("frame", "line", "ctl"),
                                     shape="square",
                                     color=None,
                                     m=root_m,
                                     width=data["size"],
                                     height=data["size"],
                                     thickness=1,
                                     up="z",
                                     po=(0, 0, 0),
                                     ro=(0, 0, 0))
            if data["plus_x"]:
                mc.move(distance_x, frame_icon + ".cv[:1]", objectSpace=True, relative=True, moveX=True,
                        worldSpaceDistance=True)
            if data["minus_x"]:
                mc.move(distance_x * -1, frame_icon + ".cv[2:]", objectSpace=True, relative=True, moveX=True,
                        worldSpaceDistance=True)
            if data["plus_y"]:
                mc.move(distance_y, frame_icon + ".cv[1:2]", objectSpace=True, relative=True, moveY=True,
                        worldSpaceDistance=True)
            if data["minus_y"]:
                mc.move(distance_y * -1, frame_icon + ".cv[0]", objectSpace=True, relative=True, moveY=True,
                        worldSpaceDistance=True)
                mc.move(distance_y * -1, frame_icon + ".cv[3]", objectSpace=True, relative=True, moveY=True,
                        worldSpaceDistance=True)
            mc.setAttr(frame_icon + ".overrideEnabled", 1)
            mc.setAttr(frame_icon + ".overrideDisplayType", 1)
        if data["plus_x"]:
            plus_x_icon = icon.create(parent=self.root,
                                      name=self.generate_name("plusX", "slider", "ctl"),
                                      shape="slider",
                                      color=None,
                                      m=root_m,
                                      width=distance_x,
                                      height=data["size"],
                                      thickness=1,
                                      po=(distance_x, 0, 0),
                                      ro=(0, 0, 180))
            mc.setAttr(plus_x_icon + ".overrideEnabled", 1)
            mc.setAttr(plus_x_icon + ".overrideDisplayType", 1)
        if data["minus_x"]:
            minus_x_icon = icon.create(parent=self.root,
                                       name=self.generate_name("minusX", "slider", "ctl"),
                                       shape="slider",
                                       color=None,
                                       m=root_m,
                                       width=distance_x,
                                       height=data["size"],
                                       thickness=1,
                                       po=(-1 * distance_x, 0, 0),
                                       ro=(0, 0, 0))
            mc.setAttr(minus_x_icon + ".overrideEnabled", 1)
            mc.setAttr(minus_x_icon + ".overrideDisplayType", 1)
        if data["plus_y"]:
            plus_y_icon = icon.create(parent=self.root,
                                      name=self.generate_name("plusY", "slider", "ctl"),
                                      shape="slider",
                                      color=None,
                                      m=root_m,
                                      width=distance_y,
                                      height=data["size"],
                                      thickness=1,
                                      po=(0, distance_y, 0),
                                      ro=(0, 0, -90))
            mc.setAttr(plus_y_icon + ".overrideEnabled", 1)
            mc.setAttr(plus_y_icon + ".overrideDisplayType", 1)
        if data["minus_y"]:
            minus_y_icon = icon.create(parent=self.root,
                                       name=self.generate_name("minusY", "slider", "ctl"),
                                       shape="slider",
                                       color=None,
                                       m=root_m,
                                       width=distance_y,
                                       height=data["size"],
                                       thickness=1,
                                       po=(0, -1 * distance_y, 0),
                                       ro=(0, 0, 90))
            mc.setAttr(minus_y_icon + ".overrideEnabled", 1)
            mc.setAttr(minus_y_icon + ".overrideDisplayType", 1)

        keyable_attr = ["tx", "ty"]
        if not data["plus_x"] and not data["minus_x"]:
            keyable_attr.remove("tx")
        if not data["plus_y"] and not data["minus_y"]:
            keyable_attr.remove("ty")

        self.ctl, self.loc = self.create_ctl(context=context,
                                             parent=self.root,
                                             name=self.generate_name("", "", "ctl"),
                                             parent_ctl=None,
                                             attrs=keyable_attr,
                                             m=data["anchors"][0],
                                             cns=False,
                                             mirror_config=(1, 1, 1, 0, 1, 1, 0, 0, 0),
                                             shape_args={
                                                 "shape": "square",
                                                 "thickness": 2,
                                                 "width": data["size"] * 0.9 / distance_x,
                                                 "height": data["size"] * 0.9 / distance_y,
                                                 "up": "z",
                                                 "color": fk_color
                                             },
                                             mirror_ctl_name=self.generate_name("", "", "ctl", True))
        mc.transformLimits(self.ctl,
                           translationX=(-1 if data["minus_x"] else 0, 1 if data["plus_x"] else 0),
                           translationY=(-1 if data["minus_y"] else 0, 1 if data["plus_y"] else 0),
                           enableTranslationX=(True, True),
                           enableTranslationY=(True, True))

    def attributes(self, context):
        super().attributes(context)

        data = self.component.data["value"]
        side_str = ""
        left_str = "l"
        right_str = "r"
        center_str = ""
        ctl = self.host
        if "ui_container" in context[self.parent.identifier]:
            left_str, right_str, center_str, ctl = context[self.parent.identifier]["ui_container"]

        if data["side"] == "L":
            side_str = left_str
        elif data["side"] == "R":
            side_str = right_str
        elif data["side"] == "C":
            side_str = center_str

        plus_x_name = self.identifier + "_plus_x"
        if data["plus_x_name"]:
            plus_x_name = data["plus_x_name"]
        minus_x_name = self.identifier + "_minus_x"
        if data["minus_x_name"]:
            minus_x_name = data["minus_x_name"]
        plus_y_name = self.identifier + "_plus_y"
        if data["plus_y_name"]:
            plus_y_name = data["plus_y_name"]
        minus_y_name = self.identifier + "_minus_y"
        if data["minus_y_name"]:
            minus_y_name = data["minus_y_name"]
        plus_x_attr_name = "_".join([x for x in [side_str, plus_x_name] if x])
        minus_x_attr_name = "_".join([x for x in [side_str, minus_x_name] if x])
        plus_y_attr_name = "_".join([x for x in [side_str, plus_y_name] if x])
        minus_y_attr_name = "_".join([x for x in [side_str, minus_y_name] if x])
        if data["plus_x"]:
            plus_x_attr = attribute.add_attr(ctl,
                                             longName=plus_x_attr_name,
                                             type="float",
                                             keyable=False)
            mc.setAttr(plus_x_attr, channelBox=True)
            clamp = mc.createNode("clamp")
            mc.setAttr(clamp + ".maxR", 10000)
            mc.connectAttr(self.ctl + ".tx", clamp + ".inputR")
            mc.connectAttr(clamp + ".outputR", plus_x_attr)
        if data["minus_x"]:
            minus_x_attr = attribute.add_attr(ctl,
                                              longName=minus_x_attr_name,
                                              type="float",
                                              keyable=False)
            mc.setAttr(minus_x_attr, channelBox=True)
            clamp = mc.createNode("clamp")
            mc.setAttr(clamp + ".minR", -10000)
            mc.connectAttr(self.ctl + ".tx", clamp + ".inputR")

            mp = mc.createNode("multiplyDivide")
            mc.setAttr(mp + ".input2X", -1)
            mc.connectAttr(clamp + ".outputR", mp + ".input1X")

            mc.connectAttr(mp + ".outputX", minus_x_attr)
        if data["plus_y"]:
            plus_y_attr = attribute.add_attr(ctl,
                                             longName=plus_y_attr_name,
                                             type="float",
                                             keyable=False)
            mc.setAttr(plus_y_attr, channelBox=True)
            clamp = mc.createNode("clamp")
            mc.setAttr(clamp + ".maxR", 10000)
            mc.connectAttr(self.ctl + ".ty", clamp + ".inputR")
            mc.connectAttr(clamp + ".outputR", plus_y_attr)
        if data["minus_y"]:
            minus_y_attr = attribute.add_attr(ctl,
                                              longName=minus_y_attr_name,
                                              type="float",
                                              keyable=False)
            mc.setAttr(minus_y_attr, channelBox=True)
            clamp = mc.createNode("clamp")
            mc.setAttr(clamp + ".minR", -10000)
            mc.connectAttr(self.ctl + ".ty", clamp + ".inputR")

            mp = mc.createNode("multiplyDivide")
            mc.setAttr(mp + ".input2X", -1)
            mc.connectAttr(clamp + ".outputR", mp + ".input1X")

            mc.connectAttr(mp + ".outputX", minus_y_attr)

    def operators(self, context):
        super().operators(context)

    def connections(self, context):
        super().connections(context)
