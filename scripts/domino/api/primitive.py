# maya
from pymel import core as pm

# domino
from . import matrix


def empty(parent, name, m):
    node = pm.group(name=name, empty=True)
    node.setMatrix(m, worldSpace=True)
    if parent:
        pm.parent(node, parent)
    return node.name()


def empty_by_pos(parent, name, pos):
    node = pm.group(name=name, empty=True)
    node.setTranslation(pos, space="world")
    if parent:
        pm.parent(node, parent)
    return node.name()


def locator(parent, name, m, size=1):
    node = pm.spaceLocator(name=name)
    node.setMatrix(m, worldSpace=True)
    node.setAttr("localScale", size, size, size)
    if parent:
        pm.parent(node, parent)
    return node.name()


def locator_by_pos(parent, name, pos, size=1):
    node = pm.spaceLocator(name=name)
    node.setTranslation(pos, space="world")
    node.setAttr("localScale", size, size, size)
    if parent:
        pm.parent(node, parent)
    return node.name()


def joint(parent, name, m, radius=0.5):
    node = pm.createNode("joint", name=name)
    node.setMatrix(m, worldSpace=True)
    node.setAttr("radius", radius)
    if parent:
        pm.parent(node, parent)
    return node.name()


def joint_by_pos(parent, name, pos, radius=0.5):
    node = pm.createNode("joint", name=name)
    node.setTranslation(pos, space="world")
    node.setAttr("radius", radius)
    if parent:
        pm.parent(node, parent)
    return node.name()


def joint_2d_chain(parent, name, positions, normal, negate=False, radius=0.5):
    if "%s" not in name:
        name += "%s"

    transforms = matrix.get_chain_matrix(positions, normal, negate)
    t = matrix.setMatrixPosition(transforms[-1], positions[-1])
    transforms.append(t)

    chain = []
    for i, t in enumerate(transforms):
        node = joint(parent, name % i, t, radius)
        chain.append(node)
        parent = node

    # moving rotation value to joint orient
    for i, jnt in enumerate(chain):
        if i == 0:
            jnt.setAttr("jointOrient", jnt.getAttr("rotate"))
            jnt.setAttr("rotate", 0, 0, 0)
        elif i == len(chain) - 1:
            jnt.setAttr("jointOrient", 0, 0, 0)
            jnt.setAttr("rotate", 0, 0, 0)
        else:
            # This will fail if chain is not always oriented the same
            # way (like X chain)
            v0 = positions[i] - positions[i - 1]
            v1 = positions[i + 1] - positions[i]
            angle = pm.datatypes.degrees(v0.angle(v1))
            jnt.setAttr("rotate", 0, 0, 0)
            jnt.setAttr("jointOrient", 0, 0, angle)

        # check if we have to negate Z angle by comparing the guide
        # position and the resulting position.
        if i >= 1:
            # round the position values to 6 decimals precission
            # TODO: test with less precision and new check after apply
            # Ik solver
            if ([round(elem, 4) for elem in matrix.getTranslation(jnt)]
                    != [round(elem, 4) for elem in positions[i]]):

                jp = jnt.getParent()

                # Aviod intermediate e.g. `transform3` groups that can appear
                # between joints due to basic moving around.
                while jp.type() == "transform":
                    jp = jp.getParent()

                jp.setAttr(
                    "jointOrient", 0, 0, jp.attr("jointOrient").get()[2] * -1)
    return chain


def ik_handle(parent, name, solver, pole_vector):
    pass


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
