# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# domino
from . import vector

# built-ins
import math


def transform(parent, name, m, offset_parent_matrix=False):
    node = mc.createNode("transform", name=name, parent=parent)
    set_matrix(node, m, world_space=True, offset_parent_matrix=offset_parent_matrix)
    return node


def get_matrix(node, world_space=True, offset_parent_matrix=False):
    if offset_parent_matrix:
        return om2.MMatrix(mc.getAttr(node + ".offsetParentMatrix"))
    return om2.MMatrix(mc.xform(node, query=True, matrix=True, worldSpace=world_space))


def set_matrix(node, m, world_space=True, offset_parent_matrix=False):
    if not isinstance(m, om2.MMatrix):
        m = om2.MMatrix(m)
    if offset_parent_matrix:
        if world_space:
            parent_inv_m = om2.MMatrix(mc.getAttr(node + ".parentInverseMatrix"))
            m = m * parent_inv_m
        mc.setAttr(node + ".offsetParentMatrix", m, type="matrix")
    else:
        mc.xform(node, matrix=m, worldSpace=world_space)


def get_look_at_matrix(pos, lookat, normal, axis="xy", negate=False):
    pos, lookat, normal = [om2.MVector(x) for x in (pos, lookat, normal)]
    normal = normal.normalize()

    if negate:
        a = pos - lookat
    else:
        a = lookat - pos

    a = a.normalize()
    c = a ^ normal
    c = c.normalize()
    b = c ^ a
    b = b.normalize()

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

    m = []
    m.extend([X[0], X[1], X[2], 0.0])
    m.extend([Y[0], Y[1], Y[2], 0.0])
    m.extend([Z[0], Z[1], Z[2], 0.0])
    m.extend([pos[0], pos[1], pos[2], 1.0])
    return om2.MMatrix(m)


def get_chain_matrix(positions, normal, negate=False):
    transforms = []
    for i in range(len(positions) - 1):
        v0 = positions[i - 1]
        v1 = positions[i]
        v2 = positions[i + 1]

        # Normal Offset
        if i > 0:
            normal = vector.get_transposed_vector(
                normal, [v0, v1], [v1, v2])
        t = get_look_at_matrix(v1, v2, normal, "xz", negate)
        transforms.append(t)
    return transforms


def get_chain_matrix2(positions, normal, negate=False):
    transforms = []
    for i in range(len(positions)):
        if i == len(positions) - 1:
            v0 = positions[i - 1]
            v1 = positions[i]
            v2 = positions[i - 2]

        else:
            v0 = positions[i - 1]
            v1 = positions[i]
            v2 = positions[i + 1]

        # Normal Offset
        if i > 0 and i != len(positions) - 1:
            normal = vector.get_transposed_vector(
                normal, [v0, v1], [v1, v2])

        if i == len(positions) - 1:
            t = get_look_at_matrix(v1, v0, normal, "-xz", negate)
        else:
            t = get_look_at_matrix(v1, v2, normal, "xz", negate)
        transforms.append(t)

    return transforms


def get_mirror_matrix(m):
    if not isinstance(m, om2.MMatrix):
        m = om2.MMatrix(m)
    mirror = om2.MMatrix([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]
    )
    return m * mirror


def set_matrix_translate(m, t):
    if not isinstance(m, om2.MTransformationMatrix):
        m = om2.MTransformationMatrix(om2.MMatrix(m))
    m.setTranslation(om2.MVector(t), om2.MSpace.kWorld)
    return m.asMatrix()


def set_matrix_rotate(m, r):
    if not isinstance(m, om2.MTransformationMatrix):
        m = om2.MTransformationMatrix(om2.MMatrix(m))
    if not isinstance(r, om2.MTransformationMatrix):
        r = om2.MTransformationMatrix(om2.MMatrix(r))
    m.setRotation(om2.MEulerRotation(r.rotation()))
    return m.asMatrix()


def set_matrix_rotate2(m, r):
    if not isinstance(m, om2.MTransformationMatrix):
        m = om2.MTransformationMatrix(om2.MMatrix(m))
    m.setRotation(om2.MEulerRotation([math.radians(x) for x in r]))
    return m.asMatrix()

def set_matrix_scale(m, s):
    if not isinstance(m, om2.MTransformationMatrix):
        m = om2.MTransformationMatrix(om2.MMatrix(m))
    m.setScale(om2.MVector(s), om2.MSpace.kWorld)
    return m.asMatrix()
