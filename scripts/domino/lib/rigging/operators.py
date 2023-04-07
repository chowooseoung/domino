# maya
from maya import cmds as mc

# domino
from domino.lib import attribute, hierarchy


def space_switch(source_ctls, target_ctl, host, attr_name="space_switch", constraint="parent", **aim_args):
    enum_name = ["this"] + [x.split("|")[-1] for x in source_ctls]
    argument = {"type": "enum", "enumName": ":".join(enum_name), "keyable": True, "longName": attr_name}
    attribute.add_attr(host, **argument)
    target_npo = hierarchy.get_parent(target_ctl)
    if mc.controller(target_npo, query=True):
        target_npo = hierarchy.get_parent(target_npo)
    cons_func = None
    argument = {"maintainOffset": True}
    if constraint == "parent":
        cons_func = mc.parentConstraint
    elif constraint == "point":
        cons_func = mc.pointConstraint
    elif constraint == "orient":
        cons_func = mc.orientConstraint
    elif constraint == "aim":
        cons_func = mc.aimConstraint
        argument.update(aim_args)
    cons = cons_func(source_ctls, target_npo, **argument)[0]
    weight_list = cons_func(cons, query=True, weightAliasList=True)
    for i, attr in enumerate(weight_list):
        condition = mc.createNode("condition")
        mc.connectAttr(host + "." + attr_name, condition + ".firstTerm")
        mc.setAttr(condition + ".secondTerm", i + 1)
        mc.setAttr(condition + ".colorIfTrueR", 1)
        mc.setAttr(condition + ".colorIfFalseR", 0)
        mc.connectAttr(condition + ".outColorR", cons + "." + attr)
    return cons


def ik_2jnt(jnt1, jnt2, scale_attr, slide_attr, stretch_value_attr, max_stretch_attr, negate):
    ik1_distance = mc.getAttr(jnt1 + ".tx")
    ik2_distance = mc.getAttr(jnt2 + ".tx")
    if negate:
        ik1_distance *= -1
        ik2_distance *= -1
        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".input1X", -1)
        mc.connectAttr(stretch_value_attr, md + ".input2X")
        stretch_value_attr = md + ".outputX"

    md = mc.createNode("multiplyDivide")
    mc.connectAttr(scale_attr, md + ".input1X")
    mc.connectAttr(scale_attr, md + ".input1Y")
    mc.setAttr(md + ".input2X", ik1_distance)
    mc.setAttr(md + ".input2Y", ik2_distance)
    scaled_ik1_distance_attr = md + ".outputX"
    scaled_ik2_distance_attr = md + ".outputY"

    pma = mc.createNode("plusMinusAverage")
    mc.connectAttr(scaled_ik1_distance_attr, pma + ".input1D[0]")
    mc.connectAttr(scaled_ik2_distance_attr, pma + ".input1D[1]")
    scaled_total_distance_attr = pma + ".output1D"

    rm = mc.createNode("remapValue")
    mc.setAttr(rm + ".inputMin", 0)
    mc.setAttr(rm + ".inputMax", 0.5)
    mc.connectAttr(slide_attr, rm + ".inputValue")
    mc.connectAttr(scaled_total_distance_attr, rm + ".outputMin")
    mc.connectAttr(scaled_ik1_distance_attr, rm + ".outputMax")
    min_ik1_slide_value_attr = rm + ".outColorR"

    rm = mc.createNode("remapValue")
    mc.setAttr(rm + ".inputMin", 0.5)
    mc.setAttr(rm + ".inputMax", 1)
    mc.connectAttr(slide_attr, rm + ".inputValue")
    mc.connectAttr(scaled_ik1_distance_attr, rm + ".outputMin")
    mc.setAttr(rm + ".outputMax", 0)
    max_ik1_slide_value_attr = rm + ".outColorR"

    condition = mc.createNode("condition")
    mc.setAttr(condition + ".operation", 4)
    mc.setAttr(condition + ".secondTerm", 0.5)
    mc.connectAttr(slide_attr, condition + ".firstTerm")
    mc.connectAttr(min_ik1_slide_value_attr, condition + ".colorIfTrueR")
    mc.connectAttr(max_ik1_slide_value_attr, condition + ".colorIfFalseR")
    ik1_slide_value_attr = condition + ".outColorR"

    pma = mc.createNode("plusMinusAverage")
    mc.setAttr(pma + ".operation", 2)
    mc.connectAttr(scaled_total_distance_attr, pma + ".input1D[0]")
    mc.connectAttr(ik1_slide_value_attr, pma + ".input1D[1]")
    ik2_slide_value_attr = pma + ".output1D"

    md = mc.createNode("multiplyDivide")
    mc.setAttr(md + ".operation", 2)
    mc.connectAttr(stretch_value_attr, md + ".input1X")
    mc.connectAttr(scaled_total_distance_attr, md + ".input2X")
    stretch_ratio_attr = md + ".outputX"

    condition = mc.createNode("condition")
    mc.setAttr(condition + ".operation", 2)
    mc.connectAttr(stretch_value_attr, condition + ".firstTerm")
    mc.connectAttr(scaled_total_distance_attr, condition + ".secondTerm")
    mc.connectAttr(stretch_ratio_attr, condition + ".colorIfTrueR")
    mc.setAttr(condition + ".colorIfFalseR", 1)
    stretch_condition_attr = condition + ".outColorR"

    condition = mc.createNode("condition")
    mc.setAttr(condition + ".operation", 4)
    mc.connectAttr(stretch_condition_attr, condition + ".firstTerm")
    mc.connectAttr(max_stretch_attr, condition + ".secondTerm")
    mc.connectAttr(stretch_condition_attr, condition + ".colorIfTrueR")
    mc.connectAttr(max_stretch_attr, condition + ".colorIfFalseR")

    md = mc.createNode("multiplyDivide")
    mc.connectAttr(ik1_slide_value_attr, md + ".input1X")
    mc.connectAttr(ik2_slide_value_attr, md + ".input1Y")
    mc.connectAttr(condition + ".outColorR", md + ".input2X")
    mc.connectAttr(condition + ".outColorR", md + ".input2Y")
    ik1_stretch_value_attr = md + ".outputX"
    ik2_stretch_value_attr = md + ".outputY"
    if negate:
        md = mc.createNode("multiplyDivide")
        mc.connectAttr(ik1_stretch_value_attr, md + ".input1X")
        mc.connectAttr(ik2_stretch_value_attr, md + ".input1Y")
        mc.setAttr(md + ".input2X", -1)
        mc.setAttr(md + ".input2Y", -1)
        ik1_stretch_value_attr = md + ".outputX"
        ik2_stretch_value_attr = md + ".outputY"

    mc.connectAttr(ik1_stretch_value_attr, jnt1 + ".tx")
    mc.connectAttr(ik2_stretch_value_attr, jnt2 + ".tx")


def ik_3jnt(jnt1, jnt2, jnt3, multi1_attr, multi2_attr, multi3_attr, stretch_value_attr, max_stretch_attr, negate):
    ik1_distance = mc.getAttr(jnt1 + ".tx")
    ik2_distance = mc.getAttr(jnt2 + ".tx")
    ik3_distance = mc.getAttr(jnt3 + ".tx")
    if negate:
        ik1_distance *= -1
        ik2_distance *= -1
        ik3_distance *= -1
        md = mc.createNode("multiplyDivide")
        mc.setAttr(md + ".input1X", -1)
        mc.connectAttr(stretch_value_attr, md + ".input2X")
        stretch_value_attr = md + ".outputX"

    md = mc.createNode("multiplyDivide")
    mc.connectAttr(multi1_attr, md + ".input1X")
    mc.connectAttr(multi2_attr, md + ".input1Y")
    mc.connectAttr(multi3_attr, md + ".input1Z")
    mc.setAttr(md + ".input2X", ik1_distance)
    mc.setAttr(md + ".input2Y", ik2_distance)
    mc.setAttr(md + ".input2Z", ik3_distance)
    multiple_ik1_distance_attr = md + ".outputX"
    multiple_ik2_distance_attr = md + ".outputY"
    multiple_ik3_distance_attr = md + ".outputZ"

    pma = mc.createNode("plusMinusAverage")
    mc.connectAttr(multiple_ik1_distance_attr, pma + ".input1D[0]")
    mc.connectAttr(multiple_ik2_distance_attr, pma + ".input1D[1]")
    mc.connectAttr(multiple_ik3_distance_attr, pma + ".input1D[2]")
    multiple_total_distance_attr = pma + ".output1D"

    md = mc.createNode("multiplyDivide")
    mc.setAttr(md + ".operation", 2)
    mc.connectAttr(stretch_value_attr, md + ".input1X")
    mc.connectAttr(multiple_total_distance_attr, md + ".input2X")
    stretch_ratio_attr = md + ".outputX"

    condition = mc.createNode("condition")
    mc.setAttr(condition + ".operation", 2)
    mc.connectAttr(stretch_value_attr, condition + ".firstTerm")
    mc.connectAttr(multiple_total_distance_attr, condition + ".secondTerm")
    mc.connectAttr(stretch_ratio_attr, condition + ".colorIfTrueR")
    mc.setAttr(condition + ".colorIfFalseR", 1)
    stretch_condition_attr = condition + ".outColorR"

    condition = mc.createNode("condition")
    mc.setAttr(condition + ".operation", 4)
    mc.connectAttr(stretch_condition_attr, condition + ".firstTerm")
    mc.connectAttr(max_stretch_attr, condition + ".secondTerm")
    mc.connectAttr(stretch_condition_attr, condition + ".colorIfTrueR")
    mc.connectAttr(max_stretch_attr, condition + ".colorIfFalseR")

    md = mc.createNode("multiplyDivide")
    mc.connectAttr(multiple_ik1_distance_attr, md + ".input1X")
    mc.connectAttr(multiple_ik2_distance_attr, md + ".input1Y")
    mc.connectAttr(multiple_ik3_distance_attr, md + ".input1Z")
    mc.connectAttr(condition + ".outColorR", md + ".input2X")
    mc.connectAttr(condition + ".outColorR", md + ".input2Y")
    mc.connectAttr(condition + ".outColorR", md + ".input2Z")
    ik1_stretch_value_attr = md + ".outputX"
    ik2_stretch_value_attr = md + ".outputY"
    ik3_stretch_value_attr = md + ".outputZ"
    if negate:
        md = mc.createNode("multiplyDivide")
        mc.connectAttr(ik1_stretch_value_attr, md + ".input1X")
        mc.connectAttr(ik2_stretch_value_attr, md + ".input1Y")
        mc.connectAttr(ik3_stretch_value_attr, md + ".input1Z")
        mc.setAttr(md + ".input2X", -1)
        mc.setAttr(md + ".input2Y", -1)
        mc.setAttr(md + ".input2Z", -1)
        ik1_stretch_value_attr = md + ".outputX"
        ik2_stretch_value_attr = md + ".outputY"
        ik3_stretch_value_attr = md + ".outputZ"

    mc.connectAttr(ik1_stretch_value_attr, jnt1 + ".tx")
    mc.connectAttr(ik2_stretch_value_attr, jnt2 + ".tx")
    mc.connectAttr(ik3_stretch_value_attr, jnt3 + ".tx")


def volume(original_distance_attr, delta_distance_attr, squash_attrs, stretch_attrs, switch_attr, nodes):
    md = mc.createNode("multiplyDivide")
    mc.setAttr(md + ".operation", 2)
    mc.connectAttr(delta_distance_attr, md + ".input1X")
    mc.connectAttr(original_distance_attr, md + ".input2X")
    ratio_attr = md + ".outputX"

    md = mc.createNode("multiplyDivide")
    mc.setAttr(md + ".operation", 3)
    mc.connectAttr(ratio_attr, md + ".input1X")
    mc.setAttr(md + ".input2X", 2)
    pow_value = md + ".outputX"

    md = mc.createNode("multiplyDivide")
    mc.setAttr(md + ".operation", 3)
    mc.connectAttr(pow_value, md + ".input1X")
    mc.setAttr(md + ".input2X", 0.5)
    abs_value = md + ".outputX"

    for i, node in enumerate(nodes):
        condition = mc.createNode("condition")
        mc.setAttr(condition + ".operation", 3)
        mc.connectAttr(ratio_attr, condition + ".firstTerm")
        mc.setAttr(condition + ".secondTerm", 0)
        mc.connectAttr(stretch_attrs[i], condition + ".colorIfTrueR")
        mc.connectAttr(squash_attrs[i], condition + ".colorIfFalseR")

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(condition + ".outColorR", md + ".input1X")
        mc.connectAttr(switch_attr, md + ".input2X")
        volume_multiple = md + ".outputX"

        md = mc.createNode("multiplyDivide")
        mc.connectAttr(abs_value, md + ".input1X")
        mc.connectAttr(volume_multiple, md + ".input2X")

        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".input3D[0]", 1, 1, 1)
        mc.connectAttr(md + ".outputX", pma + ".input3D[1].input3Dx")
        mc.connectAttr(md + ".outputX", pma + ".input3D[1].input3Dy")
        mc.connectAttr(md + ".outputX", pma + ".input3D[1].input3Dz")

        mc.connectAttr(pma + ".output3D", node + ".s")


def set_fk_ik_blend_matrix(blend, fk, ik, switch):
    for i in range(len(blend)):
        blend_m = mc.createNode("blendMatrix")
        mc.setAttr(blend_m + ".envelope", 1)

        if i == 0:
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(fk[i] + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(blend[i] + ".parentInverseMatrix", mult_m + ".matrixIn[1]")
            mc.connectAttr(mult_m + ".matrixSum", blend_m + ".inputMatrix")
        else:
            mc.connectAttr(fk[i] + ".matrix", blend_m + ".inputMatrix")

        comp_m = mc.createNode("composeMatrix")
        mc.setAttr(comp_m + ".inputTranslate", *mc.getAttr(ik[i] + ".t")[0])
        mc.setAttr(comp_m + ".inputRotate", *mc.getAttr(ik[i] + ".jointOrient")[0])

        inv_m = mc.createNode("inverseMatrix")
        mc.setAttr(inv_m + ".inputMatrix", mc.getAttr(comp_m + ".outputMatrix"), type="matrix")
        mc.delete(comp_m)

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(ik[i] + ".matrix", mult_m + ".matrixIn[0]")
        mc.connectAttr(inv_m + ".outputMatrix", mult_m + ".matrixIn[1]")

        mc.connectAttr(mult_m + ".matrixSum", blend_m + ".target[0].targetMatrix")

        decom_m = mc.createNode("decomposeMatrix")
        mc.connectAttr(blend_m + ".outputMatrix", decom_m + ".inputMatrix")

        mc.connectAttr(decom_m + ".outputTranslate", blend[i] + ".t")
        mc.connectAttr(decom_m + ".outputRotate", blend[i] + ".r")
        mc.connectAttr(decom_m + ".outputScale", blend[i] + ".s")
        mc.connectAttr(decom_m + ".outputShear", blend[i] + ".shear")

        mc.connectAttr(switch, blend_m + ".envelope")
