# built-ins
import os
import uuid

# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# domino
import domino
from domino import assembler
from domino.lib import name


class Author:
    madeBy = "Chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "noname"
    side = "C"
    index = 0
    description = \
        ("Assembly root assembler.\n"
         "It contains information used throughout the rigging.")


def component_preset():
    attributes = {
        "component": {"type": "string"},
        "component_version": {"type": "string"},
        "component_id": {"type": "string"},
        "maya_version": {"type": "string"},
        "domino_version": {"type": "string"},
        "name": {"type": "string"},
        "anchors": {"type": "matrix", "multi": True},
        "origin_sub_ctl_count": {"type": "long", "minValue": 0},
        "origin_ctl_size": {"type": "double", "minValue": 0},
        "mode": {"type": "enum", "enumName": "DEBUG:WIP:PUB"},
        "end_point": {"type": "enum", "enumName": "all:objects:attributes:operators:connections:finalize"},
        "jnt_left_name": {"type": "string"},
        "jnt_right_name": {"type": "string"},
        "jnt_center_name": {"type": "string"},
        "ctl_left_name": {"type": "string"},
        "ctl_right_name": {"type": "string"},
        "ctl_center_name": {"type": "string"},
        "jnt_name_ext": {"type": "string"},
        "ctl_name_ext": {"type": "string"},
        "jnt_name_rule": {"type": "string"},
        "ctl_name_rule": {"type": "string"},
        "jnt_description_letter_case": {"type": "enum", "enumName": "default:lower:upper:capitalize"},
        "ctl_description_letter_case": {"type": "enum", "enumName": "default:lower:upper:capitalize"},
        "jnt_index_padding": {"type": "long", "minValue": 0},
        "ctl_index_padding": {"type": "long", "minValue": 0},
        "force_uni_scale": {"type": "bool"},
        "l_color_fk": {"type": "long", "minValue": 0, "maxValue": 31},
        "l_color_ik": {"type": "long", "minValue": 0, "maxValue": 31},
        "r_color_fk": {"type": "long", "minValue": 0, "maxValue": 31},
        "r_color_ik": {"type": "long", "minValue": 0, "maxValue": 31},
        "c_color_fk": {"type": "long", "minValue": 0, "maxValue": 31},
        "c_color_ik": {"type": "long", "minValue": 0, "maxValue": 31},
        "use_RGB_colors": {"type": "bool"},
        "l_RGB_fk": {"type": "float3"},
        "l_RGB_ik": {"type": "float3"},
        "r_RGB_fk": {"type": "float3"},
        "r_RGB_ik": {"type": "float3"},
        "c_RGB_fk": {"type": "float3"},
        "c_RGB_ik": {"type": "float3"},
        "run_custom_step": {"type": "bool"},
        "custom_step": {"type": "string"},
        "ctl_shapes": {"type": "message", "multi": True},
        "icon_name": {"type": "string"},
        "pose_json": {"type": "string"},
        "publish_notes": {"type": "string"},
        "asset_container": {"type": "string"}
    }
    value = {
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "maya_version": "{0}.{1}".format(mc.about(query=True, majorVersion=True),
                                         mc.about(query=True, minorVersion=True)),
        "domino_version": domino.__version_str__,
        "name": Author.name,
        "anchors": [list(om2.MMatrix())],
        "origin_sub_ctl_count": 2,
        "origin_ctl_size": 1,
        "mode": "WIP",
        "end_point": "all",
        "jnt_left_name": name.DEFAULT_JOINT_SIDE_L_NAME,
        "jnt_right_name": name.DEFAULT_JOINT_SIDE_R_NAME,
        "jnt_center_name": name.DEFAULT_JOINT_SIDE_C_NAME,
        "ctl_left_name": name.DEFAULT_SIDE_L_NAME,
        "ctl_right_name": name.DEFAULT_SIDE_R_NAME,
        "ctl_center_name": name.DEFAULT_SIDE_C_NAME,
        "jnt_name_ext": name.DEFAULT_JOINT_EXT_NAME,
        "ctl_name_ext": name.DEFAULT_CTL_EXT_NAME,
        "jnt_name_rule": name.DEFAULT_NAMING_RULE,
        "ctl_name_rule": name.DEFAULT_NAMING_RULE,
        "jnt_description_letter_case": "default",
        "ctl_description_letter_case": "default",
        "jnt_index_padding": 0,
        "ctl_index_padding": 0,
        "force_uni_scale": True,
        "l_color_fk": 6,
        "l_color_ik": 18,
        "r_color_fk": 23,
        "r_color_ik": 14,
        "c_color_fk": 13,
        "c_color_ik": 17,
        "use_RGB_colors": False,
        "l_RGB_fk": (0, 0, 1),
        "l_RGB_ik": (0, 0.25, 1),
        "r_RGB_fk": (1, 0, 0),
        "r_RGB_ik": (1, 0.1, 0.25),
        "c_RGB_fk": (1, 1, 0),
        "c_RGB_ik": (0, 0.6, 1),
        "run_custom_step": False,
        "custom_step": ",".join(["objects", "attributes", "operators", "connections", "finalize"]),
        "icon_name": "human",
        "asset_container": Author.name
    }
    anim = {}
    nurbs_curve = {"ctl_shapes": None}
    _json = {"pose_json": {"neutral": {}, }}
    return {"attributes": attributes, "value": value, "anim": anim, "nurbs_curve": nurbs_curve, "json": _json}


def guide_recipe():
    return {"position": [],
            "lock_attrs": (("tx", "ty", "tz", "rx", "ry", "rz"),)}


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]

        origin_rig = self.create_root(context)
        m = om2.MMatrix(data["anchors"][0])

        width = 3 + data["origin_ctl_size"]
        origin_ctl, origin_loc = self.create_ctl(context=context,
                                                 parent=origin_rig,
                                                 name="origin_ctl",
                                                 m=m,
                                                 parent_ctl=None,
                                                 attrs=("tx", "ty", "tz", "sx", "sy", "sz"),
                                                 mirror_config=(),
                                                 shape_args={
                                                     "shape": "origin",
                                                     "width": width
                                                 },
                                                 mirror_ctl_name="")
        parent_loc = origin_loc
        parent_ctl = origin_ctl
        width = 3.5 + data["origin_ctl_size"]
        for i in range(data["origin_sub_ctl_count"]):
            width = width * 0.8
            parent_ctl, parent_loc = self.create_ctl(context=context,
                                                     parent=parent_loc,
                                                     name="sub{0}".format(i) + "_ctl",
                                                     m=m,
                                                     parent_ctl=parent_ctl,
                                                     attrs=("tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz"),
                                                     mirror_config=(),
                                                     shape_args={
                                                         "shape": "wave",
                                                         "width": width,
                                                         "color": om2.MColor((0, 1, 1))
                                                     },
                                                     mirror_ctl_name="")

        last_loc = parent_loc
        ref = self.create_ref(context=context,
                              name="origin_ref",
                              anchor=True,
                              m=last_loc)

        jnt = self.create_jnt(context=context,
                              parent=None,
                              name="origin_jnt",
                              description="origin",
                              ref=ref,
                              m=m,
                              uni_scale=data["force_uni_scale"])

        ctl_tag = mc.controller(origin_ctl, query=True)[0]
        choice = mc.createNode("choice")
        mc.setAttr(choice + ".input[0]", 1)
        mc.setAttr(choice + ".input[1]", 2)
        mc.connectAttr(context["asset"][1] + ".ctl_mouseover", choice + ".selector")
        mc.connectAttr(choice + ".output", ctl_tag + ".visibilityMode")

    def attributes(self, context):
        super().attributes(context)

    def operators(self, context):
        super().operators(context)

    def connections(self, context):
        super().connections(context)
