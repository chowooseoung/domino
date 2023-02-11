# maya
from pymel import core as pm

dt = pm.datatypes
nt = pm.nodetypes

set_driven_types = [nt.AnimCurveUA,
                    nt.AnimCurveUL,
                    nt.AnimCurveUT,
                    nt.AnimCurveUU]


def get_blend_weight_node(plug):
    blend_weight_node = pm.listConnections(plug, source=True, destination=False, type="blendWeighted")
    if blend_weight_node:
        return blend_weight_node[0]
    blend_weight_node = pm.createNode("blendWeighted")
    pm.connectAttr(blend_weight_node.attr("output"), plug)
    return blend_weight_node


def get_driver(fcurve):
    if not isinstance(fcurve, pm.PyNode):
        fcurve = pm.PyNode(fcurve)
    return [x.name() for x in pm.listConnections(fcurve, source=True, destination=False, plugs=True)]


def get_driven(fcurve):
    if not isinstance(fcurve, pm.PyNode):
        fcurve = pm.PyNode(fcurve)
    driven = []
    outputs = pm.listConnections(fcurve, source=False, destination=True, plugs=True)
    for output in outputs:
        if pm.nodeType(output.node()) == "blendWeighted":
            blend_weight = output.node()
            driven_plug = blend_weight.attr("output").outputs(plugs=True)
            if driven_plug:
                driven.append((driven_plug[0].name(), output.index()))
        else:
            driven.append(output.name())
    return driven


def get_fcurve(fcurve):
    if not isinstance(fcurve, pm.PyNode):
        fcurve = pm.PyNode(fcurve)

    data = {
        "name": fcurve.nodeName(),
        "type": pm.nodeType(fcurve),
        "driver": get_driver(fcurve),
        "driven": get_driven(fcurve),
        "time": pm.keyframe(fcurve, query=True),
        "floatChange": pm.keyframe(fcurve, query=True, floatChange=True),
        "valueChange": pm.keyframe(fcurve, query=True, valueChange=True),
        "inAngle": pm.keyTangent(fcurve, query=True, inAngle=True),
        "outAngle": pm.keyTangent(fcurve, query=True, outAngle=True),
        "inWeight": pm.keyTangent(fcurve, query=True, inWeight=True),
        "outWeight": pm.keyTangent(fcurve, query=True, outWeight=True),
        "inTangentType": pm.keyTangent(fcurve, query=True, inTangentType=True),
        "outTangentType": pm.keyTangent(fcurve, query=True, outTangentType=True),
        "weightedTangents": pm.keyTangent(fcurve, query=True, weightedTangents=True),
        "lock": pm.keyTangent(fcurve, query=True, lock=True)
    }
    return data


def set_fcurve(data, driver=None, driven=None):
    """TODO: driver mirror, value mirror"""
    fcurve = pm.createNode(data["type"], name=data["name"])

    for i, value in enumerate(data["valueChange"]):
        if data["time"]:
            argument = {"time": data["time"][i]}
        else:
            argument = {"float": data["floatChange"][i]}
        pm.setKeyframe(fcurve, edit=True, value=value, **argument)

    pm.keyTangent(fcurve, edit=True, weightedTangents=True)
    for i in range(len(data["valueChange"])):
        pm.keyTangent(fcurve, edit=True, index=(i, i), lock=False)
        pm.keyTangent(fcurve, edit=True, index=(i, i), itt=data["inTangentType"][i])
        pm.keyTangent(fcurve, edit=True, index=(i, i), ott=data["outTangentType"][i])
        pm.keyTangent(fcurve, edit=True, index=(i, i), ia=data["inAngle"][i])
        pm.keyTangent(fcurve, edit=True, index=(i, i), oa=data["outAngle"][i])
        pm.keyTangent(fcurve, edit=True, index=(i, i), iw=data["inWeight"][i])
        pm.keyTangent(fcurve, edit=True, index=(i, i), ow=data["outWeight"][i])
        pm.keyTangent(fcurve, edit=True, index=(i, i), lock=data["lock"][i])
    pm.keyTangent(fcurve, edit=True, weightedTangents=data["weightedTangents"][0])

    if not driver:
        if data["driver"]:
            driver = data["driver"][0]
    if driver:
        pm.connectAttr(driver, fcurve.attr("input"))

    if not driven:
        if data["driven"]:
            driven = data["driven"]
    if driven:
        for t in driven:
            if isinstance(t, tuple):
                driven, index = t
                blend_weight_node = get_blend_weight_node(driven)
                pm.connectAttr(fcurve.attr("output"), blend_weight_node.attr("input")[index])
            else:
                blend_weight_node = pm.listConnections(t,
                                                       source=True,
                                                       destination=False,
                                                       plugs=True,
                                                       type="blendWeighted")
                if blend_weight_node:
                    index = blend_weight_node[0].attr("input").numConnectedElements()
                    pm.connectAttr(fcurve.attr("output"), blend_weight_node[0].attr("input")[index])
                else:
                    pm.connectAttr(fcurve.attr("output"), t)
    return fcurve


def get_fcurve_values(fcurve, division, inputs=[], factor=1):
    incr = 1 / (division - 1.0)

    values = []
    if inputs:
        for i in inputs:
            pm.setAttr(fcurve + ".input", i)
            values.append(pm.getAttr(fcurve + ".output") * factor)
        return values
    for i in range(division):
        pm.setAttr(fcurve + ".input", i * incr)
        values.append(pm.getAttr(fcurve + ".output") * factor)
    return values
