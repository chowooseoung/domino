# maya
from maya.api import OpenMaya as om
from pymel import core as pm
from pymel import util

# domino
from . import vector

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
