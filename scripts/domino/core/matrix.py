# maya
from maya.api import OpenMaya as om
from pymel import core as pm
from pymel import util

# domino
from domino.core import vector

dt = pm.datatypes


def transform(parent, name, m, offsetParentMatrix=False):
    obj = pm.createNode("transform", name=name, parent=parent)
    if offsetParentMatrix:
        if parent:
            m = m * parent.getMatrix(worldSpace=True).inverse()
        obj.attr("offsetParentMatrix").set(m)
    else:
        obj.setMatrix(m, worldSpace=True)
    return obj


def get_matrix_from_pos(pos):
    m = dt.Matrix()
    m[0] = [1, 0, 0, 0]
    m[1] = [0, 1, 0, 0]
    m[2] = [0, 0, 1, 0]
    m[3] = [pos[0], pos[1], pos[2], 1]
    return m


def get_matrix_look_at(pos, lookat, normal, axis="xy", negate=False):
    normal.normalize()

    if negate:
        a = pos - lookat
    else:
        a = lookat - pos

    a.normalize()
    c = util.cross(a, normal)
    c.normalize()
    b = util.cross(c, a)
    b.normalize()

    if axis == "xy":
        X = a
        Y = b
        Z = c
    elif axis == "xz":
        X = a
        Z = b
        Y = -c
    elif axis == "x-z":
        X = a
        Z = -b
        Y = c
    elif axis == "yx":
        Y = a
        X = b
        Z = -c
    elif axis == "yz":
        Y = a
        Z = b
        X = c
    elif axis == "zx":
        Z = a
        X = b
        Y = c
    elif axis == "z-x":
        Z = a
        X = -b
        Y = -c
    elif axis == "zy":
        Z = a
        Y = b
        X = -c
    elif axis == "x-y":
        X = a
        Y = -b
        Z = -c
    elif axis == "-xz":
        X = -a
        Z = b
        Y = c
    elif axis == "-xy":
        X = -a
        Y = b
        Z = c
    elif axis == "-yx":
        Y = -a
        X = b
        Z = c

    m = dt.Matrix()
    m[0] = [X[0], X[1], X[2], 0.0]
    m[1] = [Y[0], Y[1], Y[2], 0.0]
    m[2] = [Z[0], Z[1], Z[2], 0.0]
    m[3] = [pos[0], pos[1], pos[2], 1.0]

    return m


def get_chain_matrix(positions, normal, negate=False):
    transforms = []
    for i in range(len(positions) - 1):
        v0 = positions[i - 1]
        v1 = positions[i]
        v2 = positions[i + 1]

        # Normal Offset
        if i > 0:
            normal = vector.getTransposedVector(
                normal, [v0, v1], [v1, v2])
        t = get_matrix_look_at(v1, v2, normal, "xz", negate)
        transforms.append(t)
    return transforms


def get_mirror_matrix(m, axis="yz"):
    if axis == "yz":
        # mirror = dt.TransformationMatrix(
        #     1, 0, 0, 0,
        #     0, -1, 0, 0,
        #     0, 0, -1, 0,
        #     t[3][0] * -2, t[3][1] * 2, t[3][2] * 2, 1)
        mirror = dt.TransformationMatrix(
            -1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1)

    # if axis == "xy":
    #     mirror = pm.datatypes.TransformationMatrix(1, 0, 0, 0,
    #                                                0, 1, 0, 0,
    #                                                0, 0, -1, 0,
    #                                                0, 0, 0, 1)
    # if axis == "zx":
    #     mirror = pm.datatypes.TransformationMatrix(1, 0, 0, 0,
    #                                                0, -1, 0, 0,
    #                                                0, 0, 1, 0,
    #                                                0, 0, 0, 1)
    m *= mirror
    return m


def set_matrix_position(in_m, pos):
    m = dt.Matrix()
    m[0] = in_m[0]
    m[1] = in_m[1]
    m[2] = in_m[2]
    m[3] = [pos[0], pos[1], pos[2], 1.0]
    return m


def set_matrix_rotation(m, rot):
    X = rot[0]
    Y = rot[1]
    Z = rot[2]

    m = dt.Matrix(m)
    m[0] = [X[0], X[1], X[2], 0.0]
    m[1] = [Y[0], Y[1], Y[2], 0.0]
    m[2] = [Z[0], Z[1], Z[2], 0.0]
    return m


def set_matrix_scale(m, scl):
    tm = dt.TransformationMatrix(m)
    tm.setScale(scl, space="world")

    m = dt.Matrix(tm)
    return m


class OrientXYZ:

    def __init__(self, m):
        m = om.MMatrix(m)
        m = om.MTransformationMatrix(m)

        x = om.MVector(1, 0, 0).rotateBy(m.rotation())
        y = om.MVector(0, 1, 0).rotateBy(m.rotation())
        z = om.MVector(0, 0, 1).rotateBy(m.rotation())

        self.x = dt.Vector(x.x, x.y, x.z)
        self.y = dt.Vector(y.x, y.y, y.z)
        self.z = dt.Vector(z.x, z.y, z.z)


def pole_vec_position(parent, positions, multiple):
    decom0 = pm.createNode("decomposeMatrix")
    decom1 = pm.createNode("decomposeMatrix")
    decom2 = pm.createNode("decomposeMatrix")

    pm.connectAttr(positions[0].attr("worldMatrix")[0], decom0.attr("inputMatrix"))
    pm.connectAttr(positions[1].attr("worldMatrix")[0], decom1.attr("inputMatrix"))
    pm.connectAttr(positions[2].attr("worldMatrix")[0], decom2.attr("inputMatrix"))

    vec0_node = pm.createNode("plusMinusAverage")
    vec1_node = pm.createNode("plusMinusAverage")
    vec0_node.attr("operation").set(2)
    vec1_node.attr("operation").set(2)

    pm.connectAttr(decom1.attr("outputTranslate"), vec0_node.attr("input3D")[0])
    pm.connectAttr(decom0.attr("outputTranslate"), vec0_node.attr("input3D")[1])

    pm.connectAttr(decom2.attr("outputTranslate"), vec1_node.attr("input3D")[0])
    pm.connectAttr(decom0.attr("outputTranslate"), vec1_node.attr("input3D")[1])

    dot = pm.createNode("vectorProduct")
    dot.attr("operation").set(1)
    pm.connectAttr(vec1_node.attr("output3D"), dot.attr("input1"))
    pm.connectAttr(vec0_node.attr("output3D"), dot.attr("input2"))

    vec1_length = pm.createNode("distanceBetween")
    pm.connectAttr(vec1_node.attr("output3D"), vec1_length.attr("point1"))
    vec1_normalize = pm.createNode("vectorProduct")
    vec1_normalize.attr("operation").set(0)
    vec1_normalize.attr("normalizeOutput").set(1)
    pm.connectAttr(vec1_node.attr("output3D"), vec1_normalize.attr("input1"))

    divided_dot = pm.createNode("multiplyDivide")
    divided_dot.attr("operation").set(2)
    pm.connectAttr(dot.attr("output"), divided_dot.attr("input1"))
    pm.connectAttr(vec1_length.attr("distance"), divided_dot.attr("input2X"))
    pm.connectAttr(vec1_length.attr("distance"), divided_dot.attr("input2Y"))
    pm.connectAttr(vec1_length.attr("distance"), divided_dot.attr("input2Z"))

    projection_point = pm.createNode("multiplyDivide")
    projection_point.attr("operation").set(1)
    pm.connectAttr(divided_dot.attr("output"), projection_point.attr("input1"))
    pm.connectAttr(vec1_normalize.attr("output"), projection_point.attr("input2"))

    move_projection_point = pm.createNode("plusMinusAverage")
    pm.connectAttr(decom0.attr("outputTranslate"), move_projection_point.attr("input3D")[0])
    pm.connectAttr(projection_point.attr("output"), move_projection_point.attr("input3D")[1])

    projection_vec = pm.createNode("plusMinusAverage")
    projection_vec.attr("operation").set(2)
    pm.connectAttr(decom1.attr("outputTranslate"), projection_vec.attr("input3D")[0])
    pm.connectAttr(move_projection_point.attr("output3D"), projection_vec.attr("input3D")[1])

    projection_vec_normalize = pm.createNode("vectorProduct")
    projection_vec_normalize.attr("operation").set(0)
    projection_vec_normalize.attr("normalizeOutput").set(1)
    pm.connectAttr(projection_vec.attr("output3D"), projection_vec_normalize.attr("input1"))

    output_vec = pm.createNode("multiplyDivide")
    pm.connectAttr(projection_vec_normalize.attr("output"), output_vec.attr("input1"))
    pm.connectAttr(multiple, output_vec.attr("input2X"))
    pm.connectAttr(multiple, output_vec.attr("input2Y"))
    pm.connectAttr(multiple, output_vec.attr("input2Z"))

    move = pm.createNode("plusMinusAverage")
    pm.connectAttr(output_vec.attr("output"), move.attr("input3D")[0])
    pm.connectAttr(decom1.attr("outputTranslate"), move.attr("input3D")[1])

    f_b_f_matrix = pm.createNode("fourByFourMatrix")
    pm.connectAttr(move.attr("output3Dx"), f_b_f_matrix.attr("in30"))
    pm.connectAttr(move.attr("output3Dy"), f_b_f_matrix.attr("in31"))
    pm.connectAttr(move.attr("output3Dz"), f_b_f_matrix.attr("in32"))

    m_m = pm.createNode("multMatrix")
    pm.connectAttr(f_b_f_matrix.attr("output"), m_m.attr("matrixIn")[0])
    pm.connectAttr(parent.attr("worldInverseMatrix")[0], m_m.attr("matrixIn")[1])

    d_m = pm.createNode("decomposeMatrix")
    pm.connectAttr(m_m.attr("matrixSum"), d_m.attr("inputMatrix"))
    return d_m.attr("outputTranslate")


def get_pole_vec_position(positions, multiple=1):
    vec1 = positions[1] - positions[0]
    vec2 = positions[2] - positions[0]
    vec1_normal = vec1.normal()
    vec2_normal = vec2.normal()

    if vec1_normal.dot(vec2_normal) == 1.0:
        return positions[1]
    prod_factor = vec1.length() * vec1_normal.dot(vec2_normal)
    dot_pos = (vec2_normal * prod_factor) + positions[0]
    projection_vec = positions[1] - dot_pos
    return (projection_vec.normal() * multiple) + positions[1]
