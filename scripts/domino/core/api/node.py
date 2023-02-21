# maya
from pymel import core as pm


def create_decom_matrix(m):
    decom_m = pm.createNode("decomposeMatrix")
    pm.connectAttr(m, decom_m.attr("inputMatrix"))
    return decom_m


def create_mult_matrix(matrix1, matrix2, output):
    mult_m = pm.createNode("multMatrix")
    for m, attr in zip([matrix1, matrix2], ["matrixIn[0]", "matrixIn[1]"]):
        if isinstance(m, pm.datatypes.Matrix):
            pm.setAttr(mult_m.attr(attr), m)
        else:
            pm.connectAttr(m, mult_m.attr(attr))
    if output:
        pm.connectAttr(mult_m.attr("matrixSum"), output)
    return mult_m


def create_pairblend(obj1,
                     obj2,
                     blender=0.5,
                     interpolation=0,
                     output=None,
                     trs="tr"):
    pair_b = pm.createNode("pairBlend")
    pair_b.attr("rotInterpolation").set(interpolation)

    if obj1:
        if "t" in trs:
            pm.connectAttr(obj1.attr("t"), pair_b.attr("inTranslate1"))
        if "r" in trs:
            pm.connectAttr(obj1.attr("r"), pair_b.attr("inRotate1"))

    if obj2:
        if "t" in trs:
            pm.connectAttr(obj2.attr("t"), pair_b.attr("inTranslate2"))
        if "r" in trs:
            pm.connectAttr(obj2.attr("r"), pair_b.attr("inRotate2"))

    if isinstance(blender, str) or isinstance(blender, pm.Attribute):
        pm.connectAttr(blender, pair_b.attr("weight"))
    else:
        pm.setAttr(pair_b.attr("weight"), blender)

    if output:
        if "r" in trs:
            pm.connectAttr(pair_b.attr("outRotate"), output.attr("r"))
        if "t" in trs:
            pm.connectAttr(pair_b.attr("outTranslate"), output.attr("t"))
    return pair_b
