# maya
from pymel import core as pm

# domino
from . import (log,
               fcurve)


dt = pm.datatypes


def hide(node, attrs):
    for attr in attrs:
        pm.setAttr(node.attr(attr), keyable=False, channelBox=False)


def lock(node, attrs):
    for attr in attrs:
        pm.setAttr(node.attr(attr), lock=True)


def unlock(node, attrs):
    for attr in attrs:
        pm.setAttr(node.attr(attr), lock=False)


def nonkeyable(node, attrs):
    for attr in attrs:
        pm.setAttr(node.attr(attr), keyable=True, channelBox=True)


def keyable(node, attrs):
    for attr in attrs:
        pm.setAttr(node.attr(attr), keyable=True)


def _get(attr):
    at = pm.getAttr(attr, type=True)
    if at == "enum":
        return attr.get(asString=True)
    elif at == "matrix":
        return list(attr.get().flat)
    return attr.get()


def _set(attr, value):
    at = pm.getAttr(attr, type=True)
    if at == "matrix":
        attr.set(dt.Matrix(value))
    else:
        attr.set(value)


def add(node, longName=None, typ=None, **kws):
    if node.hasAttr(longName):
        return node.attr(longName)

    if typ == "float3":
        return add_color(node, longName, typ, **kws)

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
                       "short3", ]

    arguments = dict()
    arguments["longName"] = longName
    if typ in datatypes:
        arguments["dataType"] = typ
    elif typ in attribute_types:
        arguments["attributeType"] = typ

    if "enumName" in kws:
        arguments["enumName"] = kws["enumName"]

    if "defaultValue" in kws:
        arguments["defaultValue"] = kws["defaultValue"]

    if "minValue" in kws:
        arguments["minValue"] = kws["minValue"]

    if "maxValue" in kws:
        arguments["maxValue"] = kws["maxValue"]

    if "keyable" in kws:
        arguments["keyable"] = kws["keyable"]

    if "multi" in kws:
        arguments["multi"] = kws["multi"]

    if "hidden" in kws:
        arguments["hidden"] = kws["hidden"]

    if "shortName" in kws:
        arguments["shortName"] = kws["shortName"]

    pm.addAttr(node, **arguments)

    if "value" in kws and typ != "message":
        if "multi" in kws:
            if kws["multi"]:
                for index, value in enumerate(kws["value"]):
                    source = pm.connectionInfo(node.attr(longName)[index],
                                               sourceFromDestination=True)
                    if not source:
                        pm.setAttr(node.attr(longName)[index], value)
                    else:
                        log.Logger.warn("{node}.{attr} is connected : \"{source}\"".format(
                            node=node.fullPath(), attr=longName, source=source))
        else:
            pm.setAttr(node.attr(longName), kws["value"])
    if "channelBox" in kws:
        if kws["channelBox"]:
            pm.setAttr(node.attr(longName), channelBox=True)
    if "fcurve" in kws:
        fcurve.set_fcurve(kws["fcurve"], driven=[node.attr(longName)])
    return node.attr(longName)


def add_color(node, longName, typ, **kws):
    r_attr = longName + "_r"
    g_attr = longName + "_g"
    b_attr = longName + "_b"

    arguments = dict()
    arguments["attributeType"] = typ
    arguments["usedAsColor"] = True

    child_arguments = dict()
    child_arguments["attributeType"] = 'float'
    child_arguments["parent"] = longName

    node.addAttr(longName, **arguments)
    node.addAttr(r_attr, **child_arguments)
    node.addAttr(g_attr, **child_arguments)
    node.addAttr(b_attr, **child_arguments)

    if "value" in kws:
        node.setAttr(longName + "_r", kws["value"][0])
        node.setAttr(longName + "_g", kws["value"][1])
        node.setAttr(longName + "_b", kws["value"][2])
    return node.attr(longName)


def reset(obj, attrs):
    for attr in attrs:
        default_value = pm.attributeQuery(attr, node=obj, listDefault=True)[0]
        try:
            pm.setAttr(f"{obj}.{attr}", default_value)
        except:
            pass


def reset_published_attr(containers):
    for container in containers:
        publish_attrs = [x[0] for x in pm.container(container, query=True, bindAttr=True)]
        for attr in publish_attrs:
            reset(attr.node(), [attr.attrName()])


def reset_all(objs):
    for obj in objs:
        keyable_attrs = pm.listAttr(obj, keyable=True) or []
        nonkeyable_attrs = pm.listAttr(obj, channelBox=True) or []
        attrs = keyable_attrs + nonkeyable_attrs
        reset(obj, list(set(attrs)))


def reset_SRT(objs, attributes=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]):
    for obj in objs:
        reset(obj, attributes)


def get_data(ctls):
    d = {}
    for ctl in ctls:
        name = ctl.nodeName()
        user_define_attrs = pm.listAttr(ctl, unlocked=True) or []
        user_define_attrs = [x for x in user_define_attrs if ctl.attr(x).isKeyable() or ctl.attr(x).isInChannelBox()]
        _d = {}
        for attr in user_define_attrs:
            _d[attr] = ctl.attr(attr).get()
        if _d:
            d[name] = _d
    return d


def set_data(data, namespace=":"):
    for ctl in data:
        name = namespace + ctl
        for attr in data[ctl]:
            pm.setAttr(name + "." + attr, data[ctl][attr])
