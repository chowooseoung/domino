# maya
from pymel import core as pm

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
    ik_h, _ = pm.ikHandle(name=name,
                          startJoint=chain[0],
                          endEffector=chain[-1],
                          solver=solver)
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


def pole_vec_position(parent, positions, multiple):
    decom0 = pm.createNode("decomposeMatrix")
    decom1 = pm.createNode("decomposeMatrix")
    decom2 = pm.createNode("decomposeMatrix")

    pm.connectAttr(positions[0].attr("worldMatrix")[0],
                   decom0.attr("inputMatrix"))
    pm.connectAttr(positions[1].attr("worldMatrix")[0],
                   decom1.attr("inputMatrix"))
    pm.connectAttr(positions[2].attr("worldMatrix")[0],
                   decom2.attr("inputMatrix"))

    vec0_node = pm.createNode("plusMinusAverage")
    vec1_node = pm.createNode("plusMinusAverage")
    vec0_node.attr("operation").set(2)
    vec1_node.attr("operation").set(2)

    pm.connectAttr(decom1.attr("outputTranslate"),
                   vec0_node.attr("input3D")[0])
    pm.connectAttr(decom0.attr("outputTranslate"),
                   vec0_node.attr("input3D")[1])

    pm.connectAttr(decom2.attr("outputTranslate"),
                   vec1_node.attr("input3D")[0])
    pm.connectAttr(decom0.attr("outputTranslate"),
                   vec1_node.attr("input3D")[1])

    dot = pm.createNode("vectorProduct")
    dot.attr("operation").set(1)
    pm.connectAttr(vec1_node.attr("output3D"),
                   dot.attr("input1"))
    pm.connectAttr(vec0_node.attr("output3D"),
                   dot.attr("input2"))

    vec1_length = pm.createNode("distanceBetween")
    pm.connectAttr(vec1_node.attr("output3D"),
                   vec1_length.attr("point1"))
    vec1_normalize = pm.createNode("vectorProduct")
    vec1_normalize.attr("operation").set(0)
    vec1_normalize.attr("normalizeOutput").set(1)
    pm.connectAttr(vec1_node.attr("output3D"),
                   vec1_normalize.attr("input1"))

    divided_dot = pm.createNode("multiplyDivide")
    divided_dot.attr("operation").set(2)
    pm.connectAttr(dot.attr("output"), divided_dot.attr("input1"))
    pm.connectAttr(vec1_length.attr("distance"),
                   divided_dot.attr("input2X"))
    pm.connectAttr(vec1_length.attr("distance"),
                   divided_dot.attr("input2Y"))
    pm.connectAttr(vec1_length.attr("distance"),
                   divided_dot.attr("input2Z"))

    projection_point = pm.createNode("multiplyDivide")
    projection_point.attr("operation").set(1)
    pm.connectAttr(divided_dot.attr("output"),
                   projection_point.attr("input1"))
    pm.connectAttr(vec1_normalize.attr("output"),
                   projection_point.attr("input2"))

    move_projection_point = pm.createNode("plusMinusAverage")
    pm.connectAttr(decom0.attr("outputTranslate"),
                   move_projection_point.attr("input3D")[0])
    pm.connectAttr(projection_point.attr("output"),
                   move_projection_point.attr("input3D")[1])

    projection_vec = pm.createNode("plusMinusAverage")
    projection_vec.attr("operation").set(2)
    pm.connectAttr(decom1.attr("outputTranslate"),
                   projection_vec.attr("input3D")[0])
    pm.connectAttr(move_projection_point.attr("output3D"),
                   projection_vec.attr("input3D")[1])

    projection_vec_normalize = pm.createNode("vectorProduct")
    projection_vec_normalize.attr("operation").set(0)
    projection_vec_normalize.attr("normalizeOutput").set(1)
    pm.connectAttr(projection_vec.attr("output3D"),
                   projection_vec_normalize.attr("input1"))

    output_vec = pm.createNode("multiplyDivide")
    pm.connectAttr(projection_vec_normalize.attr("output"),
                   output_vec.attr("input1"))
    pm.connectAttr(multiple, output_vec.attr("input2X"))
    pm.connectAttr(multiple, output_vec.attr("input2Y"))
    pm.connectAttr(multiple, output_vec.attr("input2Z"))

    move = pm.createNode("plusMinusAverage")
    pm.connectAttr(output_vec.attr("output"),
                   move.attr("input3D")[0])
    pm.connectAttr(decom1.attr("outputTranslate"),
                   move.attr("input3D")[1])

    f_b_f_matrix = pm.createNode("fourByFourMatrix")
    pm.connectAttr(move.attr("output3Dx"),
                   f_b_f_matrix.attr("in30"))
    pm.connectAttr(move.attr("output3Dy"),
                   f_b_f_matrix.attr("in31"))
    pm.connectAttr(move.attr("output3Dz"),
                   f_b_f_matrix.attr("in32"))

    m_m = pm.createNode("multMatrix")
    pm.connectAttr(f_b_f_matrix.attr("output"),
                   m_m.attr("matrixIn")[0])
    pm.connectAttr(parent.attr("worldInverseMatrix")[0],
                   m_m.attr("matrixIn")[1])

    d_m = pm.createNode("decomposeMatrix")
    pm.connectAttr(m_m.attr("matrixSum"),
                   d_m.attr("inputMatrix"))
    return d_m.attr("outputTranslate")


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
