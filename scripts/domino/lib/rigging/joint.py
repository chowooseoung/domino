# maya
from maya import mel
from maya import cmds as mc
from maya.api import OpenMaya as om2

# domino
from domino.lib import matrix

# built-ins
import math


def add_joint(parent=None, name="", m=om2.MTransformationMatrix(), radius=0.5, vis=True):
    jnt = mc.createNode("joint", name=name, parent=parent)
    mc.xform(jnt, matrix=m, worldSpace=True)
    mc.setAttr(jnt + ".radius", radius)
    mc.setAttr(jnt + ".segmentScaleCompensate", False)
    mc.setAttr(jnt + ".jointOrient", *mc.getAttr(jnt + ".r")[0])
    mc.setAttr(jnt + ".r", 0, 0, 0)
    if not vis:
        mc.setAttr(jnt + ".drawStyle", 2)
    return jnt


def add_chain_joint(parent, name, positions, normal, last_orient=None, negate=False, vis=False):
    if "%s" not in name:
        name += "%s"

    chain_matrix = matrix.get_chain_matrix(positions, normal, negate)
    m = matrix.set_matrix_translate(chain_matrix[-1], positions[-1])
    if last_orient:
        m = matrix.set_matrix_rotate(m, last_orient)
    chain_matrix.append(m)

    chain = []
    for i, m in enumerate(chain_matrix):
        jnt = add_joint(parent, name % i, m, 1, vis)
        chain.append(jnt)
        parent = jnt

    return chain


def ikh(parent, name, chain, solver="ikRPsolver", pole_vector=None):
    ik_h, _ = mc.ikHandle(name=name,
                          startJoint=chain[0],
                          endEffector=chain[-1],
                          solver=solver)
    ik_h = "|" + ik_h
    mc.setAttr(ik_h + ".v", 0)

    if parent:
        ik_h = mc.parent(ik_h, parent)[0]

    if pole_vector:
        mc.poleVectorConstraint(pole_vector, ik_h)
    return ik_h


def sp_ikh(parent, name, chain, curve=None):
    argument = {"name": name,
                "startJoint": chain[0],
                "endEffector": chain[-1],
                "solver": "ikSplineSolver"}
    if curve is None:
        argument.update({"createCurve": True})
    else:
        argument.update({"createCurve": False, "curve": curve})
    ik_h = mc.ikHandle(**argument)[0]
    ik_h = "|" + ik_h
    mc.setAttr(ik_h + ".v", 0)
    if parent:
        ik_h = mc.parent(ik_h, parent)[0]
    return ik_h


def labeling(jnt, name, side, index, description):
    if side == "C":
        mc.setAttr(jnt + ".side", 0)
    if side == "L":
        mc.setAttr(jnt + ".side", 1)
    if side == "R":
        mc.setAttr(jnt + ".side", 2)
    mc.setAttr(jnt + ".type", 18)
    if side is None and index is None:
        label = name
    else:
        label = f"{'S' if side in ['L', 'R'] else side}{index}_{name}"
    if description:
        label += f"_{description}"

    mc.setAttr(jnt + ".otherType", label, type="string")


def connect_space(source, target):
    mult_m = mc.createNode("multMatrix")
    mc.connectAttr(source + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
    mc.connectAttr(target + ".parentInverseMatrix", mult_m + ".matrixIn[1]")

    decom_m = mc.createNode("decomposeMatrix")
    mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
    mc.connectAttr(decom_m + ".outputTranslate", target + ".t")
    if mc.getAttr(decom_m + ".outputScaleZ") < 0:
        md = mc.createNode("multiplyDivide")
        mc.connectAttr(decom_m + ".outputScale", md + ".input1")
        mc.setAttr(md + ".input2", 1, 1, -1)
        mc.connectAttr(md + ".output", target + ".s")
    else:
        mc.connectAttr(decom_m + ".outputScale", target + ".s")
    mc.connectAttr(decom_m + ".outputShear", target + ".shear")

    if mc.nodeType(target) == "transform":
        mc.connectAttr(decom_m + ".outputRotate", target + ".r")
        return 0

    m = om2.MMatrix(mc.getAttr(mult_m + ".matrixSum"))
    i_m = m.inverse()

    j_orient = [math.degrees(x) for x in om2.MTransformationMatrix(m).rotation(om2.MSpace.kWorld).asEulerRotation()]

    mc.setAttr(target + ".jointOrient", *j_orient)

    mult_m2 = mc.createNode("multMatrix")
    mc.connectAttr(mult_m + ".matrixSum", mult_m2 + ".matrixIn[0]")
    mc.setAttr(mult_m2 + ".matrixIn[1]", i_m, type="matrix")
    decom_m2 = mc.createNode("decomposeMatrix")
    mc.connectAttr(mult_m2 + ".matrixSum", decom_m2 + ".inputMatrix")
    mc.connectAttr(decom_m2 + ".outputRotate", target + ".r")
