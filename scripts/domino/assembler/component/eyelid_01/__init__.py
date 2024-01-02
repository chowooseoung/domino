# domino
from domino.lib import matrix, polygon, vector, hierarchy, attribute
from domino.lib.rigging import nurbs, joint
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
    name = "eyelid"
    side = "C"
    index = 0
    description = "eyelid 입니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "eye_component": {"type": "string"},
        "mesh": {"type": "string"},
        "eyelid_vertex_loop": {"type": "string"},
        "eyelid_inner_vertex": {"type": "string"},
        "eyelid_outer_vertex": {"type": "string"},
        "eye_hole_vertex_loop": {"type": "string"},
        "eye_hole_inner_vertex": {"type": "string"},
        "eye_hole_outer_vertex": {"type": "string"},
        "auto_skinning": {"type": "bool"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0.5, 1.5))
        m1 = matrix.set_matrix_rotate2(m1, (-90, 0, -270))
        m2 = matrix.get_mirror_matrix(m1)
        m2 = matrix.set_matrix_translate(m2, (0, -0.5, 1.5))
        m2 = matrix.set_matrix_rotate2(m2, (90, 180, 90))
        m3 = matrix.set_matrix_translate(m, (1, 0, 1.5))
        m3 = matrix.set_matrix_rotate2(m3, (-90, 0, 0))
        m4 = matrix.get_mirror_matrix(m3)
        m4 = matrix.set_matrix_rotate2(m4, (-90, 0, 180))
        m5 = matrix.set_matrix_translate(m1, (0.5, 0.25, 1.5))
        m6 = matrix.get_mirror_matrix(m5)
        m7 = matrix.set_matrix_translate(m2, (0.5, -0.25, 1.5))
        m8 = matrix.get_mirror_matrix(m7)
        return m, m1, m2, m3, m4, m5, m6, m7, m8

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "auto_skinning": True,
    })
    return common_preset


def guide_recipe():
    script = """import maya.cmds as mc
for pos in ["{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}"]:
    orig_scale = mc.getAttr(pos + ".s")
    mc.setAttr(pos + ".sx", lock=False)
    mc.setAttr(pos + ".sy", lock=False)
    mc.setAttr(pos + ".sz", lock=False)
    mc.setAttr(pos + ".s", 0.2, 0.2, 0.2)
    mc.makeIdentity(pos, apply=True, scale=True)
    mc.setAttr(pos + ".s", *orig_scale[0])
    mc.setAttr(pos + ".sx", lock=True)
    mc.setAttr(pos + ".sy", lock=True)
    mc.setAttr(pos + ".sz", lock=True)
    """
    return {
        "position": [
            (0, "up", "arrow"),
            (0, "low", "arrow"),
            (0, "left", "arrow"),
            (0, "right", "arrow"),
            (0, "upLeft", "arrow"),
            (0, "upRight", "arrow"),
            (0, "lowLeft", "arrow"),
            (0, "lowRight", "arrow")
        ],
        "display_curve": [
            ((0, 1), "upCrv"),  # source node indexes, extension
            ((0, 2), "lowCrv"),  # source node indexes, extension
            ((0, 3), "leftCrv"),  # source node indexes, extension
            ((0, 4), "rightCrv"),  # source node indexes, extension
            ((1, 5, 3, 7, 2, 8, 4, 6, 1), "lipCrv"),  # source node indexes, extension
        ],
        "post": {
            "script": script,
            "indexes": [1, 2, 3, 4, 5, 6, 7, 8]
        }
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)
        root = self.create_root(context)

        orig_m = om2.MMatrix()

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        mesh = data["mesh"]
        eyelid_vertex_loop = [int(x) for x in data["eyelid_vertex_loop"].split(",")]
        eye_hole_vertex_loop = [int(x) for x in data["eye_hole_vertex_loop"].split(",")]
        self.origin_space = matrix.transform(parent=self.root,
                                             name=self.generate_name("origin", "space", "ctl"),
                                             m=orig_m)

        # TODO
        eyelid_vertex_loop = polygon.convert_component([mesh + ".e[" + str(i) + "]" for i in eyelid_vertex_loop],
                                                       vertex=True)

        eyelid_inner_vertex = int(data["eyelid_inner_vertex"])
        eyelid_outer_vertex = int(data["eyelid_outer_vertex"])

        way1, way2 = polygon.loop_to_2way(loop=eyelid_vertex_loop,
                                          start_vertex=mesh + ".vtx[" + str(eyelid_inner_vertex) + "]",
                                          end_vertex=mesh + ".vtx[" + str(eyelid_outer_vertex) + "]")
        if vector.get_position(way1[int(len(way1) / 2)])[1] > vector.get_position(way2[int(len(way2) / 2)])[1]:
            self.eyelid_upper_way = way1
            self.eyelid_lower_way = way2
        else:
            self.eyelid_upper_way = way2
            self.eyelid_lower_way = way1
        self.eyelid_upper_rest_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                            name=self.generate_name("eyelidUpperRest", "mesh", "ctl"),
                                                            points=[vector.get_position(x) for x in
                                                                    self.eyelid_upper_way])
        self.eyelid_lower_rest_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                            name=self.generate_name("eyelidLowerRest", "mesh", "ctl"),
                                                            points=[vector.get_position(x) for x in
                                                                    self.eyelid_lower_way])
        self.eyelid_upper_close_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                             name=self.generate_name("eyelidUpperClose", "mesh", "ctl"),
                                                             points=[vector.get_position(x) for x in
                                                                     self.eyelid_upper_way])
        self.eyelid_lower_close_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                             name=self.generate_name("eyelidLowerClose", "mesh", "ctl"),
                                                             points=[vector.get_position(x) for x in
                                                                     self.eyelid_lower_way])
        self.eyelid_mid_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                     name=self.generate_name("eyelidMid", "mesh", "ctl"),
                                                     points=[vector.get_position(x) for x in self.eyelid_lower_way])
        self.eyelid_upper_pin_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                           name=self.generate_name("eyelidUpperPin", "mesh", "ctl"),
                                                           points=[vector.get_position(x) for x in
                                                                   self.eyelid_upper_way])
        self.eyelid_lower_pin_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                           name=self.generate_name("eyelidLowerPin", "mesh", "ctl"),
                                                           points=[vector.get_position(x) for x in
                                                                   self.eyelid_lower_way])
        self.eyelid_upper_skin_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                            name=self.generate_name("eyelidUpperSkin", "mesh", "ctl"),
                                                            points=[vector.get_position(x) for x in
                                                                    self.eyelid_upper_way])
        self.eyelid_lower_skin_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                            name=self.generate_name("eyelidLowerSkin", "mesh", "ctl"),
                                                            points=[vector.get_position(x) for x in
                                                                    self.eyelid_lower_way])
        self.eyelid_upper_cls_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                           name=self.generate_name("eyelidUpperCls", "mesh", "ctl"),
                                                           points=[vector.get_position(x) for x in
                                                                   self.eyelid_upper_way])
        mc.setAttr(self.eyelid_upper_cls_mesh + ".inheritsTransform", 0)
        self.eyelid_lower_cls_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                           name=self.generate_name("eyelidLowerCls", "mesh", "ctl"),
                                                           points=[vector.get_position(x) for x in
                                                                   self.eyelid_lower_way])
        mc.setAttr(self.eyelid_lower_cls_mesh + ".inheritsTransform", 0)
        self.eyelid_upper_skin_pin_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                                name=self.generate_name("eyelidUpperSkinPin", "mesh",
                                                                                        "ctl"),
                                                                points=[vector.get_position(x) for x in
                                                                        self.eyelid_upper_way])
        self.eyelid_lower_skin_pin_mesh = polygon.point_to_mesh(parent=self.origin_space,
                                                                name=self.generate_name("eyelidLowerSkinPin", "mesh",
                                                                                        "ctl"),
                                                                points=[vector.get_position(x) for x in
                                                                        self.eyelid_lower_way])
        mc.makeIdentity([self.eyelid_upper_rest_mesh,
                         self.eyelid_lower_rest_mesh,
                         self.eyelid_upper_close_mesh,
                         self.eyelid_lower_close_mesh,
                         self.eyelid_mid_mesh,
                         self.eyelid_upper_pin_mesh,
                         self.eyelid_lower_pin_mesh,
                         self.eyelid_upper_skin_mesh,
                         self.eyelid_lower_skin_mesh,
                         self.eyelid_upper_cls_mesh,
                         self.eyelid_lower_cls_mesh,
                         self.eyelid_upper_skin_pin_mesh,
                         self.eyelid_lower_skin_pin_mesh],
                        apply=True,
                        translate=True,
                        rotate=True)
        self.upper_close_bs = mc.blendShape(self.eyelid_lower_rest_mesh,
                                            self.eyelid_upper_close_mesh,
                                            name=self.generate_name("upperClose", "bs", "ctl"))[0]
        self.lower_close_bs = mc.blendShape(self.eyelid_upper_rest_mesh,
                                            self.eyelid_lower_close_mesh,
                                            name=self.generate_name("lowerClose", "bs", "ctl"))[0]
        mc.blendShape([self.eyelid_upper_close_mesh,
                       self.eyelid_lower_close_mesh,
                       self.eyelid_mid_mesh],
                      name=self.generate_name("mid", "bs", "ctl"),
                      weight=((0, 0.5), (1, 0.5)))
        self.upper_close_pin_bs = mc.blendShape([self.eyelid_upper_close_mesh,
                                                 self.eyelid_mid_mesh,
                                                 self.eyelid_upper_pin_mesh],
                                                name=self.generate_name("upperCloseTarget", "bs", "ctl"),
                                                weight=((0, 1), (1, 0)))[0]
        self.lower_close_pin_bs = mc.blendShape([self.eyelid_lower_close_mesh,
                                                 self.eyelid_mid_mesh,
                                                 self.eyelid_lower_pin_mesh],
                                                name=self.generate_name("lowerCloseTarget", "bs", "ctl"),
                                                weight=((0, 1), (1, 0)))[0]
        mc.blendShape(self.eyelid_upper_pin_mesh,
                      self.eyelid_upper_skin_mesh,
                      name=self.generate_name("upper", "bs", "ctl"),
                      weight=(0, 1))
        mc.blendShape(self.eyelid_lower_pin_mesh,
                      self.eyelid_lower_skin_mesh,
                      name=self.generate_name("lower", "bs", "ctl"),
                      weight=(0, 1))
        mc.blendShape(self.eyelid_upper_skin_mesh,
                      self.eyelid_upper_cls_mesh,
                      name=self.generate_name("upperCls", "bs", "ctl"),
                      origin="world",
                      weight=(0, 1))
        mc.blendShape(self.eyelid_lower_skin_mesh,
                      self.eyelid_lower_cls_mesh,
                      name=self.generate_name("lowerCls", "bs", "ctl"),
                      origin="world",
                      weight=(0, 1))
        mc.hide([self.eyelid_upper_rest_mesh,
                 self.eyelid_lower_rest_mesh,
                 self.eyelid_upper_close_mesh,
                 self.eyelid_lower_close_mesh,
                 self.eyelid_mid_mesh,
                 self.eyelid_upper_pin_mesh,
                 self.eyelid_lower_pin_mesh,
                 self.eyelid_upper_skin_mesh,
                 self.eyelid_lower_skin_mesh,
                 self.eyelid_upper_cls_mesh,
                 self.eyelid_lower_cls_mesh,
                 self.eyelid_upper_skin_pin_mesh,
                 self.eyelid_lower_skin_pin_mesh])
        skin_mesh_sets = mc.sets(name=self.generate_name("eyelidSkinMesh", "sets", "ctl"), empty=True)
        if "specific_sets" not in context:
            context["specific_sets"] = []
        context["specific_sets"].append(skin_mesh_sets)
        mc.sets([self.eyelid_upper_skin_mesh, self.eyelid_lower_skin_mesh], edit=True, addElement=skin_mesh_sets)

        self.eyelid_upper_crv = nurbs.create(parent=self.root,
                                             name=self.generate_name("eyelidUpper", "crv", "ctl"),
                                             degree=1,
                                             positions=[vector.get_position(x) for x in self.eyelid_upper_way],
                                             m=orig_m,
                                             ep=True,
                                             vis=False)
        self.eyelid_lower_crv = nurbs.create(parent=self.root,
                                             name=self.generate_name("eyelidLower", "crv", "ctl"),
                                             degree=1,
                                             positions=[vector.get_position(x) for x in self.eyelid_lower_way],
                                             m=orig_m,
                                             ep=True,
                                             vis=False)

        # skin layer
        m = matrix.set_matrix_scale(data["anchors"][4], (1, 1, -1))
        inner_vtx = mesh + ".vtx[" + str(eyelid_inner_vertex) + "]"
        outer_vtx = mesh + ".vtx[" + str(eyelid_outer_vertex) + "]"
        distance = vector.get_distance(vector.get_position(inner_vtx), vector.get_position(outer_vtx))
        self.inner_ctl, self.inner_loc = self.create_ctl(context=context,
                                                         parent=self.origin_space,
                                                         name=self.generate_name("inner", "", "ctl"),
                                                         parent_ctl=None,
                                                         attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                                         m=m,
                                                         cns=False,
                                                         mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                                         shape_args={
                                                             "shape": "arrow",
                                                             "width": distance / 5,
                                                             "color": (1, 0, 0),
                                                         },
                                                         mirror_ctl_name=self.generate_name("inner", "", "ctl", True))
        self.inner_jnt = joint.add_joint(self.origin_space,
                                         name=self.generate_name("inner", "jnt", "ctl"),
                                         m=m,
                                         vis=False)
        mc.parentConstraint(self.inner_ctl, self.inner_jnt, maintainOffset=True)
        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.inner_ctl + ".worldMatrix", mult_m + ".matrixIn[0]")
        mc.connectAttr(self.origin_space + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
        decom_m = mc.createNode("decomposeMatrix")
        mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
        mc.connectAttr(decom_m + ".outputScale", self.inner_jnt + ".s")

        m = matrix.set_matrix_scale(data["anchors"][3], (1, 1, 1))
        self.outer_ctl, self.outer_loc = self.create_ctl(context=context,
                                                         parent=self.origin_space,
                                                         name=self.generate_name("outer", "", "ctl"),
                                                         parent_ctl=None,
                                                         attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                                         m=m,
                                                         cns=False,
                                                         mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                                         shape_args={
                                                             "shape": "arrow",
                                                             "width": distance / 5,
                                                             "color": (1, 0, 0),
                                                         },
                                                         mirror_ctl_name=self.generate_name("outer", "", "ctl", True))
        self.outer_jnt = joint.add_joint(self.origin_space,
                                         name=self.generate_name("outer", "jnt", "ctl"),
                                         m=m,
                                         vis=False)
        mc.parentConstraint(self.outer_ctl, self.outer_jnt, maintainOffset=True)
        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.outer_ctl + ".worldMatrix", mult_m + ".matrixIn[0]")
        mc.connectAttr(self.origin_space + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
        decom_m = mc.createNode("decomposeMatrix")
        mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
        mc.connectAttr(decom_m + ".outputScale", self.outer_jnt + ".s")

        m = matrix.set_matrix_scale(data["anchors"][1], (1, 1, 1))
        self.upper_ctl, self.upper_loc = self.create_ctl(context=context,
                                                         parent=self.origin_space,
                                                         name=self.generate_name("upper", "", "ctl"),
                                                         parent_ctl=None,
                                                         attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                                         m=m,
                                                         cns=False,
                                                         mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                                         shape_args={
                                                             "shape": "arrow",
                                                             "width": distance / 5,
                                                             "color": (1, 0, 0),
                                                         },
                                                         mirror_ctl_name=self.generate_name("upper", "", "ctl", True))
        self.upper_jnt = joint.add_joint(parent=self.origin_space,
                                         name=self.generate_name("upper", "jnt", "ctl"),
                                         m=m,
                                         vis=False)
        mc.parentConstraint(self.upper_ctl, self.upper_jnt, maintainOffset=True)
        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.upper_ctl + ".worldMatrix", mult_m + ".matrixIn[0]")
        mc.connectAttr(self.origin_space + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
        decom_m = mc.createNode("decomposeMatrix")
        mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
        mc.connectAttr(decom_m + ".outputScale", self.upper_jnt + ".s")

        upper_driver_pin = mc.createNode("proximityPin")
        mc.setAttr(upper_driver_pin + ".offsetTranslation", 1)
        mc.setAttr(upper_driver_pin + ".offsetOrientation", 1)
        mc.connectAttr(self.eyelid_upper_pin_mesh + ".outMesh", upper_driver_pin + ".deformedGeometry")
        orig_shape = \
            mc.ls(mc.listRelatives(self.eyelid_upper_pin_mesh, noIntermediate=False), intermediateObjects=True)[0]
        mc.connectAttr(orig_shape + ".outMesh", upper_driver_pin + ".originalGeometry")

        temp = matrix.transform(parent=self.origin_space, name="TEMP", m=m)
        mc.setAttr(upper_driver_pin + ".inputMatrix[0]", mc.getAttr(temp + ".matrix"), type="matrix")
        mc.delete(temp)
        mc.connectAttr(upper_driver_pin + ".outputMatrix[0]",
                       hierarchy.get_parent(self.upper_ctl) + ".offsetParentMatrix")

        m = matrix.set_matrix_scale(data["anchors"][2], (1, 1, -1))
        self.lower_ctl, self.lower_loc = self.create_ctl(context=context,
                                                         parent=self.origin_space,
                                                         name=self.generate_name("lower", "", "ctl"),
                                                         parent_ctl=None,
                                                         attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                                         m=m,
                                                         cns=False,
                                                         mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                                         shape_args={
                                                             "shape": "arrow",
                                                             "width": distance / 5,
                                                             "color": (1, 0, 0),
                                                         },
                                                         mirror_ctl_name=self.generate_name("lower", "", "ctl", True))
        self.lower_jnt = joint.add_joint(parent=self.origin_space,
                                         name=self.generate_name("lower", "jnt", "ctl"),
                                         m=m,
                                         vis=False)
        mc.parentConstraint(self.lower_ctl, self.lower_jnt, maintainOffset=True)
        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.lower_ctl + ".worldMatrix", mult_m + ".matrixIn[0]")
        mc.connectAttr(self.origin_space + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
        decom_m = mc.createNode("decomposeMatrix")
        mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
        mc.connectAttr(decom_m + ".outputScale", self.lower_jnt + ".s")

        lower_driver_pin = mc.createNode("proximityPin")
        mc.setAttr(lower_driver_pin + ".offsetTranslation", 1)
        mc.setAttr(lower_driver_pin + ".offsetOrientation", 1)
        mc.connectAttr(self.eyelid_lower_pin_mesh + ".outMesh", lower_driver_pin + ".deformedGeometry")
        orig_shape = \
            mc.ls(mc.listRelatives(self.eyelid_lower_pin_mesh, noIntermediate=False), intermediateObjects=True)[0]
        mc.connectAttr(orig_shape + ".outMesh", lower_driver_pin + ".originalGeometry")

        temp = matrix.transform(parent=self.origin_space, name="TEMP", m=m)
        mc.setAttr(lower_driver_pin + ".inputMatrix[0]", mc.getAttr(temp + ".matrix"), type="matrix")
        mc.delete(temp)
        mc.connectAttr(lower_driver_pin + ".outputMatrix[0]",
                       hierarchy.get_parent(self.lower_ctl) + ".offsetParentMatrix")

        self.eyelid_upper_driver_sc = mc.skinCluster([self.inner_jnt,
                                                      self.outer_jnt,
                                                      self.upper_jnt],
                                                     self.eyelid_upper_skin_mesh,
                                                     name=self.generate_name("upperDriver", "sc", "ctl"),
                                                     toSelectedBones=True,
                                                     bindMethod=1,
                                                     normalizeWeights=1,
                                                     weightDistribution=1)[0]

        self.eyelid_lower_driver_sc = mc.skinCluster([self.inner_jnt,
                                                      self.outer_jnt,
                                                      self.lower_jnt],
                                                     self.eyelid_lower_skin_mesh,
                                                     name=self.generate_name("lowerDriver", "sc", "ctl"),
                                                     toSelectedBones=True,
                                                     bindMethod=1,
                                                     normalizeWeights=1,
                                                     weightDistribution=1)[0]

        npos = [hierarchy.get_parent(ctl) for ctl in [self.inner_ctl, self.outer_ctl, self.upper_ctl, self.lower_ctl]]
        jnts = [self.inner_jnt,
                self.outer_jnt,
                self.upper_jnt,
                self.lower_jnt]

        for npo, jnt in zip(npos, jnts):
            plugs = mc.listConnections(jnt, destination=True, source=False, plugs=True)
            for plug in plugs:
                if "matrix" in plug:
                    sc = plug.split(".")[0]
                    index = plug.split("[")[1][0]
                    npo_source = mc.listConnections(npo + ".offsetParentMatrix",
                                                    source=True,
                                                    destination=False,
                                                    plugs=True)
                    mult_m = mc.createNode("multMatrix")
                    if npo_source:
                        mc.connectAttr(npo_source[0], mult_m + ".matrixIn[0]")
                    else:
                        mc.setAttr(mult_m + ".matrixIn[0]", mc.getAttr(npo + ".offsetParentMatrix"), type="matrix")

                    inv_m = mc.createNode("inverseMatrix")
                    mc.connectAttr(mult_m + ".matrixSum", inv_m + ".inputMatrix")
                    mc.connectAttr(inv_m + ".outputMatrix", sc + ".bindPreMatrix[{0}]".format(index))

                    mc.connectAttr(jnt + ".matrix", plug, force=True)

        upper_skin_pin = mc.createNode("proximityPin")
        mc.setAttr(upper_skin_pin + ".offsetTranslation", 1)
        mc.setAttr(upper_skin_pin + ".offsetOrientation", 1)
        mc.connectAttr(self.eyelid_upper_skin_mesh + ".outMesh", upper_skin_pin + ".deformedGeometry")
        orig_shape = \
            mc.ls(mc.listRelatives(self.eyelid_upper_skin_mesh, noIntermediate=False), intermediateObjects=True)[0]
        mc.connectAttr(orig_shape + ".outMesh", upper_skin_pin + ".originalGeometry")

        m = matrix.set_matrix_scale(data["anchors"][5], (1, 1, 1))
        self.upper_outer_cns = matrix.transform(parent=self.origin_space,
                                                name=self.generate_name("upperOuter", "cns", "ctl"),
                                                m=matrix.get_matrix(self.origin_space))
        temp = matrix.transform(parent=self.origin_space, name="TEMP", m=m)
        mc.setAttr(upper_skin_pin + ".inputMatrix[0]", mc.getAttr(temp + ".matrix"), type="matrix")
        mc.delete(temp)
        mc.connectAttr(upper_skin_pin + ".outputMatrix[0]", self.upper_outer_cns + ".offsetParentMatrix")

        distance /= 2
        self.upper_outer_ctl, self.upper_outer_loc = self.create_ctl(context=context,
                                                                     parent=self.upper_outer_cns,
                                                                     name=self.generate_name("upperOuter", "", "ctl"),
                                                                     parent_ctl=None,
                                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                                     m=m,
                                                                     cns=False,
                                                                     mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                                                     shape_args={
                                                                         "shape": "arrow",
                                                                         "width": distance / 5,
                                                                         "color": (1, 0, 0),
                                                                     },
                                                                     mirror_ctl_name=self.generate_name("upperOuter",
                                                                                                        "",
                                                                                                        "ctl", True))
        self.upper_outer_jnt = joint.add_joint(self.upper_outer_cns,
                                               name=self.generate_name("upperOuter", "jnt", "ctl"),
                                               m=matrix.get_matrix(self.upper_outer_loc),
                                               vis=False)
        mc.pointConstraint(self.upper_outer_loc, self.upper_outer_jnt)
        mc.orientConstraint(self.upper_outer_loc, self.upper_outer_jnt)

        m = matrix.set_matrix_scale(data["anchors"][6], (1, 1, 1))
        self.upper_inner_cns = matrix.transform(parent=self.origin_space,
                                                name=self.generate_name("upperInner", "cns", "ctl"),
                                                m=matrix.get_matrix(self.origin_space))
        temp = matrix.transform(parent=self.origin_space, name="TEMP", m=m)
        mc.setAttr(upper_skin_pin + ".inputMatrix[1]", mc.getAttr(temp + ".matrix"), type="matrix")
        mc.delete(temp)
        mc.connectAttr(upper_skin_pin + ".outputMatrix[1]", self.upper_inner_cns + ".offsetParentMatrix")

        self.upper_inner_ctl, self.upper_inner_loc = self.create_ctl(context=context,
                                                                     parent=self.upper_inner_cns,
                                                                     name=self.generate_name("upperInner", "", "ctl"),
                                                                     parent_ctl=None,
                                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                                     m=m,
                                                                     cns=False,
                                                                     mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                                                     shape_args={
                                                                         "shape": "arrow",
                                                                         "width": distance / 5,
                                                                         "color": (1, 0, 0),
                                                                     },
                                                                     mirror_ctl_name=self.generate_name("upperInner",
                                                                                                        "",
                                                                                                        "ctl", True))
        self.upper_inner_jnt = joint.add_joint(self.upper_inner_cns,
                                               name=self.generate_name("upperInner", "jnt", "ctl"),
                                               m=matrix.get_matrix(self.upper_inner_loc),
                                               vis=False)
        mc.pointConstraint(self.upper_inner_loc, self.upper_inner_jnt)
        mc.orientConstraint(self.upper_inner_loc, self.upper_inner_jnt)

        lower_skin_pin = mc.createNode("proximityPin")
        mc.setAttr(lower_skin_pin + ".offsetTranslation", 1)
        mc.setAttr(lower_skin_pin + ".offsetOrientation", 1)
        mc.connectAttr(self.eyelid_lower_skin_mesh + ".outMesh", lower_skin_pin + ".deformedGeometry")
        orig_shape = \
            mc.ls(mc.listRelatives(self.eyelid_lower_skin_mesh, noIntermediate=False), intermediateObjects=True)[0]
        mc.connectAttr(orig_shape + ".outMesh", lower_skin_pin + ".originalGeometry")

        m = matrix.set_matrix_scale(data["anchors"][7], (1, 1, 1))
        self.lower_outer_cns = matrix.transform(parent=self.origin_space,
                                                name=self.generate_name("lowerOuter", "cns", "ctl"),
                                                m=matrix.get_matrix(self.origin_space))
        temp = matrix.transform(parent=self.origin_space, name="TEMP", m=m)
        mc.setAttr(lower_skin_pin + ".inputMatrix[0]", mc.getAttr(temp + ".matrix"), type="matrix")
        mc.delete(temp)
        mc.connectAttr(lower_skin_pin + ".outputMatrix[0]", self.lower_outer_cns + ".offsetParentMatrix")

        self.lower_outer_ctl, self.lower_outer_loc = self.create_ctl(context=context,
                                                                     parent=self.lower_outer_cns,
                                                                     name=self.generate_name("lowerOuter", "", "ctl"),
                                                                     parent_ctl=None,
                                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                                     m=m,
                                                                     cns=False,
                                                                     mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                                                     shape_args={
                                                                         "shape": "arrow",
                                                                         "width": distance / 5,
                                                                         "color": (1, 0, 0),
                                                                     },
                                                                     mirror_ctl_name=self.generate_name("lowerOuter",
                                                                                                        "",
                                                                                                        "ctl", True))
        self.lower_outer_jnt = joint.add_joint(self.lower_outer_cns,
                                               name=self.generate_name("lowerOuter", "jnt", "ctl"),
                                               m=matrix.get_matrix(self.lower_outer_loc),
                                               vis=False)
        mc.pointConstraint(self.lower_outer_loc, self.lower_outer_jnt)
        mc.orientConstraint(self.lower_outer_loc, self.lower_outer_jnt)

        m = matrix.set_matrix_scale(data["anchors"][8], (1, 1, 1))
        self.lower_inner_cns = matrix.transform(parent=self.origin_space,
                                                name=self.generate_name("lowerInner", "cns", "ctl"),
                                                m=matrix.get_matrix(self.origin_space))
        temp = matrix.transform(parent=self.origin_space, name="TEMP", m=m)
        mc.setAttr(lower_skin_pin + ".inputMatrix[1]", mc.getAttr(temp + ".matrix"), type="matrix")
        mc.delete(temp)
        mc.connectAttr(lower_skin_pin + ".outputMatrix[1]", self.lower_inner_cns + ".offsetParentMatrix")

        self.lower_inner_ctl, self.lower_inner_loc = self.create_ctl(context=context,
                                                                     parent=self.lower_inner_cns,
                                                                     name=self.generate_name("lowerInner", "", "ctl"),
                                                                     parent_ctl=None,
                                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                                     m=m,
                                                                     cns=False,
                                                                     mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                                                     shape_args={
                                                                         "shape": "arrow",
                                                                         "width": distance / 5,
                                                                         "color": (1, 0, 0),
                                                                     },
                                                                     mirror_ctl_name=self.generate_name("lowerInner",
                                                                                                        "",
                                                                                                        "ctl", True))
        self.lower_inner_jnt = joint.add_joint(self.lower_inner_cns,
                                               name=self.generate_name("lowerInner", "jnt", "ctl"),
                                               m=matrix.get_matrix(self.lower_inner_loc),
                                               vis=False)
        mc.pointConstraint(self.lower_inner_loc, self.lower_inner_jnt)
        mc.orientConstraint(self.lower_inner_loc, self.lower_inner_jnt)

        self.upper_outer_cls = mc.cluster(self.eyelid_upper_cls_mesh,
                                          name=self.generate_name("upperOuter", "cls", "ctl"),
                                          bindState=1,
                                          weightedNode=(self.upper_outer_jnt, self.upper_outer_jnt))[0]
        handle = \
            mc.listConnections(self.upper_outer_cls, source=True, destination=False, type="clusterHandle", shapes=True)[
                0]
        mc.rename(handle, self.upper_outer_cls + "Handle")
        npo = hierarchy.get_parent(self.upper_outer_ctl)
        mc.connectAttr(npo + ".worldInverseMatrix[0]", self.upper_outer_cls + ".bindPreMatrix")
        self.upper_outer_falloff = mc.createNode("primitiveFalloff",
                                                 name=self.generate_name("upperOuter", "falloff", "ctl"),
                                                 parent=context["xxx"])
        matrix.set_matrix(self.upper_outer_falloff, matrix.get_matrix(self.root))
        mc.setAttr(self.upper_outer_falloff + ".primitive", 1)
        mc.setAttr(self.upper_outer_falloff + ".start", distance * -1)
        mc.setAttr(self.upper_outer_falloff + ".end", distance)
        mc.setAttr(self.upper_outer_falloff + ".ramp[0].ramp_Interp", 2)
        mc.setAttr(self.upper_outer_falloff + ".ramp[1].ramp_Interp", 2)
        mc.setAttr(self.upper_outer_falloff + ".ramp[2].ramp_Interp", 2)
        mc.setAttr(self.upper_outer_falloff + ".ramp[0].ramp_Position", 0.25)
        mc.setAttr(self.upper_outer_falloff + ".ramp[0].ramp_FloatValue", 0)
        mc.setAttr(self.upper_outer_falloff + ".ramp[1].ramp_Position", 0.8)
        mc.setAttr(self.upper_outer_falloff + ".ramp[1].ramp_FloatValue", 1)
        mc.setAttr(self.upper_outer_falloff + ".ramp[2].ramp_Position", 1)
        mc.setAttr(self.upper_outer_falloff + ".ramp[2].ramp_FloatValue", 0)
        mc.connectAttr(self.upper_outer_falloff + ".outputWeightFunction", self.upper_outer_cls + ".weightFunction[0]")

        self.upper_inner_cls = mc.cluster(self.eyelid_upper_cls_mesh,
                                          name=self.generate_name("upperInner", "cls", "ctl"),
                                          bindState=1,
                                          weightedNode=(self.upper_inner_jnt, self.upper_inner_jnt))[0]
        handle = \
            mc.listConnections(self.upper_inner_cls, source=True, destination=False, type="clusterHandle", shapes=True)[
                0]
        mc.rename(handle, self.upper_inner_cls + "Handle")
        npo = hierarchy.get_parent(self.upper_inner_ctl)
        mc.connectAttr(npo + ".worldInverseMatrix[0]", self.upper_inner_cls + ".bindPreMatrix")
        self.upper_inner_falloff = mc.createNode("primitiveFalloff",
                                                 name=self.generate_name("upperInner", "falloff", "ctl"),
                                                 parent=context["xxx"])
        matrix.set_matrix(self.upper_inner_falloff, matrix.get_matrix(self.root))
        mc.setAttr(self.upper_inner_falloff + ".primitive", 1)
        mc.setAttr(self.upper_inner_falloff + ".start", distance * -1)
        mc.setAttr(self.upper_inner_falloff + ".end", distance)
        mc.setAttr(self.upper_inner_falloff + ".ramp[0].ramp_Interp", 2)
        mc.setAttr(self.upper_inner_falloff + ".ramp[1].ramp_Interp", 2)
        mc.setAttr(self.upper_inner_falloff + ".ramp[2].ramp_Interp", 2)
        mc.setAttr(self.upper_inner_falloff + ".ramp[0].ramp_Position", 0)
        mc.setAttr(self.upper_inner_falloff + ".ramp[0].ramp_FloatValue", 0)
        mc.setAttr(self.upper_inner_falloff + ".ramp[1].ramp_Position", 0.2)
        mc.setAttr(self.upper_inner_falloff + ".ramp[1].ramp_FloatValue", 1)
        mc.setAttr(self.upper_inner_falloff + ".ramp[2].ramp_Position", 0.5)
        mc.setAttr(self.upper_inner_falloff + ".ramp[2].ramp_FloatValue", 0)
        mc.connectAttr(self.upper_inner_falloff + ".outputWeightFunction", self.upper_inner_cls + ".weightFunction[0]")

        self.lower_outer_cls = mc.cluster(self.eyelid_lower_cls_mesh,
                                          name=self.generate_name("lowerOuter", "cls", "ctl"),
                                          bindState=1,
                                          weightedNode=(self.lower_outer_jnt, self.lower_outer_jnt))[0]
        handle = \
            mc.listConnections(self.lower_outer_cls, source=True, destination=False, type="clusterHandle", shapes=True)[
                0]
        mc.rename(handle, self.lower_outer_cls + "Handle")
        npo = hierarchy.get_parent(self.lower_outer_ctl)
        mc.connectAttr(npo + ".worldInverseMatrix[0]", self.lower_outer_cls + ".bindPreMatrix")
        self.lower_outer_falloff = mc.createNode("primitiveFalloff",
                                                 name=self.generate_name("lowerOuter", "falloff", "ctl"),
                                                 parent=context["xxx"])
        matrix.set_matrix(self.lower_outer_falloff, matrix.get_matrix(self.root))
        mc.setAttr(self.lower_outer_falloff + ".primitive", 1)
        mc.setAttr(self.lower_outer_falloff + ".start", distance * -1)
        mc.setAttr(self.lower_outer_falloff + ".end", distance)
        mc.setAttr(self.lower_outer_falloff + ".ramp[0].ramp_Interp", 2)
        mc.setAttr(self.lower_outer_falloff + ".ramp[1].ramp_Interp", 2)
        mc.setAttr(self.lower_outer_falloff + ".ramp[2].ramp_Interp", 2)
        mc.setAttr(self.lower_outer_falloff + ".ramp[0].ramp_Position", 0.5)
        mc.setAttr(self.lower_outer_falloff + ".ramp[0].ramp_FloatValue", 0)
        mc.setAttr(self.lower_outer_falloff + ".ramp[1].ramp_Position", 0.8)
        mc.setAttr(self.lower_outer_falloff + ".ramp[1].ramp_FloatValue", 1)
        mc.setAttr(self.lower_outer_falloff + ".ramp[2].ramp_Position", 1)
        mc.setAttr(self.lower_outer_falloff + ".ramp[2].ramp_FloatValue", 0)
        mc.connectAttr(self.lower_outer_falloff + ".outputWeightFunction", self.lower_outer_cls + ".weightFunction[0]")

        self.lower_inner_cls = mc.cluster(self.eyelid_lower_cls_mesh,
                                          name=self.generate_name("lowerInner", "cls", "ctl"),
                                          bindState=1,
                                          weightedNode=(self.lower_inner_jnt, self.lower_inner_jnt))[0]
        handle = \
            mc.listConnections(self.lower_inner_cls, source=True, destination=False, type="clusterHandle", shapes=True)[
                0]
        mc.rename(handle, self.lower_inner_cls + "Handle")
        npo = hierarchy.get_parent(self.lower_inner_ctl)
        mc.connectAttr(npo + ".worldInverseMatrix[0]", self.lower_inner_cls + ".bindPreMatrix")
        self.lower_inner_falloff = mc.createNode("primitiveFalloff",
                                                 name=self.generate_name("lowerInner", "falloff", "ctl"),
                                                 parent=context["xxx"])
        matrix.set_matrix(self.lower_inner_falloff, matrix.get_matrix(self.root))
        mc.setAttr(self.lower_inner_falloff + ".primitive", 1)
        mc.setAttr(self.lower_inner_falloff + ".start", distance * -1)
        mc.setAttr(self.lower_inner_falloff + ".end", distance)
        mc.setAttr(self.lower_inner_falloff + ".ramp[0].ramp_Interp", 2)
        mc.setAttr(self.lower_inner_falloff + ".ramp[1].ramp_Interp", 2)
        mc.setAttr(self.lower_inner_falloff + ".ramp[2].ramp_Interp", 2)
        mc.setAttr(self.lower_inner_falloff + ".ramp[0].ramp_Position", 0)
        mc.setAttr(self.lower_inner_falloff + ".ramp[0].ramp_FloatValue", 0)
        mc.setAttr(self.lower_inner_falloff + ".ramp[1].ramp_Position", 0.2)
        mc.setAttr(self.lower_inner_falloff + ".ramp[1].ramp_FloatValue", 1)
        mc.setAttr(self.lower_inner_falloff + ".ramp[2].ramp_Position", 0.5)
        mc.setAttr(self.lower_inner_falloff + ".ramp[2].ramp_FloatValue", 0)
        mc.connectAttr(self.lower_inner_falloff + ".outputWeightFunction", self.lower_inner_cls + ".weightFunction[0]")
        mc.hide(
            [self.lower_outer_falloff, self.lower_inner_falloff, self.upper_outer_falloff, self.upper_inner_falloff])

        upper_cls_pin = mc.createNode("proximityPin")
        mc.setAttr(upper_cls_pin + ".offsetTranslation", 1)
        mc.setAttr(upper_cls_pin + ".offsetOrientation", 1)
        mc.connectAttr(self.eyelid_upper_cls_mesh + ".outMesh", upper_cls_pin + ".deformedGeometry")
        orig_shape = \
            mc.ls(mc.listRelatives(self.eyelid_upper_cls_mesh, noIntermediate=False), intermediateObjects=True)[0]
        mc.connectAttr(orig_shape + ".outMesh", upper_cls_pin + ".originalGeometry")

        upper_pos = [vector.get_position(x) for x in self.eyelid_upper_way]
        self.upper_aim_npos = []
        self.upper_aim_jnts = []
        v = vector.get_position(self.root)
        up_obj = matrix.transform(parent=None,
                                  name=self.generate_name("aim", "up", "ctl"),
                                  m=m)
        mc.setAttr(up_obj + ".t", v[0], v[1] + 1, v[2])
        up_obj = mc.parent(up_obj, self.root)[0]
        for i, pos in enumerate(upper_pos):
            temp = matrix.transform(parent=None, name="TEMP", m=orig_m)
            mc.setAttr(temp + ".t", *pos)

            mc.setAttr(upper_cls_pin + ".inputMatrix[{0}]".format(i), mc.getAttr(temp + ".matrix"), type="matrix")

            aim_m = mc.createNode("aimMatrix")
            mc.setAttr(aim_m + ".primaryMode", 1)
            mc.setAttr(aim_m + ".secondaryMode", 1)
            mc.setAttr(aim_m + ".inputMatrix", mc.getAttr(self.root + ".worldMatrix[0]"), type="matrix")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(upper_cls_pin + ".outputMatrix[{0}]".format(i), mult_m + ".matrixIn[0]")
            mc.connectAttr(self.origin_space + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            mc.connectAttr(mult_m + ".matrixSum", aim_m + ".primaryTargetMatrix")
            mc.connectAttr(up_obj + ".matrix", aim_m + ".secondaryTargetMatrix")

            aim_npo = matrix.transform(parent=self.origin_space,
                                       name=self.generate_name("upperAim{0}".format(i), "npo", "ctl"),
                                       m=matrix.get_matrix(self.origin_space))
            mc.connectAttr(aim_m + ".outputMatrix", aim_npo + ".offsetParentMatrix")

            aim_jnt = joint.add_joint(parent=aim_npo,
                                      name=self.generate_name("upperAim{0}".format(i), "jnt", "ctl"),
                                      m=matrix.get_matrix(temp),
                                      vis=False)
            mc.setAttr(aim_jnt + ".jointOrient", 0, 0, 0)
            mc.delete(temp)
            self.upper_aim_npos.append(aim_npo)
            self.upper_aim_jnts.append(aim_jnt)
        self.eyelid_upper_skin_pin_sc = mc.skinCluster(self.upper_aim_jnts,
                                                       self.eyelid_upper_skin_pin_mesh,
                                                       name=self.generate_name("upperPinDriver", "sc", "ctl"),
                                                       toSelectedBones=True,
                                                       bindMethod=1,
                                                       normalizeWeights=1,
                                                       weightDistribution=1)[0]
        for i, aim_jnt in enumerate(self.upper_aim_jnts):
            vtx = self.eyelid_upper_skin_pin_mesh + ".vtx[{0}:{1}]".format(i * 3, i * 3 + 3)
            mc.skinPercent(self.eyelid_upper_skin_pin_sc, vtx, transformValue=((aim_jnt, 1)))

        for i, aim_jnt in enumerate(self.upper_aim_jnts):
            plug = mc.listConnections(aim_jnt + ".worldMatrix[0]", source=False, destination=True, plugs=True)[0]
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(aim_jnt + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.eyelid_upper_skin_pin_mesh + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
            mc.setAttr(mult_m + ".matrixIn[2]", mc.getAttr(self.eyelid_upper_skin_pin_mesh + ".worldMatrix[0]"),
                       type="matrix")
            mc.connectAttr(mult_m + ".matrixSum", plug, force=True)

        lower_cls_pin = mc.createNode("proximityPin")
        mc.setAttr(lower_cls_pin + ".offsetTranslation", 1)
        mc.setAttr(lower_cls_pin + ".offsetOrientation", 1)
        mc.connectAttr(self.eyelid_lower_cls_mesh + ".outMesh", lower_cls_pin + ".deformedGeometry")
        orig_shape = \
            mc.ls(mc.listRelatives(self.eyelid_lower_cls_mesh, noIntermediate=False), intermediateObjects=True)[0]
        mc.connectAttr(orig_shape + ".outMesh", lower_cls_pin + ".originalGeometry")

        lower_pos = [vector.get_position(x) for x in self.eyelid_lower_way]
        self.lower_aim_npos = []
        self.lower_aim_jnts = []
        for i, pos in enumerate(lower_pos):
            temp = matrix.transform(parent=None, name="TEMP", m=orig_m)
            mc.setAttr(temp + ".t", *pos)

            mc.setAttr(lower_cls_pin + ".inputMatrix[{0}]".format(i), mc.getAttr(temp + ".matrix"), type="matrix")

            aim_m = mc.createNode("aimMatrix")
            mc.setAttr(aim_m + ".primaryMode", 1)
            mc.setAttr(aim_m + ".secondaryMode", 1)
            mc.setAttr(aim_m + ".inputMatrix", mc.getAttr(self.root + ".worldMatrix[0]"), type="matrix")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(lower_cls_pin + ".outputMatrix[{0}]".format(i), mult_m + ".matrixIn[0]")
            mc.connectAttr(self.origin_space + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            mc.connectAttr(mult_m + ".matrixSum", aim_m + ".primaryTargetMatrix")
            mc.connectAttr(up_obj + ".matrix", aim_m + ".secondaryTargetMatrix")

            aim_npo = matrix.transform(parent=self.origin_space,
                                       name=self.generate_name("lowerAim{0}".format(i), "npo", "ctl"),
                                       m=matrix.get_matrix(self.origin_space))
            mc.connectAttr(aim_m + ".outputMatrix", aim_npo + ".offsetParentMatrix")

            aim_jnt = joint.add_joint(parent=aim_npo,
                                      name=self.generate_name("lowerAim{0}".format(i), "jnt", "ctl"),
                                      m=matrix.get_matrix(temp),
                                      vis=False)
            mc.setAttr(aim_jnt + ".jointOrient", 0, 0, 0)
            mc.delete(temp)
            self.lower_aim_npos.append(aim_npo)
            self.lower_aim_jnts.append(aim_jnt)
        self.eyelid_lower_skin_pin_sc = mc.skinCluster(self.lower_aim_jnts,
                                                       self.eyelid_lower_skin_pin_mesh,
                                                       name=self.generate_name("lowerPinDriver", "sc", "ctl"),
                                                       toSelectedBones=True,
                                                       bindMethod=1,
                                                       normalizeWeights=1,
                                                       weightDistribution=1)[0]
        for i, aim_jnt in enumerate(self.lower_aim_jnts):
            vtx = self.eyelid_lower_skin_pin_mesh + ".vtx[{0}:{1}]".format(i * 3, i * 3 + 3)
            mc.skinPercent(self.eyelid_lower_skin_pin_sc, vtx, transformValue=((aim_jnt, 1)))

        for i, aim_jnt in enumerate(self.lower_aim_jnts):
            plug = mc.listConnections(aim_jnt + ".worldMatrix[0]", source=False, destination=True, plugs=True)[0]
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(aim_jnt + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.eyelid_lower_skin_pin_mesh + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
            mc.setAttr(mult_m + ".matrixIn[2]", mc.getAttr(self.eyelid_lower_skin_pin_mesh + ".worldMatrix[0]"),
                       type="matrix")
            mc.connectAttr(mult_m + ".matrixSum", plug, force=True)

        # eye hole
        mesh = data["mesh"]
        eye_hole_vertex_loop = polygon.convert_component([mesh + ".e[" + str(i) + "]" for i in eye_hole_vertex_loop],
                                                         vertex=True)

        eye_hole_inner_vertex = int(data["eye_hole_inner_vertex"])
        eye_hole_outer_vertex = int(data["eye_hole_outer_vertex"])

        way1, way2 = polygon.loop_to_2way(loop=eye_hole_vertex_loop,
                                          start_vertex=mesh + ".vtx[" + str(eye_hole_inner_vertex) + "]",
                                          end_vertex=mesh + ".vtx[" + str(eye_hole_outer_vertex) + "]")
        if vector.get_position(way1[int(len(way1) / 2)])[1] > vector.get_position(way2[int(len(way2) / 2)])[1]:
            self.eye_hole_upper_way = way1
            self.eye_hole_lower_way = way2
        else:
            self.eye_hole_upper_way = way2
            self.eye_hole_lower_way = way1

        self.eye_hole_upper_rest_mesh = polygon.point_to_mesh(parent=self.root,
                                                              name=self.generate_name("eyeHoleUpperRest", "mesh",
                                                                                      "ctl"),
                                                              points=[vector.get_position(x) for x in
                                                                      self.eye_hole_upper_way])
        self.eye_hole_lower_rest_mesh = polygon.point_to_mesh(parent=self.root,
                                                              name=self.generate_name("eyeHoleLowerRest", "mesh",
                                                                                      "ctl"),
                                                              points=[vector.get_position(x) for x in
                                                                      self.eye_hole_lower_way])
        way1_offset = int(len(self.eye_hole_upper_way) / 4)
        way2_offset = int(len(self.eye_hole_lower_way) / 4)
        points1 = []
        points2 = []
        for i in range(4):
            index = i * way1_offset
            points1.insert(i, vector.get_position(self.eye_hole_upper_way[index]))

            index = (i + 1) * way2_offset
            points2.insert(i * -1, vector.get_position(self.eye_hole_lower_way[index]))
        self.driver_crv = mc.curve(degree=3,
                                   periodic=True,
                                   name=self.generate_name("eyeHoleDriver", "crv", "ctl"),
                                   point=points1 + points2 + points1[:3],
                                   knot=list(range(-2, 11)))
        self.driver_crv = mc.parent(self.driver_crv, self.root)[0]
        mc.makeIdentity([self.eye_hole_upper_rest_mesh,
                         self.eye_hole_lower_rest_mesh,
                         self.driver_crv],
                        apply=True,
                        translate=True,
                        rotate=True,
                        scale=True)
        mc.hide([self.eye_hole_upper_rest_mesh,
                 self.eye_hole_lower_rest_mesh,
                 self.driver_crv])

        self.hole_ctls = []
        for i, p in enumerate(points1 + points2):
            m = matrix.set_matrix_translate(orig_m, p)
            ctl, loc = self.create_ctl(context=context,
                                       parent=None,
                                       name=self.generate_name("eyeHole{0}".format(i), "", "ctl"),
                                       parent_ctl=None,
                                       attrs=["tx", "ty", "tz"],
                                       m=m,
                                       cns=False,
                                       mirror_config=(0, 0, 0, 1, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "circle3",
                                           "width": distance / 5,
                                           "color": (1, 0, 0),
                                       },
                                       mirror_ctl_name=self.generate_name("eyeHole{0}".format(i), "", "ctl", True))
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(loc + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.root + ".worldInverseMatrix", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", self.driver_crv + ".cv[{0}]".format(i))

        wire = mc.wire(self.eye_hole_upper_rest_mesh, wire=self.driver_crv)[0]
        mc.setAttr(wire + ".rotation", 0)
        mc.setAttr(wire + ".dropoffDistance[0]", 999)
        wire = mc.wire(self.eye_hole_lower_rest_mesh, wire=self.driver_crv)[0]
        mc.setAttr(wire + ".rotation", 0)
        mc.setAttr(wire + ".dropoffDistance[0]", 999)

        hole_upper_pin = mc.createNode("proximityPin")
        mc.setAttr(hole_upper_pin + ".offsetTranslation", 1)
        mc.connectAttr(self.eye_hole_upper_rest_mesh + ".outMesh", hole_upper_pin + ".deformedGeometry")
        orig_shape = \
            mc.ls(mc.listRelatives(self.eye_hole_upper_rest_mesh, noIntermediate=False), intermediateObjects=True)[0]
        mc.connectAttr(orig_shape + ".outMesh", hole_upper_pin + ".originalGeometry")

        upper_pos = [vector.get_position(x) for x in self.eye_hole_upper_way]
        self.hole_upper_aim_jnts = []
        for i, pos in enumerate(upper_pos[1:-1]):
            temp = matrix.transform(parent=None, name="TEMP", m=orig_m)
            mc.setAttr(temp + ".t", *pos)
            temp = mc.parent(temp, self.root)[0]

            mc.setAttr(hole_upper_pin + ".inputMatrix[{0}]".format(i), mc.getAttr(temp + ".matrix"), type="matrix")

            jnt = joint.add_joint(parent=self.root,
                                  name=self.generate_name("eyeHoleUpper{0}".format(i), "jnt", "ctl"),
                                  m=matrix.get_matrix(temp),
                                  vis=False)

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(hole_upper_pin + ".outputMatrix[{0}]".format(i), decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", jnt + ".t")
            mc.connectAttr(decom_m + ".outputScale", jnt + ".s")
            mc.connectAttr(decom_m + ".outputShear", jnt + ".shear")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(hole_upper_pin + ".outputMatrix[{0}]".format(i), mult_m + ".matrixIn[0]")
            inv_m = om2.MMatrix(mc.getAttr(hole_upper_pin + ".outputMatrix[{0}]".format(i))).inverse()
            mc.setAttr(mult_m + ".matrixIn[1]", inv_m, type="matrix")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputRotate", jnt + ".r")
            mc.delete(temp)
            self.hole_upper_aim_jnts.append(jnt)

        hole_lower_pin = mc.createNode("proximityPin")
        mc.setAttr(hole_lower_pin + ".offsetTranslation", 1)
        mc.connectAttr(self.eye_hole_lower_rest_mesh + ".outMesh", hole_lower_pin + ".deformedGeometry")
        orig_shape = \
            mc.ls(mc.listRelatives(self.eye_hole_lower_rest_mesh, noIntermediate=False), intermediateObjects=True)[0]
        mc.connectAttr(orig_shape + ".outMesh", hole_lower_pin + ".originalGeometry")

        lower_pos = [vector.get_position(x) for x in self.eye_hole_lower_way]
        self.hole_lower_aim_jnts = []
        for i, pos in enumerate(lower_pos[1:-1]):
            temp = matrix.transform(parent=None, name="TEMP", m=orig_m)
            mc.setAttr(temp + ".t", *pos)
            temp = mc.parent(temp, self.root)[0]

            mc.setAttr(hole_lower_pin + ".inputMatrix[{0}]".format(i), mc.getAttr(temp + ".matrix"), type="matrix")

            jnt = joint.add_joint(parent=self.root,
                                  name=self.generate_name("eyeHoleLower{0}".format(i), "jnt", "ctl"),
                                  m=matrix.get_matrix(temp),
                                  vis=False)

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(hole_lower_pin + ".outputMatrix[{0}]".format(i), decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", jnt + ".t")
            mc.connectAttr(decom_m + ".outputScale", jnt + ".s")
            mc.connectAttr(decom_m + ".outputShear", jnt + ".shear")

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(hole_lower_pin + ".outputMatrix[{0}]".format(i), mult_m + ".matrixIn[0]")
            inv_m = om2.MMatrix(mc.getAttr(hole_lower_pin + ".outputMatrix[{0}]".format(i))).inverse()
            mc.setAttr(mult_m + ".matrixIn[1]", inv_m, type="matrix")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputRotate", jnt + ".r")
            mc.delete(temp)
            self.hole_lower_aim_jnts.append(jnt)

        # refs, jnts
        self.upper_refs = []
        self.lower_refs = []
        self.upper_jnts = []
        self.lower_jnts = []
        up_obj = matrix.transform(parent=self.origin_space,
                                  name=self.generate_name("ref", "up", "ctl"),
                                  m=matrix.get_matrix(self.root))
        for i, aim_jnts in enumerate([self.upper_aim_jnts, self.lower_aim_jnts]):
            if i == 0:
                s = "upper"
                mesh = self.eyelid_upper_skin_pin_mesh
                refs = self.upper_refs
                jnts = self.upper_jnts
            else:
                s = "lower"
                mesh = self.eyelid_lower_skin_pin_mesh
                refs = self.lower_refs
                jnts = self.lower_jnts
            pin = mc.createNode("proximityPin")
            mc.setAttr(pin + ".offsetTranslation", 1)
            mc.setAttr(pin + ".offsetOrientation", 1)
            mc.connectAttr(mesh + ".outMesh", pin + ".deformedGeometry")
            orig_shape = \
                mc.ls(mc.listRelatives(mesh, noIntermediate=False), intermediateObjects=True)[0]
            mc.connectAttr(orig_shape + ".outMesh", pin + ".originalGeometry")
            grp = matrix.transform(parent=self.origin_space,
                                   name=self.generate_name(s + "Result", "grp", "ctl"),
                                   m=matrix.get_matrix(self.origin_space))
            for index, aim_jnt in enumerate(aim_jnts[1:-1]):
                name = s + str(index)
                jnt_m = matrix.get_matrix(aim_jnt)
                mc.setAttr(pin + ".inputMatrix[{0}]".format(index), jnt_m, type="matrix")

                aim_m = mc.createNode("aimMatrix")
                mc.setAttr(aim_m + ".primaryMode", 1)
                mc.setAttr(aim_m + ".secondaryMode", 1)
                mc.connectAttr(pin + ".outputMatrix[{0}]".format(index), aim_m + ".inputMatrix")

                mult_m = mc.createNode("multMatrix")
                mc.connectAttr(aim_jnts[index + 2] + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
                mc.connectAttr(grp + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
                mc.connectAttr(mult_m + ".matrixSum", aim_m + ".primaryTargetMatrix")
                mc.connectAttr(up_obj + ".matrix", aim_m + ".secondaryTargetMatrix")

                source = matrix.transform(parent=grp,
                                          name=self.generate_name(name, "source", "ctl"),
                                          m=matrix.get_matrix(self.origin_space))
                mc.connectAttr(aim_m + ".outputMatrix", source + ".offsetParentMatrix")

                # refs
                ref = self.create_ref(context=context,
                                      name=self.generate_name(name, "ref", "ctl"),
                                      anchor=True,
                                      m=source)
                refs.append(ref)

                # jnts
                if data["create_jnt"]:
                    uni_scale = False
                    if assembly_data["force_uni_scale"]:
                        uni_scale = True
                    name = self.generate_name("{0}{1}".format(s, index), "", "jnt")
                    jnt = self.create_jnt(context=context,
                                          parent=None,
                                          name=name,
                                          description="{0}{1}".format(s, i),
                                          ref=ref,
                                          m=matrix.get_matrix(ref),
                                          leaf=False,
                                          uni_scale=uni_scale)
                    jnts.append(jnt)

    def attributes(self, context):
        super().attributes(context)

        data = self.component.data["value"]

        # close attribute
        self.upper_close_attr = attribute.add_attr(self.upper_ctl,
                                                   longName="close",
                                                   type="double",
                                                   keyable=True,
                                                   minValue=0,
                                                   defaultValue=0)
        self.lower_close_attr = attribute.add_attr(self.lower_ctl,
                                                   longName="close",
                                                   type="double",
                                                   keyable=True,
                                                   minValue=0,
                                                   defaultValue=0)
        # follow line of sight
        self.upper_follow_los_attr = attribute.add_attr(self.upper_ctl,
                                                        longName="line_of_sight",
                                                        type="double",
                                                        keyable=True,
                                                        minValue=0,
                                                        maxValue=1,
                                                        defaultValue=0.3)
        self.lower_follow_los_attr = attribute.add_attr(self.lower_ctl,
                                                        longName="line_of_sight",
                                                        type="double",
                                                        keyable=True,
                                                        minValue=0,
                                                        maxValue=1,
                                                        defaultValue=0.3)

        # sub ctl visibility
        self.sub_ctl_vis_attr = attribute.add_attr(self.host,
                                                   longName="sub_ctl_vis",
                                                   type="double",
                                                   keyable=True,
                                                   minValue=0,
                                                   maxValue=1,
                                                   defaultValue=0)

    def operators(self, context):
        super().operators(context)

        data = self.component.data["value"]
        orig_m = om2.MMatrix()

        # close attribute connect
        target = mc.blendShape(self.upper_close_bs, query=True, target=True)[0]
        mc.connectAttr(self.upper_close_attr, self.upper_close_bs + "." + target)
        target = mc.blendShape(self.lower_close_bs, query=True, target=True)[0]
        mc.connectAttr(self.lower_close_attr, self.lower_close_bs + "." + target)

        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".operation", 2)
        mc.setAttr(pma + ".input1D[0]", 1)
        mc.connectAttr(self.lower_close_attr, pma + ".input1D[1]")

        condition = mc.createNode("condition")
        mc.setAttr(condition + ".operation", 4)
        mc.connectAttr(self.upper_close_attr, condition + ".firstTerm")
        mc.connectAttr(pma + ".output1D", condition + ".secondTerm")
        mc.setAttr(condition + ".colorIfTrueR", 1)
        mc.setAttr(condition + ".colorIfFalseR", 0)
        mc.setAttr(condition + ".colorIfTrueG", 0)
        mc.setAttr(condition + ".colorIfFalseG", 1)

        target = mc.blendShape(self.upper_close_pin_bs, query=True, target=True)
        mc.connectAttr(condition + ".outColorR", self.upper_close_pin_bs + "." + target[0])
        mc.connectAttr(condition + ".outColorG", self.upper_close_pin_bs + "." + target[1])
        target = mc.blendShape(self.lower_close_pin_bs, query=True, target=True)
        mc.connectAttr(condition + ".outColorR", self.lower_close_pin_bs + "." + target[0])
        mc.connectAttr(condition + ".outColorG", self.lower_close_pin_bs + "." + target[1])

        # line of sight
        eye_target = matrix.transform(parent=self.origin_space,
                                      name=self.generate_name("eye", "target", "ctl"),
                                      m=orig_m)
        mc.parentConstraint(context[data["eye_component"]]["line_of_sight"], eye_target)
        eye_target_blend_up = matrix.transform(parent=self.origin_space,
                                               name=self.generate_name("eye", "targetBlendUp", "ctl"),
                                               m=matrix.get_matrix(eye_target))
        eye_target_blend_up_inv = matrix.transform(parent=eye_target_blend_up,
                                                   name=self.generate_name("eye", "targetBlendUpInv", "ctl"),
                                                   m=matrix.get_matrix(self.origin_space))
        eye_target_blend_low = matrix.transform(parent=self.origin_space,
                                                name=self.generate_name("eye", "targetBlendLow", "ctl"),
                                                m=matrix.get_matrix(eye_target))
        eye_target_blend_low_inv = matrix.transform(parent=eye_target_blend_up,
                                                    name=self.generate_name("eye", "targetBlendLowInv", "ctl"),
                                                    m=matrix.get_matrix(self.origin_space))
        pb = mc.createNode("pairBlend")
        mc.setAttr(pb + ".rotInterpolation", 1)
        mc.setAttr(pb + ".inTranslate1", *mc.getAttr(eye_target + ".t")[0])
        mc.setAttr(pb + ".inRotate1", *mc.getAttr(eye_target + ".r")[0])
        mc.connectAttr(eye_target + ".t", pb + ".inTranslate2")
        mc.connectAttr(eye_target + ".r", pb + ".inRotate2")
        mc.connectAttr(pb + ".outTranslate", eye_target_blend_up + ".t")
        mc.connectAttr(pb + ".outRotate", eye_target_blend_up + ".r")
        mc.connectAttr(self.upper_follow_los_attr, pb + ".weight")

        pb = mc.createNode("pairBlend")
        mc.setAttr(pb + ".rotInterpolation", 1)
        mc.setAttr(pb + ".inTranslate1", *mc.getAttr(eye_target + ".t")[0])
        mc.setAttr(pb + ".inRotate1", *mc.getAttr(eye_target + ".r")[0])
        mc.connectAttr(eye_target + ".t", pb + ".inTranslate2")
        mc.connectAttr(eye_target + ".r", pb + ".inRotate2")
        mc.connectAttr(pb + ".outTranslate", eye_target_blend_low + ".t")
        mc.connectAttr(pb + ".outRotate", eye_target_blend_low + ".r")
        mc.parent(hierarchy.get_parent(self.upper_ctl), eye_target_blend_up_inv)
        mc.parent(hierarchy.get_parent(self.lower_ctl), eye_target_blend_low_inv)
        mc.connectAttr(self.lower_follow_los_attr, pb + ".weight")

    def connections(self, context):
        super().connections(context)
