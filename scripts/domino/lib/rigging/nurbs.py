# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# domino
from domino.lib import hierarchy


def get_fn_curve(crv):
    selection_list = om2.MSelectionList()
    selection_list.add(crv)
    return om2.MFnNurbsCurve(selection_list.getDagPath(0))


def data(crv):
    curve_data = {"parent": hierarchy.get_parent(crv).split("|")[-1],
                  "name": crv.split("|")[-1],
                  "transform": mc.xform(crv, query=True, matrix=True, worldSpace=True),
                  "shapes": []}
    for shape in mc.listRelatives(crv, shapes=True, fullPath=True) or []:
        fn_curve = get_fn_curve(shape)
        shape_data = {"name": shape.split("|")[-1],
                      "form": fn_curve.form,
                      "knots": list(fn_curve.knots()),
                      "degree": fn_curve.degree,
                      "points": list([list(x)[:-1] for x in fn_curve.cvPositions()]),
                      "override": mc.getAttr(shape + ".overrideEnabled"),
                      "use_rgb": mc.getAttr(shape + ".overrideRGBColors"),
                      "color_rgb": mc.getAttr(shape + ".overrideColorRGB")[0],
                      "color_index": mc.getAttr(shape + ".overrideColor"),
                      "line_width": mc.getAttr(shape + ".lineWidth")}
        curve_data["shapes"].append(shape_data)
    return curve_data


def build(curve_data, name="", parent=None, replace="", match=False, inherits=True):
    if parent is None:
        if curve_data["parent"]:
            if mc.objExists(curve_data["parent"][0]):
                parent = curve_data["parent"][0]
    if replace and mc.objExists(replace):
        crv = replace
        mc.delete(mc.listRelatives(crv, shapes=True, fullPath=True))
    else:
        crv = mc.createNode("transform", name=curve_data["name"] if not name else name, parent=parent)
    if not inherits:
        mc.setAttr(crv + ".inheritsTransform", 0)
    temp_crv_name = "curve_build_temp"
    for d in curve_data["shapes"]:
        shape = mc.curve(name=temp_crv_name,
                         point=d["points"],
                         periodic=False if d["form"] == 1 else True,
                         degree=d["degree"],
                         knot=d["knots"])
        shape = mc.listRelatives(shape, shapes=True, fullPath=True)[0]
        mc.setAttr(shape + ".overrideEnabled", d["override"])
        mc.setAttr(shape + ".overrideRGBColors", d["use_rgb"])
        mc.setAttr(shape + ".overrideColorRGB", *d["color_rgb"])
        mc.setAttr(shape + ".overrideColor", d["color_index"])
        mc.setAttr(shape + ".lineWidth", d["line_width"])
        shape = mc.rename(shape, crv.split("|")[-1] + "Shape")
        mc.parent(shape, crv, relative=True, shape=True)
        mc.delete(temp_crv_name)
    if match:
        mc.xform(crv, matrix=curve_data["transform"], worldSpace=True)
    return crv


def create(parent, name, degree, positions, m=om2.MTransformationMatrix(), bezier=False, vis=True, inherits=True,
           display_type=0):
    if isinstance(m, om2.MTransformationMatrix):
        m = m.asMatrix()
    argument = {"point": [om2.MVector(p) - om2.MVector(list(m)[12:-1]) for p in positions], "bezier": bezier}
    if not bezier:
        argument.update({"degree": degree})
    crv = mc.curve(**argument)
    crv = mc.rename(crv, name)
    mc.xform(crv, matrix=m, worldSpace=True)
    if parent:
        crv = mc.parent(crv, parent)[0]
    if not vis:
        mc.setAttr(crv + ".v", 0)
    if not inherits:
        mc.setAttr(crv + ".inheritsTransform", 0)
        mc.xform(crv, matrix=m, worldSpace=True)
    if display_type != 0:
        mc.setAttr(crv + ".overrideEnabled", 1)
        mc.setAttr(crv + ".overrideDisplayType", display_type)
    return crv


def duplicate(crv, parent=None, name="duplicate_crv"):
    dup_crv = mc.createNode("transform", name=name, parent=parent)
    dup_shapes = []
    for shape in mc.listRelatives(crv, shapes=True):
        dup = mc.duplicateCurve(shape, name="temp__1")[0]
        dup_shape = mc.listRelatives(dup, shapes=True)[0]
        mc.parent(dup_shape, dup_crv, relative=True, shape=True)
        mc.delete(dup)
        mc.setAttr(dup_shape + ".lineWidth", mc.getAttr(shape + ".lineWidth"))
        mc.setAttr(dup_shape + ".overrideEnabled", mc.getAttr(shape + ".overrideEnabled"))
        mc.setAttr(dup_shape + ".overrideRGBColors", mc.getAttr(shape + ".overrideRGBColors"))
        mc.setAttr(dup_shape + ".overrideColor", mc.getAttr(shape + ".overrideColor"))
        mc.setAttr(dup_shape + ".overrideColorRGB", *mc.getAttr(shape + ".overrideColorRGB")[0])
        dup_shape = mc.rename(dup_shape, f"{dup_crv}Shape")
        dup_shapes.append(dup_shape)
    return dup_crv


def constraint(crv, source):
    shape = mc.listRelatives(crv, shapes=True, fullPath=True)
    for i, s in enumerate(source):
        decom = mc.createNode("decomposeMatrix")
        mc.connectAttr(s + ".worldMatrix[0]", decom + ".inputMatrix")
        mc.connectAttr(decom + ".outputTranslate", shape[0] + ".controlPoints[{0}]".format(i))


def get_length_attr(crv, local=True):
    ci = mc.createNode("curveInfo")
    shape = mc.listRelatives(crv, shapes=True)[0]
    if local:
        mc.connectAttr(shape + ".local", ci + ".inputCurve")
    else:
        mc.connectAttr(shape + ".worldSpace[0]", ci + ".inputCurve")
    return ci + ".arcLength"


def create_ribbon_surface(parent, name, start, end, normal, divide):
    start = om2.MVector(start)
    end = om2.MVector(end)
    n = om2.MVector(normal) * 0.1
    points = (start - n, start, start + n)
    crv1 = mc.curve(point=points, degree=1)
    points = (end - n, end, end + n)
    crv2 = mc.curve(point=points, degree=1)
    surface = mc.loft(crv1,
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
        surface = mc.parent(surface, parent)[0]
    mc.delete([crv1, crv2])
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
    mc.hide(nurbs_surf)

    sc = mc.skinCluster(bind_jnts,
                        nurbs_surf,
                        toSelectedBones=True,
                        bindMethod=1,
                        dropoffRate=2.5,
                        maximumInfluences=3,
                        normalizeWeights=1,
                        weightDistribution=1,
                        removeUnusedInfluence=False,
                        nurbsSamples=6)[0]
    # mc.setAttr(sc + ".relativeSpaceMode", 1)

    name = name_format.format("uniformCrv")
    uniform_crv, iso = mc.duplicateCurve(nurbs_surf + ".u[1]",
                                         name=name,
                                         constructionHistory=True,
                                         range=0,
                                         local=0)
    mc.hide(uniform_crv)
    uniform_crv = mc.parent(uniform_crv, parent)[0]
    mc.connectAttr(nurbs_surf + ".local", "{0}.inputSurface".format(iso), force=True)

    uniform_crv_shape = mc.listRelatives(uniform_crv, shapes=True, fullPath=True)[0]
    nurbs_surf_shape, orig = mc.listRelatives(nurbs_surf, shapes=True, fullPath=True)

    uvpin = mc.createNode("uvPin")
    # mc.setAttr(uvpin + ".relativeSpaceMode", 2)
    mc.connectAttr(orig + ".local", uvpin + ".originalGeometry")
    mc.connectAttr(nurbs_surf + ".local", uvpin + ".deformedGeometry")
    # mc.setAttr(uvpin + ".relativeSpaceMatrix",
    #            mc.xform(parent, query=True, matrix=True, worldSpace=True), type="matrix")
    mc.setAttr(uvpin + ".normalAxis", normal_axis)

    for i, x in enumerate(v_values):
        mp = mc.createNode("motionPath")
        mc.setAttr(mp + ".fractionMode", True)
        mc.setAttr(mp + ".uValue", x)
        mc.connectAttr(uniform_crv_shape + ".local", mp + ".geometryPath")

        cps = mc.createNode("closestPointOnSurface")
        mc.connectAttr(nurbs_surf + ".local", cps + ".inputSurface")
        mc.connectAttr(mp + ".allCoordinates", cps + ".inPosition")

        ba = mc.createNode("blendTwoAttr")
        mc.setAttr(ba + ".input[0]", x)
        mc.connectAttr(uniform_switch, ba + ".attributesBlender")
        mc.connectAttr(cps + ".result.parameterV", ba + ".input[1]")

        mc.setAttr(uvpin + ".coordinate[{0}].coordinateU".format(i), 0.5)
        mc.connectAttr(ba + ".output", uvpin + ".coordinate[{0}].coordinateV".format(i))

    for i, x in enumerate(v_values):
        if i == len(v_values) - 1:
            next_i = i - 1
            x_axis = primary_x_axis * -1
        else:
            next_i = i + 1
            x_axis = primary_x_axis
        aim_m = mc.createNode("aimMatrix")
        mc.setAttr(aim_m + ".primaryInputAxisX", x_axis)
        mc.setAttr(aim_m + ".secondaryMode", 2)

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(uvpin + ".outputMatrix[{0}]".format(i), mult_m + ".matrixIn[0]")
        mc.connectAttr(parent + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
        mc.connectAttr(mult_m + ".matrixSum", aim_m + ".inputMatrix")

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(uvpin + ".outputMatrix[{0}]".format(next_i), mult_m + ".matrixIn[0]")
        mc.connectAttr(parent + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

        mc.connectAttr(mult_m + ".matrixSum", aim_m + ".primaryTargetMatrix")
        mc.connectAttr(mult_m + ".matrixSum", aim_m + ".secondaryTargetMatrix")

        pick_m = mc.createNode("pickMatrix")
        mc.connectAttr(aim_m + ".outputMatrix", pick_m + ".inputMatrix")
        mc.setAttr(pick_m + ".useScale", False)
        mc.setAttr(pick_m + ".useShear", False)
        mc.connectAttr(pick_m + ".outputMatrix", outputs[i] + ".offsetParentMatrix")
    return uvpin


def point_on_curve(crv, division):
    shape = mc.listRelatives(crv, shapes=True, fullPath=True)[0]
    mp = mc.createNode("motionPath")
    mc.setAttr(mp + ".fractionMode", True)
    mc.connectAttr(shape + ".worldSpace[0]", mp + ".geometryPath")

    ratio = 1.0 / division
    positions = []
    for i in range(division + 1):
        mc.setAttr(mp + ".uValue", ratio * i)
        positions.append(mc.getAttr(mp + ".allCoordinates")[0])
    return positions


def loft(parent, curve1, curve2, name, retopo=None):
    mesh, loft_node = mc.loft(curve1,
                              curve2,
                              name=name,
                              constructionHistory=True,
                              uniform=1,
                              close=0,
                              autoReverse=1,
                              degree=3,
                              sectionSpans=1,
                              range=0,
                              polygon=1,
                              reverseSurfaceNormals=True)
    mesh = mc.parent(mesh, parent)[0]

    tessellate = mc.listConnections(loft_node + ".outputSurface",
                                    source=False,
                                    destination=True)[0]
    mc.setAttr(tessellate + ".format", 0)
    mc.setAttr(tessellate + ".polygonType", 1)
    mc.setAttr(tessellate + ".polygonCount", 200)
    mc.delete(mesh, ch=True)

    if retopo:
        mc.polyRetopo(constructionHistory=False,
                      replaceOriginal=1,
                      preserveHardEdges=0,
                      topologyRegularity=0.5,
                      faceUniformity=0,
                      anisotropy=0.75,
                      targetFaceCount=1000,
                      targetFaceCountTolerance=10)
    return mesh
