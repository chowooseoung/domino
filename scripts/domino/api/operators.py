# maya
from pymel import core as pm

# domino
from . import (attribute)


def space_switch(source_ctls, target_ctl, host, attr_name="space_switch", constraint="parent"):
    enum_name = ["this"] + [x.nodeName() for x in source_ctls]
    attribute.add(host,
                  attr_name,
                  "enum",
                  enumName=enum_name,
                  keyable=True)
    target_npo = target_ctl.getParent()
    if pm.controller(target_npo, query=True):
        target_npo = target_npo.getParent()
    if constraint == "parent":
        cons_func = pm.parentConstraint
    elif constraint == "point":
        cons_func = pm.pointConstraint
    elif constraint == "orient":
        cons_func = pm.orientConstraint
    cons = cons_func(source_ctls, target_npo, maintainOffset=True)
    weight_list = cons_func(cons, query=True, weightAliasList=True)
    for i, attr in enumerate(weight_list):
        condition = pm.createNode("condition")
        pm.connectAttr(f"{host}.{attr_name}",
                       f"{condition}.firstTerm")
        condition.attr("secondTerm").set(i + 1)
        condition.attr("colorIfTrueR").set(1)
        condition.attr("colorIfFalseR").set(0)
        pm.connectAttr(condition.attr("outColorR"), attr)
    return cons


def ik_2jnt(jnt1, jnt2, scale_attr, slide_attr, stretch_value_attr, max_stretch_attr, negate):
    ik1_distance = jnt1.attr("tx").get()
    ik2_distance = jnt2.attr("tx").get()
    if negate:
        ik1_distance *= -1
        ik2_distance *= -1
        md = pm.createNode("multiplyDivide")
        md.attr("input1X").set(-1)
        pm.connectAttr(stretch_value_attr, md.attr("input2X"))
        stretch_value_attr = md.attr("outputX")

    md = pm.createNode("multiplyDivide")
    pm.connectAttr(scale_attr, md.attr("input1X"))
    pm.connectAttr(scale_attr, md.attr("input1Y"))
    md.attr("input2X").set(ik1_distance)
    md.attr("input2Y").set(ik2_distance)
    scaled_ik1_distance_attr = md.attr("outputX")
    scaled_ik2_distance_attr = md.attr("outputY")

    pma = pm.createNode("plusMinusAverage")
    pm.connectAttr(scaled_ik1_distance_attr, pma.attr("input1D")[0])
    pm.connectAttr(scaled_ik2_distance_attr, pma.attr("input1D")[1])
    scaled_total_distance_attr = pma.attr("output1D")

    rm = pm.createNode("remapValue")
    rm.attr("inputMin").set(0)
    rm.attr("inputMax").set(0.5)
    pm.connectAttr(slide_attr, rm.attr("inputValue"))
    pm.connectAttr(scaled_total_distance_attr, rm.attr("outputMin"))
    pm.connectAttr(scaled_ik1_distance_attr, rm.attr("outputMax"))
    min_ik1_slide_value_attr = rm.attr("outColorR")

    rm = pm.createNode("remapValue")
    rm.attr("inputMin").set(0.5)
    rm.attr("inputMax").set(1)
    pm.connectAttr(slide_attr, rm.attr("inputValue"))
    pm.connectAttr(scaled_ik1_distance_attr, rm.attr("outputMin"))
    rm.attr("outputMax").set(0)
    max_ik1_slide_value_attr = rm.attr("outColorR")

    condition = pm.createNode("condition")
    condition.attr("operation").set(4)
    condition.attr("secondTerm").set(0.5)
    pm.connectAttr(slide_attr, condition.attr("firstTerm"))
    pm.connectAttr(min_ik1_slide_value_attr, condition.attr("colorIfTrueR"))
    pm.connectAttr(max_ik1_slide_value_attr, condition.attr("colorIfFalseR"))
    ik1_slide_value_attr = condition.attr("outColorR")

    pma = pm.createNode("plusMinusAverage")
    pma.attr("operation").set(2)
    pm.connectAttr(scaled_total_distance_attr, pma.attr("input1D")[0])
    pm.connectAttr(ik1_slide_value_attr, pma.attr("input1D")[1])
    ik2_slide_value_attr = pma.attr("output1D")

    md = pm.createNode("multiplyDivide")
    md.attr("operation").set(2)
    pm.connectAttr(stretch_value_attr, md.attr("input1X"))
    pm.connectAttr(scaled_total_distance_attr, md.attr("input2X"))

    condition = pm.createNode("condition")
    condition.attr("operation").set(2)
    pm.connectAttr(stretch_value_attr, condition.attr("firstTerm"))
    pm.connectAttr(scaled_total_distance_attr, condition.attr("secondTerm"))
    pm.connectAttr(md.attr("outputX"), condition.attr("colorIfTrueR"))
    condition.attr("colorIfFalseR").set(1)
    stretch_condition_attr = condition.attr("outColorR")

    condition = pm.createNode("condition")
    condition.attr("operation").set(4)
    pm.connectAttr(stretch_condition_attr, condition.attr("firstTerm"))
    pm.connectAttr(max_stretch_attr, condition.attr("secondTerm"))
    pm.connectAttr(stretch_condition_attr, condition.attr("colorIfTrueR"))
    pm.connectAttr(max_stretch_attr, condition.attr("colorIfFalseR"))

    md = pm.createNode("multiplyDivide")
    pm.connectAttr(ik1_slide_value_attr, md.attr("input1X"))
    pm.connectAttr(ik2_slide_value_attr, md.attr("input1Y"))
    pm.connectAttr(condition.attr("outColorR"), md.attr("input2X"))
    pm.connectAttr(condition.attr("outColorR"), md.attr("input2Y"))
    ik1_stretch_value_attr = md.attr("outputX")
    ik2_stretch_value_attr = md.attr("outputY")
    if negate:
        md = pm.createNode("multiplyDivide")
        pm.connectAttr(ik1_stretch_value_attr, md.attr("input1X"))
        pm.connectAttr(ik2_stretch_value_attr, md.attr("input1Y"))
        md.attr("input2X").set(-1)
        md.attr("input2Y").set(-1)
        ik1_stretch_value_attr = md.attr("outputX")
        ik2_stretch_value_attr = md.attr("outputY")

    pm.connectAttr(ik1_stretch_value_attr, jnt1.attr("tx"))
    pm.connectAttr(ik2_stretch_value_attr, jnt2.attr("tx"))


def volume(original_distance_attr, delta_distance_attr, squash_attrs, stretch_attrs, switch_attr, objs):
    md = pm.createNode("multiplyDivide")
    md.attr("operation").set(2)
    pm.connectAttr(delta_distance_attr, md.attr("input1X"))
    pm.connectAttr(original_distance_attr, md.attr("input2X"))
    ratio_attr = md.attr("outputX")

    md = pm.createNode("multiplyDivide")
    md.attr("operation").set(3)
    pm.connectAttr(ratio_attr, md.attr("input1X"))
    md.attr("input2X").set(2)
    pow_value = md.attr("outputX")

    md = pm.createNode("multiplyDivide")
    md.attr("operation").set(3)
    pm.connectAttr(pow_value, md.attr("input1X"))
    md.attr("input2X").set(0.5)
    abs_value = md.attr("outputX")

    for i, obj in enumerate(objs):
        condition = pm.createNode("condition")
        condition.attr("operation").set(3)
        pm.connectAttr(ratio_attr, condition.attr("firstTerm"))
        condition.attr("secondTerm").set(0)
        pm.connectAttr(stretch_attrs[i], condition.attr("colorIfTrueR"))
        pm.connectAttr(squash_attrs[i], condition.attr("colorIfFalseR"))

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(condition.attr("outColorR"), md.attr("input1X"))
        pm.connectAttr(switch_attr, md.attr("input2X"))
        volume_multiple = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(abs_value, md.attr("input1X"))
        pm.connectAttr(volume_multiple, md.attr("input2X"))

        pma = pm.createNode("plusMinusAverage")
        pma.attr("input3D")[0].set((1, 1, 1))
        pm.connectAttr(md.attr("outputX"), pma.attr("input3D[1].input3Dx"))
        pm.connectAttr(md.attr("outputX"), pma.attr("input3D[1].input3Dy"))
        pm.connectAttr(md.attr("outputX"), pma.attr("input3D[1].input3Dz"))

        pm.connectAttr(pma.attr("output3D"), obj.attr("s"))


def auto_clavicle():
    pass
