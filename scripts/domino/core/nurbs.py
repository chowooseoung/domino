# maya
from pymel import core as pm

dt = pm.datatypes


def data(crv):
    curve_data = {"parent": crv.getParent().strip(),
                  "name": crv.strip(),
                  "transform": crv.getMatrix(worldSpace=True).tolist(),
                  "shapes": []}
    crv_shapes = crv.getShapes()
    for shape in crv_shapes:
        shape_data = {"name": shape.nodeName(),
                      "form": shape.form().index,
                      "knots": shape.getKnots(),
                      "degree": shape.degree(),
                      "points": [[cv.x, cv.y, cv.z] for cv in shape.getCVs(space="object")],
                      "override": shape.attr("overrideEnabled").get(),
                      "use_rgb": shape.attr("overrideRGBColors").get(),
                      "color_rgb": shape.attr("overrideColorRGB").get(),
                      "color_opacity": shape.attr("overrideColorA").get(),
                      "color_index": shape.attr("overrideColor").get(),
                      "line_width": shape.attr("lineWidth").get()}
        curve_data["shapes"].append(shape_data)
    return curve_data


def build(curve_data, name="", parent=None, replace="", match=False):
    if parent is None:
        if curve_data["parent"]:
            if pm.objExists(curve_data["parent"][0]):
                parent = curve_data["parent"][0]
    if replace and pm.objExists(replace):
        crv = replace
        pm.delete(pm.listRelatives(crv,
                                   shapes=True,
                                   fullPath=True))
    else:
        crv = pm.createNode("transform",
                            name=curve_data["name"] if not name else name,
                            parent=parent)
    temp_crv_name = "curve_build_temp"
    for d in curve_data["shapes"]:
        shape = pm.curve(name=temp_crv_name,
                         point=d["points"],
                         periodic=False if d["form"] == 1 else True,
                         degree=d["degree"],
                         knot=d["knots"])
        shape = pm.listRelatives(shape, shapes=True, fullPath=True)[0]
        shape.attr("overrideEnabled").set(d["override"])
        shape.attr("overrideRGBColors").set(d["use_rgb"])
        shape.attr("overrideColorRGB").set(*d["color_rgb"])
        shape.attr("overrideColorA").set(d["color_opacity"])
        shape.attr("overrideColor").set(d["color_index"])
        shape.attr("lineWidth").set(d["line_width"])
        shape.rename(crv.nodeName() + "Shape")
        pm.parent(shape, crv, relative=True, shape=True)
        pm.delete(temp_crv_name)
    if match:
        crv.setMatrix(curve_data["transform"], worldSpace=True)
    return crv


def create(parent, name, degree, positions, m=dt.Matrix(), bezier=False, vis=True, inherits=True, display_type=0):
    argument = {"point": [p - m.translate for p in positions],
                "bezier": bezier}
    if not bezier:
        argument.update({"degree": degree})
    crv = pm.curve(**argument)
    crv.rename(name)
    crv.setMatrix(m, worldSpace=True)
    if parent:
        pm.parent(crv, parent)
    if not vis:
        crv.attr("v").set(0)
    if not inherits:
        crv.attr("t").set((0, 0, 0))
        crv.attr("r").set((0, 0, 0))
        crv.attr("s").set((1, 1, 1))
        crv.attr("inheritsTransform").set(0)
    if display_type != 0:
        crv.attr("overrideEnabled").set(1)
        crv.attr("overrideDisplayType").set(display_type)
    return crv


def duplicate(crv, parent=None, name="duplicate_crv"):
    shapes = crv.getShapes()
    dup_crv = pm.createNode("transform", name=name, parent=parent)
    dup_shapes = []
    for shape in shapes:
        dup = pm.duplicateCurve(shape, name="temp__1")[0]
        dup_shape = dup.getShape()
        pm.parent(dup_shape, dup_crv, relative=True, shape=True)
        pm.delete(dup)
        width = shape.attr("lineWidth").get()
        dup_shape.attr("lineWidth").set(width)
        enable = shape.attr("overrideEnabled").get()
        dup_shape.attr("overrideEnabled").set(enable)
        use_rgb = shape.attr("overrideRGBColors").get()
        dup_shape.attr("overrideRGBColors").set(use_rgb)
        index = shape.attr("overrideColor").get()
        dup_shape.attr("overrideColor").set(index)
        opacity = shape.attr("overrideColorA").get()
        shape.attr("overrideColorA").set(opacity)
        rgb = shape.attr("overrideColorRGB")[0].get()
        dup_shape.attr("overrideColorRGB").set(*rgb)
        dup_shape.rename(f"{dup_crv}Shape")
        dup_shapes.append(dup_shape)
    return dup_crv


def constraint(crv, source):
    shape = crv.getShape()
    for i, s in enumerate(source):
        decom = pm.createNode("decomposeMatrix")
        pm.connectAttr(s.attr("worldMatrix")[0], decom.attr("inputMatrix"))
        pm.connectAttr(decom.attr("outputTranslate"), shape.attr("controlPoints")[i])


def length(crv, worldSpace=True):
    ci = pm.createNode("curveInfo")
    if worldSpace:
        pm.connectAttr(crv.getShape().attr("worldSpace")[0], ci.attr("inputCurve"))
    else:
        pm.connectAttr(crv.getShape().attr("local"), ci.attr("inputCurve"))
    return ci.attr("arcLength")


def create_ribbon_surface(parent, name, start, end, normal, divide):
    n = normal * 0.1
    points = (start - n, start, start + n)
    crv1 = pm.curve(point=points, degree=1)
    points = (end - n, end, end + n)
    crv2 = pm.curve(point=points, degree=1)
    surface = pm.loft(crv1,
                      crv2,
                      name=name,
                      uniform=1,
                      close=0,
                      degree=3,
                      sectionSpans=divide,
                      range=0,
                      polygon=0,
                      reverseSurfaceNormals=True,
                      constructionHistory=False)[0]
    if parent:
        pm.parent(surface, parent)
    pm.delete([crv1, crv2])
    return surface


def ribbon(parent, name_format, positions, normal, v_values, bind_jnts, uniform_switch, outputs, negate=False):
    primary_x_axis = 1
    normal_axis = 1
    if negate:
        normal_axis = 4
        primary_x_axis *= -1
    name = name_format.format("surf")
    nurbs_surf = create_ribbon_surface(parent,
                                       name,
                                       positions[0],
                                       positions[1],
                                       normal,
                                       len(v_values))
    pm.hide(nurbs_surf)

    sc = pm.skinCluster(bind_jnts,
                        nurbs_surf,
                        toSelectedBones=True,
                        bindMethod=1,
                        dropoffRate=2.5,
                        maximumInfluences=3,
                        normalizeWeights=1,
                        weightDistribution=1,
                        removeUnusedInfluence=False,
                        nurbsSamples=6)
    sc.attr("relativeSpaceMode").set(1)

    name = name_format.format("uniformCrv")
    uniform_crv, iso = pm.duplicateCurve(nurbs_surf.u[1],
                                         name=name,
                                         constructionHistory=True,
                                         range=0,
                                         local=0)
    uniform_crv = pm.PyNode(uniform_crv)
    pm.hide(uniform_crv)
    pm.parent(uniform_crv, parent)
    pm.connectAttr(nurbs_surf.attr("local"), f"{iso}.inputSurface", force=True)

    uniform_crv_shape = uniform_crv.getShape()
    nurbs_surf_shape, orig = nurbs_surf.getShapes()

    uvpin = pm.createNode("uvPin")
    uvpin.attr("relativeSpaceMode").set(2)
    pm.connectAttr(orig.attr("local"), uvpin.attr("originalGeometry"))
    pm.connectAttr(nurbs_surf.attr("local"), uvpin.attr("deformedGeometry"))
    uvpin.attr("relativeSpaceMatrix").set(parent.attr("worldMatrix")[0].get())
    uvpin.attr("normalAxis").set(normal_axis)

    for i, x in enumerate(v_values):
        mp = pm.createNode("motionPath")
        mp.attr("fractionMode").set(True)
        mp.attr("uValue").set(x)
        pm.connectAttr(uniform_crv_shape.attr("local"), mp.attr("geometryPath"))

        cps = pm.createNode("closestPointOnSurface")
        pm.connectAttr(nurbs_surf.attr("local"), cps.attr("inputSurface"))
        pm.connectAttr(mp.attr("allCoordinates"), cps.attr("inPosition"))

        ba = pm.createNode("blendTwoAttr")
        ba.attr("input")[0].set(x)
        pm.connectAttr(uniform_switch, ba.attr("attributesBlender"))
        pm.connectAttr(cps.attr("result.parameterV"), ba.attr("input")[1])

        uvpin.attr(f"coordinate[{i}].coordinateU").set(0.5)
        pm.connectAttr(ba.attr("output"), uvpin.attr(f"coordinate[{i}].coordinateV"))

    for i, x in enumerate(v_values):
        if i == len(v_values) - 1:
            next_i = i - 1
            x_axis = primary_x_axis * -1
        else:
            next_i = i + 1
            x_axis = primary_x_axis
        aim_m = pm.createNode("aimMatrix")
        aim_m.attr("primaryInputAxisX").set(x_axis)
        aim_m.attr("secondaryMode").set(2)
        pm.connectAttr(uvpin.attr("outputMatrix")[i], aim_m.attr("inputMatrix"))

        pm.connectAttr(uvpin.attr("outputMatrix")[next_i], aim_m.attr("primaryTargetMatrix"))
        pm.connectAttr(uvpin.attr("outputMatrix")[next_i], aim_m.attr("secondaryTargetMatrix"))
        pm.connectAttr(aim_m.attr("outputMatrix"), outputs[i].attr("offsetParentMatrix"))
    return uvpin


def point_on_curve(crv, division):
    shape = crv.getShape()
    mp = pm.createNode("motionPath")
    mp.attr("fractionMode").set(True)
    pm.connectAttr(shape.attr("worldSpace")[0], mp.attr("geometryPath"))

    ratio = 1.0 / division
    positions = []
    for i in range(division + 1):
        mp.attr("uValue").set(ratio * i)
        positions.append(mp.attr("allCoordinates").get())
    return positions
