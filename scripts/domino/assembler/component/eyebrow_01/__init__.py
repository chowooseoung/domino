# domino
from domino.lib.rigging import nurbs, joint
from domino.lib import matrix, polygon, vector
from domino import assembler

# built-ins
import os
import uuid

# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2


class Author:
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "eyebrow"
    side = "C"
    index = 0
    description = "눈썹입니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "mesh": {"type": "string"},
        "inner_vertex": {"type": "string"},
        "outer_vertex": {"type": "string"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (-1, 0, 0.5))
        m1 = matrix.set_matrix_rotate2(m1, (-90, 0, -90))
        m2 = matrix.set_matrix_translate(m1, (-1.5, 0, 0.5))
        m2 = matrix.set_matrix_rotate2(m2, (-90, 0, 180))
        m3 = matrix.set_matrix_translate(m, (0, 0, 0.5))
        m3 = matrix.set_matrix_rotate2(m3, (-90, 0, 0))
        m4 = matrix.set_matrix_translate(m3, (1, 0, 0.5))
        return m, m1, m2, m3, m4

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
    })
    return common_preset


def guide_recipe():
    return {
        "position": [
            (0, "inner1", "arrow"),
            (1, "inner2", "arrow"),
            (0, "mid", "arrow"),
            (3, "outer", "arrow"),
        ],
        "display_curve": [
            ((2, 1, 3, 4), "eyebrowCrv"),  # source node indexes, extension
        ],
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)
        root = self.create_root(context)

        orig_m = om2.MMatrix()

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        mesh = data["mesh"]
        inner_vertex_index = int(data["inner_vertex"])
        outer_vertex_index = int(data["outer_vertex"])
        self.inner_vertex = mesh + ".vtx[{0}]".format(inner_vertex_index)
        self.outer_vertex = mesh + ".vtx[{0}]".format(outer_vertex_index)
        edges = mc.polySelect(mesh,
                              query=True,
                              shortestEdgePath=(inner_vertex_index, outer_vertex_index),
                              asSelectString=True)
        vertexes = polygon.convert_component(edges, vertex=True)
        self.vertexes = polygon.loop_to_way(vertexes, self.inner_vertex, self.outer_vertex)
        points = [mc.xform(v, query=True, translation=True, worldSpace=True) for v in self.vertexes]

        distance = vector.get_distance(points[0], points[-1])
        m = matrix.set_matrix_scale(data["anchors"][0], (1, 1, 1))
        self.brow_ctl, self.brow_loc = self.create_ctl(context=context,
                                                       parent=self.root,
                                                       name=self.generate_name("", "", "ctl"),
                                                       parent_ctl=None,
                                                       attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                                       m=m,
                                                       cns=False,
                                                       mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                                       shape_args={
                                                           "shape": "square",
                                                           "width": distance,
                                                           "height": distance / 12,
                                                           "color": (1, 0, 0),
                                                           "up": "z",
                                                       },
                                                       mirror_ctl_name=self.generate_name("", "", "ctl", True))

        self.origin_space = matrix.transform(parent=self.brow_loc,
                                             name=self.generate_name("origin", "space", "ctl"),
                                             m=orig_m)

        self.pin_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                              name=self.generate_name("pin", "mesh", "ctl"),
                                              points=points)

        self.driver_crv = nurbs.create(parent=self.origin_space,
                                       name=self.generate_name("driver", "crv", "ctl"),
                                       degree=1,
                                       positions=points,
                                       m=orig_m,
                                       vis=False,
                                       inherits=True)
        mc.rebuildCurve(self.driver_crv,
                        constructionHistory=0,
                        replaceOriginal=1,
                        rebuildType=0,
                        endKnots=0,
                        keepRange=0,
                        keepControlPoints=0,
                        keepEndPoints=1,
                        keepTangents=0,
                        spans=1,
                        degree=3,
                        tolerance=0.01)

        m = matrix.set_matrix_scale(data["anchors"][1], (1, 1, 1))
        self.inner1_ctl, self.inner1_loc = self.create_ctl(context=context,
                                                           parent=self.origin_space,
                                                           name=self.generate_name("inner1", "", "ctl"),
                                                           parent_ctl=self.brow_ctl,
                                                           attrs=["tx", "ty", "tz"],
                                                           m=m,
                                                           cns=False,
                                                           mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                                           shape_args={
                                                               "shape": "square",
                                                               "width": distance / 6,
                                                               "height": distance / 3,
                                                               "color": (1, 0, 0),
                                                               "up": "y",
                                                           },
                                                           mirror_ctl_name=self.generate_name("inner1", "", "ctl",
                                                                                              True))

        m = matrix.set_matrix_scale(data["anchors"][2], (1, 1, 1))
        self.inner2_ctl, self.inner2_loc = self.create_ctl(context=context,
                                                           parent=self.inner1_loc,
                                                           name=self.generate_name("inner2", "", "ctl"),
                                                           parent_ctl=self.inner1_ctl,
                                                           attrs=["tx", "ty", "tz"],
                                                           m=m,
                                                           cns=False,
                                                           mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                                           shape_args={
                                                               "shape": "circle",
                                                               "width": distance / 12,
                                                               "color": (1, 0, 0),
                                                           },
                                                           mirror_ctl_name=self.generate_name("inner2", "", "ctl",
                                                                                              True))

        m = matrix.set_matrix_scale(data["anchors"][3], (1, 1, 1))
        self.mid_ctl, self.mid_loc = self.create_ctl(context=context,
                                                     parent=self.origin_space,
                                                     name=self.generate_name("mid", "", "ctl"),
                                                     parent_ctl=self.brow_ctl,
                                                     attrs=["tx", "ty", "tz"],
                                                     m=m,
                                                     cns=False,
                                                     mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "circle",
                                                         "width": distance / 12,
                                                         "color": (1, 0, 0),
                                                     },
                                                     mirror_ctl_name=self.generate_name("mid", "", "ctl", True))

        m = matrix.set_matrix_scale(data["anchors"][4], (1, 1, 1))
        self.outer_ctl, self.outer_loc = self.create_ctl(context=context,
                                                         parent=self.origin_space,
                                                         name=self.generate_name("outer", "", "ctl"),
                                                         parent_ctl=self.brow_ctl,
                                                         attrs=["tx", "ty", "tz"],
                                                         m=m,
                                                         cns=False,
                                                         mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                                         shape_args={
                                                             "shape": "circle",
                                                             "width": distance / 12,
                                                             "color": (1, 0, 0),
                                                         },
                                                         mirror_ctl_name=self.generate_name("outer", "", "ctl", True))
        v1 = data["anchors"][1][12:-1]
        v2 = data["anchors"][2][12:-1]
        v3 = data["anchors"][3][12:-1]
        v4 = data["anchors"][4][12:-1]

        distance1 = vector.get_distance(v1, v2)
        distance2 = vector.get_distance(v2, v3)
        distance3 = vector.get_distance(v3, v4)
        total_distance = distance1 + distance2 + distance3

        inner2_poci = mc.createNode("pointOnCurveInfo")
        mc.setAttr(inner2_poci + ".parameter", 0)
        mc.connectAttr(self.driver_crv + ".local", inner2_poci + ".inputCurve")

        self.inner2_pos = matrix.transform(parent=self.origin_space,
                                           name=self.generate_name("inner2", "pos", "ctl"),
                                           m=orig_m)
        mc.connectAttr(inner2_poci + ".result.position", self.inner2_pos + ".t")

        u_value = distance1 / total_distance

        inner1_poci = mc.createNode("pointOnCurveInfo")
        mc.setAttr(inner1_poci + ".parameter", u_value)
        mc.connectAttr(self.driver_crv + ".local", inner1_poci + ".inputCurve")

        self.inner1_pos = matrix.transform(parent=self.origin_space,
                                           name=self.generate_name("inner1", "pos", "ctl"),
                                           m=orig_m)
        mc.connectAttr(inner1_poci + ".result.position", self.inner1_pos + ".t")
        mc.aimConstraint(self.inner1_pos, self.inner2_pos, worldUpType="objectrotation", worldUpObject=self.brow_loc)

        u_value = distance1 + distance2 / total_distance

        mid_poci = mc.createNode("pointOnCurveInfo")
        mc.setAttr(mid_poci + ".parameter", u_value)
        mc.connectAttr(self.driver_crv + ".local", mid_poci + ".inputCurve")

        self.mid_pos = matrix.transform(parent=self.origin_space,
                                        name=self.generate_name("mid", "pos", "ctl"),
                                        m=orig_m)
        mc.setAttr(self.mid_pos + ".t", *mc.getAttr(mid_poci + ".result.position")[0])
        mc.delete(mid_poci)

        outer_poci = mc.createNode("pointOnCurveInfo")
        mc.setAttr(outer_poci + ".parameter", 1)
        mc.connectAttr(self.driver_crv + ".local", outer_poci + ".inputCurve")

        self.outer_pos = matrix.transform(parent=self.origin_space,
                                          name=self.generate_name("outer", "pos", "ctl"),
                                          m=orig_m)
        mc.connectAttr(outer_poci + ".result.position", self.outer_pos + ".t")

        for i, c in enumerate([self.inner2_loc, self.inner1_loc, self.outer_loc]):
            if i == 2:
                i += 1
            pos = mc.xform(self.driver_crv + ".cv[{0}]".format(i), query=True, translation=True, worldSpace=True)
            m = matrix.set_matrix_translate(om2.MMatrix(), pos)
            p = matrix.transform(parent=c,
                                 name=self.generate_name("cv{0}".format(i), "source", "ctl"),
                                 m=m)
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(p + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.driver_crv + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", self.driver_crv + ".controlPoints[{0}]".format(i))
        p = matrix.transform(parent=self.mid_loc,
                             name=self.generate_name("", "", "ctl"),
                             m=matrix.get_matrix(self.mid_pos))
        mc.parentConstraint(p, self.mid_pos)

        self.skin_joints = []
        for i, p in enumerate([self.inner2_pos, self.inner1_pos, self.mid_pos, self.outer_pos]):
            jnt = joint.add_joint(parent=self.origin_space,
                                  name=self.generate_name("skin{0}".format(i), "jnt", "ctl"),
                                  m=matrix.get_matrix(p),
                                  vis=False)
            mc.parentConstraint(p, jnt, maintainOffset=True)
            self.skin_joints.append(jnt)

        self.pin_driver_sc = mc.skinCluster(self.skin_joints,
                                            self.pin_mesh,
                                            name=self.generate_name("pin", "sc", "ctl"),
                                            toSelectedBones=True,
                                            bindMethod=1,
                                            normalizeWeights=1,
                                            weightDistribution=1)[0]

        for plug in mc.listConnections(self.pin_driver_sc + ".matrix", destination=False, source=True, plugs=True):
            j = plug.split(".")[0]
            matrix_plug = mc.listConnections(j + ".worldMatrix[0]", destination=True, source=False, plugs=True)[0]
            index = matrix_plug.split("[")[1][0]

            inv_m = mc.createNode("inverseMatrix")
            mc.setAttr(inv_m + ".inputMatrix", mc.getAttr(j + ".worldMatrix[0]"), type="matrix")
            mc.connectAttr(inv_m + ".outputMatrix", self.pin_driver_sc + ".bindPreMatrix[{0}]".format(index))

            mc.connectAttr(j + ".matrix", matrix_plug, force=True)

        pin = mc.createNode("proximityPin")
        mc.setAttr(pin + ".offsetTranslation", 1)
        shape, orig_shape = mc.listRelatives(self.pin_mesh, shapes=True)
        mc.connectAttr(orig_shape + ".outMesh", pin + ".originalGeometry")
        mc.connectAttr(shape + ".worldMesh[0]", pin + ".deformedGeometry")
        self.refs = []
        self.jnts = []
        for i, p in enumerate(points):
            mc.setAttr(pin + ".inputMatrix[{0}]".format(i), m, type="matrix")
            m = matrix.set_matrix_translate(orig_m, p)
            t = matrix.transform(parent=self.root,
                                 name=self.generate_name("{0}".format(i), "pos", "ctl"),
                                 m=orig_m)
            mc.setAttr(t + ".t", 0, 0, 0)
            mc.setAttr(t + ".r", 0, 0, 0)


            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(pin + ".outputMatrix[{0}]".format(i), mult_m + ".matrixIn[0]")
            mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m+ ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", t + ".t")

            # refs
            name = self.generate_name("{0}".format(i), "ref", "ctl")
            ref = self.create_ref(context=context, name=name, anchor=True, m=t)
            self.refs.append(ref)

            # jnts
            if data["create_jnt"]:
                uni_scale = False
                if assembly_data["force_uni_scale"]:
                    uni_scale = True
                name = self.generate_name("{0}".format(i), "", "jnt")
                jnt = self.create_jnt(context=context,
                                      parent=None,
                                      name=name,
                                      description="{0}".format(i),
                                      ref=ref,
                                      m=matrix.get_matrix(ref),
                                      leaf=False,
                                      uni_scale=uni_scale)
                self.jnts.append(jnt)

    def attributes(self, context):
        super().attributes(context)

    def operators(self, context):
        super().operators(context)

    def connections(self, context):
        super().connections(context)
