# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# built-ins
import math

# domino
from domino.lib import hierarchy


def get_distance(v0, v1):
    return (om2.MVector(v1) - om2.MVector(v0)).length()


def get_position(node, world_space=True):
    return mc.xform(node, query=True, translation=True, worldSpace=world_space)


def get_rotation(node, world_space=True):
    return mc.xform(node, query=True, rotation=True, worldSpace=world_space)


def get_scale(node, world_space=True):
    return mc.xform(node, query=True, scale=True, worldSpace=world_space)


def get_average_position(vertices):
    sum_position = om2.MVector((0, 0, 0))
    for vtx in vertices:
        sum_position += om2.MVector(mc.xform(vtx, query=True, translation=True, worldSpace=True))
    return sum_position / len(vertices)


def get_plane_normal(p0, p1, p2):
    p0, p1, p2 = [om2.MVector(p) for p in [p0, p1, p2]]
    vector0 = p1 - p0
    vector1 = p2 - p0
    vector0.normalize()
    vector1.normalize()

    normal = vector1 ^ vector0
    normal.normalize()

    return normal


def get_plane_bi_normal(p0, p1, p2):
    p0, p1, p2 = [om2.MVector(p) for p in [p0, p1, p2]]
    normal = get_plane_normal(p0, p1, p2)

    vector0 = p1 - p0

    binormal = normal ^ vector0
    binormal.normalize()

    return binormal


def get_transposed_vector(v, position0, position1, inverse=False):
    v = om2.MVector(v)
    position0 = [om2.MVector(p) for p in position0]
    position1 = [om2.MVector(p) for p in position1]

    v0 = position0[1] - position0[0]
    v0.normalize()

    v1 = position1[1] - position1[0]
    v1.normalize()

    ra = v0.angle(v1)

    if inverse:
        ra = -ra

    axis = v0 ^ v1

    return rotate_along_axis(v, axis, ra)


def rotate_along_axis(v, axis, a):
    # https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion
    sa = math.sin(a / 2.0)
    ca = math.cos(a / 2.0)

    q1 = om2.MQuaternion(v.x, v.y, v.z, 0)
    q2 = om2.MQuaternion(axis.x * sa, axis.y * sa, axis.z * sa, ca)
    q2n = om2.MQuaternion(-axis.x * sa, -axis.y * sa, -axis.z * sa, ca)
    q = q2 * q1
    q *= q2n

    return om2.MVector(q.x, q.y, q.z)


def calculate_pole_vector(node0, node1, node2, pole_distance=1):
    vec0 = om2.MVector(get_position(node0))
    vec1 = om2.MVector(get_position(node1))
    vec2 = om2.MVector(get_position(node2))

    v1_v0 = vec1 - vec0
    v2_v0 = vec2 - vec0
    v1_v0_normal = v1_v0.normal()
    v2_v0_normal = v2_v0.normal()

    dot_value = v1_v0.length() * (v1_v0_normal * v2_v0_normal)
    proj_vec = v2_v0_normal * dot_value + vec0

    v1_proj = vec1 - proj_vec

    return (v1_proj.normal() * pole_distance) + vec1


def set_pole_vector(pole_vec_node, source_nodes, pole_distance_attr):
    decom0 = mc.createNode("decomposeMatrix")
    decom1 = mc.createNode("decomposeMatrix")
    decom2 = mc.createNode("decomposeMatrix")

    mc.connectAttr(source_nodes[0] + ".worldMatrix[0]", decom0 + ".inputMatrix")
    mc.connectAttr(source_nodes[1] + ".worldMatrix[0]", decom1 + ".inputMatrix")
    mc.connectAttr(source_nodes[2] + ".worldMatrix[0]", decom2 + ".inputMatrix")

    vec0_node = mc.createNode("plusMinusAverage")
    vec1_node = mc.createNode("plusMinusAverage")
    mc.setAttr(vec0_node + ".operation", 2)
    mc.setAttr(vec1_node + ".operation", 2)

    mc.connectAttr(decom1 + ".outputTranslate", vec0_node + ".input3D[0]")
    mc.connectAttr(decom0 + ".outputTranslate", vec0_node + ".input3D[1]")

    mc.connectAttr(decom2 + ".outputTranslate", vec1_node + ".input3D[0]")
    mc.connectAttr(decom0 + ".outputTranslate", vec1_node + ".input3D[1]")

    dot = mc.createNode("vectorProduct")
    mc.setAttr(dot + ".operation", 1)
    mc.connectAttr(vec1_node + ".output3D", dot + ".input1")
    mc.connectAttr(vec0_node + ".output3D", dot + ".input2")

    vec1_length = mc.createNode("distanceBetween")
    mc.connectAttr(vec1_node + ".output3D", vec1_length + ".point1")
    vec1_normalize = mc.createNode("vectorProduct")
    mc.setAttr(vec1_normalize + ".operation", 0)
    mc.setAttr(vec1_normalize + ".normalizeOutput", 1)
    mc.connectAttr(vec1_node + ".output3D", vec1_normalize + ".input1")

    divided_dot = mc.createNode("multiplyDivide")
    mc.setAttr(divided_dot + ".operation", 2)
    mc.connectAttr(dot + ".output", divided_dot + ".input1")
    mc.connectAttr(vec1_length + ".distance", divided_dot + ".input2X")
    mc.connectAttr(vec1_length + ".distance", divided_dot + ".input2Y")
    mc.connectAttr(vec1_length + ".distance", divided_dot + ".input2Z")

    projection_point = mc.createNode("multiplyDivide")
    mc.setAttr(projection_point + ".operation", 1)
    mc.connectAttr(divided_dot + ".output", projection_point + ".input1")
    mc.connectAttr(vec1_normalize + ".output", projection_point + ".input2")

    move_projection_point = mc.createNode("plusMinusAverage")
    mc.connectAttr(decom0 + ".outputTranslate", move_projection_point + ".input3D[0]")
    mc.connectAttr(projection_point + ".output", move_projection_point + ".input3D[1]")

    projection_vec = mc.createNode("plusMinusAverage")
    mc.setAttr(projection_vec + ".operation", 2)
    mc.connectAttr(decom1 + ".outputTranslate", projection_vec + ".input3D[0]")
    mc.connectAttr(move_projection_point + ".output3D", projection_vec + ".input3D[1]")

    projection_vec_normalize = mc.createNode("vectorProduct")
    mc.setAttr(projection_vec_normalize + ".operation", 0)
    mc.setAttr(projection_vec_normalize + ".normalizeOutput", 1)
    mc.connectAttr(projection_vec + ".output3D", projection_vec_normalize + ".input1")

    output_vec = mc.createNode("multiplyDivide")
    mc.connectAttr(projection_vec_normalize + ".output", output_vec + ".input1")
    mc.connectAttr(pole_distance_attr, output_vec + ".input2X")
    mc.connectAttr(pole_distance_attr, output_vec + ".input2Y")
    mc.connectAttr(pole_distance_attr, output_vec + ".input2Z")

    move = mc.createNode("plusMinusAverage")
    mc.connectAttr(output_vec + ".output", move + ".input3D[0]")
    mc.connectAttr(decom1 + ".outputTranslate", move + ".input3D[1]")

    f_b_f_matrix = mc.createNode("fourByFourMatrix")
    mc.connectAttr(move + ".output3Dx", f_b_f_matrix + ".in30")
    mc.connectAttr(move + ".output3Dy", f_b_f_matrix + ".in31")
    mc.connectAttr(move + ".output3Dz", f_b_f_matrix + ".in32")

    parent = hierarchy.get_parent(pole_vec_node)
    m_m = mc.createNode("multMatrix")
    mc.connectAttr(f_b_f_matrix + ".output", m_m + ".matrixIn[0]")
    mc.connectAttr(parent + ".worldInverseMatrix[0]", m_m + ".matrixIn[1]")

    d_m = mc.createNode("decomposeMatrix")
    mc.connectAttr(m_m + ".matrixSum", d_m + ".inputMatrix")
    mc.connectAttr(d_m + ".outputTranslate", pole_vec_node + ".t")


class OrientXYZ:

    def __init__(self, m):
        m = om2.MMatrix(m)
        m = om2.MTransformationMatrix(m)

        x = om2.MVector(1, 0, 0).rotateBy(m.rotation())
        y = om2.MVector(0, 1, 0).rotateBy(m.rotation())
        z = om2.MVector(0, 0, 1).rotateBy(m.rotation())

        self.x = om2.MVector(x.x, x.y, x.z)
        self.y = om2.MVector(y.x, y.y, y.z)
        self.z = om2.MVector(z.x, z.y, z.z)
