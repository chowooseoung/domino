# maya
from pymel import core as pm
from maya import cmds as mc

# domino
from domino.core import matrix

dt = pm.datatypes


def add(parent=None, name="", m=dt.Matrix(), radius=0.5, vis=True):
    j = pm.createNode("joint", name=name, parent=parent)
    j.setMatrix(m, worldSpace=True)
    pm.setAttr(j.attr("radius"), radius)
    pm.setAttr(j.attr("segmentScaleCompensate"), False)
    pm.setAttr(j.attr("jointOrient"), j.attr("r").get())
    pm.setAttr(j.attr("r"), (0, 0, 0))
    pm.disconnectAttr(j.attr("inverseScale"))
    if not vis:
        j.attr("drawStyle").set(2)
    return j


def add_chain(parent, name, positions, normal, last_orient=None, negate=False, vis=False):
    if "%s" not in name:
        name += "%s"

    chain_matrix = matrix.get_chain_matrix(positions, normal, negate)
    m = matrix.set_matrix_position(chain_matrix[-1], positions[-1])
    if last_orient:
        m = matrix.set_matrix_rotation(m, last_orient)
    chain_matrix.append(m)

    chain = []
    for i, m in enumerate(chain_matrix):
        jnt = add(parent, name % i, m, 1, vis)
        chain.append(jnt)
        parent = jnt

    return chain


def ikh(parent, name, chain, solver="ikRPsolver", pole_vector=None):
    ik_h, _ = mc.ikHandle(name=name,
                          startJoint=chain[0].strip(),
                          endEffector=chain[-1].strip(),
                          solver=solver)
    ik_h = pm.PyNode(ik_h)
    pm.setAttr(f"{ik_h}.v", 0)

    if parent:
        pm.parent(ik_h, parent)

    if pole_vector:
        pm.poleVectorConstraint(pole_vector, ik_h)
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
    ik_h = pm.ikHandle(**argument)[0]
    pm.setAttr(f"{ik_h}.v", 0)
    if parent:
        pm.parent(ik_h, parent)
    return ik_h


def labeling(jnt, name, side, index, description):
    if side == "C":
        pm.setAttr(jnt.attr("side"), 0)
    if side == "L":
        pm.setAttr(jnt.attr("side"), 1)
    if side == "R":
        pm.setAttr(jnt.attr("side"), 2)
    pm.setAttr(jnt.attr("type"), 18)
    if side is None and index is None:
        label = name
    else:
        label = f"{'S' if side in ['L', 'R'] else side}{index}_{name}"
    if description:
        label += f"_{description}"

    pm.setAttr(jnt.attr("otherType"), label, type="string")


def connect_space(source, target):
    mult_m = pm.createNode("multMatrix")
    pm.connectAttr(source.attr("worldMatrix")[0], mult_m.attr("matrixIn")[0])
    pm.connectAttr(target.attr("parentInverseMatrix"), mult_m.attr("matrixIn")[1])

    decom_m = pm.createNode("decomposeMatrix")
    pm.connectAttr(mult_m.attr("matrixSum"), decom_m.attr("inputMatrix"))
    pm.connectAttr(decom_m.attr("outputTranslate"), target.attr("t"))
    if decom_m.attr("outputScaleZ").get() < 0:
        md = pm.createNode("multiplyDivide")
        pm.connectAttr(decom_m.attr("outputScale"), md.attr("input1"))
        md.attr("input2").set(1, 1, -1)
        pm.connectAttr(md.attr("output"), target.attr("s"))
    else:
        pm.connectAttr(decom_m.attr("outputScale"), target.attr("s"))
    pm.connectAttr(decom_m.attr("outputShear"), target.attr("shear"))

    if pm.nodeType(target) == "transform":
        pm.connectAttr(decom_m.attr("outputRotate"), target.attr("r"))
        return 0

    m = mult_m.attr("matrixSum").get()
    i_m = m.inverse()

    tm = dt.TransformationMatrix(m)
    j_orient = dt.degrees(tm.getRotation())

    target.attr("jointOrient").set(j_orient)

    mult_m2 = pm.createNode("multMatrix")
    pm.connectAttr(mult_m.attr("matrixSum"), mult_m2.attr("matrixIn")[0])
    mult_m2.attr("matrixIn")[1].set(i_m)
    decom_m2 = pm.createNode("decomposeMatrix")
    pm.connectAttr(mult_m2.attr("matrixSum"), decom_m2.attr("inputMatrix"))
    pm.connectAttr(decom_m2.attr("outputRotate"), target.attr("r"))
