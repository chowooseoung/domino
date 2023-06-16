# domino
from domino.lib import matrix, attribute, icon
from domino.lib.rigging import operators, callback, nurbs
from domino import assembler

# built-ins
import os
import uuid

# maya
from maya.api import OpenMaya as om2
from maya import cmds as mc


class Author:
    madeBy = "Chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "control"
    side = "C"
    index = 0
    description = "controller와 joint를 선택적(controller만 joint만 혹은 둘 다)으로 추가할 수 있습니다. UI로 사용할 수도 있습니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "nothing": {"type": "bool"},
        "leaf_jnt": {"type": "bool"},
        "uni_scale": {"type": "bool"},
        "neutral_rotation": {"type": "bool"},
        "mirror_behaviour": {"type": "bool"},
        "icon": {"type": "string"},
        "k_tx": {"type": "bool"},
        "k_ty": {"type": "bool"},
        "k_tz": {"type": "bool"},
        "k_rx": {"type": "bool"},
        "k_ry": {"type": "bool"},
        "k_rz": {"type": "bool"},
        "k_sx": {"type": "bool"},
        "k_sy": {"type": "bool"},
        "k_sz": {"type": "bool"},
        "default_rotate_order": {"type": "enum", "enumName": "xyz:yzx:zxy:xzy:yxz:zyx"},
        "space_switch_array": {"type": "string"},
        "ctl_size": {"type": "double"},
        "move_pivot": {"type": "bool"}
    })
    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(om2.MMatrix())],
        "nothing": False,
        "leaf_jnt": False,
        "uni_scale": False,
        "neutral_rotation": False,
        "mirror_behaviour": False,
        "icon": "cube",
        "k_tx": True,
        "k_ty": True,
        "k_tz": True,
        "k_rx": True,
        "k_ry": True,
        "k_rz": True,
        "k_sx": True,
        "k_sy": True,
        "k_sz": True,
        "default_rotate_order": "xyz",
        "ctl_size": 1,
        "move_pivot": False
    })
    return common_preset


def guide_recipe():
    return {}


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        m = om2.MMatrix(data["anchors"][0])
        if data["neutral_rotation"]:
            m = matrix.set_matrix_translate(om2.MMatrix(), om2.MTransformationMatrix(m).translation(om2.MSpace.kWorld))
        else:
            scl = [1, 1, -1] if data["mirror_behaviour"] and self.component.negate else [1, 1, 1]
            m = matrix.set_matrix_scale(m, scl)

        root = self.create_root(context)
        color = self.generate_color("ik")

        if data["nothing"]:
            ref = self.create_ref(context=context,
                                  name=self.generate_name("", "ref", "ctl"),
                                  anchor=True,
                                  m=None)
            return None
        uni_scale = True if data["uni_scale"] else False
        if assembly_data["force_uni_scale"]:
            uni_scale = True
        if not data["leaf_jnt"]:
            mul_size = om2.MTransformationMatrix(om2.MMatrix(data["anchors"][0])).scale(om2.MSpace.kWorld)[2]
            attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
            key_attrs = [attr for attr in attrs if data["k_" + attr]]
            mirror_config = (0, 0, 0, 0, 0, 0, 0, 0, 0) if data["mirror_behaviour"] else (0, 0, 1, 1, 1, 0, 0, 0, 0)
            self.ctl, loc = self.create_ctl(context=context,
                                            parent=root,
                                            name=self.generate_name("", "", "ctl"),
                                            parent_ctl=None,
                                            attrs=key_attrs,
                                            m=m,
                                            cns=True if data["space_switch_array"] else False,
                                            mirror_config=mirror_config,
                                            shape_args={
                                                "shape": data["icon"],
                                                "color": color,
                                                "width": data["ctl_size"] * mul_size,
                                                "height": data["ctl_size"] * mul_size,
                                                "depth": data["ctl_size"] * mul_size,
                                            },
                                            mirror_ctl_name=self.generate_name("", "", "ctl", True))
            mc.setAttr(self.ctl + ".ro", ["xyz", "yzx", "zxy", "xzy", "yxz", "zyx"].index(data["default_rotate_order"]))
            ref = self.create_ref(context=context,
                                  name=self.generate_name("", "ref", "ctl"),
                                  anchor=True,
                                  m=loc)
            if data["move_pivot"]:
                self.pivot_ctl = icon.create(parent=loc,
                                             name=self.generate_name("pivot", "", "ctl"),
                                             shape="locator",
                                             color=om2.MColor((0, 1, 1)),
                                             m=m,
                                             width=data["ctl_size"] * mul_size * 0.8,
                                             height=data["ctl_size"] * mul_size * 0.8,
                                             depth=data["ctl_size"] * mul_size * 0.8,
                                             thickness=1,
                                             po=(0, 0, 0),
                                             ro=(0, 0, 0))
                attrs = ["rx", "ry", "rz", "sx", "sy", "sz"]
                [mc.setAttr(self.pivot_ctl + "." + attr, lock=True) for attr in attrs]
                [mc.setAttr(self.pivot_ctl + "." + attr, keyable=False) for attr in attrs + ["v"]]
                self.dp_crv = nurbs.create(parent=self.root,
                                           name=self.generate_name("dp", "crv", "ctl"),
                                           degree=1,
                                           positions=((0, 0, 0), (1, 1, 1)),
                                           display_type=2)
                nurbs.constraint(self.dp_crv, [self.ctl, self.pivot_ctl])

            if data["create_jnt"]:
                self.create_jnt(context=context,
                                parent=None,
                                name=self.generate_name("", "", "jnt"),
                                description="",
                                ref=ref,
                                m=m,
                                leaf=False,
                                uni_scale=uni_scale)
        elif data["leaf_jnt"] and data["create_jnt"]:
            self.create_jnt(context=context,
                            parent=None,
                            name=self.generate_name("", "", "jnt"),
                            description="",
                            ref=None,
                            m=m,
                            leaf=True,
                            uni_scale=uni_scale)

    def attributes(self, context):
        super().attributes(context)
        data = self.component.data["value"]

        if data["move_pivot"]:
            self.pivot_vis_attr = attribute.add_attr(self.ctl,
                                                     longName="pivot_vis",
                                                     type="bool",
                                                     keyable=True,
                                                     defaultValue=False)

    def operators(self, context):
        super().operators(context)
        data = self.component.data["value"]

        if data["move_pivot"] and not data["leaf_jnt"]:
            mc.connectAttr(self.pivot_ctl + ".t", self.ctl + ".rotatePivot")
            mc.connectAttr(self.pivot_ctl + ".t", self.ctl + ".scalePivot")
            mc.connectAttr(self.pivot_vis_attr, self.pivot_ctl + ".v")
            mc.connectAttr(self.pivot_vis_attr, self.dp_crv + ".v")

        if data["nothing"]:
            return None

        host = context[self.identifier]["host"]
        if data["space_switch_array"] and not data["leaf_jnt"]:
            source_ctls = self.find_ctls(context, data["space_switch_array"])
            operators.space_switch(source_ctls, self.ctl, host)
            script_node = callback.space_switch(source_ctls, self.ctl, host)
            if script_node:
                context["callbacks"].append(script_node)

    def connections(self, context):
        super().connections(context)
