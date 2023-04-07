# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# built-ins
import re


def get_index(attr):
    match = re.search(r'\[(\d+)\]', attr)
    return int(match.group(1)) if match else None


def get_plug(node, attr):
    selection_list = om2.MSelectionList()
    selection_list.add(node)
    fn_node = om2.MFnDependencyNode(selection_list.getDependNode(0))
    # wantNetworkedPlug always 0
    # https://forums.autodesk.com/t5/maya-programming/maya-api-what-is-a-networked-plug-and-do-i-want-it-or-not/td-p/7182472
    return fn_node.findPlug(attr, 0)


def add_attr(node, **add_attr_args):
    def solve_type(_type):
        datatypes = ["string",
                     "stringArray",
                     "matrix",
                     "reflectanceRGB",
                     "spectrumRGB",
                     "doubleArray",
                     "floatArray",
                     "Int32Array",
                     "vectorArray",
                     "nurbsCurve",
                     "nurbsSurface",
                     "mesh",
                     "lattice",
                     "pointArray"]
        attribute_types = ["bool",
                           "long",
                           "short",
                           "byte",
                           "char",
                           "enum",
                           "float",
                           "double",
                           "doubleAngle",
                           "doubleLinear",
                           "compound",
                           "message",
                           "time",
                           "fltMatrix",
                           "reflectance",
                           "spectrum",
                           "float2",
                           "float3",
                           "double2",
                           "double3",
                           "long2",
                           "long3",
                           "short2",
                           "short3"]
        if _type in datatypes:
            return {"dataType": _type}
        elif _type in attribute_types:
            return {"attributeType": _type}

    if mc.attributeQuery(add_attr_args["longName"], node=node, exists=True):
        return None

    add_attr_args.update(solve_type(add_attr_args.pop("type")))

    if "attributeType" in add_attr_args and add_attr_args["attributeType"] == "float3":
        return add_color_attr(node, **add_attr_args)

    mc.addAttr(node, **add_attr_args)
    return node + "." + add_attr_args["longName"]


def add_color_attr(node, **add_attr_args):
    r_attr = add_attr_args["longName"] + "_r"
    g_attr = add_attr_args["longName"] + "_g"
    b_attr = add_attr_args["longName"] + "_b"

    arguments = {
        "longName": add_attr_args["longName"],
        "attributeType": add_attr_args["attributeType"],
        "usedAsColor": True
    }

    child_arguments = {
        "attributeType": "float",
        "parent": add_attr_args["longName"]
    }
    mc.addAttr(node, **arguments)
    for rgb_attr in [r_attr, g_attr, b_attr]:
        child_arguments["longName"] = rgb_attr
        mc.addAttr(node, **child_arguments)
    return node + "." + add_attr_args["longName"]


def add_mirror_config_channels(ctl, conf=(0,) * 9):
    attrs = ["Tx", "Ty", "Tz", "Rx", "Ry", "Rz", "Sx", "Sy", "Sz"]
    long_names = ["inv" + x for x in attrs]
    nice_names = ["Invert Mirror " + x for x in attrs]
    for i, _conf in enumerate(conf):
        add_args = {"longName": long_names[i],
                    "type": "bool",
                    "defaultValue": _conf,
                    "keyable": False,
                    "niceName": nice_names[i]}
        add_attr(ctl, **add_args)


def collect_attr(ctls):
    d = {}
    for ctl in ctls:
        name = ctl.split("|")[-1]
        unlocked_attrs = mc.listAttr(ctl, unlocked=True, keyable=True, shortNames=True) or []
        user_define_attrs = []
        for attr in unlocked_attrs:
            plug = get_plug(ctl, attr)
            if plug.isChannelBox or plug.isKeyable:
                user_define_attrs.append(attr)
        _d = {}
        for attr in user_define_attrs:
            _d[attr] = mc.getAttr(ctl + "." + attr)
        if _d:
            d[name] = _d
    return d


def apply_attr(data, namespace=":", *args, **kwargs):
    for ctl in data:
        name = namespace + ctl
        for attr in data[ctl]:
            mc.setAttr(name + "." + attr, data[ctl][attr])
