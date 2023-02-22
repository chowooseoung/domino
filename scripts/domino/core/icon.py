# maya
from pymel import core as pm

# domino
from . import attribute
from .color import (RED, GREEN, BLUE)

dt = pm.datatypes


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

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)
    return obj


def replace(source, target):
    pm.delete(target.getShapes())
    shapes = source.getShapes()
    pm.parent(shapes, target, relative=True, shape=True)


def generate(obj, points, degree, color, close=False, thickness=1, po=(0, 0, 0), ro=(0, 0, 0)):
    if close:
        points.extend(points[:degree])
        knots = range(len(points) + degree - 1)
        curve = pm.curve(point=points, degree=degree, per=close, k=knots)
    else:
        curve = pm.curve(point=points, degree=degree)
    curve.attr("t").set(po)
    curve.attr("r").set(ro)
    pm.makeIdentity(curve, apply=True, translate=True, rotate=True)
    shape = curve.getShape()
    shape.rename(str(obj) + "Shape")
    pm.parent(shape, obj, relative=True, shape=True)
    pm.delete(curve)

    if color:
        shape.attr("overrideEnabled").set(True)
    if isinstance(color, int):
        shape.attr("overrideRGBColors").set(0)
        shape.attr("overrideColor").set(color)
    elif isinstance(color, dt.Color):
        shape.attr("overrideRGBColors").set(1)
        shape.attr("overrideColorRGB").set(color)
    shape.attr("lineWidth").set(thickness)
    shape.attr("isHistoricallyInteresting").set(0)


def origin(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = dt.Vector(0, 0, -dlen * 1.108) * width
    v1 = dt.Vector(dlen * .78, 0, -dlen * .78) * width
    v2 = dt.Vector(dlen * 1.108, 0, 0) * width
    v3 = dt.Vector(dlen * .78, 0, dlen * .78) * width
    v4 = dt.Vector(0, 0, dlen * 1.108) * width
    v5 = dt.Vector(-dlen * .78, 0, dlen * .78) * width
    v6 = dt.Vector(-dlen * 1.108, 0, 0) * width
    v7 = dt.Vector(-dlen * .78, 0, -dlen * .78) * width

    v8 = dt.Vector(dlen - 0.01, 0, 0) * width
    v9 = dt.Vector(dlen + 0.01, 0, 0) * width
    v10 = dt.Vector(0, 0, dlen - 0.01) * width
    v11 = dt.Vector(0, 0, dlen + 0.01) * width
    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)
    obj.attr("displayRotatePivot").set(True)
    obj.attr("overrideEnabled").set(True)
    obj.attr("overrideRGBColors").set(0)
    obj.attr("overrideColor").set(16)

    generate(obj=obj,
             points=[v0, v1, v2, v3, v4, v5, v6, v7],
             degree=3,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    generate(obj=obj,
             points=[v8, v9],
             degree=1,
             color=RED,
             thickness=5,
             po=po,
             ro=ro)
    generate(obj=obj,
             points=[v10, v11],
             degree=1,
             color=BLUE,
             thickness=5,
             po=po,
             ro=ro)
    return obj


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
    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    generate(obj=obj,
             points=[dt.Vector(x) * width for x in points1],
             degree=1,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    generate(obj=obj,
             points=[dt.Vector(x) * width for x in points2],
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    generate(obj=obj,
             points=[dt.Vector(x) * width for x in points3],
             close=True,
             degree=3,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return obj


def arrow(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    points = [(-0.0, 0.0, -0.5),
              (0.5, 0.0, 0.0),
              (-0.0, 0.0, 0.5),
              (0.0, 0.0, 0.211),
              (-0.5, 0.0, 0.211),
              (-0.5, 0.0, -0.211),
              (0.0, 0.0, -0.211),
              (-0.0, 0.0, -0.5)]

    points = [dt.Vector(x) * width for x in points]

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    generate(obj=obj,
             points=points,
             degree=1,
             close=True,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return obj


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

    points = [dt.Vector(x) * width for x in points]

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    generate(obj=obj,
             points=points,
             degree=1,
             close=True,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return obj


def square(parent, name, color, m, thickness=1, width=1, height=1, up="y", po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = dt.Vector(dlen, 0, 0)
    v1 = dt.Vector(-dlen, 0, 0)
    v2 = dt.Vector(0, dlen, 0)
    v3 = dt.Vector(0, -dlen, 0)
    v4 = dt.Vector(0, 0, dlen)
    v5 = dt.Vector(0, 0, -dlen)

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

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    generate(obj=obj,
             points=points,
             degree=1,
             close=True,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return obj


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
    points = [dt.Vector(p) * width for p in points]
    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    generate(obj=obj,
             points=points,
             degree=3,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    return obj


def halfmoon(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

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
    points = [dt.Vector(p) * width for p in points]
    generate(obj=obj,
             points=points,
             degree=3,
             color=color,
             close=False,
             thickness=thickness,
             po=po,
             ro=ro)

    points = [[0.0, 0.0, -0.5],
              [0.0, -0.0, 0.5]]
    points = [dt.Vector(p) * width for p in points]
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             close=False,
             thickness=thickness,
             po=po,
             ro=ro)
    return obj


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
    points = [dt.Vector(p) * width for p in points]

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    generate(obj=obj,
             points=points,
             degree=3,
             color=color,
             close=False,
             thickness=thickness,
             po=po,
             ro=ro)
    return obj


def circle(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = dt.Vector(0, 0, -dlen * 1.108) * width
    v1 = dt.Vector(dlen * .78, 0, -dlen * .78) * width
    v2 = dt.Vector(dlen * 1.108, 0, 0) * width
    v3 = dt.Vector(dlen * .78, 0, dlen * .78) * width
    v4 = dt.Vector(0, 0, dlen * 1.108) * width
    v5 = dt.Vector(-dlen * .78, 0, dlen * .78) * width
    v6 = dt.Vector(-dlen * 1.108, 0, 0) * width
    v7 = dt.Vector(-dlen * .78, 0, -dlen * .78) * width

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    generate(obj=obj,
             points=[v0, v1, v2, v3, v4, v5, v6, v7],
             degree=3,
             color=color,
             close=True,
             thickness=thickness,
             po=po,
             ro=ro)
    return obj


def circle3(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    c0 = circle(None, "Temp_circle0", color, dt.Matrix(), thickness, width, po, ro)
    c0.attr("rz").set(90)
    c1 = circle(None, "Temp_circle1", color, dt.Matrix(), thickness, width, po, ro)
    c1.attr("rx").set(90)
    c2 = circle(None, "Temp_circle2", color, dt.Matrix(), thickness, width, po, ro)
    pm.makeIdentity([c0, c1], apply=True, rotate=True)

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    c0_shape = c0.getShape()
    c1_shape = c1.getShape()
    c2_shape = c2.getShape()
    pm.parent([c0_shape, c1_shape, c2_shape], obj, relative=True, shape=True)

    c0_shape.rename(f"{obj.nodeName()}Shape")
    c1_shape.rename(f"{obj.nodeName()}Shape1")
    c2_shape.rename(f"{obj.nodeName()}Shape2")

    pm.delete([c0, c1, c2])
    return obj


def locator(parent, name, color, m, thickness=1, width=1, po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = dt.Vector(dlen, 0, 0) * width
    v1 = dt.Vector(-dlen, 0, 0) * width
    v2 = dt.Vector(0, dlen, 0) * width
    v3 = dt.Vector(0, -dlen, 0) * width
    v4 = dt.Vector(0, 0, dlen) * width
    v5 = dt.Vector(0, 0, -dlen) * width

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)
    obj.attr("displayRotatePivot").set(True)

    points = [v0 * 2, v1 * 2]
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)

    points = [v2 * 2, v3 * 2]
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)

    points = [v4 * 2, v5 * 2]
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             thickness=thickness,
             po=po,
             ro=ro)
    return obj


def cube(parent,
         name,
         color,
         thickness=1,
         width=1,
         height=1,
         depth=1,
         m=dt.Matrix(),
         po=(0, 0, 0),
         ro=(0, 0, 0)):
    dlen = 0.5
    v0 = dt.Vector(dlen * width, dlen * height, dlen * depth)
    v1 = dt.Vector(dlen * width, dlen * height, -dlen * depth)
    v2 = dt.Vector(dlen * width, -dlen * height, dlen * depth)
    v3 = dt.Vector(dlen * width, -dlen * height, -dlen * depth)

    v4 = dt.Vector(-dlen * width, dlen * height, dlen * depth)
    v5 = dt.Vector(-dlen * width, dlen * height, -dlen * depth)
    v6 = dt.Vector(-dlen * width, -dlen * height, dlen * depth)
    v7 = dt.Vector(-dlen * width, -dlen * height, -dlen * depth)

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    points = [v0, v1, v3, v2, v0, v4, v5, v7, v6, v4, v5, v1, v3, v7, v6, v2]
    points = get_point_array_with_offset(points, po, ro)
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             thickness=thickness)
    return obj


def cylinder(parent,
             name,
             color,
             thickness=1,
             width=1,
             height=1,
             m=dt.Matrix(),
             po=(0, 0, 0),
             ro=(0, 0, 0)):
    dlen = 0.5
    v0 = dt.Vector(0, 0, -dlen * 1.108) * width
    v1 = dt.Vector(dlen * .78, 0, -dlen * .78) * width
    v2 = dt.Vector(dlen * 1.108, 0, 0) * width
    v3 = dt.Vector(dlen * .78, 0, dlen * .78) * width
    v4 = dt.Vector(0, 0, dlen * 1.108) * width
    v5 = dt.Vector(-dlen * .78, 0, dlen * .78) * width
    v6 = dt.Vector(-dlen * 1.108, 0, 0) * width
    v7 = dt.Vector(-dlen * .78, 0, -dlen * .78) * width
    up_circle_points = [p + dt.Vector(0, height / 2.0, 0) for p in [v0, v1, v2, v3, v4, v5, v6, v7]]
    down_circle_points = [p + dt.Vector(0, height / -2.0, 0) for p in [v0, v1, v2, v3, v4, v5, v6, v7]]

    points = [[0.354, 0.5, 0.354],
              [0.354, -0.5, 0.354]]
    line_points = [p * dt.Vector(width, height, width) for p in points]

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    points = get_point_array_with_offset(up_circle_points, po, ro)
    generate(obj=obj,
             points=points,
             degree=3,
             color=color,
             close=True,
             thickness=thickness)
    points = get_point_array_with_offset(down_circle_points, po, ro)
    generate(obj=obj,
             points=points,
             degree=3,
             color=color,
             close=True,
             thickness=thickness)
    _ro = 45
    for i in range(8):
        points = get_point_array_with_offset(line_points, (0, 0, 0), (0, 45 * i, 0))
        points = get_point_array_with_offset(points, po, ro)
        generate(obj=obj,
                 points=points,
                 degree=1,
                 color=color,
                 thickness=thickness)
    return obj


def x(parent, name, color, thickness=1, width=1, height=1, depth=1, m=dt.Matrix(), po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.25
    v0 = dt.Vector(dlen * width, 0, 0)
    v1 = dt.Vector(-dlen * width, 0, 0)
    v2 = dt.Vector(0, dlen * height, 0)
    v3 = dt.Vector(0, -dlen * height, 0)
    v4 = dt.Vector(0, 0, dlen * depth)
    v5 = dt.Vector(0, 0, -dlen * depth)

    points = [(v0 + v2 + v4), (v1 + v3 + v5)]
    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             thickness=thickness)

    points = [(v1 + v2 + v4), (v0 + v3 + v5)]
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             thickness=thickness)

    points = [(v0 + v3 + v4), (v1 + v2 + v5)]
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             thickness=thickness)

    points = [(v0 + v2 + v5), (v1 + v3 + v4)]
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             thickness=thickness)
    return obj


def angle(parent, name, color, thickness=1, width=1, height=1, m=dt.Matrix(), po=(0, 0, 0), ro=(0, 0, 0)):
    dlen = 0.5
    v0 = dt.Vector(dlen * width, 0, dlen * height)
    v1 = dt.Vector(dlen * width, 0, -dlen * height)
    v2 = dt.Vector(-dlen * width, 0, -dlen * height)
    v3 = dt.Vector(dlen * width, 0, dlen * height)

    points = [v0, v1, v2, v3]
    points = get_point_array_with_offset(points, po, ro)

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)
    generate(obj=obj,
             points=points,
             degree=1,
             color=color,
             thickness=thickness)
    return obj


def dodecahedron(parent,
                 name,
                 color,
                 thickness=1,
                 width=1,
                 height=1,
                 depth=1,
                 m=dt.Matrix(),
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

    obj = pm.createNode("transform", name=name, parent=parent)
    obj.setMatrix(m, worldSpace=True)

    for shape in shapes:
        points = [s * dt.Vector((width, height, depth)) for s in shape]
        points = get_point_array_with_offset(points, po, ro)
        generate(obj=obj,
                 points=points,
                 degree=1,
                 color=color,
                 thickness=thickness)
    return obj


def guide_root(obj, parent):
    dlen = 0.5
    v0 = dt.Vector(dlen, 0, 0)
    v1 = dt.Vector(-dlen, 0, 0)
    v2 = dt.Vector(0, dlen, 0)
    v3 = dt.Vector(0, -dlen, 0)
    v4 = dt.Vector(0, 0, dlen)
    v5 = dt.Vector(0, 0, -dlen)

    points = [v0 + v2 + v5, v0 + v2 + v4, v0 + v3 + v4, v0 + v3 + v5]
    generate(obj=obj, points=points, degree=1, color=RED)

    points = [v1 + v2 + v4, v1 + v2 + v5, v1 + v3 + v5, v1 + v3 + v4]
    generate(obj=obj, points=points, degree=1, color=RED)

    points = [v1 + v3 + v5, v0 + v3 + v5, v0 + v2 + v5, v1 + v2 + v5]
    generate(obj=obj, points=points, degree=1, color=RED)

    points = [v0 + v3 + v4, v1 + v3 + v4, v1 + v2 + v4, v0 + v2 + v4]
    generate(obj=obj, points=points, degree=1, color=RED)

    points = [v0 * 2, v1 * 2]
    generate(obj=obj, points=points, degree=1, color=RED)

    points = [v2 * 2, v3 * 2]
    generate(obj=obj, points=points, degree=1, color=RED)

    points = [v4 * 2, v5 * 2]
    generate(obj=obj, points=points, degree=1, color=RED)

    pm.parent(obj, parent)

    attribute.nonkeyable(obj, ["tx", "ty", "tz",
                               "rx", "ry", "rz",
                               "sx", "sy", "sz",
                               "v"])


def guide_position(obj, parent, m):
    dlen = 0.25
    v0 = dt.Vector(dlen, 0, 0)
    v1 = dt.Vector(-dlen, 0, 0)
    v2 = dt.Vector(0, dlen, 0)
    v3 = dt.Vector(0, -dlen, 0)
    v4 = dt.Vector(0, 0, dlen)
    v5 = dt.Vector(0, 0, -dlen)

    points = [(v0 + v2 + v4), (v1 + v3 + v5)]
    generate(obj=obj,
             points=points,
             degree=1,
             color=RED + GREEN)

    points = [(v1 + v2 + v4), (v0 + v3 + v5)]
    generate(obj=obj,
             points=points,
             degree=1,
             color=RED + GREEN)

    points = [(v0 + v3 + v4), (v1 + v2 + v5)]
    generate(obj=obj,
             points=points,
             degree=1,
             color=RED + GREEN)

    points = [(v0 + v2 + v5), (v1 + v3 + v4)]
    generate(obj=obj,
             points=points,
             degree=1,
             color=RED + GREEN)

    pm.parent(obj, parent)
    obj.setMatrix(m, worldSpace=True)

    attribute.nonkeyable(obj, ["tx", "ty", "tz",
                               "rx", "ry", "rz",
                               "sx", "sy", "sz",
                               "v"])
    attribute.lock(obj, ["sx", "sy", "sz", "v"])
    attribute.hide(obj, ["sx", "sy", "sz", "v"])


def guide_orientation(obj, parent):
    dlen = 2
    v0 = dt.Vector(dlen, 0, 0)
    v1 = dt.Vector(0, dlen, 0)
    v2 = dt.Vector(0, 0, dlen)

    points = [v0, v0 / 2]
    generate(obj=obj, points=points,
             degree=1, color=RED, thickness=5)

    points = [v1 / 4 * 3, v1 / 2]
    generate(obj=obj, points=points,
             degree=1, color=GREEN, thickness=5)

    points = [v2 / 4 * 3, v2 / 2]
    generate(obj=obj, points=points,
             degree=1, color=BLUE, thickness=5)

    pm.matchTransform(obj, parent)
    pm.parent(obj, parent)

    attribute.lock(obj, ["tx", "ty", "tz",
                         "sx", "sy", "sz",
                         "v"])
    attribute.hide(obj, ["tx", "ty", "tz",
                         "rx", "ry", "rz",
                         "sx", "sy", "sz",
                         "v"])


def get_point_array_with_offset(point_pos, pos_offset=None, rot_offset=None):
    points = []
    for v in point_pos:
        if rot_offset:
            v = dt.Vector(v)
            v = v.rotateBy(dt.EulerRotation(rot_offset))
        if pos_offset:
            v = dt.Vector(v) + dt.Vector(pos_offset)
        points.append(v)
    return points
