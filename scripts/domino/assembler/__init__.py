# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# built-ins
import json
import uuid
import os
import inspect
from importlib import import_module, reload
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

# domino
from ..lib import attribute, hierarchy, color, icon, vector, matrix, log, utils
from ..lib.rigging import joint, controller, nurbs, container, callback
from ..lib.animation import fcurve
from domino import DOMINO_CUSTOM_COMPONENT, DOMINO_DEFAULT_COMPONENT, DOMINO_CUSTOM_STEP_DIR


def common_component_preset():
    attributes = {
        "component": {"type": "string"},
        "component_version": {"type": "string"},
        "component_id": {"type": "string"},
        "name": {"type": "string"},
        "side": {"type": "enum", "enumName": "C:L:R"},
        "index": {"type": "long"},
        "anchors": {"type": "matrix", "multi": True},
        "parent_anchor": {"type": "string"},
        "custom_ref_index": {"type": "long"},
        "override_colors": {"type": "bool"},
        "use_RGB_colors": {"type": "bool"},
        "RGB_ik": {"type": "float3"},
        "RGB_fk": {"type": "float3"},
        "color_ik": {"type": "long", "minValue": 0, "maxValue": 31},
        "color_fk": {"type": "long", "minValue": 0, "maxValue": 31},
        "create_jnt": {"type": "bool"},
        "jnt_names": {"type": "string"},
        "offset_orient_x": {"type": "double", "minValue": -360, "maxValue": 360},
        "offset_orient_y": {"type": "double", "minValue": -360, "maxValue": 360},
        "offset_orient_z": {"type": "double", "minValue": -360, "maxValue": 360},
        "ctl_shapes": {"type": "nurbsCurve", "multi": True},
        "asset_container": {"type": "string"}
    }
    value = {
        "component_id": str(uuid.uuid4()),
        "parent_anchor": "",
        "custom_ref_index": -1,
        "override_colors": False,
        "use_RGB_colors": False,
        "RGB_ik": (0, 0, 1),
        "RGB_fk": (0, 0.25, 1),
        "color_ik": 13,
        "color_fk": 17,
        "create_jnt": True
    }
    anim = {}
    nurbs_curve = {"ctl_shapes": None}
    _json = {}
    return {"attributes": attributes, "value": value, "anim": anim, "nurbs_curve": nurbs_curve, "json": _json}


class Component:

    def __eq__(self, other):
        return tuple(other) == self.identifier

    def __str__(self):
        return "{0} instance [{1}]".format(self.__class__.__name__, "_".join([x for x in self.identifier if x]))

    def __init__(self, data=None):
        self.data = {k: data[k] for k in data.keys() if not k.startswith("_")} if data else common_component_preset()
        self.children = []
        self.parent = None

    @property
    def identifier(self):
        return (self.data["value"]["name"], None, None) \
            if self.data["value"]["component"] == "assembly" \
            else (self.data["value"]["name"], self.data["value"]["side"], self.data["value"]["index"])

    @property
    def negate(self):
        return True if self.data["value"]["side"] == "R" else False

    def add_child(self, data):
        self.children.append(data if isinstance(data, Component) else Component(data))
        self.children[-1].parent = self

    def get_parent(self, generations=1):
        component = self
        while component.parent:
            if generations == 0:
                return component
            component = component.parent
            generations -= 1
        if component.identifier == self.identifier:
            return None
        return component

    def pull_data_from_node(self, node):
        def _nurbs_curve(__attr):
            curve_data = {}
            if "multi" in attributes[attr]:
                for child_attr in mc.listAttr(node + "." + attr, multi=True) or []:
                    selection_list = om2.MSelectionList()
                    selection_list.add(node + "." + child_attr)
                    plug = selection_list.getPlug(0)

                    crv = mc.listConnections(node + "." + child_attr, destination=False, source=True)
                    if crv:
                        curve_data[str(plug.logicalIndex())] = nurbs.data(crv[0])
            else:
                crv = mc.listConnections(node + "." + __attr, destination=False, source=True)
                if crv:
                    curve_data["0"] = nurbs.data(crv[0])
            return curve_data

        def _enum(__attr):
            return mc.getAttr(node + "." + __attr, asString=True)

        def _string(__attr):
            if __attr == "parent_anchor" and mc.nodeType(node) == "dagContainer":
                parent = hierarchy.get_parent(node)
                plug = None
                while not plug and parent:
                    plug = mc.listConnections(parent + ".worldMatrix[0]",
                                              source=False,
                                              destination=True,
                                              plugs=True,
                                              type="dagContainer")
                    parent = hierarchy.get_parent(parent)
                if plug:
                    selection_list = om2.MSelectionList()
                    selection_list.add(plug[0])
                    plug = selection_list.getPlug(0)
                    return str(plug.logicalIndex())
            return mc.getAttr(node + "." + __attr) or ""

        def _anim(__attr):
            anim_curve = mc.listConnections(node + "." + __attr, source=True, destination=False, type="animCurve")
            return fcurve.get_fcurve(anim_curve[0])

        def pull():
            def _get_attr(_attr):
                if attributes[attr]["type"] == "string":
                    return _string(_attr)
                elif attributes[attr]["type"] == "enum":
                    return _enum(_attr)
                elif attributes[attr]["type"] == "float3":
                    return mc.getAttr(node + "." + _attr)[0]
                else:
                    return mc.getAttr(node + "." + _attr)

            if attr in nurbs_curve:
                data = _nurbs_curve(attr)
            elif "multi" in attributes[attr]:
                data = []
                for i, child_attr in enumerate(mc.listAttr(node + "." + attr, multi=True) or []):
                    data.append(_get_attr(child_attr))
            elif attr in anim:
                data = _anim(attr)
            elif attr in _json:
                data = json.loads(_get_attr(attr))
            else:
                data = _get_attr(attr)

            # self.data update
            if attr in anim:
                anim[attr] = data
            elif attr in nurbs_curve:
                nurbs_curve[attr] = data
            elif attr in _json:
                _json[attr] = data
            else:
                value[attr] = data

        component_name = mc.getAttr(node + ".component")
        component_mod = import_component_module(component_name)
        component_preset = component_mod.component_preset()
        attributes = component_preset["attributes"]
        value = component_preset["value"]
        anim = component_preset["anim"]
        nurbs_curve = component_preset["nurbs_curve"]
        _json = component_preset["json"]
        for attr in attributes.keys():
            if mc.attributeQuery(attr, node=node, exists=True):
                pull()
        self.data = component_preset

    def push_data_to_node(self, node):
        def _nurbs_curve(__attr, __value):
            if mc.nodeType(node) == "dagContainer" and __value:
                if attr == "ctl_shapes":
                    root = hierarchy.get_parent(node, generations=-1)
                    if root is None:
                        root = node
                    parent = root + "|ctl_shapes"
                else:
                    parent = node
                if "multi" in attributes[attr]:
                    for index in __value.keys():
                        crv = nurbs.build(__value[index], parent=parent, match=True)
                        mc.connectAttr(crv + ".worldSpace[0]", node + "." + __attr + "[{0}]".format(index))
                        mc.setAttr(crv + ".dispHull", 1)
                        mc.setAttr(crv + ".dispCV", 1)
                        mc.setAttr(crv + ".overrideEnabled", 1)
                        mc.setAttr(crv + ".overrideDisplayType", 2)
                else:
                    crv = nurbs.build(__value[str(0)], parent=parent, match=True)
                    mc.connectAttr(crv + ".worldSpace[0]", node + "." + __attr)
                    mc.setAttr(crv + ".dispHull", 1)
                    mc.setAttr(crv + ".dispCV", 1)
                    mc.setAttr(crv + ".overrideEnabled", 1)
                    mc.setAttr(crv + ".overrideDisplayType", 2)

        def _enum(__attr, __value):
            enum_name = mc.attributeQuery(__attr, node=node, listEnum=True)[0]
            mc.setAttr(node + "." + __attr, enum_name.split(":").index(__value))

        def _matrix(__attr, __value):
            inputs = mc.listConnections(node + "." + __attr, source=True, destination=False)
            if inputs:
                mc.xform(inputs[0], matrix=__value, worldSpace=True)
            else:
                mc.setAttr(node + "." + __attr, __value, type="matrix")

        def _string(__attr, __value):
            mc.setAttr(node + "." + __attr, __value, type="string")

        def _anim(__attr, __value):
            fcurve.set_fcurve(__value, driven=[node + "." + __attr])

        def push():
            def _set_attr(_attr, _value):
                if attributes[attr]["type"] == "matrix":
                    _matrix(_attr, _value)
                elif attributes[attr]["type"] == "string":
                    _string(_attr, _value)
                elif attributes[attr]["type"] == "enum":
                    _enum(_attr, _value)
                elif isinstance(_value, (tuple, list)):
                    mc.setAttr(node + "." + _attr, *_value)
                else:
                    mc.setAttr(node + "." + _attr, _value)

            if attr in nurbs_curve:
                _nurbs_curve(attr, nurbs_curve[attr])
            elif "multi" in attributes[attr]:
                if attr in value:
                    for i, v in enumerate(value[attr]):
                        _set_attr(attr + "[{}]".format(i), v)
            elif attr in value:
                _set_attr(attr, value[attr])
            elif attr in anim:
                _anim(attr, anim[attr])
            elif attr in _json:
                _set_attr(attr, json.dumps(_json[attr], ensure_ascii=False))

        attributes = self.data["attributes"]
        value = self.data["value"]
        anim = self.data["anim"]
        nurbs_curve = self.data["nurbs_curve"]
        _json = self.data["json"]
        for attr in attributes.keys():
            attribute.add_attr(node, longName=attr, **attributes[attr])
            push()


class Guide:

    def __init__(self, component=None, root=None, recipe=None):
        self.component = component
        if root:
            self.component.pull_data_from_node(root)
        self.root = root
        self.guide_recipe = recipe

    @property
    def identifier(self):
        return "_".join([str(x) for x in self.component.identifier if x is not None])

    def create(self):
        def _root(_parent, _m, name="guide"):
            ctr = mc.container(name=self.identifier + "_" + name, type="dagContainer")
            icon.guide_root(ctr, _parent, _m)
            attribute.add_attr(ctr, longName="is_guide", type="bool", keyable=False)
            attribute.add_attr(ctr, longName="_extension", type="string")
            mc.setAttr(ctr + "._extension", name, type="string")
            attribute.add_attr(ctr, longName="_orientation", type="message")
            attribute.add_attr(ctr, longName="_pole_vec", type="message")
            attribute.add_attr(ctr, longName="_display_curve", type="message", multi=True)
            return ctr

        def _position(_parent, _extension, _m, _shape=None):
            _pos = mc.createNode("transform")
            icon.guide_position(_pos, _parent, _m)
            guide_container = _parent
            if mc.nodeType(guide_container) != "dagContainer":
                guide_container = mc.container(query=True, findContainer=_parent)
            index = len(mc.listConnections(guide_container + ".anchors", source=True, destination=False))
            _pos = mc.rename(_pos, self.identifier + "_" + _extension)
            mc.setAttr(_pos + ".displayHandle", True)
            attribute.add_attr(_pos, longName="is_guide", type="bool", keyable=False)
            attribute.add_attr(_pos, longName="_extension", type="string")
            mc.setAttr(_pos + "._extension", _extension, type="string")
            mc.connectAttr(_pos + ".worldMatrix[0]", guide_container + ".anchors[{0}]".format(index))

            if _shape is not None:
                s = icon.create(None,
                                "TEMP",
                                "axis",
                                None,
                                om2.MMatrix(),
                                width=1,
                                height=1,
                                depth=1,
                                po=(0, 0, 0),
                                ro=(0, 0, 0))
                mc.setAttr(s + ".s", 0.3, 0.3, 0.3)
                mc.makeIdentity(s, apply=True, scale=True)
                icon.replace(s, _pos)
                mc.delete(s)

        def _orientation(_parent, _target, _extension):
            ori = mc.createNode("transform", parent=_parent)
            icon.guide_orientation(ori)
            aim = mc.aimConstraint(_target,
                                   ori,
                                   aimVector=(1, 0, 0),
                                   upVector=(0, 1, 0),
                                   worldUpType="objectrotation",
                                   worldUpVector=(0, 1, 0),
                                   worldUpObject=_parent)[0]
            mc.connectAttr(_parent + ".offset", aim + ".offsetX")
            mc.connectAttr(ori + ".worldMatrix[0]", _parent + ".offset_matrix")
            lock_attrs = ("rx", "ry", "rz")
            [mc.setAttr(ori + "." + _attr, lock=True) for _attr in lock_attrs]
            ori = mc.rename(ori, self.identifier + "_" + _extension)
            mc.setAttr(ori + ".hiddenInOutliner", True)
            attribute.add_attr(ori, longName="is_guide", type="bool", keyable=False)
            attribute.add_attr(ori, longName="_extension", type="string")
            mc.setAttr(ori + "._extension", _extension, type="string")
            mc.connectAttr(ori + ".message", _parent + "._orientation")
            mc.setAttr(self.root + ".offset", channelBox=True)

        def _pole_vec(_parent, _source_nodes, _extension):
            pole_vec_node = mc.spaceLocator()
            pole_vec_node = mc.parent(pole_vec_node, _parent)
            pole_vec_node = mc.rename(pole_vec_node, self.identifier + "_loc")
            mc.matchTransform(pole_vec_node, _parent, position=True, rotation=True, scale=True)
            mc.setAttr(pole_vec_node + ".hiddenInOutliner", True)
            mc.setAttr(pole_vec_node + ".overrideEnabled", 1)
            mc.setAttr(pole_vec_node + ".overrideRGBColors", 1)
            mc.setAttr(pole_vec_node + ".overrideColorRGB", 0.1, 1, 0.8)
            mc.setAttr(pole_vec_node + ".localScale", 0.5, 0.5, 0.5)

            distance_attr = _parent + ".offset_pole_vec"
            vector.set_pole_vector(pole_vec_node, _source_nodes, distance_attr)

            lock_hide_attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
            [mc.setAttr(pole_vec_node + "." + _attr, lock=True) for _attr in lock_hide_attrs]
            [mc.setAttr(pole_vec_node + "." + _attr, keyable=False) for _attr in lock_hide_attrs]
            mc.connectAttr(pole_vec_node + ".worldMatrix[0]", _parent + ".offset_pole_vec_matrix")
            attribute.add_attr(pole_vec_node, longName="is_guide", type="bool", keyable=False)
            attribute.add_attr(pole_vec_node, longName="_extension", type="string")
            mc.setAttr(pole_vec_node + "._extension", _extension, type="string")
            mc.connectAttr(pole_vec_node + ".message", _parent + "._pole_vec")
            _display_curve(self.root, [_source_nodes[1], pole_vec_node], _extension="pvDpCrv", _thickness=1)
            mc.setAttr(self.root + ".offset_pole_vec", channelBox=True)

        def _display_curve(_parent, _nodes, _extension, _degree=1, _thickness=2):
            display_curve = mc.createNode("transform")
            icon.generate(display_curve,
                          [(0, 0, 0) for _ in _nodes],
                          _degree,
                          om2.MColor((0.55, 0.55, 0.55, 0.55)),
                          thickness=_thickness)
            shape = mc.listRelatives(display_curve, shapes=True)[0]
            mc.setAttr(shape + ".overrideDisplayType", 2)
            nurbs.constraint(display_curve, _nodes)
            mc.connectAttr(_parent + ".worldInverseMatrix[0]", display_curve + ".offsetParentMatrix")
            lock_hide_attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
            [mc.setAttr(display_curve + "." + _attr, lock=True) for _attr in lock_hide_attrs]
            [mc.setAttr(display_curve + "." + _attr, keyable=False) for _attr in lock_hide_attrs]
            display_curve = mc.parent(display_curve, _parent)[0]
            mc.setAttr(display_curve + ".hiddenInOutliner", True)
            display_curve = mc.rename(display_curve, self.identifier + "_displayCrv")
            attribute.add_attr(display_curve, longName="is_guide", type="bool", keyable=False)
            attribute.add_attr(display_curve, longName="_extension", type="string")
            mc.setAttr(display_curve + "._extension", _extension, type="string")
            index = len(mc.listAttr(_parent + "._display_curve", multi=True) or [])
            mc.connectAttr(display_curve + ".message", _parent + "._display_curve[{0}]".format(index))

        attributes = self.component.data["attributes"]
        value = self.component.data["value"]

        if "flexible_position" in self.guide_recipe:
            position_min_value, guide_name_extension, direction_vector = self.guide_recipe["flexible_position"]
            div_value = 0
            if len(value["anchors"]) <= position_min_value:
                result = mc.promptDialog(title="Divide input",
                                         message="number (int)",
                                         button=("ok", "cancel"),
                                         defaultButton="ok")
                if result == "ok":
                    text = mc.promptDialog(query=True, text=True)
                    try:
                        div_value = int(text)
                    except ValueError:
                        pass
                self.suitable_anchors(div_value, direction_vector)
            if len(self.guide_recipe["position"]) < position_min_value:
                direction_vector = len(value["anchors"]) - len(self.guide_recipe["position"]) - 1
                self.suitable_recipe(div_value if div_value else direction_vector)
            if len(value["anchors"]) <= position_min_value:
                return False

        parent = None
        if "parent_anchor" in attributes:
            if value["parent_anchor"]:
                parent_component_root = mc.ls(selection=True)[0]
                while mc.nodeType(parent_component_root) != "dagContainer":
                    parent_component_root = hierarchy.get_parent(parent_component_root)
                    if parent_component_root is None:
                        break
                parent = mc.listConnections(parent_component_root + ".anchors[{0}]".format(value["parent_anchor"]),
                                            destination=False,
                                            source=True,
                                            type="transform")[0]
            else:
                parent = mc.ls(selection=True)[0]

        anchors_matrices = value["anchors"]
        root_name = "guide"
        if "root" in self.guide_recipe:
            root_name = self.guide_recipe["root"]
        self.root = _root(parent, anchors_matrices[0], root_name)
        self.component.push_data_to_node(self.root)
        mc.connectAttr(self.root + ".worldMatrix[0]", self.root + ".anchors[0]")

        if "position" in self.guide_recipe:
            for i, m in enumerate(anchors_matrices[1:]):
                if len(self.guide_recipe["position"][i]) < 3:
                    self.guide_recipe["position"][i] = list(self.guide_recipe["position"][i]) + [None]
                parent_guide_index, guide_name_extension, shape = self.guide_recipe["position"][i]
                parent = mc.listConnections(self.root + ".anchors[{0}]".format(parent_guide_index),
                                            source=True,
                                            destination=False)[0]
                _position(parent, guide_name_extension, m, shape)

        if "orientation" in self.guide_recipe:
            parent_target_index, guide_name_extension = self.guide_recipe["orientation"]
            target = mc.listConnections(self.root + ".anchors[{0}]".format(parent_target_index),
                                        source=True,
                                        destination=False)[0]
            _orientation(self.root, target, guide_name_extension)

        if "pole_vec" in self.guide_recipe:
            source_indexes, guide_name_extension = self.guide_recipe["pole_vec"]
            anchors = mc.listConnections(self.root + ".anchors", source=True, destination=False)
            _pole_vec(self.root, [anchors[x] for x in source_indexes], guide_name_extension)

        if "display_curve" in self.guide_recipe:
            for dp_crv_info in self.guide_recipe["display_curve"]:
                source_indexes = dp_crv_info[0]
                guide_name_extension = dp_crv_info[1]
                degree = 1
                thickness = 2
                if len(dp_crv_info) > 2:
                    degree = dp_crv_info[2]
                    thickness = dp_crv_info[3]
                anchors = mc.listConnections(self.root + ".anchors", source=True, destination=False)
                _display_curve(self.root,
                               [anchors[x] for x in source_indexes],
                               guide_name_extension,
                               _degree=degree,
                               _thickness=thickness)

        if "lock_attrs" in self.guide_recipe:
            for i, attrs in enumerate(self.guide_recipe["lock_attrs"]):
                pos = mc.listConnections(self.root + ".anchors[{0}]".format(i),
                                         source=True,
                                         destination=False)[0]
                for attr in attrs:
                    mc.setAttr(pos + "." + attr, lock=True)

        if value["component"] == "assembly":
            ctl_shapes = mc.createNode("transform", name="ctl_shapes", parent=self.root)
            mc.setAttr(ctl_shapes + ".v", False)
            mc.setAttr(self.root + ".displayHandle", True)
            mc.delete(mc.listRelatives(self.root, shapes=True))
        mc.select(self.root)
        return True

    def rename(self):
        attrs = ["anchors", "_orientation", "_pole_vec", "_display_curve"]
        new_names = []
        sel_list = om2.MSelectionList()
        count = 0
        for attr in attrs:
            for node in mc.listConnections(self.root + "." + attr, source=True, destination=False) or []:
                sel_list.add(node)
                count += 1
        for i in range(count):
            node = sel_list.getDagPath(i).fullPathName()
            extension = mc.getAttr(node + "._extension")
            new_names.append(mc.rename(node, self.identifier + "_" + extension))
        return new_names

    def suitable_recipe(self, div_value):
        min_value = len(self.guide_recipe["position"])
        flex_display_curve = list([x + min_value + 1 for x in range(div_value)])
        if 0 not in flex_display_curve:
            flex_display_curve.insert(0, 0)
        if "display_curve" not in self.guide_recipe:
            self.guide_recipe["display_curve"] = []
        self.guide_recipe["display_curve"].append((flex_display_curve, "flexDpCrv"))

        for i in range(div_value):
            parent_index = 0 if i == 0 else len(self.guide_recipe["position"])
            name = self.guide_recipe["flexible_position"][1] % i
            self.guide_recipe["position"].append((parent_index, name))

    def suitable_anchors(self, div_value, direction_vector=(1, 0, 0)):
        for i in range(div_value):
            m = om2.MTransformationMatrix()
            m.setTranslation(om2.MVector(direction_vector) + om2.MVector([x * i for x in direction_vector]),
                             om2.MSpace.kWorld)
            self.component.data["value"]["anchors"].append(list(m.asMatrix()))

    def suitable_index(self, name, side, remove_index=None):
        def _recursive(h):
            for node, v in h.items():
                if mc.getAttr(node + ".name") == name and mc.getAttr(node + ".side", asString=True) == side:
                    indexes.append(mc.getAttr(node + ".index"))
                _recursive(v)

        guide_hierarchy = get_guide_hierarchy(self.root, full_path=True)
        indexes = []
        for value in guide_hierarchy.values():
            _recursive(value)
        if remove_index and remove_index in indexes:
            indexes.remove(remove_index)

        index = 0
        while index in indexes:
            index += 1
        return index


class Rig:

    def __init__(self, component):
        self.component = component
        self.root = None
        self.host = None
        self.children = []
        self.parent = None

    @property
    def identifier(self):
        return "_".join([str(x) for x in self.component.identifier if x is not None])

    def add_child(self, rig):
        self.children.append(rig)
        rig.parent = self

    def generate_color(self, color_type):
        return color.solve(self.component.data["value"], self.component.get_parent(-1).data["value"], color_type)

    def generate_name(self, description="", extension="", rule="ctl" or "jnt", negate=False):
        component_data = self.component.data["value"]
        assembly_component = self.component.get_parent(generations=-1)
        if assembly_component is None:
            assembly_component = self.component
        assembly_data = assembly_component.data["value"]

        name_rule = assembly_data["{0}_name_rule".format(rule)]
        padding = assembly_data["{0}_index_padding".format(rule)]
        description_letter_case = assembly_data["{0}_description_letter_case".format(rule)]
        side_set = [assembly_data["{0}_center_name".format(rule)],
                    assembly_data["{0}_left_name".format(rule)],
                    assembly_data["{0}_right_name".format(rule)]]
        if not extension:
            extension = assembly_data["{0}_name_ext".format(rule)]

        if description_letter_case == "lower":
            description = description.lower()
        elif description_letter_case == "upper":
            description = description.upper()
        elif description_letter_case == "capitalize":
            description = description.capitalize()

        index_filter = ["C", "L", "R"]
        if None in self.component.identifier:
            args = {
                "name": component_data["name"],
                "side": "",
                "index": "",
                "description": description,
                "extension": extension
            }
        else:
            side = component_data["side"]
            if negate and component_data["side"] != "C":
                side = "R" if component_data["side"] == "L" else "L"
            args = {
                "name": component_data["name"],
                "side": side_set[index_filter.index(side)],
                "index": str(component_data["index"]).zfill(int(padding)),
                "description": description,
                "extension": extension
            }
        for k in args.copy():
            if k not in name_rule:
                del args[k]
        name = name_rule.format(**args)
        name = "_".join([x for x in name.split("_") if x])
        return name

    def find_ctls(self, context, data):
        data = [x.split(" | ") for x in data.split(",")]
        ctls = []
        for index, identifier in data:
            if identifier not in context:
                log.Logger.warning(identifier + " don't exists")
                continue
            ctls.append(context[identifier]["ctls"][int(index)].fullPathName())
        return ctls

    def create_root(self, context):
        name = self.generate_name(description="", extension="_root", rule="ctl")

        rig_grp = context["asset"][1]
        self.root = mc.createNode("transform", name=name, parent=rig_grp + "|roots")
        self.component.push_data_to_node(self.root)
        attribute.add_attr(self.root, longName="ctls", type="message", multi=True)
        attribute.add_attr(self.root, longName="refs", type="message", multi=True)
        attribute.add_attr(self.root, longName="ref_anchors", type="message", multi=True)
        attribute.add_attr(self.root, longName="jnts", type="message", multi=True)
        attribute.add_attr(self.root, longName="host", type="message")
        attribute.add_attr(self.root, longName="__children", type="message")
        attribute.add_attr(self.root, longName="__parent", type="message")

        value = self.component.data["value"]
        ref = None
        parent_rig = self.parent
        if None in self.component.identifier:
            attribute.add_attr(rig_grp, longName="assembly_node", type="message")
            attribute.add_attr(self.root, longName="rig_grp", type="message")
            mc.connectAttr(rig_grp + ".assembly_node", self.root + ".rig_grp")
        elif parent_rig and None in parent_rig.component.identifier and None not in self.component.identifier:
            ref = mc.listConnections(parent_rig.root + ".refs[0]", destination=False, source=True)[0]
        elif parent_rig and None not in parent_rig.component.identifier and None not in self.component.identifier:
            ref_anchor = int(value["parent_anchor"])
            custom_ref_index = value["custom_ref_index"]

            refs_element = mc.listAttr(parent_rig.root + ".refs", multi=True)
            ref_anchors_element = mc.listAttr(parent_rig.root + ".ref_anchors", multi=True)

            refs_index = None
            ref_anchors_index = None
            if -1 < custom_ref_index < len(refs_element):
                refs_index = custom_ref_index
            elif custom_ref_index >= len(refs_element):
                refs_index = -1
            elif custom_ref_index == -1:
                if ref_anchor >= len(ref_anchors_element):
                    ref_anchors_index = -1
                else:
                    ref_anchors_index = ref_anchor
            if refs_index is not None:
                attr = refs_element[refs_index]
                ref = mc.listConnections(parent_rig.root + "." + attr, destination=False, source=True)[0]
            if ref_anchors_index is not None:
                attr = ref_anchors_element[ref_anchors_index]
                ref = mc.listConnections(parent_rig.root + "." + attr, destination=False, source=True)[0]

        if ref:
            mc.connectAttr(parent_rig.root + ".__children", self.root + ".__parent")
            mc.connectAttr(ref + ".worldMatrix[0]", self.root + ".offsetParentMatrix")

        m = om2.MMatrix(value["anchors"][0])
        m = matrix.set_matrix_scale(m, (1, 1, 1))
        mc.xform(self.root, matrix=m, worldSpace=True)
        cb_attrs = mc.listAttr(self.root, keyable=True)
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
        [mc.setAttr(self.root + "." + attr, lock=True) for attr in attrs + cb_attrs]
        [mc.setAttr(self.root + "." + attr, keyable=False) for attr in attrs + cb_attrs + ["v"]]

        context[self.identifier] = {
            "root": self.root,
            "ctls": [],
            "refs": [],
            "jnts": []
        }
        return self.root

    def finalize_ctl_setup(self, ctl):
        index = len(mc.listAttr(self.root + ".ctls", multi=True) or [])
        mc.connectAttr(ctl + ".message", self.root + ".ctls[{0}]".format(index))
        if str(index) in self.component.data["nurbs_curve"]["ctl_shapes"]:
            nurbs.build(self.component.data["nurbs_curve"]["ctl_shapes"][str(index)], replace=ctl)
            mc.connectAttr(ctl + ".message", self.root + ".ctl_shapes[{0}]".format(index), force=True)
            for s in mc.listRelatives(ctl, shapes=True, fullPath=True) or []:
                mc.setAttr(s + ".isHistoricallyInteresting", 0)

    def create_host(self, context):
        name = self.generate_name(description="", extension="_host", rule="ctl")
        negate_name = self.generate_name(description="", extension="_host", rule="ctl", negate=True)
        parent_ctl = controller.get_parent(context[self.identifier]["ctls"][0])
        shape_args = {"shape": None, "color": om2.MColor((0, 0, 0))}
        config = {"identifier": self.identifier, "mirror_ctl_name": negate_name}
        self.host = controller.add_ctl(self.root, name, om2.MMatrix(), parent_ctl, shape_args=shape_args, **config)
        self.finalize_ctl_setup(self.host)
        mc.connectAttr(self.host + ".message", self.root + ".host")
        context[self.identifier]["host"] = self.host
        return self.host

    def create_ctl(self, context, parent, name, m, parent_ctl, attrs, mirror_config, shape_args, cns=False, **config):
        config.update(identifier=self.identifier)
        assembly_component = self.component.get_parent(generations=-1)
        if assembly_component is None:
            assembly_component = self.component
        assembly_component_data = assembly_component.data["value"]

        # get parent
        if parent is None:
            parent = self.root

        if parent_ctl is None:
            # get parent controller
            parent_rig = self.parent
            if parent_rig is not None:
                while not context[parent_rig.identifier]["ctls"]:
                    parent_rig = parent_rig.parent
                    if parent_rig is None:
                        break
                parent_ctl = None if parent_rig is None else context[parent_rig.identifier]["ctls"][-1]

        # name
        npo_name = name.replace(assembly_component_data["ctl_name_ext"], "npo")
        ph_name = name.replace(assembly_component_data["ctl_name_ext"], "placeholder")

        if "color" not in shape_args:
            shape_args.update(color=om2.MColor((1, 1, 0)))
        if "thickness" not in shape_args:
            shape_args.update(thickness=1)
        if "po" not in shape_args:
            shape_args.update(po=(0, 0, 0))
        if "ro" not in shape_args:
            shape_args.update(ro=(0, 0, 0))

        # create
        cns_ctl = None
        if cns:
            cns_config = config.copy()
            cns_name = name.replace(assembly_component_data["ctl_name_ext"], "cns")
            cns_config.update(
                mirror_ctl_name=config["mirror_ctl_name"].replace(assembly_component_data["ctl_name_ext"], "cns"))
            cns_ctl = controller.add_ctl(parent, cns_name, m, parent_ctl, ("tx", "ty", "tz", "rx", "ry", "rz"),
                                         mirror_config, shape_args=shape_args, **cns_config)
            parent_ctl = cns_ctl

        ctl = controller.add_ctl(parent, name, m, parent_ctl, attrs, mirror_config, shape_args=shape_args, **config)
        npo, ctl = controller.add_npo(ctl, npo_name, offset_parent_matrix=True)
        if cns_ctl:
            cns_ctl = mc.parent(cns_ctl, npo)[0]
            ctl = mc.parent(ctl, cns_ctl)[0]
            mc.addAttr(ctl, longName="cns_vis", attributeType="bool", keyable=True)
            mc.setAttr(ctl + ".cns_vis", False)
        ph = controller.add_placeholder(ctl, ph_name)
        npo_opm = matrix.get_matrix(npo, offset_parent_matrix=True)
        npo_scale_z = om2.MTransformationMatrix(npo_opm).scale(om2.MSpace.kObject)[2]
        if npo_scale_z < 0:
            mc.setAttr(ph + ".sz", -1)

        # finalize setup
        if cns:
            self.finalize_ctl_setup(cns_ctl)
            for shape in mc.listRelatives(cns_ctl, shapes=True, fullPath=True):
                mc.connectAttr(ctl + ".cns_vis", shape + ".v")
        self.finalize_ctl_setup(ctl)

        if cns:
            cns_l = om2.MSelectionList()
            cns_l.add(cns_ctl)
            context[self.identifier]["ctls"].append(cns_l.getDagPath(0))
        sel_l = om2.MSelectionList()
        sel_l.add(ctl)
        context[self.identifier]["ctls"].append(sel_l.getDagPath(0))
        return ctl, ph

    def create_ref(self, context, name, anchor, m):
        value = self.component.data["value"]
        offset_rotate = (0, 0, 0)
        if None not in self.component.identifier:
            offset_rotate = (value["offset_orient_x"], value["offset_orient_y"], value["offset_orient_z"])
        ref = controller.add_placeholder(self.root, name, offset_rotate)
        if m:
            mc.setAttr(ref + ".inheritsTransform", False)
            mc.connectAttr(m + ".worldMatrix[0]", ref + ".offsetParentMatrix")
        index = len(mc.listAttr(self.root + ".refs", multi=True) or [])
        mc.connectAttr(ref + ".message", self.root + ".refs[{0}]".format(index))
        lock_hide_attrs = ["tx", "ty", "tz", "sx", "sy", "sz", "v"]
        [mc.setAttr(ref + "." + attr, lock=True) for attr in lock_hide_attrs]
        [mc.setAttr(ref + "." + attr, keyable=False) for attr in lock_hide_attrs]
        if anchor:
            index = len(mc.listAttr(self.root + ".ref_anchors", multi=True) or [])
            mc.connectAttr(ref + ".message", self.root + ".ref_anchors[{0}]".format(index))
        context[self.identifier]["refs"].append(ref)
        return ref

    def create_jnt(self, context, parent, name, description, ref, m, leaf=False, uni_scale=False):
        value = self.component.data["value"]

        index = len(mc.listAttr(self.root + ".jnts", multi=True) or [])
        # joint name
        if "jnt_names" in value and value["jnt_names"]:
            jnt_name = value["jnt_names"].split(",")
            if index < len(jnt_name):
                if jnt_name:
                    name = jnt_name[index]

        # get parent piece joint
        skeleton_grp = context["skeleton"]
        parent_rig = self.parent
        if not parent:
            if None in self.component.identifier:
                parent = skeleton_grp
            elif parent_rig and (None in parent_rig.component.identifier):
                parent = mc.listConnections(parent_rig.root + ".jnts[0]", destination=False, source=True)[0]

        if not parent:
            ref_anchor = int(value["parent_anchor"])
            custom_ref_index = value["custom_ref_index"]
            rig = self
            attr = None
            while not parent:
                rig = rig.parent
                # Infinite Loop Prevention
                if rig is None:
                    break
                if not len(mc.listAttr(rig.root + ".jnts", multi=True) or []):
                    ref_anchor = -1
                    continue

                refs_element = mc.listAttr(rig.root + ".refs", multi=True)
                ref_anchors_element = mc.listAttr(rig.root + ".ref_anchors", multi=True)

                refs_index = None
                ref_anchors_index = None
                if -1 < custom_ref_index < len(refs_element):
                    refs_index = custom_ref_index
                elif custom_ref_index >= len(refs_element):
                    refs_index = -1
                elif custom_ref_index == -1:
                    if ref_anchor >= len(ref_anchors_element):
                        ref_anchors_index = -1
                    else:
                        ref_anchors_index = ref_anchor
                if ref_anchors_index is not None:
                    _ref = mc.listConnections(rig.root + ".ref_anchors",
                                              source=True,
                                              destination=False)[ref_anchors_index]
                    plugs = mc.listConnections(_ref + ".message", source=False, destination=True, plugs=True)
                    for plug in plugs:
                        if "refs" not in plug:
                            continue
                        attr_name, index_str = plug.split(".")[-1].split("[")
                        if attr_name == "refs":
                            refs_index = int(index_str.split("]")[0])
                if refs_index is not None:
                    if refs_index >= len(mc.listAttr(rig.root + ".jnts", multi=True) or []):
                        refs_index = -1
                    attr = mc.listAttr(rig.root + ".jnts", multi=True)[refs_index]
                parent = mc.listConnections(rig.root + "." + attr, destination=False, source=True)[0]

        # create joint
        jnt = joint.add_joint(parent, name, m)
        container.remove_node_from_asset(jnt)
        nonkeyable_attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz"]
        [mc.setAttr(jnt + "." + attr, channelBox=True) for attr in nonkeyable_attrs]
        mc.setAttr(jnt + ".v", lock=True)
        mc.setAttr(jnt + ".v", keyable=False)

        # connect ref to jnt
        if ref:
            joint.connect_space(ref, jnt)

        # joint label setup
        if "side" not in value:
            value["side"] = None
        if "index" not in value:
            value["index"] = None
        joint.labeling(jnt, value["name"], value["side"], value["index"], description)

        # jnts connect
        mc.connectAttr(jnt + ".message", self.root + ".jnts[{0}]".format(index))
        context[self.identifier]["jnts"].append(jnt)

        if leaf:
            index = len(mc.listAttr(self.root + ".refs", multi=True) or [])
            mc.connectAttr(jnt + ".message", self.root + ".refs[{0}".format(index))
            context[self.identifier]["refs"].append(jnt)
        return jnt

    def set_current_container(self, context):
        identifier = self.component.data["value"]["asset_container"]
        container_name = identifier + "_container" if identifier else self.identifier + "_container"

        if context["asset"][0].startswith(container_name):
            container.set_current_asset(context["asset"][0])
            return None
        is_exists = False
        for c in context["container"]:
            if c.startswith(container_name):
                is_exists = True
                container.set_current_asset(c)
        if not is_exists:
            child_container = container.add_advanced_asset(context["asset"][0], container_name)
            context["container"].append(child_container)

    def build(self, context, step):
        if step == 0:
            log.Logger.info("objects [" + self.identifier + "]")
            self.set_current_container(context)
            self.objects(context)
        elif step == 1:
            log.Logger.info("attributes [" + self.identifier + "]")
            self.set_current_container(context)
            self.attributes(context)
        elif step == 2:
            log.Logger.info("operators [" + self.identifier + "]")
            self.set_current_container(context)
            self.operators(context)
        elif step == 3:
            log.Logger.info("connections [" + self.identifier + "]")
            self.set_current_container(context)
            self.connections(context)

    def objects(self, context):
        ...

    def attributes(self, context):
        self.create_host(context)
        attr = attribute.add_attr(self.host, longName="_I", type="enum", enumName="I")
        mc.setAttr(attr, channelBox=True)

    def operators(self, context):
        ...

    def connections(self, context):
        ...


class CustomStep:

    def run(self, context):
        ...


def get_rig_hierarchy(node):
    def _recursive(_node, _data):
        data[_node] = {}
        for child in mc.listConnections(_node + ".__children", source=False, destination=True, type="transform") or []:
            _data[_node][child] = {}
            _recursive(child, _data[_node])

    data = {}
    _recursive(node, data)
    return data


def get_guide_hierarchy(node, node_type="dagContainer", full_path=False):
    def _recursive(_node, _data, parent):
        __data = _data
        if mc.nodeType(_node) == node_type and _node != parent:
            if parent not in _data:
                _data[parent] = {}
            _data[parent].update({_node: {}})
            __data = _data[parent]
        children = mc.listRelatives(_node, children=True, fullPath=full_path) or []
        for child in children:
            _recursive(child, __data, _node if mc.nodeType(_node) == node_type else parent)

    node = mc.ls(node, long=full_path)[0]
    hierarchy_data = {}
    if mc.nodeType(node) == node_type:
        hierarchy_data[node] = {}
    _recursive(node, hierarchy_data, node if mc.nodeType(node) == node_type else None)

    if mc.getAttr(list(hierarchy_data.keys())[0] + ".component") != "assembly":
        hierarchy_data = {hierarchy.get_parent(node, generations=-1): hierarchy_data}
    return hierarchy_data


def convert_node_to_component(node_hierarchy):
    def _recursive(data, parent_component):
        for key, value in data.items():
            comp = Component()
            comp.pull_data_from_node(key)
            _recursive(value, comp)
            parent_component.add_child(comp)

    component = Component()
    component.pull_data_from_node(list(node_hierarchy.keys())[0])
    _recursive(list(node_hierarchy.values())[0], component)
    return component


def convert_data_to_component(data_hierarchy):
    def _recursive(data, comp):
        for child in data["__children"]:
            comp.add_child(child)
            _recursive(child, comp.children[-1])

    component = Component(data=data_hierarchy)
    _recursive(data_hierarchy, component)
    return component


def convert_component_to_data(component):
    def _recursive(comp, child_list):
        for child in comp.children:
            child_data = child.data
            child_data.update(__children=[])
            child_list.append(child_data)
            _recursive(child, child_data["__children"])

    data = component.data
    data.update(__children=[])
    _recursive(component, data["__children"])
    return data


def import_component_module(name, ui=False):
    default_dir = os.getenv(DOMINO_DEFAULT_COMPONENT, None)
    custom_dir = os.getenv(DOMINO_CUSTOM_COMPONENT, None)
    try:
        module_name = default_dir + "." + name
        if ui:
            module_name += ".settings"
        module = import_module(module_name)
        reload(module)
    except ModuleNotFoundError:
        base_dir = None
        if custom_dir is None:
            raise ModuleNotFoundError(name + " don't exists")
        for d in os.listdir(custom_dir):
            if d == "__pycache__" or not os.path.isdir(os.path.join(custom_dir, d)):
                continue
            if name in os.listdir(os.path.join(custom_dir, d)):
                base_dir = d
            if base_dir:
                break
        try:
            module_name = base_dir + "." + name
            if ui:
                module_name += ".settings"
            module = import_module(module_name)
            reload(module)
        except ModuleNotFoundError:
            raise ModuleNotFoundError(name + " don't exists")
    return module


def create_guide(data):
    def _create(_component, _parent):
        if _parent:
            parent_anchor = int(_component.data["value"]["parent_anchor"])
            parent_anchor_node = mc.listConnections(_parent + ".anchors",
                                                    source=True,
                                                    destination=False)[parent_anchor]
            mc.select(parent_anchor_node)
        component_name = _component.data["value"]["component"]
        module = import_component_module(component_name)
        _guide = Guide(component=_component, recipe=module.guide_recipe())
        _guide.create()
        for child in _component.children:
            _create(child, _guide.root)
        return _guide

    component = convert_data_to_component(data)
    guide = _create(component, None)
    mc.select(guide.root)


def add_guide(parent, component_name):
    if parent:
        guide_root = hierarchy.get_parent(parent, generations=-1)
        if guide_root is None:
            guide_root = parent
        if not mc.objExists(guide_root + ".is_guide"):
            return None
        parent_root = parent
        if not mc.objExists(parent_root + ".component"):
            parent_root = hierarchy.get_parent(parent_root, type="dagContainer")
        guide_hierarchy = get_guide_hierarchy(guide_root, full_path=True)
        comp = convert_node_to_component(guide_hierarchy)
        guide = Guide(component=comp, root=guide_root)
        new_comp_mod = import_component_module(component_name)
        new_comp_preset = new_comp_mod.component_preset()
        name = new_comp_preset["value"]["name"]
        side = new_comp_preset["value"]["side"]
        if mc.objExists(parent_root + ".side"):
            side = new_comp_preset["value"]["side"] = mc.getAttr(parent_root + ".side", asString=True)
        new_comp_preset["value"]["index"] = guide.suitable_index(name, side)
        new_guide = Guide(component=Component(new_comp_preset), recipe=new_comp_mod.guide_recipe())
        mc.select(parent)
        new_guide.create()
        mc.select(new_guide.root)
        mc.setAttr(new_guide.root + ".t", 0, 0, 0)
        mc.setAttr(new_guide.root + ".s", 1, 1, 1)
    else:
        assembly_comp_mod = import_component_module("assembly")
        guide = Guide(component=Component(assembly_comp_mod.component_preset()),
                      recipe=assembly_comp_mod.guide_recipe())
        guide.create()
        new_comp_mod = import_component_module(component_name)
        new_guide = Guide(component=Component(new_comp_mod.component_preset()), recipe=new_comp_mod.guide_recipe())
        mc.select(guide.root)
        is_fail = new_guide.create()
        if not is_fail:
            mc.delete(guide.root)


def copy_guide(guide):
    def set_suitable_index(data):
        for k in data.keys():
            n = mc.getAttr(k + ".name")
            s = mc.getAttr(k + ".side", asString=True)
            index = g.suitable_index(name=n, side=s)
            mc.setAttr(k + ".index", index)
            mc.setAttr(k + ".component_id", str(uuid.uuid4()), type="string")

            mod = import_component_module(mc.getAttr(k + ".component"))
            comp = Component(mod.component_preset())
            _g = Guide(component=comp, root=k)
            _g.rename()
            set_suitable_index(data[k])

    new = mc.duplicate(guide, returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
    sel_list = om2.MSelectionList()
    sel_list.add(new[0])

    root = hierarchy.get_parent(guide, generations=-1)
    guide_hierarchy = get_guide_hierarchy(new[0])
    g = Guide(component=Component(), root=root)

    for v in guide_hierarchy.values():
        set_suitable_index(v)
    mc.select(sel_list.getDagPath(0))


def mirror_guide(guide):
    def find_center_comp(data):
        check = False
        for _k in data.keys():
            if mc.attributeQuery("side", node=_k, exists=True) and mc.getAttr(_k + ".side", asString=True) == "C":
                return True
            check = find_center_comp(data[_k])
            if check:
                break
        return check

    def replace_comp_data(orig_data, new_data):
        for orig_node, new_node in zip(orig_data.keys(), new_data.keys()):
            # new component id
            mc.setAttr(new_node + ".component_id", str(uuid.uuid4()), type="string")

            # side mirror
            orig_side = mc.getAttr(new_node + ".side", asString=True)
            side = "R" if orig_side == "L" else "L"
            side_enum = mc.attributeQuery("side", node=new_node, listEnum=True)[0]
            mc.setAttr(new_node + ".side", side_enum.split(":").index(side))

            asset_container = mc.getAttr(new_node + ".asset_container") or ""
            if asset_container:
                n, s, i = asset_container.split("_")
                if s != "C":
                    mc.setAttr(new_node + ".asset_container", "_".join([n, side, i]), type="string")

            # space switch mirror
            for attr in mc.listAttr(new_node, userDefined=True) or []:
                if attr.endswith("switch_array"):
                    orig_str = mc.getAttr(new_node + "." + attr) or ""
                    new_str = orig_str.replace("_{0}_".format(orig_side), "_{0}_".format(side))
                    mc.setAttr(new_node + "." + attr, new_str, type="string")

            # guide rename
            mod = import_component_module(mc.getAttr(new_node + ".component"))
            comp = Component(mod.component_preset())
            g = Guide(component=comp, root=new_node)
            renamed_node = g.rename()[0]

            orig_m = matrix.get_matrix(orig_node)
            new_m = matrix.get_mirror_matrix(orig_m)
            matrix.set_matrix(renamed_node, new_m)

            # recursive
            replace_comp_data(orig_data[orig_node], new_data[new_node])

    guide_hierarchy = get_guide_hierarchy(guide)
    if find_center_comp(guide_hierarchy):
        return None
    new = mc.duplicate(guide, returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
    sel_list = om2.MSelectionList()
    sel_list.add(new[0])

    new_guide_hierarchy = get_guide_hierarchy(new)
    for orig, new in zip(guide_hierarchy.keys(), new_guide_hierarchy.keys()):
        replace_comp_data(guide_hierarchy[orig], new_guide_hierarchy[new])
    mc.select(sel_list.getDagPath(0))


def run_script(context, name, path):
    n = "domino.custom_step." + name
    spec = spec_from_loader(n, SourceFileLoader(n, path))
    module = None
    if spec:
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        utils.reload_module(module)
    _cls = False
    if module:
        log.Logger.info(f"Run CUSTOM STEP [{name} {path}]...")
        for a in dir(module):
            custom_step_cls = getattr(module, a)
            if inspect.isclass(custom_step_cls) and issubclass(custom_step_cls, CustomStep):
                _cls = custom_step_cls()
                _cls.run(context)
                break
    if not _cls:
        log.Logger.error(f"CUSTOM STEP [{name} {path}]...")


def create_rig(guide=None, rig=None, data=None, context=None):
    def rig_grp():
        name = comp.data["value"]["name"]
        rig_icon = comp.data["value"]["icon_name"]
        asset_container = mc.container(name=name + "_asset")
        container.set_current_asset(asset_container)
        mc.setAttr(asset_container + ".iconName", rig_icon + ".png", type="string")
        asset_rig = mc.createNode("transform", name=name + "_rig")

        geometry = mc.createNode("transform", name="geometry", parent=asset_rig)
        skeleton = mc.createNode("transform", name="skeleton", parent=asset_rig)
        roots = mc.createNode("transform", name="roots", parent=asset_rig)
        xxx = mc.createNode("transform", name="xxx", parent=asset_rig)

        context.update({
            "name": name,
            "asset": (asset_container, asset_rig),
            "geometry": geometry,
            "skeleton": skeleton,
            "roots": roots,
            "xxx": xxx,
            "callbacks": [],
            "container": [],
            "mode": comp.data["value"]["mode"]
        })
        mc.setAttr(geometry + ".overrideEnabled", 1)
        mc.setAttr(skeleton + ".overrideEnabled", 1)

        mc.container(asset_container, edit=True, publishAsRoot=(asset_rig, 1))
        container.publish_node(geometry)
        container.publish_node(skeleton)
        container.publish_node(roots)

        attribute.add_attr(asset_rig, longName="is_rig", type="bool")
        attribute.add_attr(asset_rig, longName="ctl_vis", type="bool")
        mc.setAttr(asset_rig + ".ctl_vis", channelBox=True)
        mc.setAttr(asset_rig + ".ctl_vis", True)
        attribute.add_attr(asset_rig, longName="ctl_mouseover", type="bool")
        mc.setAttr(asset_rig + ".ctl_mouseover", channelBox=True)
        mc.setAttr(asset_rig + ".ctl_mouseover", False)
        attribute.add_attr(asset_rig, longName="ctl_on_playback", type="bool")
        mc.setAttr(asset_rig + ".ctl_on_playback", channelBox=True)
        mc.setAttr(asset_rig + ".ctl_on_playback", True)
        attribute.add_attr(asset_rig, longName="ctl_x_ray", type="bool")
        mc.setAttr(asset_rig + ".ctl_x_ray", channelBox=True)
        mc.setAttr(asset_rig + ".ctl_x_ray", True)
        attribute.add_attr(asset_rig, longName="jnt_vis", type="bool")
        mc.setAttr(asset_rig + ".jnt_vis", channelBox=True)
        mc.setAttr(asset_rig + ".jnt_vis", True)
        attribute.add_attr(asset_rig, longName="model_dp_type", type="enum", enumName="normal:reference",
                           defaultValue=1)
        mc.setAttr(asset_rig + ".model_dp_type", channelBox=True)
        attribute.add_attr(asset_rig, longName="skeleton_dp_type", type="enum", enumName="normal:reference",
                           defaultValue=1)
        mc.setAttr(asset_rig + ".skeleton_dp_type", channelBox=True)

        condition = mc.createNode("condition")
        mc.connectAttr(asset_rig + ".model_dp_type", condition + ".firstTerm")
        mc.setAttr(condition + ".secondTerm", 0)
        mc.setAttr(condition + ".colorIfTrueR", 0)
        mc.setAttr(condition + ".colorIfFalseR", 2)
        mc.connectAttr(condition + ".outColorR", geometry + ".overrideDisplayType")

        condition = mc.createNode("condition")
        mc.connectAttr(asset_rig + ".skeleton_dp_type", condition + ".firstTerm")
        mc.setAttr(condition + ".secondTerm", 0)
        mc.setAttr(condition + ".colorIfTrueR", 0)
        mc.setAttr(condition + ".colorIfFalseR", 2)
        mc.connectAttr(condition + ".outColorR", skeleton + ".overrideDisplayType")

        mc.connectAttr(asset_rig + ".jnt_vis", skeleton + ".v")
        container.publish_node(asset_rig)
        container.publish_attribute(asset_rig)

        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
        [mc.setAttr(asset_rig + "." + attr, lock=True) for attr in attrs]
        [mc.setAttr(asset_rig + "." + attr, keyable=False) for attr in attrs + ["v"]]
        [mc.setAttr(geometry + "." + attr, lock=True) for attr in attrs]
        [mc.setAttr(geometry + "." + attr, keyable=False) for attr in attrs + ["v"]]
        [mc.setAttr(skeleton + "." + attr, lock=True) for attr in attrs]
        [mc.setAttr(skeleton + "." + attr, keyable=False) for attr in attrs + ["v"]]
        [mc.setAttr(roots + "." + attr, lock=True) for attr in attrs]
        [mc.setAttr(roots + "." + attr, keyable=False) for attr in attrs + ["v"]]
        [mc.setAttr(xxx + "." + attr, lock=True) for attr in attrs]
        [mc.setAttr(xxx + "." + attr, keyable=False) for attr in attrs + ["v"]]

    def custom_step():
        for _p in custom_step_scripts.copy():
            if _p in ["objects", "attributes", "operators", "connections", "finalize"]:
                break
            name, path = _p.split(" | ")
            if not os.path.exists(path):
                custom_scripts_dir = os.path.abspath(os.getenv(DOMINO_CUSTOM_STEP_DIR, None))
                if custom_scripts_dir:
                    path = os.path.join(custom_scripts_dir, path[1:])
            if name.startswith("*"):
                log.Logger.info(f"Skip Custom Step [{name[1:]} {path}]...")
                custom_step_scripts.pop(0)
                continue
            elif not os.path.isfile(path) or not os.path.splitext(path)[-1] == ".py":
                log.Logger.info(f"Plz confirm [{name[1:]} {path}]...")
                custom_step_scripts.pop(0)
                continue
            run_script(context, name, path)
            custom_step_scripts.pop(0)
        if custom_step_scripts:
            custom_step_scripts.pop(0)

    def build():
        def convert_component_to_rig(_component):
            component_name = _component.data["value"]["component"]
            module = import_component_module(component_name)
            rig_instance = module.Rig(_component)

            for child in _component.children:
                rig_instance.add_child(convert_component_to_rig(child))

            return rig_instance

        def _build(_rig, step):
            _rig.build(context, step)
            for child in _rig.children:
                _build(child, step)

        _rig = convert_component_to_rig(comp)
        context["mode"] = _rig.component.data["value"]["mode"]
        _build(_rig, 0)
        if comp.data["value"]["end_point"] == "objects":
            return False
        custom_step()
        _build(_rig, 1)
        if comp.data["value"]["end_point"] == "attributes":
            return False
        custom_step()
        _build(_rig, 2)
        if comp.data["value"]["end_point"] == "operators":
            return False
        custom_step()
        _build(_rig, 3)
        if comp.data["value"]["end_point"] == "connections":
            return False
        custom_step()
        return True

    def finalize():
        container.set_current_asset(None)

        # create sets
        name = comp.data["value"]["name"]
        rig_sets = mc.sets(name=name + "_sets", empty=True)
        root_sets = mc.sets(name=name + "_root_sets", empty=True)
        model_sets = mc.sets(name=name + "_model_sets", empty=True)
        geometry_sets = mc.sets(name=name + "_geometry_sets", empty=True)
        skeleton_sets = mc.sets(name=name + "_skeleton_sets", empty=True)
        controller_sets = mc.sets(name=name + "_controller_sets", empty=True)

        # rig convenience func
        mc.connectAttr(context["asset"][1] + ".ctl_on_playback", context["roots"] + ".hideOnPlayback")
        mc.connectAttr(context["asset"][1] + ".ctl_vis", context["roots"] + ".v")
        assembly_root = mc.listConnections(context["asset"][1] + ".assembly_node", source=False, destination=True)[0]
        pose_data = json.loads(mc.getAttr(assembly_root + ".pose_json").replace("'", "\""))
        if not pose_data["neutral"]:
            neutral_pose_data = {}
            for v in context.values():
                if "ctls" in v:
                    neutral_pose_data.update(**attribute.collect_attr([x.fullPathName() for x in v["ctls"]]))
            pose_data["neutral"] = neutral_pose_data
            mc.setAttr(assembly_root + ".pose_json", json.dumps(pose_data), type="string")

        # root setup
        for v in context.values():
            if "root" in v and isinstance(v, dict):
                mc.sets(v["root"], edit=True, addElement=root_sets)

        # ctls setup
        for v in context.values():
            if "ctls" in v:
                for ctl in v["ctls"]:
                    ctl_name = ctl.fullPathName()
                    mc.connectAttr(v["root"] + ".message", ctl_name + ".component_root")
                    mc.connectAttr(v["host"] + ".message", ctl_name + ".component_host")
                    container.publish_node(ctl_name)

                    for shape in mc.listRelatives(ctl_name, shapes=True, fullPath=True) or []:
                        mc.connectAttr(context["asset"][1] + ".ctl_x_ray", shape + ".alwaysDrawOnTop")
                mc.sets(v["ctls"], edit=True, addElement=controller_sets)

        # jnts setup
        for v in context.values():
            if "jnts" in v:
                for jnt in v["jnts"]:
                    mc.setAttr(jnt + ".segmentScaleCompensate", False)
                    target = mc.listConnections(jnt + ".inverseScale", source=True, destination=False, plugs=True)
                    if target:
                        mc.disconnectAttr(target[0], jnt + ".inverseScale")
                if v["jnts"]:
                    mc.sets(v["jnts"], edit=True, addElement=skeleton_sets)

        # host setup
        for v in context.values():
            if "host" in v:
                mc.connectAttr(v["root"] + ".message", v["host"] + ".component_root")
                mc.connectAttr(v["host"] + ".message", v["host"] + ".component_host")
                container.publish_node(v["host"])
                container.publish_attribute(v["host"])
                mc.sets(v["host"], edit=True, addElement=controller_sets)

        # sets final
        mc.sets(context["geometry"], addElement=model_sets)
        geometries = list(
            set([hierarchy.get_parent(x) for x in mc.ls(context["geometry"], dagObjects=True, type="mesh")]))
        if geometries:
            mc.sets(geometries, edit=True, addElement=geometry_sets)
        s = [root_sets, model_sets, geometry_sets, skeleton_sets, controller_sets]
        mc.sets(s, edit=True, addElement=rig_sets)
        attribute.add_attr(context["asset"][1], longName="root_sets", type="message")
        attribute.add_attr(context["asset"][1], longName="geo_sets", type="message")
        attribute.add_attr(context["asset"][1], longName="ctl_sets", type="message")
        attribute.add_attr(context["asset"][1], longName="jnt_sets", type="message")
        mc.connectAttr(root_sets + ".message", context["asset"][1] + ".root_sets")
        mc.connectAttr(geometry_sets + ".message", context["asset"][1] + ".geo_sets")
        mc.connectAttr(controller_sets + ".message", context["asset"][1] + ".ctl_sets")
        mc.connectAttr(skeleton_sets + ".message", context["asset"][1] + ".jnt_sets")

        # callback
        if context["callbacks"]:
            component_id = mc.getAttr(assembly_root + ".component_id")

            callback_root = mc.createNode("script")
            mc.setAttr(callback_root + ".sourceType", 1)
            mc.setAttr(callback_root + ".scriptType", 1)
            attribute.add_attr(callback_root, longName="callbacks", type="message")
            mc.connectAttr(assembly_root + ".message", callback_root + ".callbacks")
            for callback_node in context["callbacks"]:
                mc.connectAttr(callback_root + ".callbacks", callback_node + ".root")

            before_script_code = callback.base_callback.format(component_id=component_id)
            mc.scriptNode(callback_root, edit=True, beforeScript=before_script_code)
            mc.scriptNode(callback_root, executeBefore=True)
            context["callbacks"].append(callback_root)

    if context is None:
        context = dict()

    comp = None

    node_hierarchy = None
    if guide:
        if mc.nodeType(guide) != "dagContainer":
            guide = hierarchy.get_parent(guide, type="dagContainer")
        node_hierarchy = get_guide_hierarchy(guide, full_path=True)
    elif rig:
        root = hierarchy.get_parent(rig, generations=-1)
        if root is None:
            root = rig
        assembly_node = mc.listConnections(root + ".assembly_node", source=False, destination=True)[0]
        node_hierarchy = get_rig_hierarchy(assembly_node)
    if node_hierarchy:
        comp = convert_node_to_component(node_hierarchy)
    if data:
        comp = convert_data_to_component(data)

    # create
    try:
        log.Logger.info("{: ^50}".format("- domino -"))
        mc.undoInfo(openChunk=True)
        custom_step_scripts = comp.data["value"]["custom_step"].split(",")
        custom_step()
        rig_grp()
        end_point_check = build()
        if not end_point_check:
            return None
        finalize()
        custom_step()
    finally:
        if context["mode"] == "DEBUG":
            log.Logger.info("Debug mode. all contents remove from asset")
            for c in context["container"]:
                container.remove_node_from_asset(mc.container(c, query=True, nodeList=True))
            container.remove_node_from_asset(mc.container(context["asset"][0], query=True, nodeList=True))
            mc.delete(context["container"] + [context["asset"][0]])
        elif context["mode"] == "PUB":
            log.Logger.info("Publish mode. all assets not publish attribute lock")
            for c in context["container"]:
                mc.setAttr(c + ".blackBox", True)

        log.Logger.info("")
        log.Logger.info("{:+^50}".format("Context"))
        for key, value in context.items():
            log.Logger.info(f"{key}: {value}")
        log.Logger.info("{:-^50}".format("-"))
        del context
        container.set_current_asset(None)
        mc.undoInfo(closeChunk=True)


def extract_shape(ctls):
    for ctl in ctls:
        if not mc.attributeQuery("is_ctl", node=ctl, exists=True):
            continue
        node = attr = None
        plugs = mc.listConnections(ctl + ".message", destination=True, source=False, plugs=True, type="transform")
        for plug in plugs:
            node, attr = plug.split(".")
            if mc.attributeQuery("component", node=node, exists=True):
                break
        if attr.split("[")[0] != "ctls":
            continue

        index = attribute.get_index(attr)
        orig_shape_plug = mc.listConnections(node + ".ctl_shapes[{0}]".format(index),
                                             source=True,
                                             destination=False,
                                             plugs=True)
        if orig_shape_plug:
            mc.disconnectAttr(orig_shape_plug[0], node + ".ctl_shapes[{0}]".format(index))
        mc.connectAttr(ctl + ".message", node + ".ctl_shapes[{0}]".format(index), force=True)


def extract_guide_from_rig():
    node = mc.ls(selection=True)
    node = node[0] if hierarchy.is_assembly(node[0]) else hierarchy.get_parent(node[0], generations=-1)
    if mc.attributeQuery("is_rig", node=node, exists=True):
        assembly_node = mc.listConnections(node + ".assembly_node", source=False, destination=True)[0]
        node_hierarchy = get_rig_hierarchy(assembly_node)

        comp = convert_node_to_component(node_hierarchy)
        data = convert_component_to_data(comp)

        create_guide(data)
