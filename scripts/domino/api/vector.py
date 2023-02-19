# maya
from maya import OpenMaya as om2
from pymel import core as pm

# built-ins
import math

dt = pm.datatypes


def getPlaneNormal(v0, v1, v2):
    """Get the normal vector of a plane (Defined by 3 positions).
    Arguments:
        v0 (vector): First position on the plane.
        v1 (vector): Second position on the plane.
        v2 (vector): Third position on the plane.
    Returns:
        vector: The normal.
    """
    vector0 = v1 - v0
    vector1 = v2 - v0
    vector0.normalize()
    vector1.normalize()

    normal = vector1 ^ vector0
    normal.normalize()

    return normal


def getPlaneBiNormal(v0, v1, v2):
    """Get the binormal vector of a plane (Defined by 3 positions).
    Arguments:
        v0 (vector): First position on the plane.
        v1 (vector): Second position on the plane.
        v2 (vector): Third position on the plane.
    Returns:
        vector: The binormal.
    """
    normal = getPlaneNormal(v0, v1, v2)

    vector0 = v1 - v0

    binormal = normal ^ vector0
    binormal.normalize()

    return binormal


def get_distance(v1, v2):
    return (v2 - v1).length()


def getTransposedVector(v, position0, position1, inverse=False):
    """Get the transposed vector.
    Arguments:
        v (vector): Input Vector.
        position0 (vector): Position A.
        position1 (vector): Position B.
        inverse (bool): Invert the rotation.
    Returns:
        vector: The transposed vector.
    >>> normal = vec.getTransposedVector(self.normal,
                                         [self.guide.apos[0],
                                          self.guide.apos[1]],
                                         [self.guide.apos[-2],
                                          self.guide.apos[-1]])
    """
    v0 = position0[1] - position0[0]
    v0.normalize()

    v1 = position1[1] - position1[0]
    v1.normalize()

    ra = v0.angle(v1)

    if inverse:
        ra = -ra

    axis = v0 ^ v1

    vector = rotateAlongAxis(v, axis, ra)

    # Check if the rotation has been set in the right order
    # ra2 = (math.pi *.5 ) - v1.angle(vector)
    # vector = rotateAlongAxis(v, axis, -ra2)

    return vector


def rotateAlongAxis(v, axis, a):
    """Rotate a vector around a given axis defined by other vector.
    Arguments:
        v (vector): The vector to rotate.
        axis (vector): The axis to rotate around.
        a (float): The rotation angle in radians.
    """
    sa = math.sin(a / 2.0)
    ca = math.cos(a / 2.0)

    q1 = om2.MQuaternion(v.x, v.y, v.z, 0)
    q2 = om2.MQuaternion(axis.x * sa, axis.y * sa, axis.z * sa, ca)
    q2n = om2.MQuaternion(-axis.x * sa, -axis.y * sa, -axis.z * sa, ca)
    q = q2 * q1
    q *= q2n

    out = om2.MVector(q.x, q.y, q.z)

    return out
