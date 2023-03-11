# maya
from pymel import core as pm

# built-ins
import uuid
import copy
import json
from typing import Type

# domino
from ...core import nurbs, attribute, controller, log, fcurve, icon, joint, matrix
from . import naming

dt = pm.datatypes


def find_guide_from_id(root, d_id):
    for c in pm.ls(root, dagObjects=True, type="dagContainer"):
        if c.hasAttr("d_id"):
            if c.attr("d_id").get() == d_id:
                return c
    return None


def find_guide_from_identifier(root, identifier):
    for c in pm.ls(root, dagObjects=True, type="dagContainer"):
        if c.hasAttr("d_id"):
            name = c.attr("name").get()
            side = None
            index = None
            if c.attr("piece").get() != "assembly_01":
                side = c.attr("side").get(asString=True)
                index = c.attr("index").get()
            if Identifier.to_str(name, side, index) == identifier:
                return c
    return None


def find_rig_from_id(root, d_id):
    container = pm.container(query=True, findContainer=root)
    binding = pm.containerPublish(container,
                                  query=True,
                                  bindNode=True)
    roots_index = binding.index("roots")
    roots_grp = binding[roots_index + 1]
    children = pm.listRelatives(roots_grp,
                                children=True,
                                type="transform",
                                fullPath=True)
    for c in children:
        if c.hasAttr("d_id"):
            if c.attr("d_id").get() == d_id:
                return pm.container(query=True, findContainer=c), c
    return None, None


def find_rig_from_identifier(root, identifier):
    container = pm.container(query=True, findContainer=root)
    binding = pm.containerPublish(container,
                                  query=True,
                                  bindNode=True)
    roots_index = binding.index("roots")
    roots_grp = binding[roots_index + 1]
    children = pm.listRelatives(roots_grp,
                                children=True,
                                type="transform",
                                fullPath=True)
    for c in children:
        if c.hasAttr("d_id"):
            name = c.attr("name").get()
            side = None
            index = None
            if c.attr("piece").get() != "assembly_01":
                side = c.attr("side").get(asString=True)
                index = c.attr("index").get()
            if Identifier.to_str(name, side, index) == identifier:
                return pm.container(query=True, findContainer=c), c
    return None, None


class Identifier:

    def __init__(self, ddata):
        self._ddata = ddata

    def __init_subclass__(cls):
        if not hasattr(cls, "name"):
            raise NotImplementedError("Implement property 'name'")
        if not hasattr(cls, "side"):
            raise NotImplementedError("Implement property 'side'")
        if not hasattr(cls, "index"):
            raise NotImplementedError("Implement property 'index'")
        if not hasattr(cls, "piece"):
            raise NotImplementedError("Implement property 'piece'")
        if not hasattr(cls, "version"):
            raise NotImplementedError("Implement property 'version'")
        if not hasattr(cls, "description"):
            raise NotImplementedError("Implement property 'description'")
        if not hasattr(cls, "madeBy"):
            raise NotImplementedError("Implement property 'madeBy'")

    def __str__(self):
        if self._ddata._data["piece"] == "assembly_01":
            return self.to_str(self._ddata._data["name"], None, None)
        name = self._ddata._data["name"]
        side = self._ddata._data["side"]
        index = self._ddata._data["index"]
        return self.to_str(name, side, index)

    @staticmethod
    def to_str(name, side, index):
        if side is None and index is None:
            return name
        return f"{name}_{side}{index}"


class DData:
    SELF, PARENT, ASSEMBLY = (0, 1, 2)

    def __init_subclass__(cls):
        if not hasattr(cls, "identifier"):
            raise NotImplementedError("Implement property 'identifier'")
        if not hasattr(cls, "preset"):
            raise NotImplementedError("Implement property 'preset'")

    def __init__(self, node=None, data=None):
        self._parent = None
        self._node = None
        self._data = {x: self.preset[x]["value"] if "fcurve" not in self.preset[x] else self.preset[x]["fcurve"]
                      for x in self.preset}
        if node and data is None:
            self._node = node
            self.sync()
        elif data and node is None:
            self._data = data

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, pieces):
        if "parent_anchor" in self._data:
            for p in pieces:
                d_id = p.ddata._data["d_id"]
                if self._data["parent_anchor"]:
                    p_d_id = self._data["parent_anchor"].split(",")[0]
                    if d_id == p_d_id:
                        self._parent = p.ddata
                        break
            else:
                self._parent = pieces[0].ddata

    @property
    def assembly(self):
        d = self
        while d._parent:
            d = d._parent
        return d

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, n):
        self._node = n

    @property
    def negate(self):
        return True if self._data["side"] == "R" else False

    def data(self, kind):
        if kind == self.SELF:
            d = self._data
        elif kind == self.PARENT:
            if self.parent:
                d = self.parent._data
        elif kind == self.ASSEMBLY:
            d = self.assembly._data
        return d

    @property
    def preset(self):
        if "_preset" not in self.__dict__:
            self._preset = {
                "d_id": {"typ": "string",
                         "value": str(uuid.uuid4())},
                "piece": {"typ": "string",
                          "value": f"{self.identifier.piece}"},
                "piece_version": {"typ": "string",
                                  "value": ". ".join([str(x) for x in self.identifier.version])},
                "name": {"typ": "string",
                         "value": f"{self.identifier.name}"},
                "side": {"typ": "enum",
                         "enumName": ["C", "L", "R"],
                         "value": f"{self.identifier.side}"},
                "index": {"typ": "long",
                          "value": self.identifier.index},
                "parent_anchor": {"typ": "string",
                                  "value": ""},
                "custom_ref_index": {"typ": "long",
                                     "value": -1},
                "override_colors": {"typ": "bool",
                                    "value": False},
                "use_RGB_colors": {"typ": "bool",
                                   "value": False},
                "RGB_ik": {"typ": "float3",
                           "value": (0, 0, 1)},
                "RGB_fk": {"typ": "float3",
                           "value": (0, 0.25, 1)},
                "color_ik": {"typ": "long",
                             "value": 13,
                             "minValue": 0,
                             "maxValue": 31},
                "color_fk": {"typ": "long",
                             "value": 17,
                             "minValue": 0,
                             "maxValue": 31},
                "jnt_names": {"typ": "string",
                              "value": ""},
                "blended_jnt_names": {"typ": "string",
                                      "value": ""},
                "blended_jnt_indices": {"typ": "string",
                                        "value": ""},
                "support_jnt_names": {"typ": "string",
                                      "value": ""},
                "support_jnt_indices": {"typ": "string",
                                        "value": ""},
                "support_jnt_descriptions": {"typ": "string",
                                             "value": ""},
                "support_jnt_matrices": {"typ": "matrix",
                                         "multi": True,
                                         "value": []},
                "blended_jnts": {"typ": "message",
                                 "multi": True,
                                 "value": []},
                "support_jnts": {"typ": "message",
                                 "multi": True,
                                 "value": []},
                "offset_orient_x": {"typ": "double",
                                    "value": 0,
                                    "minValue": -360,
                                    "maxValue": 360},
                "offset_orient_y": {"typ": "double",
                                    "value": 0,
                                    "minValue": -360,
                                    "maxValue": 360},
                "offset_orient_z": {"typ": "double",
                                    "value": 0,
                                    "minValue": -360,
                                    "maxValue": 360},
                "ncurve_ctls_shapes": {"typ": "message",
                                       "multi": True,
                                       "value": {}},
                "host": {"typ": "string",
                         "value": ""}
            }
        return self._preset

    def sync(self, reverse=False):
        if reverse:
            _data = self.data(DData.SELF)
            for key in self.preset:
                if key not in _data:
                    argument = self.preset[key]
                    attribute.add(self.node,
                                  longName=key,
                                  **argument)
                    continue
                value = _data[key]
                if not pm.objExists(f"{self.node}.{key}"):
                    argument = self.preset[key].copy()
                    if "fcurve" in argument:
                        if isinstance(value, dict):
                            argument["fcurve"] = value
                    else:
                        argument["value"] = value
                    attribute.add(self.node,
                                  longName=key,
                                  **argument)
                    continue
                if key == "anchors":
                    for i, v in enumerate(value):
                        guide = pm.listConnections(f"{self.node}.{key}[{i}]",
                                                   destination=False,
                                                   source=True)
                        if guide:
                            guide[0].setMatrix(v, worldSpace=True)
                        else:
                            attribute._set(self.node.attr(key)[i], v)
                    continue
                if key in ["offset_matrix", "offset_pole_vec_matrix"]:
                    guide = pm.listConnections(f"{self.node}.{key}",
                                               destination=False,
                                               source=True)
                    if not guide:
                        attribute._set(self.node.attr(key), value)
                    continue
                if key.startswith("ncurve"):
                    parent = self.node
                    root = self.node.getParent(generations=-1)
                    if key == "ncurve_ctls_shapes":
                        if pm.nodeType(self.node) == "dagContainer":
                            parent = f"{root.fullPathName()}|ctl_shapes"
                        else:
                            parent = f"{root.fullPathName()}|xxx"
                    if "multi" in self.preset[key]:
                        for i, v in value.items():
                            crv = nurbs.build(v,
                                              parent=parent)
                            pm.connectAttr(f"{crv}.message",
                                           self.node.attr(key)[int(i)])
                    else:
                        crv = nurbs.build(value["0"],
                                          parent=parent)
                        pm.connectAttr(f"{crv}.message",
                                       self.node.attr(key))
                    continue
                if self.node.attr(key).isConnected():
                    anim = self.node.attr(key).inputs(type="animCurve")
                    if anim:
                        pm.delete(anim)
                        fcurve.set_fcurve(value, driven=[self.node.attr(key)])
                        continue
                if pm.attributeQuery(key, node=self.node, multi=True):
                    for i, v in enumerate(value):
                        attribute._set(self.node.attr(key)[i], v)
                else:
                    attribute._set(self.node.attr(key), value)
            if pm.nodeType(self.node) != "dagContainer":
                return 0
            child_node = [x for x in pm.container(self.node,
                                                  query=True,
                                                  nodeList=True)
                          if pm.nodeType(x) == "transform"]
            child_node.insert(0, self.node)
            for i, child in enumerate(child_node):
                if child == "ctl_shapes":
                    continue
                if child.type() == "dagContainer":
                    name = child.split("_")[-1]
                    name = "_".join([str(self.identifier), name])
                    pm.rename(child, name)
                    continue
                index, name = child.split("_")[-2:]
                name = "_".join([str(self.identifier), f"{index}_{name}"])
                pm.rename(child, name)
            pm.select(self.node)
            return 0

        ###
        data = copy.deepcopy(self.data(self.SELF))
        for key, value in self.data(self.SELF).items():
            if not self.node.hasAttr(key):
                continue
            # parent anchor
            if key == "parent_anchor":
                if pm.nodeType(self.node) == "transform":
                    data[key] = attribute._get(self.node.attr(key))
                elif pm.nodeType(self.node) == "dagContainer":
                    _parent = self.node.getParent()
                    _attr = None
                    while not _attr and _parent:
                        _attr = pm.listConnections(_parent.attr("worldMatrix")[0],
                                                   plugs=True,
                                                   destination=True,
                                                   source=False,
                                                   type="dagContainer")
                        _parent = _parent.getParent()
                    if _attr:
                        index = _attr[0].index()
                        _node = _attr[0].node()
                        d_id = _node.attr("d_id").get()
                        data[key] = f"{d_id},{index}"
                continue
            # sub jnt
            elif key in ["blended_jnt_names",
                         "blended_jnts",
                         "support_jnt_names",
                         "support_jnt_descriptions",
                         "support_jnt_matrices",
                         "support_jnts"]:
                continue
            elif key in ["blended_jnt_indices", "support_jnt_indices"]:
                is_blended = True if key.startswith("blended") else False
                _name = "blended_jnts" if is_blended else "support_jnts"

                # don't exists jnt
                num_connected = self.node.attr(_name).numConnectedElements()
                if not self.node.hasAttr("jnts") or not num_connected:
                    if is_blended:
                        data["blended_jnt_names"] = self.node.attr("blended_jnt_names").get()
                        data["blended_jnt_indices"] = self.node.attr("blended_jnt_indices").get()
                        continue
                    data["support_jnt_names"] = self.node.attr("support_jnt_names").get()
                    data["support_jnt_indices"] = self.node.attr("support_jnt_indices").get()
                    data["support_jnt_descriptions"] = self.node.attr("support_jnt_descriptions").get()
                    data["support_jnt_matrices"] = self.node.attr("support_jnt_matrices").get()
                    continue

                # blended_jnts or support_jnts connected list
                _attrs = pm.listAttr(self.node.attr(_name), multi=True)
                indices = []
                matrices = []
                names = []
                descriptions = []
                # blended jnt
                # get indices, names
                if _name.startswith("blended"):
                    for _attr in _attrs:
                        if pm.connectionInfo(self.node.attr(_attr),
                                             isDestination=True):
                            index = self.node.attr(_attr).index()
                            indices.append(index)
                            jnt = pm.listConnections(self.node.attr(_name)[index],
                                                     destination=False,
                                                     source=True,
                                                     type="joint")
                            names.append(jnt[0])
                # support jnt
                # get indices, names, descriptions, matrices
                else:
                    for _attr in _attrs:
                        source = pm.connectionInfo(self.node.attr(_attr),
                                                   sourceFromDestination=True)
                        if source:
                            # name, description
                            support_jnt = source.split(".")[0]
                            names.append(support_jnt)
                            description = \
                                pm.getAttr(f"{support_jnt}.description")
                            descriptions.append(description)
                            # indices
                            blended_jnt = \
                                pm.listRelatives(support_jnt, parent=True)[0]
                            d_attr = pm.listConnections(f"{blended_jnt}.message",
                                                        plugs=True,
                                                        type="transform",
                                                        destination=True,
                                                        source=False)
                            d_attr = \
                                [x for x in d_attr if x.attrName().startswith("blended")]
                            index = d_attr[0].index()
                            indices.append(index)
                            # matrices
                            m_attr = self.node.attr("support_jnt_matrices")
                            _attr_index = self.node.attr(_attr).index()
                            matrices.append(attribute._get(m_attr[_attr_index]))
                if is_blended:
                    data["blended_jnt_names"] = \
                        ",".join([str(x) for x in names])
                    data["blended_jnt_indices"] = \
                        ",".join([str(x) for x in indices])
                    continue
                data["support_jnt_names"] = \
                    ",".join([str(x) for x in names])
                data["support_jnt_indices"] = \
                    ",".join([str(x) for x in indices])
                data["support_jnt_descriptions"] = \
                    ",".join([str(x) for x in descriptions])
                data["support_jnt_matrices"] = matrices
                continue
            elif key.startswith("ncurve"):
                curve_data = {}
                if pm.getAttr(self.node.attr(key), type=True) == "TdataCompound":
                    attrs = pm.listAttr(self.node.attr(key), multi=True) or []
                    for attr in attrs:
                        index = self.node.attr(attr).index()
                        crv = pm.listConnections(self.node.attr(attr),
                                                 destination=False,
                                                 source=True)[0]
                        curve_data[f"{index}"] = nurbs.data(crv)
                else:
                    crvs = pm.listConnections(self.node.attr(key),
                                              destination=False,
                                              source=True)
                    for crv in crvs:
                        plugs = [x for x in crv.outputs(plugs=True, type=self.node.type()) if "ncurve" in x.attrName()]
                        index = plugs[0].index()
                        curve_data[f"{index}"] = nurbs.data(crv)
                data[key] = curve_data
                continue
            elif "json" in self.preset[key]:
                data[key] = json.loads(self.node.attr(key).get())
                continue
            elif self.node.attr(key).isConnected():
                anim = self.node.attr(key).inputs(type="animCurve")
                if anim:
                    data[key] = fcurve.get_fcurve(anim[0])
                    continue

            # general multi attribute
            if pm.getAttr(self.node.attr(key), type=True) == "TdataCompound":
                data[key] = [attribute._get(self.node.attr(x))
                             for x in pm.listAttr(self.node.attr(key), multi=True)]
            # general attribute
            else:
                data[key] = attribute._get(self.node.attr(key))
        self._data = data


class Guide:

    def guide(self):
        parent = None
        data = self.data(DData.SELF)
        if "parent_anchor" in data:
            if data["parent_anchor"]:
                d_id, index = data["parent_anchor"].split(",")
                root = pm.ls(selection=True)[0].getParent(generations=-1)
                parent_guide = find_guide_from_id(root, d_id)
                if parent_guide:
                    anchors = pm.listConnections(parent_guide.attr("anchors")[index],
                                                 destination=False,
                                                 source=True,
                                                 type="transform")
                    if anchors:
                        parent = anchors[0]
                    else:
                        log.Logger.error(f"Parent Guide : {parent_guide}")
                        log.Logger.error(f"Parent Guide Index: {index}")
        return self.create_root(parent)

    def __init__(self, ddata: Type[DData]):
        self.ddata = ddata

    @property
    def data(self):
        return self.ddata.data

    def create_root(self, parent):
        container = pm.container(name=f"{str(self.ddata.identifier)}_{naming.GUIDE_EXT}",
                                 type="dagContainer")
        icon.guide_root(container, parent)
        container.attr("displayHandle").set(True)
        attribute.add(container,
                      longName="is_domino_guide",
                      typ="bool",
                      keyable=False)
        attribute.add(container,
                      longName="extension",
                      typ="string",
                      value=naming.GUIDE_EXT)
        self.ddata.node = container
        self.ddata.sync(True)
        m = container.attr("anchors")[0].get()
        container.setMatrix(m, worldSpace=True)
        pm.connectAttr(container.attr("worldMatrix")[0],
                       container.attr("anchors")[0])
        return container

    def create_position(self, parent, m):
        pos = pm.createNode("transform")
        icon.guide_position(pos, parent, m)
        if pm.nodeType(parent) != "dagContainer":
            parent = pm.container(query=True, findContainer=parent)
        index = parent.attr("anchors").numConnectedElements()
        pm.connectAttr(pos.attr("worldMatrix")[0],
                       parent.attr("anchors")[index])
        pos.rename(f"{str(self.ddata.identifier)}_{index}_{naming.GUIDE_POS_EXT}")
        pos.attr("displayHandle").set(True)
        attribute.add(pos,
                      longName="is_domino_guide",
                      typ="bool",
                      keyable=False)
        attribute.add(pos,
                      longName="extension",
                      typ="string",
                      value=naming.GUIDE_POS_EXT)
        return pos

    def create_orientation(self, parent, target):
        ori = pm.createNode("transform")
        icon.guide_orientation(ori, parent)
        if pm.nodeType(parent) != "dagContainer":
            parent = pm.PyNode(pm.container(query=True, findContainer=parent))
        aim = pm.aimConstraint(target,
                               ori,
                               aimVector=(1, 0, 0),
                               upVector=(0, 0, 1),
                               worldUpType="objectrotation",
                               worldUpVector=(0, 0, 1),
                               worldUpObject=parent)
        pm.connectAttr(parent.attr("offset"), aim.attr("offsetX"))
        pm.connectAttr(ori.attr("worldMatrix")[0], parent.attr("offset_matrix"))
        attribute.lock(ori, ["rx", "ry", "rz"])
        ori.rename(f"{str(self.ddata.identifier)}_{naming.GUIDE_ORI_EXT}")
        ori.attr("hiddenInOutliner").set(True)
        attribute.add(ori,
                      longName="is_domino_guide",
                      typ="bool",
                      keyable=False)
        attribute.add(ori,
                      longName="extension",
                      typ="string",
                      value=naming.GUIDE_ORI_EXT)

    def create_display_crv(self, parent, sources, degree=1, thickness=2):
        display_curve = pm.createNode("transform")
        icon.generate(display_curve,
                      [(0, 0, 0) for _ in sources],
                      degree,
                      dt.Color(0.55, 0.55, 0.55, 0.55),
                      thickness=thickness)
        shape = display_curve.getShape()
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
        nurbs.constraint(display_curve, sources)
        pm.connectAttr(parent.attr("worldInverseMatrix")[0],
                       display_curve.attr("offsetParentMatrix"))
        attribute.lock(display_curve, attrs)
        attribute.hide(display_curve, attrs)
        shape.attr("overrideDisplayType").set(2)
        pm.parent(display_curve, parent)
        display_curve.attr("hiddenInOutliner").set(True)
        display_curve.rename(f"{str(self.ddata.identifier)}_{naming.GUIDE_CRV_EXT}")
        attribute.add(display_curve,
                      longName="is_domino_guide",
                      typ="bool",
                      keyable=False)
        attribute.add(display_curve,
                      longName="extension",
                      typ="string",
                      value=naming.GUIDE_CRV_EXT)

    def create_locator(self, parent):
        loc = pm.spaceLocator()
        pm.parent(loc, parent)
        pm.matchTransform(loc, parent, position=True, rotation=True, scale=True)
        loc.rename(f"{str(self.ddata.identifier)}_{naming.GUIDE_LOC_EXT}")
        loc.attr("hiddenInOutliner").set(True)
        loc.attr("overrideEnabled").set(1)
        loc.attr("overrideRGBColors").set(1)
        loc.attr("overrideColorRGB").set(0.1, 1, 0.8)
        attribute.add(loc,
                      longName="is_domino_guide",
                      typ="bool",
                      keyable=False)
        attribute.add(loc,
                      longName="extension",
                      typ="string",
                      value=naming.GUIDE_LOC_EXT)
        return loc

    def create_pv_locator(self, parent, positions):
        multiple_attr = parent.attr("offset_pole_vec")
        position_attr = matrix.pole_vec_position(parent=parent,
                                                 positions=positions,
                                                 multiple=multiple_attr)
        loc = self.create_locator(parent=parent)
        loc.attr("localScale").set(0.5, 0.5, 0.5)
        pm.connectAttr(position_attr, loc.attr("t"))
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
        attribute.lock(loc, attrs)
        attribute.hide(loc, attrs)
        if pm.nodeType(parent) != "dagContainer":
            parent = pm.container(query=True, findContainer=parent)
        pm.connectAttr(loc.attr("worldMatrix")[0],
                       parent.attr("offset_pole_vec_matrix"))
        return loc

    def set_suitable_index(self, pieces, remove_self=False):
        self_data = self.data(DData.SELF)
        index = self_data["index"]
        indexes = []
        for p in pieces:
            data = p.ddata.data(DData.SELF)
            if data["piece"] == "assembly_01":
                continue
            if remove_self:
                if self_data["name"] == data["name"] \
                        and self_data["side"] == data["side"] \
                        and self_data["index"] == data["index"]:
                    continue
            if self_data["name"] == data["name"] and self_data["side"] == data["side"]:
                indexes.append(data["index"])
        while index in indexes:
            index += 1
        self_data = self.data(DData.SELF)
        self_data["index"] = index
        self.ddata._data = self_data
        if self.ddata.node:
            self.ddata.sync(True)

    def set_parent_anchor(self, parent):
        anchor_attr = pm.listConnections(parent.attr("worldMatrix")[0],
                                         destination=True,
                                         source=False,
                                         plugs=True,
                                         type="dagContainer")
        if not anchor_attr:
            log.Logger.warning(f"Parent Node({parent!r}) is wrong."
                               "This node is not anchors."
                               "please reparenting node.")
            return None
        index = anchor_attr[0].index()
        d_id = anchor_attr[0].node().attr("d_id").get()
        data = self.data(DData.SELF)
        data["parent_anchor"] = f"{d_id},{index}"
        self.ddata._data = data


class Rig:

    def __init__(self, ddata: Type[DData]):
        self.ddata = ddata
        self.container = None
        self.root = None

    @property
    def data(self):
        return self.ddata.data

    def host(self):
        if self.root is None:
            return None
        host_root = self.root
        data = self.data(DData.SELF)
        original_host = host_root.attr("host").inputs()
        if self.ddata.parent is not None:
            if data["host"]:
                host_container, host_root = find_rig_from_identifier(self.root.getParent(generations=-1), data["host"])
        host = host_root.attr("host").inputs()
        if original_host != host:
            pm.delete(original_host)
            pm.connectAttr(host[0].attr("message"), self.root.attr("host"))
            pm.container(self.container, edit=True, force=True, addNode=host[0])
        name = str(self.ddata.identifier)
        if not host[0].hasAttr(name):
            attr = attribute.add(host[0],
                                 name,
                                 "enum",
                                 enumName=["I"],
                                 keyable=True)
            attr.lock()
        return host[0]

    def naming(self, description="", extension="", _s="ctl" or "jnt"):
        data = self.data(DData.SELF)
        assembly_data = self.data(kind=DData.ASSEMBLY)

        extension = "_" if extension is None else extension

        rule = assembly_data[f"{_s}_name_rule"]
        padding = assembly_data[f"{_s}_index_padding"]
        description_letter_case = assembly_data[f"{_s}_description_letter_case"]
        side_set = [assembly_data[f"{_s}_center_name"],
                    assembly_data[f"{_s}_left_name"],
                    assembly_data[f"{_s}_right_name"]]
        if not extension:
            extension = assembly_data[f"{_s}_name_ext"]

        if description_letter_case == "lower":
            description = description.lower()
        elif description_letter_case == "upper":
            description = description.upper()
        elif description_letter_case == "capitalize":
            description = description.capitalize()

        index_filter = ["C", "L", "R"]
        if data == assembly_data:
            args = {
                "name": "",
                "side": "",
                "index": "",
                "description": description,
                "extension": extension
            }
        else:
            args = {
                "name": data["name"],
                "side": side_set[index_filter.index(data["side"])],
                "index": str(data["index"]).zfill(padding),
                "description": description,
                "extension": extension
            }
        for a in args.copy():
            if a not in rule:
                del args[a]
        name = rule.format(**args)
        name = "_".join([x for x in name.split("_") if x])
        return name

    def get_ik_ctl_color(self):
        color = None
        data = self.data(DData.SELF)
        assembly_data = self.data(DData.ASSEMBLY)
        if data["override_colors"]:
            if data["use_RGB_colors"]:
                color = data["RGB_ik"]
            else:
                color = data["color_ik"]
        else:
            if assembly_data["use_RGB_colors"]:
                if data["side"] == "L":
                    color = assembly_data["l_RGB_ik"]
                elif data["side"] == "R":
                    color = assembly_data["r_RGB_ik"]
                elif data["side"] == "C":
                    color = assembly_data["c_RGB_ik"]
            else:
                if data["side"] == "L":
                    color = assembly_data["l_color_ik"]
                elif data["side"] == "R":
                    color = assembly_data["r_color_ik"]
                elif data["side"] == "C":
                    color = assembly_data["c_color_ik"]
        return color

    def get_fk_ctl_color(self):
        color = None
        data = self.data(DData.SELF)
        assembly_data = self.data(kind=DData.ASSEMBLY)
        if data["override_colors"]:
            if data["use_RGB_colors"]:
                color = data["RGB_fk"]
            else:
                color = data["color_fk"]
        else:
            if assembly_data["use_RGB_colors"]:
                if data["side"] == "L":
                    color = assembly_data["l_RGB_fk"]
                elif data["side"] == "R":
                    color = assembly_data["r_RGB_fk"]
                elif data["side"] == "C":
                    color = assembly_data["c_RGB_fk"]
            else:
                if data["side"] == "L":
                    color = assembly_data["l_color_fk"]
                elif data["side"] == "R":
                    color = assembly_data["r_color_fk"]
                elif data["side"] == "C":
                    color = assembly_data["c_color_fk"]
        return color

    def find_ctls(self, data):
        data = [x.split(" | ") for x in data.split(",")]
        asset_root = self.ddata.node.getParent(generations=-1)
        ctls = []
        for index, identifier in data:
            container, root = find_rig_from_identifier(asset_root, identifier)
            if container is None:
                continue
            ctl = pm.listConnections(root.attr("ctls")[index],
                                     destination=False,
                                     source=True)
            if not ctl:
                continue
            ctls.append(ctl[0])
        return ctls

    def create_asset(self, context):
        assembly_data = self.data(DData.ASSEMBLY)
        asset_container_name = f"{assembly_data['name']}_{naming.ASSET_EXT}"
        asset_name = f"{assembly_data['name']}_rig"
        asset_container = pm.container(name=asset_container_name)
        asset_container.attr("iconName").set(f"{assembly_data['icon_name']}.png")
        pm.container(asset_container, edit=True, current=True)
        asset = pm.createNode("transform", name=asset_name)
        model = pm.createNode("transform", name="model", parent=asset)
        skeleton = pm.createNode("transform", name="skeleton", parent=asset)
        roots = pm.createNode("transform", name="roots", parent=asset)
        xxx = pm.createNode("transform", name="xxx", parent=asset)
        attribute.lock(xxx, pm.listAttr(xxx, keyable=True))
        attribute.hide(xxx, pm.listAttr(xxx, keyable=True))
        context["asset"] = (asset_container, asset)
        context["model"] = model
        context["skeleton"] = skeleton
        context["roots"] = roots
        context["xxx"] = xxx
        context["containers"] = []
        context["jnts"] = []
        context["ctls"] = []
        context["refs"] = []
        context["callbacks"] = []
        model.attr("overrideEnabled").set(1)
        skeleton.attr("overrideEnabled").set(1)

        pm.container(asset_container,
                     edit=True,
                     publishAsRoot=(asset, 1))
        pm.containerPublish(asset_container,
                            publishNode=("model", ""))
        pm.containerPublish(asset_container,
                            bindNode=("model", context["model"]))
        pm.containerPublish(asset_container,
                            publishNode=("skeleton", ""))
        pm.containerPublish(asset_container,
                            bindNode=("skeleton", context["skeleton"]))
        pm.containerPublish(asset_container,
                            publishNode=("roots", ""))
        pm.containerPublish(asset_container,
                            bindNode=("roots", context["roots"]))
        attribute.add(asset,
                      longName="is_domino_asset",
                      typ="bool",
                      value=False)

    def create_container(self, context):
        pm.container(context["asset"][0], edit=True, current=True)
        if self.container is None:
            name = str(self.ddata.identifier)
            container_name = f"{name}_{naming.CONTAINER_EXT}"
            self.container = pm.container(name=container_name)
            self.container.attr("viewMode").set(0)
        return self.container

    def set_current_container(self):
        if self.container:
            pm.container(self.container, edit=True, current=True)

    def create_root(self, context, t):
        name = str(self.ddata.identifier)
        root_name = f"{name}_{naming.ROOT_EXT}"
        self.root = pm.createNode("transform",
                                  name=root_name,
                                  parent=context["roots"])

        self.ddata.node = self.root
        self.ddata.sync(True)
        pm.container(self.container,
                     edit=True,
                     publishAsRoot=(self.root, 1))
        data = self.data(DData.SELF)
        asset_container, asset_root = context["asset"]
        attribute.add(self.root,
                      longName="ctls",
                      typ="message",
                      multi=True)
        attribute.add(self.root,
                      longName="refs",
                      typ="message",
                      multi=True)
        attribute.add(self.root,
                      longName="ref_anchors",
                      typ="message",
                      multi=True)
        attribute.add(self.root,
                      longName="jnts",
                      typ="message",
                      multi=True)
        attribute.add(self.root,
                      longName="host",
                      typ="message")

        if asset_container:
            if self.root.attr("piece").get() != "assembly_01":
                parent_d_id, ref_anchor = data["parent_anchor"].split(",")
                parent_container, parent_root = find_rig_from_id(
                    asset_root, parent_d_id)
                if parent_container:
                    if parent_root.attr("piece").get() != "assembly_01":
                        custom_ref_index = data["custom_ref_index"]
                        refs_element = pm.listAttr(parent_root.attr("refs"),
                                                   multi=True)
                        ref_anchors_element = pm.listAttr(parent_root.attr("ref_anchors"),
                                                          multi=True)
                        refs_index = None
                        ref_anchors_index = None
                        if -1 < custom_ref_index < len(refs_element):
                            refs_index = custom_ref_index
                        elif custom_ref_index >= len(refs_element):
                            refs_index = -1
                            log.Logger.warning(
                                f"\tcheck 'root' custom_ref_index")
                            log.Logger.warning("\tcustom_ref_index : "
                                               f"{custom_ref_index!r}")
                            log.Logger.warning(f"\tresult attr : "
                                               f"{parent_root}.{refs_element[int(ref_anchor)]!r}")
                        elif custom_ref_index == -1:
                            if int(ref_anchor) >= len(ref_anchors_element):
                                ref_anchors_index = -1
                            else:
                                ref_anchors_index = int(ref_anchor)
                        if refs_index is not None:
                            attr = refs_element[refs_index]
                            ref = pm.listConnections(parent_root.attr(attr),
                                                     destination=False,
                                                     source=True)[0]
                        if ref_anchors_index is not None:
                            attr = ref_anchors_element[ref_anchors_index]
                            ref = pm.listConnections(parent_root.attr(attr),
                                                     destination=False,
                                                     source=True)[0]
                    else:
                        ref = pm.listConnections(parent_root.attr("refs")[0],
                                                 destination=False,
                                                 source=True)[0]
                    pm.connectAttr(ref.attr("worldMatrix")[0], self.root.attr("offsetParentMatrix"))

        m0 = dt.Matrix(data["anchors"][0])
        pm.xform(self.root, translation=t, worldSpace=True)
        pm.xform(self.root, rotation=dt.degrees(m0.rotate.asEulerRotation()), worldSpace=True)
        cb_attrs = pm.listAttr(self.root, keyable=True)
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
        attribute.lock(self.root, attrs + cb_attrs)
        attribute.hide(self.root, attrs + ["v"] + cb_attrs)
        context["containers"].append((self.container, self.root))
        return self.root

    def create_host(self, context, ctl=None):
        if ctl:
            host = ctl
        else:
            name = str(self.ddata.identifier)
            host = matrix.transform(parent=self.root, name=f"{name}_host", m=self.root.getMatrix(worldSpace=True))
            context["ctls"].insert(0, host)
            attribute.add(host,
                          longName="is_domino_ctl",
                          typ="bool",
                          value=True,
                          keyable=False)
            attrs = ["tx", "ty", "tz",
                     "rx", "ry", "rz", "ro",
                     "sx", "sy", "sz", "v"]
            attribute.lock(host, attrs)
            attribute.hide(host, attrs)
        pm.connectAttr(host.attr("message"), self.root.attr("host"))
        return self.host()

    def create_ctl(self,
                   context,
                   parent,
                   name,
                   parent_ctl,
                   color,
                   keyable_attrs,
                   m,
                   shape,
                   cns=False,
                   width=1,
                   height=1,
                   depth=1,
                   po=(0, 0, 0),
                   ro=(0, 0, 0)):
        assembly_data = self.data(DData.ASSEMBLY)
        data = self.data(DData.SELF)
        if parent is None:
            parent = self.root
        attrs = pm.listAttr(self.root.attr("ctls"), multi=True)
        if not attrs:
            index = 0
        else:
            index = len(attrs)

        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz", "v"]
        # name
        npo_name = name.replace(assembly_data["ctl_name_ext"], "npo")
        ctl_name = name
        loc_name = name.replace(assembly_data["ctl_name_ext"], "loc")

        if isinstance(color, (tuple, list)):
            color = dt.Color(color)

        # create
        npo = pm.createNode("transform", name=npo_name, parent=parent)
        p_i_m = npo.attr("parentInverseMatrix").get()
        pm.setAttr(npo.attr("offsetParentMatrix"), m * p_i_m, type="matrix")
        ctl = icon.create(parent=npo,
                          name=ctl_name,
                          shape=shape,
                          color=color,
                          m=m,
                          thickness=1,
                          width=width,
                          height=height,
                          depth=depth,
                          up="y",
                          po=po,
                          ro=ro)
        pm.connectAttr(ctl.attr("message"), self.root.attr("ctls")[index])
        if str(index) in data["ncurve_ctls_shapes"]:
            nurbs.build(data["ncurve_ctls_shapes"][str(index)], replace=ctl)
            pm.connectAttr(ctl.attr("message"), self.root.attr("ncurve_ctls_shapes")[index])
            shapes = ctl.getShapes()
            for shape in shapes:
                shape.attr("isHistoricallyInteresting").set(0)

        cns_ctl = None
        # create cns
        if cns:
            cns_name = name.replace(assembly_data["ctl_name_ext"], "cns")
            cns_ctl = icon.create(parent=npo,
                                  name=cns_name,
                                  shape="locator",
                                  color=dt.Color(1, 0, 1),
                                  m=m,
                                  thickness=2,
                                  width=1,
                                  height=1,
                                  depth=1,
                                  po=(0, 0, 0),
                                  ro=(0, 0, 0))
            remove_attrs = ["tx", "ty", "tz", "rx", "ry", "rz"]
            attribute.keyable(cns_ctl, set(attrs) - set(remove_attrs))
            attribute.lock(cns_ctl, set(attrs) - set(remove_attrs))
            attribute.hide(cns_ctl, set(attrs) - set(remove_attrs))
            visible = attribute.add(ctl, "cns_visibility", typ="bool", value=False, defaultValue=False, keyable=True)
            for s in cns_ctl.getShapes():
                pm.connectAttr(visible, s.attr("v"))
            pm.connectAttr(visible, cns_ctl.attr("displayRotatePivot"))
            pm.parent(ctl, cns_ctl)
            pm.connectAttr(cns_ctl.attr("message"), self.root.attr("ctls")[index + 1])

        attribute.keyable(ctl, attrs)
        attribute.lock(ctl, set(attrs) - set(keyable_attrs))
        attribute.hide(ctl, set(attrs) - set(keyable_attrs))
        # if loc: loc flag test
        loc = pm.createNode("transform", name=loc_name, parent=ctl)
        if npo.attr("offsetParentMatrix").get().scale[2] < 0:
            loc.attr("sz").set(-1)
        attribute.lock(loc, attrs)
        attribute.hide(loc, attrs)

        # get parent piece controller
        if parent_ctl is None:
            asset_container, asset_root = context["asset"]
            if "parent_anchor" in data:
                parent_d_id, _ = data["parent_anchor"].split(",")
                while not parent_ctl:
                    parent_container, parent_root = find_rig_from_id(asset_root,
                                                                     parent_d_id)
                    if not parent_container:
                        break
                    if parent_root.attr("piece").get() == "assembly_01":
                        index = len(pm.listAttr(parent_root.attr("ctls"), multi=True)) - 1
                        parent_ctl = pm.listConnections(parent_root.attr("ctls")[index],
                                                        destination=False,
                                                        source=True)[0]
                        break
                    parent_anchor = pm.getAttr(f"{parent_root}.parent_anchor")
                    parent_d_id, _ = parent_anchor.split(",")
                    num = parent_root.attr("ctls").numConnectedElements()
                    if not num:
                        continue
                    index = len(pm.listAttr(parent_root.attr("ctls"), multi=True)) - 1
                    parent_ctl = pm.listConnections(parent_root.attr("ctls")[index],
                                                    destination=False,
                                                    source=True)[0]

        # controller tag
        if parent_ctl:
            if cns_ctl:
                controller.tag(cns_ctl, parent_ctl)
                parent_ctl = cns_ctl
            controller.tag(ctl, parent_ctl)
        else:
            if cns_ctl:
                controller.tag(cns_ctl, None)
                parent_ctl = cns_ctl
            controller.tag(ctl, parent_ctl)

        if cns_ctl:
            context["ctls"].append(cns_ctl)
            attribute.add(cns_ctl,
                          longName="is_domino_ctl",
                          typ="bool",
                          value=True)
        context["ctls"].append(ctl)
        attribute.add(ctl,
                      longName="is_domino_ctl",
                      typ="bool",
                      value=True)
        return ctl, loc

    def create_ref(self, context, name, anchor, m):
        data = self.data(DData.SELF)
        attrs = pm.listAttr(self.root.attr("refs"), multi=True)
        if not attrs:
            index = 0
        else:
            index = len(attrs)
        obj = pm.createNode("transform", name=name, parent=self.root)
        if m:
            obj.attr("inheritsTransform").set(False)
            pm.connectAttr(m.attr("worldMatrix")[0], obj.attr("offsetParentMatrix"))
        pm.connectAttr(obj.attr("message"), self.root.attr("refs")[index])
        attribute.lock(obj, ["tx", "ty", "tz",
                             "sx", "sy", "sz", "v"])
        attribute.hide(obj, ["tx", "ty", "tz",
                             "sx", "sy", "sz", "v"])
        if anchor:
            attrs = pm.listAttr(self.root.attr("ref_anchors"), multi=True)
            if not attrs:
                a_index = 0
            else:
                a_index = len(attrs)
            pm.connectAttr(obj.attr("message"),
                           self.root.attr("ref_anchors")[a_index])
        context["refs"].append(obj)
        if self.root.attr("piece").get() != "assembly_01":
            offset_rotate = (data["offset_orient_x"],
                             data["offset_orient_y"],
                             data["offset_orient_z"])
            obj.attr("r").set(*offset_rotate)
        return obj

    def create_jnt(self, context, parent, name, description, ref, m, leaf=False, uni_scale=False):
        data = self.data(DData.SELF)
        attrs = pm.listAttr(self.root.attr("jnts"), multi=True)
        if not attrs:
            index = 0
        else:
            index = len(attrs)

        # joint name
        if data["jnt_names"]:
            jnt_name = data["jnt_names"].split(",")
            if index < len(jnt_name):
                if jnt_name:
                    name = jnt_name[index]

        # get parent piece joint
        skeleton_grp = context["skeleton"]
        asset_container, asset_root = context["asset"]
        if "parent_anchor" in data:
            parent_d_id, ref_anchor = data["parent_anchor"].split(",")
            while not parent:
                parent_container, parent_root = find_rig_from_id(
                    asset_root, parent_d_id)
                # assembly_01 piece
                if not parent_container:
                    parent = skeleton_grp
                    break
                # assembly_01 piece
                if parent_root.attr("piece").get() == "assembly_01":
                    parent = pm.listConnections(parent_root.attr("jnts")[0],
                                                destination=False,
                                                source=True)[0]
                    break
                parent_anchor = parent_root.attr("parent_anchor").get()
                parent_d_id, _ = parent_anchor.split(",")
                # if don't exists joint in piece, continue
                if not pm.listAttr(parent_root.attr("jnts"), multi=True):
                    ref_anchor = -1
                    continue

                custom_ref_index = data["custom_ref_index"]
                refs_element = pm.listAttr(parent_root.attr("refs"), multi=True)
                ref_anchors_element = pm.listAttr(parent_root.attr("ref_anchors"), multi=True)
                refs_index = None
                ref_anchors_index = None
                if -1 < custom_ref_index < len(refs_element):
                    refs_index = custom_ref_index
                elif custom_ref_index >= len(refs_element):
                    refs_index = -1
                    log.Logger.warning(
                        f"\tcheck 'jnt' custom_ref_index")
                    log.Logger.warning("\tcustom_ref_index : "
                                       f"{custom_ref_index!r}")
                    log.Logger.warning(f"\tresult attr : "
                                       f"{parent_root}.{refs_element[int(ref_anchor)]!r}")
                elif custom_ref_index == -1:
                    if int(ref_anchor) >= len(ref_anchors_element):
                        ref_anchors_index = -1
                    else:
                        ref_anchors_index = int(ref_anchor)
                if ref_anchors_index is not None:
                    e = pm.listAttr(parent_root.attr("ref_anchors"), multi=True)
                    _ref = pm.listConnections(parent_root.attr(e[ref_anchors_index]),
                                              destination=False,
                                              source=True)[0]
                    attrs = pm.listConnections(_ref.attr("message"),
                                               plugs=True,
                                               destination=True,
                                               source=False)
                    for attr in attrs:
                        if attr.attrName() == "refs":
                            break
                    refs_index = attr.index()
                if refs_index is not None:
                    if refs_index >= parent_root.attr("jnts").numConnectedElements():
                        refs_index = -1
                    attr = pm.listAttr(parent_root.attr("jnts"), multi=True)[refs_index]
                parent = pm.listConnections(parent_root.attr(attr),
                                            destination=False,
                                            source=True)[0]
        else:
            parent = skeleton_grp

        # create joint
        obj = joint.add(parent, name, m)
        pm.container(self.container, edit=True, removeNode=obj)
        pm.container(context["asset"][0], edit=True, removeNode=obj)
        attribute.nonkeyable(obj, ["tx", "ty", "tz",
                                   "rx", "ry", "rz", "ro",
                                   "sx", "sy", "sz"])
        attribute.lock(obj, ["v"])
        attribute.hide(obj, ["v"])

        # connect ref to jnt
        if ref:
            joint.connect_space(ref, obj)

        # joint label setup
        if "side" not in data:
            data["side"] = None
        if "index" not in data:
            data["index"] = None
        joint.labeling(obj,
                       data["name"],
                       data["side"],
                       data["index"],
                       description)
        pm.disconnectAttr(obj.attr("inverseScale"))

        # jnts connect
        pm.connectAttr(obj.attr("message"),
                       self.root.attr("jnts")[index])
        context["jnts"].append(obj)

        if leaf:
            attrs = pm.listAttr(self.root.attr("refs"), multi=True)
            if not attrs:
                index = 0
            else:
                index = len(attrs)
            pm.connectAttr(obj.attr("message"),
                           self.root.attr("refs")[index])
            context["refs"].append(obj)
        return obj

    def create_blended_jnt(self, name, index):
        data = self.data(DData.SELF)

        if pm.listConnections(self.root.attr("blended_jnts")[index],
                              destination=False,
                              source=True,
                              type="joint"):
            return None
        source = pm.listConnections(self.root.attr("jnts")[index],
                                    destination=False,
                                    source=True,
                                    type="joint")[0]
        m = source.getMatrix(worldSpace=True)
        parent = source.getParent()

        description = f"blended{index}"
        if not name:
            name = self.naming(description, "", "jnt")
        jnt = joint.add(parent, name, dt.Matrix(m))
        jnt.attr("jointOrient").set(source.attr("jointOrient").get())
        jnt.attr("r").set(0, 0, 0)
        jnt.attr("radius").set(0.75)

        pair_b = pm.createNode("pairBlend")
        pair_b.attr("rotInterpolation").set(1)
        pair_b.attr("weight").set(0.5)

        pm.connectAttr(source.attr("r"), pair_b.attr("inRotate1"))
        pm.connectAttr(source.attr("t"), pair_b.attr("inTranslate1"))
        pm.connectAttr(source.attr("t"), pair_b.attr("inTranslate2"))

        pm.connectAttr(pair_b.attr("outTranslate"), jnt.attr("t"))
        pm.connectAttr(pair_b.attr("outRotate"), jnt.attr("r"))
        pm.connectAttr(source.attr("s"), jnt.attr("s"))

        # connect blended jnts
        pm.connectAttr(jnt.attr("message"),
                       self.root.attr("blended_jnts")[index])

        # joint label setup
        joint.labeling(jnt,
                       data["name"],
                       data["side"],
                       data["index"],
                       description)

        container = pm.container(query=True, findContainer=self.root)
        pm.container(container, edit=True, removeNode=[jnt, pair_b])
        parent_container = pm.container(query=True,
                                        findContainer=container)
        pm.container(parent_container, edit=True, removeNode=[jnt, pair_b])
        return jnt

    def create_support_jnt(self, name, description, blended_index, count, m):
        data = self.data(DData.SELF)

        if not name:
            name = self.naming(description, "", "jnt")

        parent = pm.listConnections(self.root.attr("blended_jnts")[blended_index],
                                    destination=False,
                                    source=True,
                                    type="joint")[0]

        jnt = joint.add(parent, name, m)
        jnt.attr("jointOrient").set(jnt.attr("r").get())
        jnt.attr("r").set(0, 0, 0)
        jnt.attr("radius").set(0.25)

        # connect support jnts, matrices
        pm.connectAttr(jnt.attr("message"),
                       self.root.attr("support_jnts")[count])
        pm.connectAttr(jnt.attr("worldMatrix")[0],
                       self.root.attr("support_jnt_matrices")[count])

        # joint label setup
        joint.labeling(jnt,
                       data["name"],
                       data["side"],
                       data["index"],
                       description)
        # description save
        attribute.add(jnt,
                      longName="description",
                      typ="string",
                      value=description)

        container = pm.container(query=True, findContainer=self.root)
        pm.container(container, edit=True, removeNode=jnt)
        parent_container = pm.container(query=True,
                                        findContainer=container)
        pm.container(parent_container, edit=True, removeNode=jnt)
        return jnt

    def sub_jnt(self, context):
        data = self.data(DData.SELF)
        assembly_data = self.data(DData.ASSEMBLY)

        if data == assembly_data:
            return 0
        blended_jnt_names = data["blended_jnt_names"].split(",")
        support_jnt_names = data["support_jnt_names"].split(",")
        support_jnt_descriptions = data["support_jnt_descriptions"].split(",")
        blended_jnt_indices = [int(x) for x in data["blended_jnt_indices"].split(",") if x]
        support_jnt_indices = [int(x) for x in data["support_jnt_indices"].split(",") if x]
        support_jnt_matrices = [dt.Matrix(x) for x in data["support_jnt_matrices"]]

        # blend
        name = ""
        for count, index in enumerate(blended_jnt_indices):
            if assembly_data["sub_jnt_custom_name"]:
                name = blended_jnt_names[count]
            blended_jnt = self.create_blended_jnt(name, index)
            context["jnts"].append(blended_jnt)

        # support
        name = ""
        for count, index in enumerate(support_jnt_indices):
            if assembly_data["sub_jnt_custom_name"]:
                name = support_jnt_names[count]
            m = support_jnt_matrices[count]
            description = support_jnt_descriptions[count]
            support_jnt = self.create_support_jnt(name,
                                                  description,
                                                  index,
                                                  count,
                                                  m)
            context["jnts"].append(support_jnt)

    @staticmethod
    def setup_host(context):
        roots = context["roots"].getChildren(type="transform")
        hosts = [root.attr("host").inputs() for root in roots]
        hosts = list(set([host[0] for host in hosts if host]))
        for host in hosts:
            publish_attrs = pm.listAttr(host, userDefined=True, shortNames=True) or []
            publish_attrs = [x for x in publish_attrs if host.attr(x).isInChannelBox() or host.attr(x).isKeyable()]
            container = pm.container(query=True, findContainer=host)
            for attr in publish_attrs:
                publish_name = "hostI_" + attr
                pm.container(container,
                             edit=True,
                             publishName=publish_name)
                pm.container(container,
                             edit=True,
                             bindAttr=[host.attr(attr), publish_name])

    @staticmethod
    def setup_ctl(context):
        # controller publish and x ray
        for ctl in context["ctls"].copy():
            if not ctl.exists():
                context["ctls"].remove(ctl)
                continue
            pub_name = ctl.nodeName()
            container = pm.container(query=True, findContainer=ctl)
            pm.containerPublish(container, publishNode=(pub_name, ""))
            pm.containerPublish(container, bindNode=(pub_name, ctl))

            shapes = ctl.getShapes()
            for shape in shapes:
                pm.connectAttr(context["asset"][1].attr("ctl_x_ray"), shape.attr("alwaysDrawOnTop"))
        pm.connectAttr(context["asset"][1].attr("ctl_on_playback"), context["roots"].attr("hideOnPlayback"))
        pm.connectAttr(context["asset"][1].attr("ctl_vis"), context["roots"].attr("v"))
        assembly_root = context["asset"][1].attr("assembly_piece").get()
        pose_data = json.loads(assembly_root.attr("pose_json").get().replace("'", "\""))
        if pose_data["neutral"]:
            return
        neutral_pose_data = attribute.get_data(context["ctls"])
        pose_data["neutral"] = neutral_pose_data
        assembly_root.attr("pose_json").set(json.dumps(pose_data))

    @staticmethod
    def setup_jnt(context):
        for jnt in context["jnts"]:
            jnt.attr("segmentScaleCompensate").set(False)
            target = pm.listConnections(jnt.attr("inverseScale"), source=True, destination=False, plugs=True)
            if target:
                pm.disconnectAttr(target[0], jnt.attr("inverseScale"))

    @staticmethod
    def create_sets(context):
        name = context["name"]
        rig_sets = pm.sets(name=f"{name}_{naming.SETS_EXT}", empty=True)
        model_sets = pm.sets(name=f"{name}_model_{naming.SETS_EXT}", empty=True)
        geometry_sets = pm.sets(name=f"{name}_geometry_{naming.SETS_EXT}", empty=True)
        skeleton_sets = pm.sets(name=f"{name}_skeleton_{naming.SETS_EXT}", empty=True)
        controller_sets = pm.sets(name=f"{name}_controller_{naming.SETS_EXT}", empty=True)

        pm.sets(model_sets, addElement=context["model"])
        geometries = list(set([x.getParent() for x in pm.ls(context["model"], dagObjects=True, type="mesh")]))
        if geometries:
            pm.sets(geometry_sets, edit=True, addElement=geometries)
        if "jnts" in context:
            pm.sets(skeleton_sets, edit=True, addElement=context["jnts"])
        pm.sets(controller_sets, edit=True, addElement=context["ctls"])
        s = [model_sets, geometry_sets, skeleton_sets, controller_sets]
        pm.sets(rig_sets, edit=True, addElement=s)
        geo_sets_attr = attribute.add(context["asset"][1], longName="geo_sets", typ="message")
        ctl_sets_attr = attribute.add(context["asset"][1], longName="ctl_sets", typ="message")
        jnt_sets_attr = attribute.add(context["asset"][1], longName="jnt_sets", typ="message")
        pm.connectAttr(geometry_sets.attr("message"), geo_sets_attr)
        pm.connectAttr(controller_sets.attr("message"), ctl_sets_attr)
        pm.connectAttr(skeleton_sets.attr("message"), jnt_sets_attr)

    @staticmethod
    def callback(context):
        callback_nodes = context["callbacks"]
        if not callback_nodes:
            return 0
        assembly_node = context["containers"][0][1]
        d_id = assembly_node.attr("d_id").get()

        callback_root = pm.createNode("script")
        callback_root.attr("sourceType").set(1)
        callback_root.attr("scriptType").set(1)
        attribute.add(callback_root, "callbacks", "message")
        pm.connectAttr(assembly_node.attr("message"),
                       callback_root.attr("callbacks"))
        for callback_node in callback_nodes:
            pm.connectAttr(callback_root.attr("callbacks"),
                           callback_node.attr("root"))

        before_script_code = f"""import maya.cmds as mc
import maya.api.OpenMaya as om2
import traceback


def destroy_cb(*args):  # all callback clear
    global domino_destroy_new_id
    global domino_destroy_open_id
    global domino_destroy_remove_ref_id
    global domino_destroy_unload_ref_id
    global domino_character_cb_registry
    global domino_character_namespace_registry
    try:
        for array in domino_character_cb_registry:
            om2.MNodeMessage.removeCallback(array[1])
        om2.MSceneMessage.removeCallback(domino_destroy_new_id)
        om2.MSceneMessage.removeCallback(domino_destroy_open_id)
        om2.MSceneMessage.removeCallback(domino_destroy_remove_ref_id)
        om2.MSceneMessage.removeCallback(domino_destroy_unload_ref_id)
        del domino_character_cb_registry
        del domino_character_namespace_registry
        del domino_destroy_new_id
        del domino_destroy_open_id
        del domino_destroy_remove_ref_id
        del domino_destroy_unload_ref_id
    except:
        traceback.print_exc()


def refresh_registry(*argc):  # refresh registry at reference unload, remove
    global domino_character_cb_registry
    global domino_character_namespace_registry

    remove_list = []
    for ns in domino_character_namespace_registry:
        if not mc.namespaceInfo(ns, listNamespace=True):
            remove_list.append(ns)
    for rm in remove_list:
        domino_character_namespace_registry.remove(rm)
    for array in domino_character_cb_registry:
        if array[0].fullPathName() == "":
            om2.MNodeMessage.removeCallback(array[1])
    domino_character_cb_registry = [x for x in domino_character_cb_registry if x[0].fullPathName() != ""]


def run_callback_root():
    global domino_script_node_id_registry
    global domino_destroy_id
    global domino_character_namespace_registry
    try:
        domino_character_namespace_registry
    except:
        domino_character_namespace_registry = []
    domino_script_node_id_registry = []

    d_id = '{d_id}'

    roots = [mc.container(c, query=True, publishAsRoot=True)
             for c in mc.ls(type="container")]
    roots = [r for r in roots if r and mc.objExists(r + ".d_id")]
    roots = [r for r in roots if mc.getAttr(r + ".d_id") == d_id]
    
    if "" in domino_character_namespace_registry:
        domino_character_namespace_registry.remove("")
    if not roots:
        return
    for root in roots:
        callback_root = mc.listConnections(root + ".message",
                                           destination=True,
                                           source=False,
                                           type="script")
        namespace = mc.ls(root, showNamespace=True)[1]
        namespace = "" if namespace == ":" else namespace
        if callback_root and namespace not in domino_character_namespace_registry:
            callbacks = mc.listConnections(callback_root[0] + ".callbacks",
                                           destination=True,
                                           source=False,
                                           type="script")
            for cb in callbacks:
                mc.scriptNode(cb, executeBefore=True)
            domino_character_namespace_registry.append(namespace)

run_callback_root()
try:
    om2.MSceneMessage.removeCallback(domino_destroy_new_id)
except:
    pass
finally:
    domino_destroy_new_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterNew, destroy_cb)

try:
    om2.MSceneMessage.removeCallback(domino_destroy_open_id)
except:
    pass
finally:
    domino_destroy_open_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterOpen, destroy_cb)

try:
    om2.MSceneMessage.removeCallback(domino_destroy_remove_ref_id)
except:
    pass
finally:
    domino_destroy_remove_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterRemoveReference, refresh_registry)
    
try:
    om2.MSceneMessage.removeCallback(domino_destroy_unload_ref_id)
except:
    pass
finally:
    domino_destroy_unload_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterUnloadReference, refresh_registry)"""
        pm.scriptNode(callback_root, edit=True, beforeScript=before_script_code)
        pm.scriptNode(callback_root, executeBefore=True)
        context["callbacks"].append(callback_root)

    @staticmethod
    def debug_mode(context):
        for container, _ in context["containers"]:
            nodes = pm.container(container, query=True, nodeList=True)
            for n in nodes:
                if n.strip() == "__pymelUndoNode":
                    continue
                pm.container(container, edit=True, removeNode=n)
        nodes = pm.container(context["asset"][0],
                             query=True,
                             nodeList=True)
        for n in nodes:
            pm.container(context["asset"][0], edit=True, removeNode=n)
        containers = [context["asset"][0]] + [x[0] for x in context["containers"]]
        pm.delete(containers)

    @staticmethod
    def blackbox(context):
        containers = [x[0] for x in context["containers"]]
        for container in containers:
            container.attr("blackBox").set(True)

    def objects(self, context):
        self.set_current_container()

    def attributes(self, context):
        self.set_current_container()

    def operators(self, context):
        self.set_current_container()

    def connections(self, context):
        self.set_current_container()


class AbstractPiece:

    @property
    def identifier(self):
        return self._ddata.identifier

    @property
    def ddata(self):
        return self._ddata

    @property
    def guide(self):
        return self._guide

    @property
    def rig(self):
        return self._rig


class AbstractSubPiece:

    def __init_subclass__(cls):
        if not hasattr(cls, "run"):
            raise NotImplementedError("Implement 'run'")

    # example
    def run(self, context):
        ...
