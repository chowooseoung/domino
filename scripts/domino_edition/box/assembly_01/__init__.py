# built-ins
import os
import uuid
import json

# maya
from pymel import core as pm

# domino
from domino_edition.api import (piece,
                                naming)
from domino.api import (attribute,
                        matrix)
import domino

dt = pm.datatypes


class Assembly01Identifier(piece.Identifier):
    madeBy = "Chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "noname"
    side = "C"
    index = 0
    description = \
        ("Assembly(top) piece.\n"
         "It contains information used throughout the rigging. It is also a \n"
         "piece that creates a asset interface grp(asset, model, skeleton)\n")


class Assembly01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Assembly01Identifier(self)
        super(Assembly01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        return {
            "d_id": {"typ": "string",
                     "value": str(uuid.uuid4())},
            "piece": {"typ": "string",
                      "value": f"{self.identifier.piece}"},
            "maya_version": {"typ": "string",
                             "value": (f"{pm.about(query=True, majorVersion=True)}."
                                       f"{pm.about(query=True, minorVersion=True)}")},
            "domino_version": {"typ": "string",
                               "value": domino.__version_str__},
            "piece_version": {"typ": "string",
                              "value": ". ".join([str(x) for x in self.identifier.version])},
            "name": {"typ": "string",
                     "value": f"{self.identifier.name}"},
            "anchors": {"typ": "matrix",
                        "value": [self._m1],
                        "multi": True},
            "origin_sub_ctl_count": {"typ": "long",
                                     "value": 2},
            "origin_ctl_size": {"typ": "float",
                                "value": 1},
            "mode": {"typ": "enum",
                     "enumName": ["DEBUG", "WIP", "PUB"],
                     "value": "WIP"},
            "end_point": {"typ": "enum",
                          "enumName": ["all",
                                       "objects",
                                       "attributes",
                                       "operators",
                                       "connections",
                                       "cleanup"],
                          "value": "all"},
            "jnt_left_name": {"typ": "string",
                              "value": naming.DEFAULT_JOINT_SIDE_L_NAME},
            "jnt_right_name": {"typ": "string",
                               "value": naming.DEFAULT_JOINT_SIDE_R_NAME},
            "jnt_center_name": {"typ": "string",
                                "value": naming.DEFAULT_JOINT_SIDE_C_NAME},
            "ctl_left_name": {"typ": "string",
                              "value": naming.DEFAULT_SIDE_L_NAME},
            "ctl_right_name": {"typ": "string",
                               "value": naming.DEFAULT_SIDE_R_NAME},
            "ctl_center_name": {"typ": "string",
                                "value": naming.DEFAULT_SIDE_C_NAME},
            "jnt_name_ext": {"typ": "string",
                             "value": naming.DEFAULT_JOINT_EXT_NAME},
            "ctl_name_ext": {"typ": "string",
                             "value": naming.DEFAULT_CTL_EXT_NAME},
            "jnt_name_rule": {"typ": "string",
                              "value": naming.DEFAULT_NAMING_RULE},
            "ctl_name_rule": {"typ": "string",
                              "value": naming.DEFAULT_NAMING_RULE},
            "jnt_description_letter_case": {"typ": "enum",
                                            "enumName": ["default",
                                                         "lower",
                                                         "upper",
                                                         "capitalize"],
                                            "value": "default"},
            "ctl_description_letter_case": {"typ": "enum",
                                            "enumName": ["default",
                                                         "lower",
                                                         "upper",
                                                         "capitalize"],
                                            "value": "default"},
            "jnt_index_padding": {"typ": "long",
                                  "value": 0},
            "ctl_index_padding": {"typ": "long",
                                  "value": 0},
            "connect_jnt_rig": {"typ": "bool",
                                "value": False},
            "force_uni_scale": {"typ": "bool",
                                "value": True},
            "jnt_names": {"typ": "string",
                          "value": ""},
            "sub_jnt_custom_name": {"typ": "bool",
                                    "value": False},
            "l_color_fk": {"typ": "long",
                           "value": 6,
                           "minValue": 0,
                           "maxValue": 31},
            "l_color_ik": {"typ": "long",
                           "value": 18,
                           "minValue": 0,
                           "maxValue": 31},
            "r_color_fk": {"typ": "long",
                           "value": 23,
                           "minValue": 0,
                           "maxValue": 31},
            "r_color_ik": {"typ": "long",
                           "value": 14,
                           "minValue": 0,
                           "maxValue": 31},
            "c_color_fk": {"typ": "long",
                           "value": 13,
                           "minValue": 0,
                           "maxValue": 31},
            "c_color_ik": {"typ": "long",
                           "value": 17,
                           "minValue": 0,
                           "maxValue": 31},
            "use_RGB_colors": {"typ": "bool",
                               "value": False},
            "l_RGB_fk": {"typ": "float3",
                         "value": (0, 0, 1)},
            "l_RGB_ik": {"typ": "float3",
                         "value": (0, 0.25, 1)},
            "r_RGB_fk": {"typ": "float3",
                         "value": (1, 0, 0)},
            "r_RGB_ik": {"typ": "float3",
                         "value": (1, 0.1, 0.25)},
            "c_RGB_fk": {"typ": "float3",
                         "value": (1, 1, 0)},
            "c_RGB_ik": {"typ": "float3",
                         "value": (0, 0.6, 1)},
            "run_sub_pieces": {"typ": "bool",
                               "value": False},
            "sub_pieces": {"typ": "string",
                           "value": ",".join(["objects",
                                              "attributes",
                                              "operators",
                                              "connections",
                                              "cleanup"])},
            "ncurve_ctls_shapes": {"typ": "message",
                                   "multi": True,
                                   "value": {}},
            "icon_name": {"typ": "string",
                          "value": "human"},
            "publish_notes": {"typ": "string",
                              "value": ""}
        }


class Assembly01Guide(piece.Guide):

    def guide(self):
        container = super(Assembly01Guide, self).guide()
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
        attribute.lock(container, attrs)
        attribute.hide(container, attrs)
        pm.delete(container.getShapes())
        ctl_shapes = pm.createNode("transform", name="ctl_shapes", parent=container)
        ctl_shapes.attr("v").set(False)


class Assembly01Rig(piece.Rig):

    def objects(self, context):
        super(Assembly01Rig, self).objects(context)
        data = self.data(Assembly01Data.SELF)

        context["mode"] = data["mode"]
        context["name"] = data["name"]
        asset_container, asset_root = context["asset"]
        model = context["model"]
        skeleton = context["skeleton"]

        origin_rig = self.create_root(context, (0, 0, 0))

        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz"]
        for obj in [asset_root, skeleton]:
            attribute.lock(obj, attrs)
            attribute.hide(obj, attrs + ["v"])
        attribute.hide(model, attrs + ["v"])

        m = dt.Matrix(data["anchors"][0])

        width = 3 + data["origin_ctl_size"]
        name = self.naming("origin", "", "ctl")
        origin_ctl, origin_loc = self.create_ctl(context=context, parent=origin_rig, name=name, parent_ctl=None,
                                                 color=dt.Color(1, 1, 0), keyable_attrs=["tx", "ty", "tz",
                                                                                         "sx", "sy", "sz"], m=m,
                                                 shape="origin", cns=False, width=width)
        host = self.create_host(context, origin_ctl)
        parent_loc = origin_loc
        parent_ctl = origin_ctl
        width = 3.5 + data["origin_ctl_size"]
        for i in range(data["origin_sub_ctl_count"]):
            width = width * 0.8
            name = self.naming(f"sub{i}", "", "ctl")
            parent_ctl, parent_loc = self.create_ctl(context=context, parent=parent_loc, name=name,
                                                     parent_ctl=parent_ctl, color=dt.Color(
                    0, 1, 1), keyable_attrs=["tx", "ty", "tz",
                                             "rx", "ry", "rz", "ro",
                                             "sx", "sy", "sz"], m=m, shape="wave", cns=False, width=width)

        last_loc = parent_loc
        name = self.naming("origin", "ref", "ctl")
        ref = self.create_ref(context=context,
                              name=name,
                              anchor=True,
                              m=last_loc)

        name = self.naming("origin", "", "jnt")
        jnt = self.create_jnt(context=context,
                              parent=None,
                              name=name,
                              description="origin",
                              ref=origin_loc,
                              m=origin_loc.getMatrix(worldSpace=True),
                              uni_scale=data["force_uni_scale"])
        ctl_vis_attr = attribute.add(asset_root,
                                     longName="ctl_vis",
                                     typ="bool",
                                     channelBox=True,
                                     value=True)
        ctl_mouseover_attr = attribute.add(asset_root,
                                           longName="ctl_mouseover",
                                           typ="bool",
                                           channelBox=True,
                                           value=False)
        ctl_playback_attr = attribute.add(asset_root,
                                          longName="ctl_on_playback",
                                          typ="bool",
                                          channelBox=True,
                                          value=True)
        ctl_x_ray_attr = attribute.add(asset_root,
                                       longName="ctl_x_ray",
                                       typ="bool",
                                       channelBox=True,
                                       value=True)
        jnt_vis_attr = attribute.add(asset_root,
                                     longName="jnt_vis",
                                     typ="bool",
                                     channelBox=True,
                                     value=True)
        model_display_type_attr = attribute.add(asset_root,
                                                longName="model_dp_type",
                                                typ="enum",
                                                enumName=["normal", "reference"],
                                                defaultValue=1,
                                                channelBox=True)
        skeleton_display_type_attr = attribute.add(asset_root,
                                                   longName="skeleton_dp_type",
                                                   typ="enum",
                                                   enumName=["normal", "reference"],
                                                   defaultValue=1,
                                                   channelBox=True)
        condition = pm.createNode("condition")
        pm.connectAttr(model_display_type_attr, condition.attr("firstTerm"))
        condition.attr("secondTerm").set(0)
        condition.attr("colorIfTrueR").set(0)
        condition.attr("colorIfFalseR").set(2)
        pm.connectAttr(condition.attr("outColorR"), context["model"].attr("overrideDisplayType"))
        condition = pm.createNode("condition")
        pm.connectAttr(skeleton_display_type_attr, condition.attr("firstTerm"))
        condition.attr("secondTerm").set(0)
        condition.attr("colorIfTrueR").set(0)
        condition.attr("colorIfFalseR").set(2)
        pm.connectAttr(condition.attr("outColorR"), context["skeleton"].attr("overrideDisplayType"))

        pm.container(asset_container,
                     edit=True,
                     publishName="ctl_vis")
        pm.container(asset_container,
                     edit=True,
                     bindAttr=[ctl_vis_attr, "ctl_vis"])
        pm.container(asset_container,
                     edit=True,
                     publishName="ctl_mouseover")
        pm.container(asset_container,
                     edit=True,
                     bindAttr=[ctl_mouseover_attr, "ctl_mouseover"])
        pm.container(asset_container,
                     edit=True,
                     publishName="ctl_on_playback")
        pm.container(asset_container,
                     edit=True,
                     bindAttr=[ctl_playback_attr, "ctl_on_playback"])
        pm.container(asset_container,
                     edit=True,
                     publishName="ctl_x_ray")
        pm.container(asset_container,
                     edit=True,
                     bindAttr=[ctl_x_ray_attr, "ctl_x_ray"])
        pm.container(asset_container,
                     edit=True,
                     publishName="jnt_vis")
        pm.container(asset_container,
                     edit=True,
                     bindAttr=[jnt_vis_attr, "jnt_vis"])
        pm.container(asset_container,
                     edit=True,
                     publishName="model_dp_type")
        pm.container(asset_container,
                     edit=True,
                     bindAttr=[model_display_type_attr, "model_dp_type"])
        pm.container(asset_container,
                     edit=True,
                     publishName="skeleton_dp_type")
        pm.container(asset_container,
                     edit=True,
                     bindAttr=[skeleton_display_type_attr, "skeleton_dp_type"])
        pm.connectAttr(jnt_vis_attr, f"{skeleton}.v")

        ctl_tag = pm.PyNode(pm.controller(origin_ctl, query=True)[0])
        choice = pm.createNode("choice")
        choice.attr("input")[0].set(1)
        choice.attr("input")[1].set(2)
        pm.connectAttr(ctl_mouseover_attr, choice.attr("selector"))
        pm.connectAttr(choice.attr("output"), ctl_tag.attr("visibilityMode"))

    def attributes(self, context):
        self.set_current_container()
        current_container = pm.container(query=True, current=True)
        attrs = pm.listAttr(context["containers"][0][1], channelBox=True) or []
        for attr in attrs:
            pm.container(current_container,
                         edit=True,
                         publishName=attr)
            pm.container(current_container,
                         edit=True,
                         bindAttr=[context['containers'][0][1].attr(attr), attr])

    def operators(self, context):
        super(Assembly01Rig, self).operators(context)

    def connections(self, context):
        super(Assembly01Rig, self).connections(context)


class Assembly01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Assembly01Data(node=node, data=data)
        self._guide = Assembly01Guide(self._ddata)
        self._rig = Assembly01Rig(self._ddata)
