# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# domino
from . import matrix
from .color import RED, GREEN, BLUE


def create(parent, name, shape, color, m, **kwargs):
    if shape == "cube":
        return cube(parent=parent,
                    name=name,
                    color=color,
                    thickness=kwargs["thickness"],
                    width=kwargs["width"],
                    height=kwargs["height"],
                    depth=kwargs["depth"],
                    m=m,
                    po=kwargs["po"],
                    ro=kwargs["ro"])
    elif shape == "cylinder":
        return cylinder(parent=parent,
                        name=name,
                        color=color,
                        thickness=kwargs["thickness"],
                        width=kwargs["width"],
                        height=kwargs["height"],
                        m=m,
                        po=kwargs["po"],
                        ro=kwargs["ro"])
    elif shape == "halfmoon":
        return halfmoon(parent=parent,
                        name=name,
                        color=color,
                        m=m,
                        thickness=kwargs["thickness"],
                        width=kwargs["width"],
                        po=kwargs["po"],
                        ro=kwargs["ro"])
    elif shape == "half_circle":
        return half_circle(parent=parent,
                           name=name,
                           color=color,
                           m=m,
                           thickness=kwargs["thickness"],
                           width=kwargs["width"],
                           po=kwargs["po"],
                           ro=kwargs["ro"])
    elif shape == "circle":
        return circle(parent=parent,
                      name=name,
                      color=color,
                      m=m,
                      thickness=kwargs["thickness"],
                      width=kwargs["width"],
                      po=kwargs["po"],
                      ro=kwargs["ro"])
    elif shape == "circle3":
        return circle3(parent=parent,
                       name=name,
                       color=color,
                       m=m,
                       thickness=kwargs["thickness"],
                       width=kwargs["width"],
                       po=kwargs["po"],
                       ro=kwargs["ro"])
    elif shape == "locator":
        return locator(parent=parent,
                       name=name,
                       color=color,
                       m=m,
                       thickness=kwargs["thickness"],
                       width=kwargs["width"],
                       po=kwargs["po"],
                       ro=kwargs["ro"])
    elif shape == "wave":
        return wave(parent=parent,
                    name=name,
                    color=color,
                    m=m,
                    thickness=kwargs["thickness"],
                    width=kwargs["width"],
                    po=kwargs["po"],
                    ro=kwargs["ro"])
    elif shape == "square":
        return square(parent=parent,
                      name=name,
                      color=color,
                      m=m,
                      thickness=kwargs["thickness"],
                      width=kwargs["width"],
                      height=kwargs["height"],
                      up=kwargs["up"],
                      po=kwargs["po"],
                      ro=kwargs["ro"])
    elif shape == "origin":
        return origin(parent=parent,
                      name=name,
                      color=color,
                      m=m,
                      thickness=kwargs["thickness"],
                      width=kwargs["width"],
                      po=kwargs["po"],
                      ro=kwargs["ro"])
    elif shape == "host":
        return host(parent=parent,
                    name=name,
                    color=color,
                    m=m,
                    thickness=kwargs["thickness"],
                    width=kwargs["width"],
                    po=kwargs["po"],
                    ro=kwargs["ro"])
    elif shape == "arrow":
        return arrow(parent=parent,
                     name=name,
                     color=color,
                     m=m,
                     thickness=kwargs["thickness"],
                     width=kwargs["width"],
                     po=kwargs["po"],
                     ro=kwargs["ro"])
    elif shape == "arrow4":
        return arrow4(parent=parent,
                      name=name,
                      color=color,
                      m=m,
                      thickness=kwargs["thickness"],
                      width=kwargs["width"],
                      po=kwargs["po"],
                      ro=kwargs["ro"])
    elif shape == "x":
        return x(parent=parent,
                 name=name,
                 color=color,
                 m=m,
                 thickness=kwargs["thickness"],
                 width=kwargs["width"],
                 height=kwargs["height"],
                 depth=kwargs["depth"],
                 po=kwargs["po"],
                 ro=kwargs["ro"])
    elif shape == "angle":
        return angle(parent=parent,
                     name=name,
                     color=color,
                     m=m,
                     thickness=kwargs["thickness"],
                     width=kwargs["width"],
                     height=kwargs["height"],
                     po=kwargs["po"],
                     ro=kwargs["ro"])
    elif shape == "dodecahedron":
        return dodecahedron(parent=parent,
                            name=name,
                            color=color,
                            m=m,
                            thickness=kwargs["thickness"],
                            width=kwargs["width"],
                            height=kwargs["height"],
                            depth=kwargs["depth"],
                            po=kwargs["po"],
                            ro=kwargs["ro"])
    elif shape == "axis":
        return axis(parent=parent,
                    name=name,
                    m=m,
                    width=kwargs["width"],
                    height=kwargs["height"],
                    depth=kwargs["depth"],
                    po=kwargs["po"],
                    ro=kwargs["ro"])

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)
    return node


def replace(source, target):
    shapes = mc.listRelatives(source, shapes=True, fullPath=True)
    mc.delete(mc.listRelatives(target, shapes=True, fullPath=True))
    shapes = mc.parent(shapes, target, relative=True, shape=True)
    [mc.rename(shape, target + "Shape") for shape in shapes]


def generate(node, points, degree, color, close=False, thickness=1, po=(0, 0, 0), ro=(0, 0, 0)):
    if close:
        points.extend(points[:degree])
        knots = range(len(points) + degree - 1)
        curve = mc.curve(point=points, degree=degree, per=close, k=knots)
    else:
        curve = mc.curve(point=points, degree=degree)
    mc.setAttr(curve + ".t", *po)
    mc.setAttr(curve + ".r", *ro)
    mc.makeIdentity(curve, apply=True, translate=True, rotate=True)
    shape = mc.rename(mc.listRelatives(curve, shapes=True)[0], node + "Shape")
    shape = mc.parent(shape, node, relative=True, shape=True)[0]
    mc.delete(curve)

    if color:
        mc.setAttr(shape + ".overrideEnabled", True)
    if isinstance(color, int):
        mc.setAttr(shape + ".overrideRGBColors", 0)
        mc.setAttr(shape + ".overrideColor", color)
    elif isinstance(color, (list, tuple, om2.MColor)):
        mc.setAttr(shape + ".overrideRGBColors", 1)
        mc.setAttr(shape + ".overrideColorRGB", *color)
    mc.setAttr(shape + ".lineWidth", thickness)
    mc.setAttr(shape + ".isHistoricallyInteresting", 0)


def origin(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = om2.MVector(0, 0, -dlen * 1.108) * width
    v1 = om2.MVector(dlen * .78, 0, -dlen * .78) * width
    v2 = om2.MVector(dlen * 1.108, 0, 0) * width
    v3 = om2.MVector(dlen * .78, 0, dlen * .78) * width
    v4 = om2.MVector(0, 0, dlen * 1.108) * width
    v5 = om2.MVector(-dlen * .78, 0, dlen * .78) * width
    v6 = om2.MVector(-dlen * 1.108, 0, 0) * width
    v7 = om2.MVector(-dlen * .78, 0, -dlen * .78) * width

    v8 = om2.MVector(dlen - 0.01, 0, 0) * width
    v9 = om2.MVector(dlen + 0.01, 0, 0) * width
    v10 = om2.MVector(0, 0, dlen - 0.01) * width
    v11 = om2.MVector(0, 0, dlen + 0.01) * width
    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)
    mc.setAttr(node + ".displayRotatePivot", True)
    mc.setAttr(node + ".overrideEnabled", True)
    mc.setAttr(node + ".overrideRGBColors", 0)
    mc.setAttr(node + ".overrideColor", 16)

    generate(node=node,
             points=[v0, v1, v2, v3, v4, v5, v6, v7],
             degree=3,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    generate(node=node,
             points=[v8, v9],
             degree=1,
             color=RED,
             thickness=5,
             po=po,
             ro=ro)
    generate(node=node,
             points=[v10, v11],
             degree=1,
             color=BLUE,
             thickness=5,
             po=po,
             ro=ro)
    return node


def host(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    points1 = [[-0.3535, 0.0, -0.3535],
               [-0.3535, 0.0, 0.3535],
               [0.3535, 0.0, 0.3535],
               [0.3535, 0.0, -0.3535],
               [-0.3535, 0.0, -0.3535]]
    points2 = [[-0.499925, 0.0, 0.0],
               [0.0, 0.0, 0.499925],
               [0.499925, 0.0, -0.0],
               [-0.0, 0.0, -0.499925],
               [-0.499925, 0.0, 0.0]]
    points3 = [[0.244906, 0.0, -0.244906],
               [0.0, 0.0, -0.34635],
               [-0.244906, 0.0, -0.244906],
               [-0.34635, 0.0, -0.0],
               [-0.244906, -0.0, 0.244906],
               [-0.0, -0.0, 0.34635],
               [0.244906, -0.0, 0.244906],
               [0.34635, -0.0, 0.0]]
    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    generate(node=node,
             points=[om2.MVector(x) * width for x in points1],
             degree=1,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    generate(node=node,
             points=[om2.MVector(x) * width for x in points2],
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    generate(node=node,
             points=[om2.MVector(x) * width for x in points3],
             close=True,
             degree=3,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def arrow(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    points = [(-0.0, 0.0, -0.5),
              (0.5, 0.0, 0.0),
              (-0.0, 0.0, 0.5),
              (0.0, 0.0, 0.211),
              (-0.5, 0.0, 0.211),
              (-0.5, 0.0, -0.211),
              (0.0, 0.0, -0.211),
              (-0.0, 0.0, -0.5)]

    points = [om2.MVector(x) * width for x in points]

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    generate(node=node,
             points=points,
             degree=1,
             close=True,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def arrow4(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    points = [[-0.1, 0.0, -0.3],
              [-0.2, 0.0, -0.3],
              [0.0, 0.0, -0.5],
              [0.2, 0.0, -0.3],
              [0.1, 0.0, -0.3],
              [0.1, 0.0, -0.1],
              [0.3, 0.0, -0.1],
              [0.3, 0.0, -0.2],
              [0.5, 0.0, 0.0],
              [0.3, 0.0, 0.2],
              [0.3, 0.0, 0.1],
              [0.1, 0.0, 0.1],
              [0.1, 0.0, 0.3],
              [0.2, 0.0, 0.3],
              [0.0, 0.0, 0.5],
              [-0.2, 0.0, 0.3],
              [-0.1, 0.0, 0.3],
              [-0.1, 0.0, 0.1],
              [-0.3, 0.0, 0.1],
              [-0.3, 0.0, 0.2],
              [-0.5, 0.0, 0.0],
              [-0.3, 0.0, -0.2],
              [-0.3, 0.0, -0.1],
              [-0.1, 0.0, -0.1],
              [-0.1, 0.0, -0.3]]

    points = [om2.MVector(x) * width for x in points]

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    generate(node=node,
             points=points,
             degree=1,
             close=True,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def square(parent, name, color, m, thickness=1, width=1, height=1, up="y", po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = om2.MVector(dlen, 0, 0)
    v1 = om2.MVector(-dlen, 0, 0)
    v2 = om2.MVector(0, dlen, 0)
    v3 = om2.MVector(0, -dlen, 0)
    v4 = om2.MVector(0, 0, dlen)
    v5 = om2.MVector(0, 0, -dlen)

    points = None
    if up == "x":
        points = [(v3 * height + v4 * width),
                  (v2 * height + v4 * width),
                  (v2 * height + v5 * width),
                  (v3 * height + v5 * width)]
    if up == "y":
        points = [(v1 * width + v4 * height),
                  (v0 * width + v4 * height),
                  (v0 * width + v5 * height),
                  (v1 * width + v5 * height)]
    if up == "z":
        points = [(v3 * height + v0 * width),
                  (v2 * height + v0 * width),
                  (v2 * height + v1 * width),
                  (v3 * height + v1 * width)]

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    generate(node=node,
             points=points,
             degree=1,
             close=True,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def wave(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    points = [[0.129648, 0.0, -0.567988],
              [0.0, 0.0, -0.338736],
              [-0.129648, 0.0, -0.567988],
              [-0.14698, 0.0, -0.305169],
              [-0.363233, 0.0, -0.4555],
              [-0.264842, 0.0, -0.211169],
              [-0.524946, 0.0, -0.252767],
              [-0.330243, 0.0, -0.075397],
              [-0.577752, 0.0, 0.0],
              [-0.330243, 0.0, 0.075397],
              [-0.524946, 0.0, 0.252767],
              [-0.264842, 0.0, 0.211169],
              [-0.363233, 0.0, 0.4555],
              [-0.14698, 0.0, 0.305169],
              [-0.129648, 0.0, 0.567988],
              [0.0, 0.0, 0.338736],
              [0.129648, 0.0, 0.567988],
              [0.14698, 0.0, 0.305169],
              [0.363233, 0.0, 0.4555],
              [0.264842, 0.0, 0.211169],
              [0.524946, 0.0, 0.252767],
              [0.330243, 0.0, 0.075397],
              [0.577752, 0.0, 0.0],
              [0.330243, 0.0, -0.075397],
              [0.524946, 0.0, -0.252767],
              [0.264842, 0.0, -0.211169],
              [0.363233, 0.0, -0.4555],
              [0.14698, 0.0, -0.305169]]
    points = [om2.MVector(p) * width for p in points]
    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    generate(node=node,
             points=points,
             degree=3,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def halfmoon(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    points = [[0.0, 0.0, -0.5],
              [-0.065, 0.0, -0.5],
              [-0.197, 0.0, -0.474],
              [-0.363, 0.0, -0.363],
              [-0.474, 0.0, -0.196],
              [-0.513, -0.0, 0.0],
              [-0.474, -0.0, 0.196],
              [-0.363, -0.0, 0.363],
              [-0.197, -0.0, 0.474],
              [-0.065, -0.0, 0.5],
              [0.0, -0.0, 0.5]]
    points = [om2.MVector(p) * width for p in points]
    generate(node=node,
             points=points,
             degree=3,
             color=color,
             close=False,
             thickness=thickness,
             po=po,
             ro=ro)

    points = [[0.0, 0.0, -0.5],
              [0.0, -0.0, 0.5]]
    points = [om2.MVector(p) * width for p in points]
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             close=False,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def half_circle(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    points = [[0.0, 0.0, -0.5],
              [-0.065, 0.0, -0.5],
              [-0.197, 0.0, -0.474],
              [-0.363, 0.0, -0.363],
              [-0.474, 0.0, -0.196],
              [-0.513, -0.0, 0.0],
              [-0.474, -0.0, 0.196],
              [-0.363, -0.0, 0.363],
              [-0.197, -0.0, 0.474],
              [-0.065, -0.0, 0.5],
              [0.0, -0.0, 0.5]]
    points = [om2.MVector(p) * width for p in points]

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    generate(node=node,
             points=points,
             degree=3,
             color=color,
             close=False,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def circle(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = om2.MVector(0, 0, -dlen * 1.108) * width
    v1 = om2.MVector(dlen * .78, 0, -dlen * .78) * width
    v2 = om2.MVector(dlen * 1.108, 0, 0) * width
    v3 = om2.MVector(dlen * .78, 0, dlen * .78) * width
    v4 = om2.MVector(0, 0, dlen * 1.108) * width
    v5 = om2.MVector(-dlen * .78, 0, dlen * .78) * width
    v6 = om2.MVector(-dlen * 1.108, 0, 0) * width
    v7 = om2.MVector(-dlen * .78, 0, -dlen * .78) * width

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    generate(node=node,
             points=[v0, v1, v2, v3, v4, v5, v6, v7],
             degree=3,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def circle3(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    c0 = circle(None, "Temp_circle0", color, om2.MMatrix(), thickness, width, po, ro)
    mc.setAttr(c0 + ".rz", 90)
    c1 = circle(None, "Temp_circle1", color, om2.MMatrix(), thickness, width, po, ro)
    mc.setAttr(c1 + ".rx", 90)
    c2 = circle(None, "Temp_circle2", color, om2.MMatrix(), thickness, width, po, ro)
    mc.makeIdentity([c0, c1], apply=True, rotate=True)

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    c0_shape = mc.listRelatives(c0, shapes=True)[0]
    c1_shape = mc.listRelatives(c1, shapes=True)[0]
    c2_shape = mc.listRelatives(c2, shapes=True)[0]
    mc.parent([c0_shape, c1_shape, c2_shape], node, relative=True, shape=True)

    mc.rename(c0_shape, node + "Shape")
    mc.rename(c1_shape, node + "Shape1")
    mc.rename(c2_shape, node + "Shape2")

    mc.delete([c0, c1, c2])
    return node


def locator(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = om2.MVector(dlen, 0, 0) * width
    v1 = om2.MVector(-dlen, 0, 0) * width
    v2 = om2.MVector(0, dlen, 0) * width
    v3 = om2.MVector(0, -dlen, 0) * width
    v4 = om2.MVector(0, 0, dlen) * width
    v5 = om2.MVector(0, 0, -dlen) * width

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)
    mc.setAttr(node + ".displayRotatePivot", True)

    points = [v0 * 2, v1 * 2]
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)

    points = [v2 * 2, v3 * 2]
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)

    points = [v4 * 2, v5 * 2]
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def cube(parent,
         name,
         color,
         thickness=1,
         width=1,
         height=1,
         depth=1,
         m=om2.MMatrix(),
         po=(0, 0, 0),
         ro=(0, 0, 0)):
    dlen = 0.5
    v0 = om2.MVector(dlen * width, dlen * height, dlen * depth)
    v1 = om2.MVector(dlen * width, dlen * height, -dlen * depth)
    v2 = om2.MVector(dlen * width, -dlen * height, dlen * depth)
    v3 = om2.MVector(dlen * width, -dlen * height, -dlen * depth)

    v4 = om2.MVector(-dlen * width, dlen * height, dlen * depth)
    v5 = om2.MVector(-dlen * width, dlen * height, -dlen * depth)
    v6 = om2.MVector(-dlen * width, -dlen * height, dlen * depth)
    v7 = om2.MVector(-dlen * width, -dlen * height, -dlen * depth)

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    points = [v0, v1, v3, v2, v0, v4, v5, v7, v6, v4, v5, v1, v3, v7, v6, v2]
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def cylinder(parent,
             name,
             color,
             thickness=1,
             width=1,
             height=1,
             m=om2.MMatrix(),
             po=(0, 0, 0),
             ro=(0, 0, 0)):
    dlen = 0.5
    v0 = om2.MVector(0, 0, -dlen * 1.108) * width
    v1 = om2.MVector(dlen * .78, 0, -dlen * .78) * width
    v2 = om2.MVector(dlen * 1.108, 0, 0) * width
    v3 = om2.MVector(dlen * .78, 0, dlen * .78) * width
    v4 = om2.MVector(0, 0, dlen * 1.108) * width
    v5 = om2.MVector(-dlen * .78, 0, dlen * .78) * width
    v6 = om2.MVector(-dlen * 1.108, 0, 0) * width
    v7 = om2.MVector(-dlen * .78, 0, -dlen * .78) * width
    up_circle_points = [p + om2.MVector(0, height / 2.0, 0) for p in [v0, v1, v2, v3, v4, v5, v6, v7]]
    down_circle_points = [p + om2.MVector(0, height / -2.0, 0) for p in [v0, v1, v2, v3, v4, v5, v6, v7]]

    points = [[0.354, 0.5, 0.354],
              [0.354, -0.5, 0.354]]
    line_points = [p * om2.MVector(width, height, width) for p in points]

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    generate(node=node,
             points=up_circle_points,
             degree=3,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    generate(node=node,
             points=down_circle_points,
             degree=3,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    _ro = 45
    for i in range(8):
        points = get_point_array_with_offset(line_points, (0, 0, 0), (0, 45 * i, 0))
        points = get_point_array_with_offset(points, po, ro)
        generate(node=node,
                 points=points,
                 degree=1,
                 color=color,
                 thickness=thickness)
    return node


def x(parent, name, color, thickness=1, width=1, height=1, depth=1, m=om2.MMatrix(), po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.25
    v0 = om2.MVector(dlen * width, 0, 0)
    v1 = om2.MVector(-dlen * width, 0, 0)
    v2 = om2.MVector(0, dlen * height, 0)
    v3 = om2.MVector(0, -dlen * height, 0)
    v4 = om2.MVector(0, 0, dlen * depth)
    v5 = om2.MVector(0, 0, -dlen * depth)

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    points = [(v0 + v2 + v4), (v1 + v3 + v5)]
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)

    points = [(v1 + v2 + v4), (v0 + v3 + v5)]
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)

    points = [(v0 + v3 + v4), (v1 + v2 + v5)]
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)

    points = [(v0 + v2 + v5), (v1 + v3 + v4)]
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def angle(parent, name, color, thickness=1, width=1, height=1, m=om2.MMatrix(), po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = om2.MVector(dlen * width, 0, dlen * height)
    v1 = om2.MVector(dlen * width, 0, -dlen * height)
    v2 = om2.MVector(-dlen * width, 0, -dlen * height)
    v3 = om2.MVector(dlen * width, 0, dlen * height)

    points = [v0, v1, v2, v3]

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)
    generate(node=node,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return node


def dodecahedron(parent,
                 name,
                 color,
                 thickness=1,
                 width=1,
                 height=1,
                 depth=1,
                 m=om2.MMatrix(),
                 po=(0, 0, 0),
                 ro=(0, 0, 0)):
    shapes = [[[-0.19, 0.496, 0.0],
               [0.19, 0.496, 0.0],
               [0.307, 0.307, -0.307],
               [0.0, 0.19, -0.496],
               [-0.307, 0.307, -0.307],
               [-0.19, 0.496, 0.0]],
              [[0.19, 0.496, 0.0],
               [0.307, 0.307, -0.307],
               [0.496, 0.0, -0.19],
               [0.496, 0.0, 0.19],
               [0.307, 0.307, 0.307],
               [0.19, 0.496, 0.0]],
              [[-0.19, 0.496, 0.0],
               [0.19, 0.496, 0.0],
               [0.307, 0.307, 0.307],
               [0.0, 0.19, 0.496],
               [-0.307, 0.307, 0.307],
               [-0.19, 0.496, 0.0]],
              [[0.496, 0.0, 0.19],
               [0.307, 0.307, 0.307],
               [0.0, 0.19, 0.496],
               [0.0, -0.19, 0.496],
               [0.307, -0.307, 0.307],
               [0.496, 0.0, 0.19]],
              [[-0.307, 0.307, 0.307],
               [0.0, 0.19, 0.496],
               [0.0, -0.19, 0.496],
               [-0.307, -0.307, 0.307],
               [-0.496, 0.0, 0.19],
               [-0.307, 0.307, 0.307]],
              [[-0.307, 0.307, 0.307],
               [-0.496, 0.0, 0.19],
               [-0.496, 0.0, -0.19],
               [-0.307, 0.307, -0.307],
               [-0.19, 0.496, 0.0]],
              [[-0.496, 0.0, -0.19],
               [-0.496, 0.0, 0.19],
               [-0.307, -0.307, 0.307],
               [-0.19, -0.496, 0.0],
               [-0.307, -0.307, -0.307],
               [-0.496, 0.0, -0.19]],
              [[-0.307, 0.307, -0.307],
               [0.0, 0.19, -0.496],
               [0.0, -0.19, -0.496],
               [-0.307, -0.307, -0.307],
               [-0.496, 0.0, -0.19],
               [-0.307, 0.307, -0.307]],
              [[-0.19, -0.496, 0.0],
               [0.19, -0.496, 0.0],
               [0.307, -0.307, -0.307],
               [0.0, -0.19, -0.496],
               [-0.307, -0.307, -0.307],
               [-0.19, -0.496, 0.0]],
              [[0.0, 0.19, -0.496],
               [0.307, 0.307, -0.307],
               [0.496, 0.0, -0.19],
               [0.307, -0.307, -0.307],
               [0.0, -0.19, -0.496],
               [0.0, 0.19, -0.496]],
              [[0.496, 0.0, -0.19],
               [0.496, 0.0, 0.19],
               [0.307, -0.307, 0.307],
               [0.19, -0.496, 0.0],
               [0.307, -0.307, -0.307],
               [0.496, 0.0, -0.19]]]

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    for shape in shapes:
        points = [(s[0] * width, s[1] * height, s[2] * depth) for s in shape]
        generate(node=node,
                 points=points,
                 degree=1,
                 color=color,
                 thickness=thickness,
                 po=po,
                 ro=ro)
    return node


def axis(parent,
         name,
         m=om2.MMatrix(),
         width=1,
         height=1,
         depth=1,
         po=(0, 0, 0),
         ro=(0, 0, 0)):
    dlen = 2
    v0 = om2.MVector(dlen * width, 0, 0)
    v1 = om2.MVector(0, dlen * height, 0)
    v2 = om2.MVector(0, 0, dlen * depth)

    node = mc.createNode("transform", name=name, parent=parent)
    matrix.set_matrix(node, m)

    points = [v0, v0 / 2]
    generate(node=node, points=points,
             degree=1, color=RED, thickness=5, po=po, ro=ro)

    points = [v1 / 4 * 3, v1 / 2]
    generate(node=node, points=points,
             degree=1, color=GREEN, thickness=5, po=po, ro=ro)

    points = [v2 / 4 * 3, v2 / 2]
    generate(node=node, points=points,
             degree=1, color=BLUE, thickness=5, po=po, ro=ro)
    return node


def guide_root(node, parent, m):
    dlen = 0.5
    v0 = om2.MVector(dlen, 0, 0)
    v1 = om2.MVector(-dlen, 0, 0)
    v2 = om2.MVector(0, dlen, 0)
    v3 = om2.MVector(0, -dlen, 0)
    v4 = om2.MVector(0, 0, dlen)
    v5 = om2.MVector(0, 0, -dlen)

    points = [v0 + v2 + v5, v0 + v2 + v4, v0 + v3 + v4, v0 + v3 + v5]
    generate(node=node, points=points, degree=1, color=RED)

    points = [v1 + v2 + v4, v1 + v2 + v5, v1 + v3 + v5, v1 + v3 + v4]
    generate(node=node, points=points, degree=1, color=RED)

    points = [v1 + v3 + v5, v0 + v3 + v5, v0 + v2 + v5, v1 + v2 + v5]
    generate(node=node, points=points, degree=1, color=RED)

    points = [v0 + v3 + v4, v1 + v3 + v4, v1 + v2 + v4, v0 + v2 + v4]
    generate(node=node, points=points, degree=1, color=RED)

    points = [v0 * 2, v1 * 2]
    generate(node=node, points=points, degree=1, color=RED)

    points = [v2 * 2, v3 * 2]
    generate(node=node, points=points, degree=1, color=RED)

    points = [v4 * 2, v5 * 2]
    generate(node=node, points=points, degree=1, color=RED)

    if parent:
        node = mc.parent(node, parent)[0]
    matrix.set_matrix(node, m)

    nonkeyable_attrs = ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v")
    [mc.setAttr(node + "." + attr, channelBox=True) for attr in nonkeyable_attrs]
    return node


def guide_position(node, parent, m):
    dlen = 0.25
    v0 = om2.MVector(dlen, 0, 0)
    v1 = om2.MVector(-dlen, 0, 0)
    v2 = om2.MVector(0, dlen, 0)
    v3 = om2.MVector(0, -dlen, 0)
    v4 = om2.MVector(0, 0, dlen)
    v5 = om2.MVector(0, 0, -dlen)

    points = [(v0 + v2 + v4), (v1 + v3 + v5)]
    generate(node=node,
             points=points,
             degree=1,
             color=RED + GREEN)

    points = [(v1 + v2 + v4), (v0 + v3 + v5)]
    generate(node=node,
             points=points,
             degree=1,
             color=RED + GREEN)

    points = [(v0 + v3 + v4), (v1 + v2 + v5)]
    generate(node=node,
             points=points,
             degree=1,
             color=RED + GREEN)

    points = [(v0 + v2 + v5), (v1 + v3 + v4)]
    generate(node=node,
             points=points,
             degree=1,
             color=RED + GREEN)

    node = mc.parent(node, parent)[0]
    matrix.set_matrix(node, m)

    lock_hide_attrs = ("sx", "sy", "sz", "v")
    nonkeyable_attrs = ("tx", "ty", "tz", "rx", "ry", "rz")
    [mc.setAttr(node + "." + attr, channelBox=True) for attr in nonkeyable_attrs]
    [mc.setAttr(node + "." + attr, lock=True) for attr in lock_hide_attrs]
    [mc.setAttr(node + "." + attr, keyable=False) for attr in lock_hide_attrs]
    return node


def guide_orientation(node):
    dlen = 2
    v0 = om2.MVector(dlen, 0, 0)
    v1 = om2.MVector(0, dlen, 0)
    v2 = om2.MVector(0, 0, dlen)

    points = [v0, v0 / 2]
    generate(node=node, points=points,
             degree=1, color=RED, thickness=5)

    points = [v1 / 4 * 3, v1 / 2]
    generate(node=node, points=points,
             degree=1, color=GREEN, thickness=5)

    points = [v2 / 4 * 3, v2 / 2]
    generate(node=node, points=points,
             degree=1, color=BLUE, thickness=5)

    lock_attrs = ("tx", "ty", "tz", "sx", "sy", "sz", "v")
    hide_attrs = ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v")
    [mc.setAttr(node + "." + attr, lock=True) for attr in lock_attrs]
    [mc.setAttr(node + "." + attr, keyable=False) for attr in hide_attrs]
    return node


def get_point_array_with_offset(point_pos, pos_offset=None, rot_offset=None):
    points = []
    for v in point_pos:
        if rot_offset:
            v = om2.MVector(v)
            v = v.rotateBy(om2.MEulerRotation(rot_offset))
        if pos_offset:
            v = om2.MVector(v) + om2.MVector(pos_offset)
        points.append(v)
    return points
