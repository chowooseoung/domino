# domino
from domino.lib import matrix, polygon, vector, hierarchy, attribute
from domino.lib.rigging import nurbs, joint
from domino.lib.animation import fcurve
from domino import assembler

# built-ins
import os
import uuid

# maya
from maya import mel
from maya import cmds as mc
from maya.api import OpenMaya as om2


class Author:
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "lip"
    side = "C"
    index = 0
    description = "human 입술입니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "head_component": {"type": "string"},
        "jaw_component": {"type": "string"},
        "mesh": {"type": "string"},
        "outer_edge_loop": {"type": "string"},
        "outer_upper_vertex": {"type": "string"},
        "outer_lower_vertex": {"type": "string"},
        "inner_edge_loop": {"type": "string"},
        "inner_upper_vertex": {"type": "string"},
        "inner_lower_vertex": {"type": "string"},
        "auto_skinning": {"type": "bool"},
        "skin_fcurve": {"type": "double"},
        #
        "individual_settings_hide": {"type": "bool"},
        "left_up": {"type": "double"},
        "left_down": {"type": "double"},
        "left_in": {"type": "double"},
        "left_out": {"type": "double"},
        #
        "right_up": {"type": "double"},
        "right_down": {"type": "double"},
        "right_in": {"type": "double"},
        "right_out": {"type": "double"},
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
        "auto_skinning": True
    })
    common_preset["anim"].update({
        "skin_fcurve": {"name": "skin_fcurve_UU",
                        "driven": [],
                        "driver": [],
                        "floatChange": [0.0, 1.0],
                        "inAngle": [0.0, 0.0],
                        "inTangentType": ["auto", "auto"],
                        "inWeight": [1.0, 10.0],
                        "lock": [True, False],
                        "outAngle": [0.0, 0.0],
                        "outTangentType": ["auto", "auto"],
                        "outWeight": [10.0, 1.0],
                        "time": [],
                        "type": "animCurveUU",
                        "valueChange": [0.0, 1],
                        "weightedTangents": [True]}
    })
    return common_preset


def guide_recipe():
    script = """import maya.cmds as mc
for pos in ["{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}"]:
    orig_scale = mc.getAttr(pos + ".s")
    mc.setAttr(pos + ".sx", lock=False)
    mc.setAttr(pos + ".sy", lock=False)
    mc.setAttr(pos + ".sz", lock=False)
    mc.setAttr(pos + ".s", 0.3, 0.3, 0.3)
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
        outer_edge_loop = [int(x) for x in data["outer_edge_loop"].split(",")]
        inner_edge_loop = [int(x) for x in data["inner_edge_loop"].split(",")]

        outer_upper_vertex = int(data["outer_upper_vertex"])
        outer_lower_vertex = int(data["outer_lower_vertex"])
        inner_upper_vertex = int(data["inner_upper_vertex"])
        inner_lower_vertex = int(data["inner_lower_vertex"])

        sub_ctl_number = 5

        def get_lip_vertex(edges, previous_vertices, destination_vertex, edge_loop, way1=[], way2=[]):
            new_edges = []
            new_previous_vertices = []
            for way, edge, previous_vertex in zip([way1, way2], edges, previous_vertices):
                # edge 의 vertex
                vertex = polygon.convert_component(edge, vertex=True)
                # 이전에 등록된 vertex 는 제거
                if previous_vertex in vertex:
                    vertex.remove(previous_vertex)
                # 남은 vertex 는 다음 재귀에서 previous_vertices
                new_previous_vertices.append(vertex[0])
                way.append(vertex[0])

                # 연결된 edge
                connected_edges = polygon.convert_component(vertex[0], edge=True)
                # 연결된 edge 가 edge_loop 에 없으면 삭제
                for e in connected_edges.copy():
                    if e not in edge_loop:
                        connected_edges.remove(e)
                    if e in edges:
                        connected_edges.remove(e)
                # 유효한 edge 가 없으면
                if not connected_edges:
                    continue
                # 다음 재귀에서 edges
                new_edges.append(connected_edges[0])

            # 목적지에 도착했다면 return
            if way1[-1] == destination_vertex:
                return way1, way2
            return get_lip_vertex(new_edges, new_previous_vertices, destination_vertex, edge_loop, way1, way2)

        # curve
        outer_edges = polygon.convert_component(mesh + ".vtx[" + str(outer_upper_vertex) + "]", edge=True)
        outer_edges = [x for x in outer_edges if int(next(polygon.get_component_index([x]))) in outer_edge_loop]

        vertex_index = mesh + ".vtx[" + str(outer_upper_vertex) + "]"
        destination_index = mesh + ".vtx[" + str(outer_lower_vertex) + "]"
        edge_loop_string = [mesh + ".e[" + str(i) + "]" for i in outer_edge_loop]

        outer_way1, outer_way2 = get_lip_vertex(outer_edges,
                                                [vertex_index, vertex_index],
                                                destination_index,
                                                edge_loop_string,
                                                [vertex_index],
                                                [vertex_index])
        outer_side_vertex1 = outer_way1[int(len(outer_way1) / 2)]
        outer_side_vertex2 = outer_way2[int(len(outer_way2) / 2)]
        if vector.get_position(outer_side_vertex1)[0] < vector.get_position(outer_side_vertex2)[0]:
            left_way = outer_way1
            right_way = outer_way2
        else:
            left_way = outer_way2
            right_way = outer_way1
        self.outer_upper_way = list(reversed(left_way[:int(len(left_way) / 2) + 1])) + right_way[
                                                                                       1:int(len(right_way) / 2)]
        self.outer_lower_way = left_way[int(len(left_way) / 2):-1] + list(
            reversed(right_way[int((len(right_way) - 1) / 2):]))

        self.upper_outer_ep_crv = nurbs.create(parent=self.root,
                                               name=self.generate_name("upperOuterEP", "crv", "ctl"),
                                               degree=3,
                                               positions=[vector.get_position(x) for x in self.outer_upper_way],
                                               m=orig_m,
                                               ep=True,
                                               vis=False)
        mc.rebuildCurve(self.upper_outer_ep_crv, keepControlPoints=True)
        self.lower_outer_ep_crv = nurbs.create(parent=self.root,
                                               name=self.generate_name("lowerOuterEP", "crv", "ctl"),
                                               degree=3,
                                               positions=[vector.get_position(x) for x in self.outer_lower_way],
                                               m=orig_m,
                                               ep=True,
                                               vis=False)
        mc.rebuildCurve(self.lower_outer_ep_crv, keepControlPoints=True)

        self.upper_outer_driver_crv = nurbs.create(parent=self.root,
                                                   name=self.generate_name("upperOuterDriver", "crv", "ctl"),
                                                   degree=1,
                                                   positions=[vector.get_position(x) for x in self.outer_upper_way],
                                                   m=orig_m,
                                                   vis=False)
        self.lower_outer_driver_crv = nurbs.create(parent=self.root,
                                                   name=self.generate_name("lowerOuterDriver", "crv", "ctl"),
                                                   degree=1,
                                                   positions=[vector.get_position(x) for x in self.outer_lower_way],
                                                   m=orig_m,
                                                   vis=False)
        mc.rebuildCurve(self.upper_outer_driver_crv,
                        constructionHistory=0,
                        replaceOriginal=1,
                        rebuildType=0,
                        endKnots=1,
                        keepRange=1,
                        keepControlPoints=0,
                        keepEndPoints=1,
                        keepTangents=0,
                        spans=sub_ctl_number - 1,
                        degree=3,
                        tolerance=0.01)
        wire = mc.wire(self.upper_outer_ep_crv, wire=self.upper_outer_driver_crv)[0]
        mc.setAttr(wire + ".rotation", 0)
        mc.setAttr(wire + ".dropoffDistance[0]", 999)
        base_wire = mc.listConnections(wire + ".baseWire[0]", source=True, destination=False)[0]
        mc.setAttr(base_wire + ".inheritsTransform", 1)
        mc.setAttr(base_wire + ".t", *mc.getAttr(self.upper_outer_ep_crv + ".t")[0])
        mc.setAttr(base_wire + ".r", *mc.getAttr(self.upper_outer_ep_crv + ".r")[0])
        connections = mc.listConnections(wire, source=True, destination=False, connections=True, plugs=True)
        sources = connections[1::2]
        destinations = connections[0::2]
        for source, destination in zip(sources, destinations):
            if source.endswith("worldSpace"):
                mc.connectAttr(source.replace("worldSpace", "local"), destination, force=True)
        mc.rebuildCurve(self.lower_outer_driver_crv,
                        constructionHistory=0,
                        replaceOriginal=1,
                        rebuildType=0,
                        endKnots=1,
                        keepRange=1,
                        keepControlPoints=0,
                        keepEndPoints=1,
                        keepTangents=0,
                        spans=sub_ctl_number - 1,
                        degree=3,
                        tolerance=0.01)
        wire = mc.wire(self.lower_outer_ep_crv, wire=self.lower_outer_driver_crv)[0]
        mc.setAttr(wire + ".rotation", 0)
        mc.setAttr(wire + ".dropoffDistance[0]", 999)
        base_wire = mc.listConnections(wire + ".baseWire[0]", source=True, destination=False)[0]
        mc.setAttr(base_wire + ".inheritsTransform", 1)
        mc.setAttr(base_wire + ".t", *mc.getAttr(self.lower_outer_ep_crv + ".t")[0])
        mc.setAttr(base_wire + ".r", *mc.getAttr(self.lower_outer_ep_crv + ".r")[0])
        connections = mc.listConnections(wire, source=True, destination=False, connections=True, plugs=True)
        sources = connections[1::2]
        destinations = connections[0::2]
        for source, destination in zip(sources, destinations):
            if source.endswith("worldSpace"):
                mc.connectAttr(source.replace("worldSpace", "local"), destination, force=True)

        inner_edges = polygon.convert_component(mesh + ".vtx[" + str(inner_upper_vertex) + "]", edge=True)
        inner_edges = [x for x in inner_edges if int(next(polygon.get_component_index([x]))) in inner_edge_loop]

        vertex_index = mesh + ".vtx[" + str(inner_upper_vertex) + "]"
        destination_index = mesh + ".vtx[" + str(inner_lower_vertex) + "]"
        edge_loop_string = [mesh + ".e[" + str(i) + "]" for i in inner_edge_loop]

        inner_way1, inner_way2 = get_lip_vertex(inner_edges,
                                                [vertex_index, vertex_index],
                                                destination_index,
                                                edge_loop_string,
                                                [vertex_index],
                                                [vertex_index])
        inner_side_vertex1 = inner_way1[int(len(inner_way1) / 2)]
        inner_side_vertex2 = inner_way2[int(len(inner_way2) / 2)]
        if vector.get_position(inner_side_vertex1)[0] < vector.get_position(inner_side_vertex2)[0]:
            left_way = inner_way1
            right_way = inner_way2
        else:
            left_way = inner_way2
            right_way = inner_way1
        self.inner_upper_way = list(reversed(left_way[:int(len(left_way) / 2) + 1])) + right_way[
                                                                                       1:int(len(right_way) / 2)]
        self.inner_lower_way = left_way[int(len(left_way) / 2):-1] + list(
            reversed(right_way[int((len(right_way) - 1) / 2):]))

        self.upper_inner_ep_crv = nurbs.create(parent=self.root,
                                               name=self.generate_name("upperInnerEP", "crv", "ctl"),
                                               degree=3,
                                               positions=[vector.get_position(x) for x in self.inner_upper_way],
                                               m=orig_m,
                                               ep=True,
                                               vis=False)
        mc.rebuildCurve(self.upper_inner_ep_crv, keepControlPoints=True)
        self.lower_inner_ep_crv = nurbs.create(parent=self.root,
                                               name=self.generate_name("lowerInnerEP", "crv", "ctl"),
                                               degree=3,
                                               positions=[vector.get_position(x) for x in self.inner_lower_way],
                                               m=orig_m,
                                               ep=True,
                                               vis=False)
        mc.rebuildCurve(self.lower_inner_ep_crv, keepControlPoints=True)

        self.upper_inner_driver_crv = nurbs.create(parent=self.root,
                                                   name=self.generate_name("upperInnerDriver", "crv", "ctl"),
                                                   degree=1,
                                                   positions=[vector.get_position(x) for x in self.inner_upper_way],
                                                   m=orig_m,
                                                   vis=False)
        self.lower_inner_driver_crv = nurbs.create(parent=self.root,
                                                   name=self.generate_name("lowerInnerDriver", "crv", "ctl"),
                                                   degree=1,
                                                   positions=[vector.get_position(x) for x in self.inner_lower_way],
                                                   m=orig_m,
                                                   vis=False)
        mc.rebuildCurve(self.upper_inner_driver_crv,
                        constructionHistory=0,
                        replaceOriginal=1,
                        rebuildType=0,
                        endKnots=1,
                        keepRange=1,
                        keepControlPoints=0,
                        keepEndPoints=1,
                        keepTangents=0,
                        spans=sub_ctl_number - 1,
                        degree=3,
                        tolerance=0.01)
        wire = mc.wire(self.upper_inner_ep_crv, wire=self.upper_inner_driver_crv)[0]
        mc.setAttr(wire + ".rotation", 0)
        mc.setAttr(wire + ".dropoffDistance[0]", 999)
        base_wire = mc.listConnections(wire + ".baseWire[0]", source=True, destination=False)[0]
        mc.setAttr(base_wire + ".inheritsTransform", 1)
        mc.setAttr(base_wire + ".t", *mc.getAttr(self.upper_inner_ep_crv + ".t")[0])
        mc.setAttr(base_wire + ".r", *mc.getAttr(self.upper_inner_ep_crv + ".r")[0])
        connections = mc.listConnections(wire, source=True, destination=False, connections=True, plugs=True)
        sources = connections[1::2]
        destinations = connections[0::2]
        for source, destination in zip(sources, destinations):
            if source.endswith("worldSpace"):
                mc.connectAttr(source.replace("worldSpace", "local"), destination, force=True)
        mc.rebuildCurve(self.lower_inner_driver_crv,
                        constructionHistory=0,
                        replaceOriginal=1,
                        rebuildType=0,
                        endKnots=1,
                        keepRange=1,
                        keepControlPoints=0,
                        keepEndPoints=1,
                        keepTangents=0,
                        spans=sub_ctl_number - 1,
                        degree=3,
                        tolerance=0.01)
        wire = mc.wire(self.lower_inner_ep_crv, wire=self.lower_inner_driver_crv)[0]
        mc.setAttr(wire + ".rotation", 0)
        mc.setAttr(wire + ".dropoffDistance[0]", 999)
        base_wire = mc.listConnections(wire + ".baseWire[0]", source=True, destination=False)[0]
        mc.setAttr(base_wire + ".inheritsTransform", 1)
        mc.setAttr(base_wire + ".t", *mc.getAttr(self.lower_inner_ep_crv + ".t")[0])
        mc.setAttr(base_wire + ".r", *mc.getAttr(self.lower_inner_ep_crv + ".r")[0])
        connections = mc.listConnections(wire, source=True, destination=False, connections=True, plugs=True)
        sources = connections[1::2]
        destinations = connections[0::2]
        for source, destination in zip(sources, destinations):
            if source.endswith("worldSpace"):
                mc.connectAttr(source.replace("worldSpace", "local"), destination, force=True)

        # polygon
        planes = []
        number = sub_ctl_number + 2
        for i in range(number):
            planes.append(mc.polyPlane(constructionHistory=False,
                                       subdivisionsHeight=1,
                                       subdivisionsWidth=1,
                                       width=0.01,
                                       height=0.01)[0])
            mc.setAttr(planes[i] + ".t",
                       *vector.get_position(self.upper_outer_driver_crv + ".cv[{0}]".format(i % number)))
        for i in range(number, number * 2):
            planes.append(mc.polyPlane(constructionHistory=False,
                                       subdivisionsHeight=1,
                                       subdivisionsWidth=1,
                                       width=0.01,
                                       height=0.01)[0])
            mc.setAttr(planes[i] + ".t",
                       *vector.get_position(self.upper_inner_driver_crv + ".cv[{0}]".format(i % number)))
        for i in range(number * 2, number * 3):
            planes.append(mc.polyPlane(constructionHistory=False,
                                       subdivisionsHeight=1,
                                       subdivisionsWidth=1,
                                       width=0.01,
                                       height=0.01)[0])
            mc.setAttr(planes[i] + ".t",
                       *vector.get_position(self.lower_outer_driver_crv + ".cv[{0}]".format(i % number)))
        for i in range(number * 3, number * 4):
            planes.append(mc.polyPlane(constructionHistory=False,
                                       subdivisionsHeight=1,
                                       subdivisionsWidth=1,
                                       width=0.01,
                                       height=0.01)[0])
            mc.setAttr(planes[i] + ".t",
                       *vector.get_position(self.lower_inner_driver_crv + ".cv[{0}]".format(i % number)))
        self.driver_mesh = mc.polyUnite(planes,
                                        constructionHistory=False,
                                        mergeUVSets=True,
                                        name=self.generate_name("driver", "mesh", "ctl"))[0]
        self.driver_mesh = mc.parent(self.driver_mesh, context["xxx"])[0]

        mc.setAttr(self.driver_mesh + ".componentTags[0].componentTagName",
                   self.driver_mesh + "_upper",
                   type="string")
        mc.setAttr(self.driver_mesh + ".componentTags[1].componentTagName",
                   self.driver_mesh + "_lower",
                   type="string")
        mc.setAttr(self.driver_mesh + ".componentTags[0].componentTagContents",
                   2,
                   "vtx[4:{0}]".format((sub_ctl_number + 2) * 4 - 5),
                   "vtx[{0}:{1}]".format((sub_ctl_number + 2) * 4 + 4, (sub_ctl_number + 2) * 8 - 5),
                   type="componentList")
        mc.setAttr(self.driver_mesh + ".componentTags[1].componentTagContents",
                   2,
                   "vtx[{0}:{1}]".format((sub_ctl_number + 2) * 8 + 4, (sub_ctl_number + 2) * 12 - 5),
                   "vtx[{0}:{1}]".format((sub_ctl_number + 2) * 12 + 4, (sub_ctl_number + 2) * 16 - 5),
                   type="componentList")

        mc.hide(self.driver_mesh)

        # ctls
        m = matrix.set_matrix_scale(data["anchors"][3], (1, 1, 1))
        distance = vector.get_distance(vector.get_position(outer_side_vertex1), vector.get_position(outer_side_vertex2))
        self.left_ctl, self.left_loc = self.create_ctl(context=context,
                                                       parent=None,
                                                       name=self.generate_name("left", "", "ctl"),
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
                                                       mirror_ctl_name=self.generate_name("right", "", "ctl"))
        self.left_jnt = joint.add_joint(self.left_loc,
                                        name=self.generate_name("left", "jnt", "ctl"),
                                        m=matrix.get_matrix(self.left_loc),
                                        vis=False)

        m = matrix.set_matrix_scale(data["anchors"][4], (1, 1, -1))
        self.right_ctl, self.right_loc = self.create_ctl(context=context,
                                                         parent=None,
                                                         name=self.generate_name("right", "", "ctl"),
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
                                                         mirror_ctl_name=self.generate_name("left", "", "ctl"))
        self.right_jnt = joint.add_joint(self.right_loc,
                                         name=self.generate_name("right", "jnt", "ctl"),
                                         m=matrix.get_matrix(self.right_loc),
                                         vis=False)

        m = matrix.set_matrix_scale(data["anchors"][1], (1, 1, 1))
        self.upper_ctl, self.upper_loc = self.create_ctl(context=context,
                                                         parent=None,
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
                                                         mirror_ctl_name="")
        self.upper_jnt = joint.add_joint(self.upper_loc,
                                         name=self.generate_name("upper", "jnt", "ctl"),
                                         m=matrix.get_matrix(self.upper_loc),
                                         vis=False)
        m = matrix.set_matrix_scale(data["anchors"][2], (1, 1, -1))
        self.lower_ctl, self.lower_loc = self.create_ctl(context=context,
                                                         parent=None,
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
                                                         mirror_ctl_name="")
        self.lower_jnt = joint.add_joint(self.lower_loc,
                                         name=self.generate_name("lower", "jnt", "ctl"),
                                         m=matrix.get_matrix(self.lower_loc),
                                         vis=False)
        self.driver_sc = mc.skinCluster([self.left_jnt, self.right_jnt, self.upper_jnt, self.lower_jnt],
                                        self.driver_mesh,
                                        name=self.generate_name("driver", "sc", "ctl"),
                                        toSelectedBones=True,
                                        bindMethod=1,
                                        normalizeWeights=1,
                                        weightDistribution=1)[0]
        # skinning
        # right side
        cv_number = sub_ctl_number + 2
        curves = [self.upper_outer_driver_crv,
                  self.upper_inner_driver_crv,
                  self.lower_outer_driver_crv,
                  self.lower_inner_driver_crv]
        mid_jnt = self.upper_jnt
        offset = (sub_ctl_number + 2) * 4
        for i, crv in enumerate(curves):
            if i == 2:
                mid_jnt = self.lower_jnt
            positions = [vector.get_position(crv + ".cv[{0}]".format(cv)) for cv in range(cv_number)]
            left_positions = list(reversed(positions[int(cv_number / 2):]))
            right_positions = positions[:int(cv_number / 2) + 1]

            left_total_length = 0
            lengths = []
            for x in range(len(left_positions[:-1])):
                length = vector.get_distance(left_positions[x], left_positions[x + 1])
                left_total_length += length
                lengths.append(length)
            left_weights = [l / left_total_length for l in lengths]

            right_total_length = 0
            lengths = []
            for x in range(len(right_positions[:-1])):
                length = vector.get_distance(right_positions[x], right_positions[x + 1])
                right_total_length += length
                lengths.append(length)
            right_weights = [l / right_total_length for l in lengths]

            weight = 0
            n = 0
            mc.skinPercent(self.driver_sc,
                           self.driver_mesh + ".vtx[{0}:{1}]".format(n + offset * i, n + offset * i + 3),
                           transformValue=((self.right_jnt, 1)))
            n += 4
            for w in right_weights:
                weight += w
                skin_fcurve = mc.listConnections(self.root + ".skin_fcurve",
                                                 source=True,
                                                 destination=False)[0]
                multiple_weight = fcurve.get_fcurve_values(skin_fcurve, division=0, inputs=[weight])[0]
                mc.skinPercent(self.driver_sc,
                               self.driver_mesh + ".vtx[{0}:{1}]".format(n + offset * i, n + offset * i + 3),
                               transformValue=((self.right_jnt, 1 - multiple_weight),
                                               (mid_jnt, multiple_weight)))
                n += 4
            weight = 0
            n = 8
            for w in left_weights:
                weight += w
                skin_fcurve = mc.listConnections(self.root + ".skin_fcurve",
                                                 source=True,
                                                 destination=False)[0]
                multiple_weight = fcurve.get_fcurve_values(skin_fcurve, division=0, inputs=[weight])[0]
                mc.skinPercent(self.driver_sc,
                               self.driver_mesh + ".vtx[{0}:{1}]".format(offset * (i + 1) - n,
                                                                         offset * (i + 1) + 3 - n),
                               transformValue=((self.left_jnt, 1 - multiple_weight),
                                               (mid_jnt, multiple_weight)))
                n += 4

        # proximity wrap ctls
        m = matrix.set_matrix_scale(data["anchors"][5], (1, 1, 1))
        self.upper_left_cns = matrix.transform(parent=self.root,
                                               name=self.generate_name("upperLeft", "cns", "ctl"),
                                               m=matrix.get_matrix(self.root))
        source0 = matrix.transform(parent=self.root,
                                   name=self.generate_name("upperLeft0", "source", "ctl"),
                                   m=m)
        mc.pointConstraint(self.upper_jnt, source0, maintainOffset=True)
        source1 = matrix.transform(parent=self.root,
                                   name=self.generate_name("upperLeft1", "source", "ctl"),
                                   m=m)
        mc.pointConstraint(self.left_jnt, source1, maintainOffset=True)
        wt_m = mc.createNode("wtAddMatrix")
        mc.connectAttr(source0 + ".worldMatrix[0]", wt_m + ".wtMatrix[0].matrixIn")
        mc.setAttr(wt_m + ".wtMatrix[0].weightIn", 0.5)
        mc.connectAttr(source1 + ".worldMatrix[0]", wt_m + ".wtMatrix[1].matrixIn")
        mc.setAttr(wt_m + ".wtMatrix[1].weightIn", 0.5)

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(wt_m + ".matrixSum", mult_m + ".matrixIn[0]")
        mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
        mc.connectAttr(mult_m + ".matrixSum", self.upper_left_cns + ".offsetParentMatrix")

        distance = vector.get_distance(vector.get_position(vertex_index), vector.get_position(destination_index))
        self.upper_left_ctl, self.upper_left_loc = self.create_ctl(context=context,
                                                                   parent=self.upper_left_cns,
                                                                   name=self.generate_name("upperLeft", "", "ctl"),
                                                                   parent_ctl=None,
                                                                   attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx",
                                                                          "sy", "sz"],
                                                                   m=m,
                                                                   cns=False,
                                                                   mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                                                   shape_args={
                                                                       "shape": "arrow",
                                                                       "width": distance / 2,
                                                                       "color": (1, 0, 0),
                                                                   },
                                                                   mirror_ctl_name=self.generate_name("upperRight", "",
                                                                                                      "ctl"))
        self.upper_left_jnt = joint.add_joint(self.upper_left_cns,
                                              name=self.generate_name("upperLeft", "jnt", "ctl"),
                                              m=matrix.get_matrix(self.upper_left_loc),
                                              vis=False)
        mc.pointConstraint(self.upper_left_loc, self.upper_left_jnt)
        mc.orientConstraint(self.upper_left_loc, self.upper_left_jnt)
        mc.scaleConstraint(self.upper_left_loc, self.upper_left_jnt)

        m = matrix.set_matrix_scale(data["anchors"][6], (1, 1, 1))
        self.upper_right_cns = matrix.transform(parent=self.root,
                                                name=self.generate_name("upperRight", "cns", "ctl"),
                                                m=matrix.get_matrix(self.root))
        source0 = matrix.transform(parent=self.root,
                                   name=self.generate_name("upperRight0", "source", "ctl"),
                                   m=m)
        mc.pointConstraint(self.upper_jnt, source0, maintainOffset=True)
        source1 = matrix.transform(parent=self.root,
                                   name=self.generate_name("upperRight1", "source", "ctl"),
                                   m=m)
        mc.pointConstraint(self.right_jnt, source1, maintainOffset=True)
        wt_m = mc.createNode("wtAddMatrix")
        mc.connectAttr(source0 + ".worldMatrix[0]", wt_m + ".wtMatrix[0].matrixIn")
        mc.setAttr(wt_m + ".wtMatrix[0].weightIn", 0.5)
        mc.connectAttr(source1 + ".worldMatrix[0]", wt_m + ".wtMatrix[1].matrixIn")
        mc.setAttr(wt_m + ".wtMatrix[1].weightIn", 0.5)

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(wt_m + ".matrixSum", mult_m + ".matrixIn[0]")
        mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
        mc.connectAttr(mult_m + ".matrixSum", self.upper_right_cns + ".offsetParentMatrix")

        self.upper_right_ctl, self.upper_right_loc = self.create_ctl(context=context,
                                                                     parent=self.upper_right_cns,
                                                                     name=self.generate_name("upperRight", "", "ctl"),
                                                                     parent_ctl=None,
                                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx",
                                                                            "sy", "sz"],
                                                                     m=m,
                                                                     cns=False,
                                                                     mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                                                     shape_args={
                                                                         "shape": "arrow",
                                                                         "width": distance / 2,
                                                                         "color": (1, 0, 0),
                                                                     },
                                                                     mirror_ctl_name=self.generate_name("upperLeft", "",
                                                                                                        "ctl"))
        self.upper_right_jnt = joint.add_joint(self.upper_right_cns,
                                               name=self.generate_name("upperRight", "jnt", "ctl"),
                                               m=matrix.get_matrix(self.upper_right_loc),
                                               vis=False)
        mc.pointConstraint(self.upper_right_loc, self.upper_right_jnt)
        mc.orientConstraint(self.upper_right_loc, self.upper_right_jnt)
        mc.scaleConstraint(self.upper_right_loc, self.upper_right_jnt)

        m = matrix.set_matrix_scale(data["anchors"][7], (1, 1, 1))
        self.lower_left_cns = matrix.transform(parent=self.root,
                                               name=self.generate_name("lowerLeft", "cns", "ctl"),
                                               m=matrix.get_matrix(self.root))
        source0 = matrix.transform(parent=self.root,
                                   name=self.generate_name("lowerLeft0", "source", "ctl"),
                                   m=m)
        mc.pointConstraint(self.lower_jnt, source0, maintainOffset=True)
        source1 = matrix.transform(parent=self.root,
                                   name=self.generate_name("lowerLeft1", "source", "ctl"),
                                   m=m)
        mc.pointConstraint(self.left_jnt, source1, maintainOffset=True)
        wt_m = mc.createNode("wtAddMatrix")
        mc.connectAttr(source0 + ".worldMatrix[0]", wt_m + ".wtMatrix[0].matrixIn")
        mc.setAttr(wt_m + ".wtMatrix[0].weightIn", 0.5)
        mc.connectAttr(source1 + ".worldMatrix[0]", wt_m + ".wtMatrix[1].matrixIn")
        mc.setAttr(wt_m + ".wtMatrix[1].weightIn", 0.5)

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(wt_m + ".matrixSum", mult_m + ".matrixIn[0]")
        mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
        mc.connectAttr(mult_m + ".matrixSum", self.lower_left_cns + ".offsetParentMatrix")

        self.lower_left_ctl, self.lower_left_loc = self.create_ctl(context=context,
                                                                   parent=self.lower_left_cns,
                                                                   name=self.generate_name("lowerLeft", "", "ctl"),
                                                                   parent_ctl=None,
                                                                   attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx",
                                                                          "sy", "sz"],
                                                                   m=m,
                                                                   cns=False,
                                                                   mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                                                   shape_args={
                                                                       "shape": "arrow",
                                                                       "width": distance / 2,
                                                                       "color": (1, 0, 0),
                                                                   },
                                                                   mirror_ctl_name=self.generate_name("lowerRight", "",
                                                                                                      "ctl"))
        self.lower_left_jnt = joint.add_joint(self.lower_left_cns,
                                              name=self.generate_name("lowerLeft", "jnt", "ctl"),
                                              m=matrix.get_matrix(self.lower_left_loc),
                                              vis=False)
        mc.pointConstraint(self.lower_left_loc, self.lower_left_jnt)
        mc.orientConstraint(self.lower_left_loc, self.lower_left_jnt)
        mc.scaleConstraint(self.lower_left_loc, self.lower_left_jnt)

        m = matrix.set_matrix_scale(data["anchors"][8], (1, 1, 1))
        self.lower_right_cns = matrix.transform(parent=self.root,
                                                name=self.generate_name("lowerRight", "cns", "ctl"),
                                                m=matrix.get_matrix(self.root))
        source0 = matrix.transform(parent=self.root,
                                   name=self.generate_name("lowerRight0", "source", "ctl"),
                                   m=m)
        mc.pointConstraint(self.lower_jnt, source0, maintainOffset=True)
        source1 = matrix.transform(parent=self.root,
                                   name=self.generate_name("lowerRight1", "source", "ctl"),
                                   m=m)
        mc.pointConstraint(self.right_jnt, source1, maintainOffset=True)
        wt_m = mc.createNode("wtAddMatrix")
        mc.connectAttr(source0 + ".worldMatrix[0]", wt_m + ".wtMatrix[0].matrixIn")
        mc.setAttr(wt_m + ".wtMatrix[0].weightIn", 0.5)
        mc.connectAttr(source1 + ".worldMatrix[0]", wt_m + ".wtMatrix[1].matrixIn")
        mc.setAttr(wt_m + ".wtMatrix[1].weightIn", 0.5)

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(wt_m + ".matrixSum", mult_m + ".matrixIn[0]")
        mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
        mc.connectAttr(mult_m + ".matrixSum", self.lower_right_cns + ".offsetParentMatrix")

        self.lower_right_ctl, self.lower_right_loc = self.create_ctl(context=context,
                                                                     parent=self.lower_right_cns,
                                                                     name=self.generate_name("lowerRight", "", "ctl"),
                                                                     parent_ctl=None,
                                                                     attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx",
                                                                            "sy", "sz"],
                                                                     m=m,
                                                                     cns=False,
                                                                     mirror_config=(0, 0, 1, 1, 1, 0, 0, 0, 0),
                                                                     shape_args={
                                                                         "shape": "arrow",
                                                                         "width": distance / 2,
                                                                         "color": (1, 0, 0),
                                                                     },
                                                                     mirror_ctl_name=self.generate_name("lowerLeft", "",
                                                                                                        "ctl"))
        self.lower_right_jnt = joint.add_joint(self.lower_right_cns,
                                               name=self.generate_name("lowerRight", "jnt", "ctl"),
                                               m=matrix.get_matrix(self.lower_right_loc),
                                               vis=False)
        mc.pointConstraint(self.lower_right_loc, self.lower_right_jnt)
        mc.orientConstraint(self.lower_right_loc, self.lower_right_jnt)
        mc.scaleConstraint(self.lower_right_loc, self.lower_right_jnt)

        distance = vector.get_distance(vector.get_position(outer_side_vertex2), vector.get_position(outer_side_vertex1))
        self.upper_left_cls = mc.cluster(self.driver_mesh,
                                         name=self.generate_name("upperLeft", "cls", "ctl"),
                                         bindState=1,
                                         weightedNode=(self.upper_left_jnt, self.upper_left_jnt))[0]
        mc.setAttr(self.upper_left_cls + ".input[0].componentTagExpression", self.driver_mesh + "_upper", type="string")
        handle = \
            mc.listConnections(self.upper_left_cls, source=True, destination=False, type="clusterHandle", shapes=True)[
                0]
        mc.rename(handle, self.upper_left_cls + "Handle")
        npo = hierarchy.get_parent(self.upper_left_ctl)
        mc.connectAttr(npo + ".worldInverseMatrix[0]", self.upper_left_cls + ".bindPreMatrix")
        self.upper_left_falloff = mc.createNode("primitiveFalloff",
                                                name=self.generate_name("upperLeft", "falloff", "ctl"),
                                                parent=context["xxx"])
        mc.setAttr(self.upper_left_falloff + ".primitive", 1)
        mc.setAttr(self.upper_left_falloff + ".start", distance / -1.8)
        mc.setAttr(self.upper_left_falloff + ".end", distance / 1.8)
        mc.setAttr(self.upper_left_falloff + ".ramp[0].ramp_Interp", 2)
        mc.setAttr(self.upper_left_falloff + ".ramp[1].ramp_Interp", 2)
        mc.setAttr(self.upper_left_falloff + ".ramp[2].ramp_Interp", 2)
        mc.setAttr(self.upper_left_falloff + ".ramp[0].ramp_Position", 0.5)
        mc.setAttr(self.upper_left_falloff + ".ramp[0].ramp_FloatValue", 0)
        mc.setAttr(self.upper_left_falloff + ".ramp[1].ramp_Position", 0.8)
        mc.setAttr(self.upper_left_falloff + ".ramp[1].ramp_FloatValue", 1)
        mc.setAttr(self.upper_left_falloff + ".ramp[2].ramp_Position", 1)
        mc.setAttr(self.upper_left_falloff + ".ramp[2].ramp_FloatValue", 0.5)
        mc.connectAttr(self.upper_left_falloff + ".outputWeightFunction", self.upper_left_cls + ".weightFunction[0]")
        self.upper_right_cls = mc.cluster(self.driver_mesh,
                                          name=self.generate_name("upperRight", "cls", "ctl"),
                                          bindState=1,
                                          weightedNode=(self.upper_right_jnt, self.upper_right_jnt))[0]
        mc.setAttr(self.upper_right_cls + ".input[0].componentTagExpression", self.driver_mesh + "_upper",
                   type="string")
        handle = \
            mc.listConnections(self.upper_right_cls, source=True, destination=False, type="clusterHandle", shapes=True)[
                0]
        mc.rename(handle, self.upper_right_cls + "Handle")
        npo = hierarchy.get_parent(self.upper_right_ctl)
        mc.connectAttr(npo + ".worldInverseMatrix[0]", self.upper_right_cls + ".bindPreMatrix")
        self.upper_right_falloff = mc.createNode("primitiveFalloff",
                                                 name=self.generate_name("upperRight", "falloff", "ctl"),
                                                 parent=context["xxx"])
        mc.setAttr(self.upper_right_falloff + ".primitive", 1)
        mc.setAttr(self.upper_right_falloff + ".start", distance / -1.8)
        mc.setAttr(self.upper_right_falloff + ".end", distance / 1.8)
        mc.setAttr(self.upper_right_falloff + ".ramp[0].ramp_Interp", 2)
        mc.setAttr(self.upper_right_falloff + ".ramp[1].ramp_Interp", 2)
        mc.setAttr(self.upper_right_falloff + ".ramp[2].ramp_Interp", 2)
        mc.setAttr(self.upper_right_falloff + ".ramp[0].ramp_Position", 0)
        mc.setAttr(self.upper_right_falloff + ".ramp[0].ramp_FloatValue", 0.5)
        mc.setAttr(self.upper_right_falloff + ".ramp[1].ramp_Position", 0.2)
        mc.setAttr(self.upper_right_falloff + ".ramp[1].ramp_FloatValue", 1)
        mc.setAttr(self.upper_right_falloff + ".ramp[2].ramp_Position", 0.5)
        mc.setAttr(self.upper_right_falloff + ".ramp[2].ramp_FloatValue", 0)
        mc.connectAttr(self.upper_right_falloff + ".outputWeightFunction", self.upper_right_cls + ".weightFunction[0]")
        mc.hide([self.upper_left_falloff, self.upper_right_falloff])

        self.lower_left_cls = mc.cluster(self.driver_mesh,
                                         name=self.generate_name("lowerLeft", "cls", "ctl"),
                                         bindState=1,
                                         weightedNode=(self.lower_left_jnt, self.lower_left_jnt))[0]
        mc.setAttr(self.lower_left_cls + ".input[0].componentTagExpression", self.driver_mesh + "_lower", type="string")
        handle = \
            mc.listConnections(self.lower_left_cls, source=True, destination=False, type="clusterHandle", shapes=True)[
                0]
        mc.rename(handle, self.lower_left_cls + "Handle")
        npo = hierarchy.get_parent(self.lower_left_ctl)
        mc.connectAttr(npo + ".worldInverseMatrix[0]", self.lower_left_cls + ".bindPreMatrix")
        self.lower_left_falloff = mc.createNode("primitiveFalloff",
                                                name=self.generate_name("lowerLeft", "falloff", "ctl"),
                                                parent=context["xxx"])
        mc.setAttr(self.lower_left_falloff + ".primitive", 1)
        mc.setAttr(self.lower_left_falloff + ".start", distance / -1.8)
        mc.setAttr(self.lower_left_falloff + ".end", distance / 1.8)
        mc.setAttr(self.lower_left_falloff + ".ramp[0].ramp_Interp", 2)
        mc.setAttr(self.lower_left_falloff + ".ramp[1].ramp_Interp", 2)
        mc.setAttr(self.lower_left_falloff + ".ramp[2].ramp_Interp", 2)
        mc.setAttr(self.lower_left_falloff + ".ramp[0].ramp_Position", 0.5)
        mc.setAttr(self.lower_left_falloff + ".ramp[0].ramp_FloatValue", 0)
        mc.setAttr(self.lower_left_falloff + ".ramp[1].ramp_Position", 0.8)
        mc.setAttr(self.lower_left_falloff + ".ramp[1].ramp_FloatValue", 1)
        mc.setAttr(self.lower_left_falloff + ".ramp[2].ramp_Position", 1)
        mc.setAttr(self.lower_left_falloff + ".ramp[2].ramp_FloatValue", 0.5)
        mc.connectAttr(self.lower_left_falloff + ".outputWeightFunction", self.lower_left_cls + ".weightFunction[0]")
        self.lower_right_cls = mc.cluster(self.driver_mesh,
                                          name=self.generate_name("lowerRight", "cls", "ctl"),
                                          bindState=1,
                                          weightedNode=(self.lower_right_jnt, self.lower_right_jnt))[0]
        mc.setAttr(self.lower_right_cls + ".input[0].componentTagExpression", self.driver_mesh + "_lower",
                   type="string")
        handle = \
            mc.listConnections(self.lower_right_cls, source=True, destination=False, type="clusterHandle", shapes=True)[
                0]
        mc.rename(handle, self.lower_right_cls + "Handle")
        npo = hierarchy.get_parent(self.lower_right_ctl)
        mc.connectAttr(npo + ".worldInverseMatrix[0]", self.lower_right_cls + ".bindPreMatrix")
        self.lower_right_falloff = mc.createNode("primitiveFalloff",
                                                 name=self.generate_name("lowerRight", "falloff", "ctl"),
                                                 parent=context["xxx"])
        mc.setAttr(self.lower_right_falloff + ".primitive", 1)
        mc.setAttr(self.lower_right_falloff + ".start", distance / -1.8)
        mc.setAttr(self.lower_right_falloff + ".end", distance / 1.8)
        mc.setAttr(self.lower_right_falloff + ".ramp[0].ramp_Interp", 2)
        mc.setAttr(self.lower_right_falloff + ".ramp[1].ramp_Interp", 2)
        mc.setAttr(self.lower_right_falloff + ".ramp[2].ramp_Interp", 2)
        mc.setAttr(self.lower_right_falloff + ".ramp[0].ramp_Position", 0)
        mc.setAttr(self.lower_right_falloff + ".ramp[0].ramp_FloatValue", 0.5)
        mc.setAttr(self.lower_right_falloff + ".ramp[1].ramp_Position", 0.2)
        mc.setAttr(self.lower_right_falloff + ".ramp[1].ramp_FloatValue", 1)
        mc.setAttr(self.lower_right_falloff + ".ramp[2].ramp_Position", 0.5)
        mc.setAttr(self.lower_right_falloff + ".ramp[2].ramp_FloatValue", 0)
        mc.connectAttr(self.lower_right_falloff + ".outputWeightFunction", self.lower_right_cls + ".weightFunction[0]")
        mc.hide([self.lower_left_falloff, self.lower_right_falloff])

        self.upper_curve_ctls = []
        pin = mc.createNode("proximityPin")
        mc.setAttr(pin + ".offsetTranslation", 1)
        shape, orig_shape = mc.listRelatives(self.driver_mesh, shapes=True)
        mc.connectAttr(orig_shape + ".outMesh", pin + ".originalGeometry")
        mc.connectAttr(shape + ".worldMesh[0]", pin + ".deformedGeometry")

        outer_positions = [vector.get_position(self.upper_outer_driver_crv + ".cv[{0}]".format(i + 1)) for i in
                           range(sub_ctl_number)]
        inner_positions = [vector.get_position(self.upper_inner_driver_crv + ".cv[{0}]".format(i + 1)) for i in
                           range(sub_ctl_number)]
        root_m = matrix.get_matrix(self.root)
        self.upper_ctl_display_crv = nurbs.create(parent=self.root,
                                                  name=self.generate_name("upperDisplay", "crv", "ctl"),
                                                  degree=1,
                                                  positions=[om2.MVector([0, 0, 0]) for _ in range(sub_ctl_number)],
                                                  m=orig_m,
                                                  inherits=False,
                                                  display_type=2)
        mc.setAttr(self.upper_ctl_display_crv + ".lineWidth", 2)
        mc.setAttr(self.upper_ctl_display_crv + ".alwaysDrawOnTop", 1)
        for i, outer_pos in enumerate(outer_positions):
            ctl, loc = self.create_ctl(context=context,
                                       parent=None,
                                       name=self.generate_name("upper{0}".format(i), "", "ctl"),
                                       parent_ctl=None,
                                       attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                       m=root_m,
                                       cns=False,
                                       mirror_config=(1, 0, 0, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "circle",
                                           "width": distance / 10,
                                           "color": (0, 1, 1),
                                           "ro": (90, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("upper{0}".format(sub_ctl_number - 1 - i), "",
                                                                          "ctl"))
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(loc + ".worldMatrix[0]", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", self.upper_ctl_display_crv + ".controlPoints[{0}]".format(i))
            outer_m = matrix.set_matrix_translate(orig_m, outer_pos)
            inner_m = matrix.set_matrix_translate(orig_m, inner_positions[i])

            outer_index = i * 2
            inner_index = i * 2 + 1

            # outer pos
            mc.setAttr(pin + ".inputMatrix[{0}]".format(outer_index), outer_m, type="matrix")
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(pin + ".outputMatrix[{0}]".format(outer_index), mult_m + ".matrixIn[0]")
            mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(decom_m + ".outputTranslate", npo + ".t")

            # inner
            mc.setAttr(pin + ".inputMatrix[{0}]".format(inner_index), inner_m, type="matrix")
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(pin + ".outputMatrix[{0}]".format(inner_index), mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            inner_pos = matrix.transform(parent=npo,
                                         name=self.generate_name("upperInner{0}".format(i), "pos", "ctl"),
                                         m=orig_m)
            mc.connectAttr(decom_m + ".outputTranslate", inner_pos + ".t")
            inner_cv = matrix.transform(parent=ctl,
                                        name=self.generate_name("upperInner{0}".format(i), "cv", "ctl"),
                                        m=orig_m)
            mc.connectAttr(inner_pos + ".t", inner_cv + ".t")

            # cons curve cv
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(loc + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.upper_outer_driver_crv + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate",
                           self.upper_outer_driver_crv + ".controlPoints[{0}]".format(i + 1))

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(inner_cv + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.upper_inner_driver_crv + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate",
                           self.upper_inner_driver_crv + ".controlPoints[{0}]".format(i + 1))
            self.upper_curve_ctls.append(ctl)

        self.lower_curve_ctls = []
        outer_positions = [vector.get_position(self.lower_outer_driver_crv + ".cv[{0}]".format(i + 1)) for i in
                           range(sub_ctl_number)]
        inner_positions = [vector.get_position(self.lower_inner_driver_crv + ".cv[{0}]".format(i + 1)) for i in
                           range(sub_ctl_number)]
        self.lower_ctl_display_crv = nurbs.create(parent=self.root,
                                                  name=self.generate_name("lowerDisplay", "crv", "ctl"),
                                                  degree=1,
                                                  positions=[om2.MVector([0, 0, 0]) for _ in range(sub_ctl_number)],
                                                  m=orig_m,
                                                  inherits=False,
                                                  display_type=2)
        mc.setAttr(self.lower_ctl_display_crv + ".lineWidth", 2)
        mc.setAttr(self.lower_ctl_display_crv + ".alwaysDrawOnTop", 1)
        for i, outer_pos in enumerate(outer_positions):
            ctl, loc = self.create_ctl(context=context,
                                       parent=None,
                                       name=self.generate_name("lower{0}".format(i), "", "ctl"),
                                       parent_ctl=None,
                                       attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                       m=root_m,
                                       cns=False,
                                       mirror_config=(1, 0, 0, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "circle",
                                           "width": distance / 10,
                                           "color": (0, 1, 1),
                                           "ro": (90, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name("lower{0}".format(sub_ctl_number - 1 - i), "",
                                                                          "ctl"))
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(loc + ".worldMatrix[0]", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", self.lower_ctl_display_crv + ".controlPoints[{0}]".format(i))
            outer_m = matrix.set_matrix_translate(orig_m, outer_pos)
            inner_m = matrix.set_matrix_translate(orig_m, inner_positions[i])

            outer_index = i * 2 + (sub_ctl_number * 2)
            inner_index = i * 2 + (sub_ctl_number * 2 + 1)

            # outer
            mc.setAttr(pin + ".inputMatrix[{0}]".format(outer_index), outer_m, type="matrix")
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(pin + ".outputMatrix[{0}]".format(outer_index), mult_m + ".matrixIn[0]")
            mc.connectAttr(self.root + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            npo = hierarchy.get_parent(ctl)
            mc.connectAttr(decom_m + ".outputTranslate", npo + ".t")

            # inner
            mc.setAttr(pin + ".inputMatrix[{0}]".format(inner_index), inner_m, type="matrix")
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(pin + ".outputMatrix[{0}]".format(inner_index), mult_m + ".matrixIn[0]")
            mc.connectAttr(npo + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            inner_pos = matrix.transform(parent=npo,
                                         name=self.generate_name("lowerInner{0}".format(i), "pos", "ctl"),
                                         m=orig_m)
            mc.connectAttr(decom_m + ".outputTranslate", inner_pos + ".t")
            inner_cv = matrix.transform(parent=ctl,
                                        name=self.generate_name("lowerInner{0}".format(i), "cv", "ctl"),
                                        m=orig_m)
            mc.connectAttr(inner_pos + ".t", inner_cv + ".t")

            # cons curve cv
            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(loc + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.lower_outer_driver_crv + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate",
                           self.lower_outer_driver_crv + ".controlPoints[{0}]".format(i + 1))

            mult_m = mc.createNode("multMatrix")
            mc.connectAttr(inner_cv + ".worldMatrix[0]", mult_m + ".matrixIn[0]")
            mc.connectAttr(self.lower_inner_driver_crv + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate",
                           self.lower_inner_driver_crv + ".controlPoints[{0}]".format(i + 1))
            self.lower_curve_ctls.append(ctl)

        cv_number = sub_ctl_number + 2 - 1
        outer_left_pos = vector.get_position(self.upper_outer_driver_crv + ".cv[{0}]".format(cv_number))
        outer_right_pos = vector.get_position(self.upper_outer_driver_crv + ".cv[0]")
        inner_left_pos = vector.get_position(self.lower_inner_driver_crv + ".cv[{0}]".format(cv_number))
        inner_right_pos = vector.get_position(self.lower_inner_driver_crv + ".cv[0]")
        pos_list = [outer_left_pos, outer_right_pos, inner_left_pos, inner_right_pos]
        outer_left_cp = (self.upper_outer_driver_crv + ".controlPoints[{0}]".format(cv_number),
                         self.lower_outer_driver_crv + ".controlPoints[{0}]".format(cv_number))
        outer_right_cp = (self.upper_outer_driver_crv + ".controlPoints[0]",
                          self.lower_outer_driver_crv + ".controlPoints[0]")
        inner_left_cp = (self.upper_inner_driver_crv + ".controlPoints[{0}]".format(cv_number),
                         self.lower_inner_driver_crv + ".controlPoints[{0}]".format(cv_number))
        inner_right_cp = (self.upper_inner_driver_crv + ".controlPoints[0]",
                          self.lower_inner_driver_crv + ".controlPoints[0]")
        cps_list = [outer_left_cp, outer_right_cp, inner_left_cp, inner_right_cp]
        for i in range(4):
            index = i + sub_ctl_number * 4
            m = matrix.set_matrix_translate(orig_m, pos_list[i])
            mc.setAttr(pin + ".inputMatrix[{0}]".format(index), m, type="matrix")

            for cp in cps_list[i]:
                crv = cp.split(".")[0]

                mult_m = mc.createNode("multMatrix")
                mc.connectAttr(pin + ".outputMatrix[{0}]".format(index), mult_m + ".matrixIn[0]")
                mc.connectAttr(crv + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

                decom_m = mc.createNode("decomposeMatrix")
                mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")
                mc.connectAttr(decom_m + ".outputTranslate", cp)

        self.refs = []
        prefix = "upper"
        outer_crv = self.upper_outer_ep_crv
        inner_crv = self.upper_inner_ep_crv
        self.outer_upper_jnts = []
        self.inner_upper_jnts = []
        self.outer_lower_jnts = []
        self.inner_lower_jnts = []
        outer_jnt_list = self.outer_upper_jnts
        inner_jnt_list = self.inner_upper_jnts
        for way in [outer_way1, inner_way1]:
            outer_aim_grp = matrix.transform(parent=self.root,
                                             name=self.generate_name("{0}OuterAim".format(prefix), "grp", "ctl"),
                                             m=orig_m)
            inner_aim_grp = matrix.transform(parent=self.root,
                                             name=self.generate_name("{0}InnerAim".format(prefix), "grp", "ctl"),
                                             m=orig_m)
            for i in range(len(way[1:-1])):
                outer_aim_obj = matrix.transform(parent=outer_aim_grp,
                                                 name=self.generate_name("{0}OuterAim{1}".format(prefix, i),
                                                                         "obj",
                                                                         "ctl"),
                                                 m=orig_m)
                inner_aim_obj = matrix.transform(parent=inner_aim_grp,
                                                 name=self.generate_name("{0}InnerAim{1}".format(prefix, i),
                                                                         "obj",
                                                                         "ctl"),
                                                 m=orig_m)

                outer_poci = mc.createNode("pointOnCurveInfo")
                mc.setAttr(outer_poci + ".parameter", i + 1)
                mc.connectAttr(outer_crv + ".local", outer_poci + ".inputCurve")

                inner_poci = mc.createNode("pointOnCurveInfo")
                mc.setAttr(inner_poci + ".parameter", i + 1)
                mc.connectAttr(inner_crv + ".local", inner_poci + ".inputCurve")

                # up axis
                comp_m = mc.createNode("composeMatrix")
                mc.connectAttr(outer_poci + ".result.position", comp_m + ".inputTranslate")

                aim_m = mc.createNode("aimMatrix")
                mc.setAttr(aim_m + ".primaryMode", 2)
                mc.setAttr(aim_m + ".secondaryMode", 1)
                mc.connectAttr(comp_m + ".outputMatrix", aim_m + ".inputMatrix")
                mc.connectAttr(outer_poci + ".result.normalizedTangent", aim_m + ".primaryTargetVector")
                mc.connectAttr(inner_poci + ".result.position", aim_m + ".secondaryTargetVector")

                mc.connectAttr(aim_m + ".outputMatrix", outer_aim_obj + ".offsetParentMatrix")

                comp_m = mc.createNode("composeMatrix")
                mc.connectAttr(inner_poci + ".result.position", comp_m + ".inputTranslate")

                aim_m = mc.createNode("aimMatrix")
                mc.setAttr(aim_m + ".primaryMode", 2)
                mc.setAttr(aim_m + ".secondaryMode", 1)
                mc.connectAttr(comp_m + ".outputMatrix", aim_m + ".inputMatrix")
                mc.connectAttr(inner_poci + ".result.normalizedTangent", aim_m + ".primaryTargetVector")
                mc.connectAttr(outer_poci + ".result.position", aim_m + ".secondaryTargetVector")

                mc.connectAttr(aim_m + ".outputMatrix", inner_aim_obj + ".offsetParentMatrix")

                # refs
                name = self.generate_name("{0}Outer{1}".format(prefix, i), "ref", "ctl")
                outer_ref = self.create_ref(context=context, name=name, anchor=True, m=outer_aim_obj)
                self.refs.append(outer_ref)
                name = self.generate_name("{0}Inner{1}".format(prefix, i), "ref", "ctl")
                inner_ref = self.create_ref(context=context, name=name, anchor=True, m=inner_aim_obj)
                self.refs.append(inner_ref)

                # jnts
                if data["create_jnt"]:
                    uni_scale = False
                    if assembly_data["force_uni_scale"]:
                        uni_scale = True
                    name = self.generate_name("{0}Outer{1}".format(prefix, i), "", "jnt")
                    outer_jnt = self.create_jnt(context=context,
                                                parent=None,
                                                name=name,
                                                description="{0}Outer{1}".format(prefix, i),
                                                ref=outer_ref,
                                                m=matrix.get_matrix(outer_ref),
                                                leaf=False,
                                                uni_scale=uni_scale)
                    outer_jnt_list.append(outer_jnt)

                    name = self.generate_name("{0}Inner{1}".format(prefix, i), "", "jnt")
                    inner_jnt = self.create_jnt(context=context,
                                                parent=None,
                                                name=name,
                                                description="{0}Inner{1}".format(prefix, i),
                                                ref=inner_ref,
                                                m=matrix.get_matrix(inner_ref),
                                                leaf=False,
                                                uni_scale=uni_scale)
                    inner_jnt_list.append(inner_jnt)

            prefix = "lower"
            outer_crv = self.lower_outer_ep_crv
            inner_crv = self.lower_inner_ep_crv
            outer_jnt_list = self.outer_lower_jnts
            inner_jnt_list = self.inner_lower_jnts

    def attributes(self, context):
        super().attributes(context)

        data = self.component.data["value"]

        # pin attribute
        self.left_pin_attr = attribute.add_attr(self.left_ctl,
                                                longName="pin",
                                                type="double",
                                                keyable=True,
                                                minValue=-1,
                                                maxValue=1,
                                                defaultValue=0)
        self.right_pin_attr = attribute.add_attr(self.right_ctl,
                                                 longName="pin",
                                                 type="double",
                                                 keyable=True,
                                                 minValue=-1,
                                                 maxValue=1,
                                                 defaultValue=0)
        self.upper_pin_attr = attribute.add_attr(self.upper_ctl,
                                                 longName="pin",
                                                 type="double",
                                                 keyable=True,
                                                 minValue=-1,
                                                 maxValue=1,
                                                 defaultValue=1)
        self.lower_pin_attr = attribute.add_attr(self.lower_ctl,
                                                 longName="pin",
                                                 type="double",
                                                 keyable=True,
                                                 minValue=-1,
                                                 maxValue=1,
                                                 defaultValue=-1)

        # sub ctl visibility attribute
        self.lip_sub_ctl_vis_attr = attribute.add_attr(self.host,
                                                       longName="sub_ctl_vis",
                                                       type="enum",
                                                       enumName="off:on",
                                                       keyable=True)

        # side auto rotate attribute
        if data["individual_settings_hide"]:
            self.left_up_attr = self.root + ".left_up"
            self.left_down_attr = self.root + ".left_down"
            self.left_in_attr = self.root + ".left_in"
            self.left_out_attr = self.root + ".left_out"
            self.right_up_attr = self.root + ".right_up"
            self.right_down_attr = self.root + ".right_down"
            self.right_in_attr = self.root + ".right_in"
            self.right_out_attr = self.root + ".right_out"
        else:
            self.left_up_attr = attribute.add_attr(self.left_ctl,
                                                   longName="up",
                                                   type="double",
                                                   defaultValue=data["left_up"])
            mc.setAttr(self.left_up_attr, channelBox=True)
            mc.connectAttr(self.left_up_attr, self.root + ".left_up")
            self.left_down_attr = attribute.add_attr(self.left_ctl,
                                                     longName="down",
                                                     type="double",
                                                     defaultValue=data["left_down"])
            mc.setAttr(self.left_down_attr, channelBox=True)
            mc.connectAttr(self.left_down_attr, self.root + ".left_down")
            self.left_in_attr = attribute.add_attr(self.left_ctl,
                                                   longName="in",
                                                   type="double",
                                                   defaultValue=data["left_in"])
            mc.setAttr(self.left_in_attr, channelBox=True)
            mc.connectAttr(self.left_in_attr, self.root + ".left_in")
            self.left_out_attr = attribute.add_attr(self.left_ctl,
                                                    longName="out",
                                                    type="double",
                                                    defaultValue=data["left_out"])
            mc.setAttr(self.left_out_attr, channelBox=True)
            mc.connectAttr(self.left_out_attr, self.root + ".left_out")

            self.right_up_attr = attribute.add_attr(self.right_ctl,
                                                    longName="up",
                                                    type="double",
                                                    defaultValue=data["right_up"])
            mc.setAttr(self.right_up_attr, channelBox=True)
            mc.connectAttr(self.right_up_attr, self.root + ".right_up")
            self.right_down_attr = attribute.add_attr(self.right_ctl,
                                                      longName="down",
                                                      type="double",
                                                      defaultValue=data["right_down"])
            mc.setAttr(self.right_down_attr, channelBox=True)
            mc.connectAttr(self.right_down_attr, self.root + ".right_down")
            self.right_in_attr = attribute.add_attr(self.right_ctl,
                                                    longName="in",
                                                    type="double",
                                                    defaultValue=data["right_in"])
            mc.setAttr(self.right_in_attr, channelBox=True)
            mc.connectAttr(self.right_in_attr, self.root + ".right_in")
            self.right_out_attr = attribute.add_attr(self.right_ctl,
                                                     longName="out",
                                                     type="double",
                                                     defaultValue=data["right_out"])
            mc.setAttr(self.right_out_attr, channelBox=True)
            mc.connectAttr(self.right_out_attr, self.root + ".right_out")

    def operators(self, context):
        super().operators(context)

        data = self.component.data["value"]

        mesh = data["mesh"]
        head_jnt = context[data["head_component"]]["jnts"][0]
        jaw_jnt = context[data["jaw_component"]]["jnts"][0]

        # sub ctl visibility
        for ctl in self.upper_curve_ctls:
            for shape in mc.listRelatives(ctl, shapes=True):
                mc.connectAttr(self.lip_sub_ctl_vis_attr, shape + ".v")
        for ctl in self.lower_curve_ctls:
            for shape in mc.listRelatives(ctl, shapes=True):
                mc.connectAttr(self.lip_sub_ctl_vis_attr, shape + ".v")
        for crv in [self.upper_ctl_display_crv, self.lower_ctl_display_crv]:
            for shape in mc.listRelatives(crv, shapes=True):
                mc.connectAttr(self.lip_sub_ctl_vis_attr, shape + ".v")

        # jaw follow
        jaw_npo = matrix.transform(parent=self.root,
                                   name=self.generate_name("jaw", "space", "ctl"),
                                   m=matrix.get_matrix(jaw_jnt))
        mc.pointConstraint(jaw_jnt, jaw_npo, maintainOffset=True)
        mc.orientConstraint(jaw_jnt, jaw_npo, maintainOffset=True)

        m = matrix.get_matrix(self.left_ctl)
        self.left_head_follow = matrix.transform(parent=self.root,
                                                 name=self.generate_name("leftHead", "follow", "ctl"),
                                                 m=m)
        self.left_jaw_follow = matrix.transform(parent=jaw_npo,
                                                name=self.generate_name("leftJaw", "follow", "ctl"),
                                                m=m)
        self.left_follow_wt_m = mc.createNode("wtAddMatrix")
        mc.connectAttr(self.left_head_follow + ".matrix", self.left_follow_wt_m + ".wtMatrix[0].matrixIn")

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.left_jaw_follow + ".matrix", mult_m + ".matrixIn[0]")
        mc.connectAttr(jaw_npo + ".matrix", mult_m + ".matrixIn[1]")
        mc.connectAttr(mult_m + ".matrixSum", self.left_follow_wt_m + ".wtMatrix[1].matrixIn")

        r_v = mc.createNode("remapValue")
        mc.setAttr(r_v + ".inputMin", -1)
        mc.setAttr(r_v + ".inputMax", 1)
        mc.setAttr(r_v + ".outputMin", 0)
        mc.setAttr(r_v + ".outputMax", 1)
        mc.connectAttr(self.left_pin_attr, r_v + ".inputValue")
        mc.connectAttr(r_v + ".outValue", self.left_follow_wt_m + ".wtMatrix[0].weightIn")

        reverse = mc.createNode("reverse")
        mc.connectAttr(r_v + ".outValue", reverse + ".inputX")
        mc.connectAttr(reverse + ".outputX", self.left_follow_wt_m + ".wtMatrix[1].weightIn")

        m = matrix.get_matrix(self.right_ctl)
        self.right_head_follow = matrix.transform(parent=self.root,
                                                  name=self.generate_name("rightHead", "follow", "ctl"),
                                                  m=m)
        self.right_jaw_follow = matrix.transform(parent=jaw_npo,
                                                 name=self.generate_name("rightJaw", "follow", "ctl"),
                                                 m=m)
        self.right_follow_wt_m = mc.createNode("wtAddMatrix")
        mc.connectAttr(self.right_head_follow + ".matrix", self.right_follow_wt_m + ".wtMatrix[0].matrixIn")

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.right_jaw_follow + ".matrix", mult_m + ".matrixIn[0]")
        mc.connectAttr(jaw_npo + ".matrix", mult_m + ".matrixIn[1]")
        mc.connectAttr(mult_m + ".matrixSum", self.right_follow_wt_m + ".wtMatrix[1].matrixIn")

        r_v = mc.createNode("remapValue")
        mc.setAttr(r_v + ".inputMin", -1)
        mc.setAttr(r_v + ".inputMax", 1)
        mc.setAttr(r_v + ".outputMin", 0)
        mc.setAttr(r_v + ".outputMax", 1)
        mc.connectAttr(self.right_pin_attr, r_v + ".inputValue")
        mc.connectAttr(r_v + ".outValue", self.right_follow_wt_m + ".wtMatrix[0].weightIn")

        reverse = mc.createNode("reverse")
        mc.connectAttr(r_v + ".outValue", reverse + ".inputX")
        mc.connectAttr(reverse + ".outputX", self.right_follow_wt_m + ".wtMatrix[1].weightIn")

        m = matrix.get_matrix(self.upper_ctl)
        self.upper_head_follow = matrix.transform(parent=self.root,
                                                  name=self.generate_name("upperHead", "follow", "ctl"),
                                                  m=m)
        self.upper_jaw_follow = matrix.transform(parent=jaw_npo,
                                                 name=self.generate_name("upperJaw", "follow", "ctl"),
                                                 m=m)
        self.upper_follow_wt_m = mc.createNode("wtAddMatrix")
        mc.connectAttr(self.upper_head_follow + ".matrix", self.upper_follow_wt_m + ".wtMatrix[0].matrixIn")

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.upper_jaw_follow + ".matrix", mult_m + ".matrixIn[0]")
        mc.connectAttr(jaw_npo + ".matrix", mult_m + ".matrixIn[1]")
        mc.connectAttr(mult_m + ".matrixSum", self.upper_follow_wt_m + ".wtMatrix[1].matrixIn")

        r_v = mc.createNode("remapValue")
        mc.setAttr(r_v + ".inputMin", -1)
        mc.setAttr(r_v + ".inputMax", 1)
        mc.setAttr(r_v + ".outputMin", 0)
        mc.setAttr(r_v + ".outputMax", 1)
        mc.connectAttr(self.upper_pin_attr, r_v + ".inputValue")
        mc.connectAttr(r_v + ".outValue", self.upper_follow_wt_m + ".wtMatrix[0].weightIn")

        reverse = mc.createNode("reverse")
        mc.connectAttr(r_v + ".outValue", reverse + ".inputX")
        mc.connectAttr(reverse + ".outputX", self.upper_follow_wt_m + ".wtMatrix[1].weightIn")

        m = matrix.get_matrix(self.lower_ctl)
        self.lower_head_follow = matrix.transform(parent=self.root,
                                                  name=self.generate_name("lowerHead", "follow", "ctl"),
                                                  m=m)
        self.lower_jaw_follow = matrix.transform(parent=jaw_npo,
                                                 name=self.generate_name("lowerJaw", "follow", "ctl"),
                                                 m=m)
        self.lower_follow_wt_m = mc.createNode("wtAddMatrix")
        mc.connectAttr(self.lower_head_follow + ".matrix", self.lower_follow_wt_m + ".wtMatrix[0].matrixIn")

        mult_m = mc.createNode("multMatrix")
        mc.connectAttr(self.lower_jaw_follow + ".matrix", mult_m + ".matrixIn[0]")
        mc.connectAttr(jaw_npo + ".matrix", mult_m + ".matrixIn[1]")
        mc.connectAttr(mult_m + ".matrixSum", self.lower_follow_wt_m + ".wtMatrix[1].matrixIn")

        r_v = mc.createNode("remapValue")
        mc.setAttr(r_v + ".inputMin", -1)
        mc.setAttr(r_v + ".inputMax", 1)
        mc.setAttr(r_v + ".outputMin", 0)
        mc.setAttr(r_v + ".outputMax", 1)
        mc.connectAttr(self.lower_pin_attr, r_v + ".inputValue")
        mc.connectAttr(r_v + ".outValue", self.lower_follow_wt_m + ".wtMatrix[0].weightIn")

        reverse = mc.createNode("reverse")
        mc.connectAttr(r_v + ".outValue", reverse + ".inputX")
        mc.connectAttr(reverse + ".outputX", self.lower_follow_wt_m + ".wtMatrix[1].weightIn")

        mc.connectAttr(self.left_follow_wt_m + ".matrixSum",
                       hierarchy.get_parent(self.left_ctl) + ".offsetParentMatrix")
        mc.connectAttr(self.right_follow_wt_m + ".matrixSum",
                       hierarchy.get_parent(self.right_ctl) + ".offsetParentMatrix")
        mc.connectAttr(self.upper_follow_wt_m + ".matrixSum",
                       hierarchy.get_parent(self.upper_ctl) + ".offsetParentMatrix")
        mc.connectAttr(self.lower_follow_wt_m + ".matrixSum",
                       hierarchy.get_parent(self.lower_ctl) + ".offsetParentMatrix")

        # side auto rotate
        ph = mc.listRelatives(self.left_ctl, children=True, type="transform")[0]

        mp = mc.createNode("multiplyDivide")
        mc.setAttr(mp + ".input1X", -1)
        mc.setAttr(mp + ".input1Y", -1)
        mc.connectAttr(self.left_up_attr, mp + ".input2X")
        mc.connectAttr(self.left_ctl + ".tz", mp + ".input2Y")

        r_v = mc.createNode("remapValue")
        mc.connectAttr(self.left_ctl + ".tz", r_v + ".inputValue")
        mc.connectAttr(mp + ".outputX", r_v + ".outputMax")

        condition = mc.createNode("condition")
        mc.setAttr(condition + ".operation", 5)
        mc.connectAttr(self.left_ctl + ".tz", condition + ".firstTerm")
        mc.connectAttr(r_v + ".outValue", condition + ".colorIfFalseR")

        r_v = mc.createNode("remapValue")
        mc.connectAttr(mp + ".outputY", r_v + ".inputValue")
        mc.connectAttr(self.left_down_attr, r_v + ".outputMax")
        mc.connectAttr(r_v + ".outValue", condition + ".colorIfTrueR")

        mc.connectAttr(condition + ".outColorR", ph + ".ry")

        condition = mc.createNode("condition")
        mc.setAttr(condition + ".operation", 3)
        mc.connectAttr(self.left_ctl + ".tx", condition + ".firstTerm")

        r_v = mc.createNode("remapValue")
        mc.connectAttr(self.left_ctl + ".tx", r_v + ".inputValue")
        mc.connectAttr(self.left_out_attr, r_v + ".outputMax")
        mc.connectAttr(r_v + ".outValue", condition + ".colorIfTrueR")

        mp = mc.createNode("multiplyDivide")
        mc.setAttr(mp + ".input1X", -1)
        mc.setAttr(mp + ".input1Y", -1)
        mc.connectAttr(self.left_in_attr, mp + ".input2X")
        mc.connectAttr(self.left_ctl + ".tx", mp + ".input2Y")

        r_v = mc.createNode("remapValue")
        mc.connectAttr(mp + ".outputY", r_v + ".inputValue")
        mc.connectAttr(mp + ".outputX", r_v + ".outputMax")
        mc.connectAttr(r_v + ".outValue", condition + ".colorIfFalseR")

        mc.connectAttr(condition + ".outColorR", ph + ".rz")

        # auto skinning
        if not data["auto_skinning"]:
            return None
        sc = mel.eval("findRelatedSkinCluster {0}".format(mesh))
        if not sc:
            sc = mc.skinCluster([head_jnt, jaw_jnt],
                                mesh,
                                name=mesh + "_0_sc",
                                toSelectedBones=True,
                                bindMethod=1,
                                normalizeWeights=1,
                                weightDistribution=1)[0]
        outer_edge_loop = data["outer_edge_loop"]
        inner_edge_loop = data["inner_edge_loop"]
        mc.skinCluster(sc,
                       edit=True,
                       weight=0,
                       addInfluence=self.outer_upper_jnts + self.inner_upper_jnts + self.outer_lower_jnts + self.inner_lower_jnts)

        skinned_vertices = []
        skinned_sets = mc.sets(name=self.generate_name("lipInfVertices", "sets", "ctl"), empty=True)
        if "specific_sets" not in context:
            context["specific_sets"] = []
        context["specific_sets"].append(skinned_sets)

        # outer, inner 사이 vertex skinning
        upper_lt = zip(self.outer_upper_way[1:],
                       self.inner_upper_way[1:],
                       self.outer_upper_jnts,
                       self.inner_upper_jnts)
        lower_lt = zip(self.outer_lower_way[1:],
                       self.inner_lower_way[1:],
                       self.outer_lower_jnts,
                       self.inner_lower_jnts)
        for lt in [upper_lt, lower_lt]:
            for outer_vtx, inner_vtx, outer_jnt, inner_jnt in lt:
                mc.skinPercent(sc, outer_vtx, transformValue=((outer_jnt, 1)))
                mc.skinPercent(sc, inner_vtx, transformValue=((inner_jnt, 1)))
                outer_edges = polygon.convert_component(outer_vtx, edge=True)
                inner_edges = polygon.convert_component(inner_vtx, edge=True)

                outer_edges = [int(x) for x in polygon.get_component_index(outer_edges) if x not in outer_edge_loop]
                inner_edges = [int(x) for x in polygon.get_component_index(inner_edges) if x not in inner_edge_loop]

                loop0 = set(mc.polySelect(mesh, query=True, edgeLoopPath=(outer_edges[0], inner_edges[0])))
                loop1 = set(mc.polySelect(mesh, query=True, edgeLoopPath=(outer_edges[0], inner_edges[1])))
                loop2 = set(mc.polySelect(mesh, query=True, edgeLoopPath=(outer_edges[1], inner_edges[0])))
                loop3 = set(mc.polySelect(mesh, query=True, edgeLoopPath=(outer_edges[1], inner_edges[1])))

                intersection = loop0 & loop1 & loop2 & loop3
                skinned_vertices.extend([outer_vtx, inner_vtx])

                count = 1
                ratio = 1 / len(intersection)
                while intersection and count < len(intersection):
                    outer_edges = set(polygon.convert_component(outer_vtx, edge=True, to_string=False))
                    inner_edges = set(polygon.convert_component(inner_vtx, edge=True, to_string=False))

                    outer_edge = outer_edges & intersection
                    inner_edge = inner_edges & intersection

                    intersection -= outer_edge
                    intersection -= inner_edge

                    outer_vertices = set(
                        polygon.convert_component(mesh + ".e[" + str(outer_edge.pop()) + "]", vertex=True))
                    inner_vertices = set(
                        polygon.convert_component(mesh + ".e[" + str(inner_edge.pop()) + "]", vertex=True))

                    outer_vtx = (outer_vertices - set([outer_vtx])).pop()
                    inner_vtx = (inner_vertices - set([inner_vtx])).pop()
                    skinned_vertices.extend([outer_vtx, inner_vtx])

                    mc.skinPercent(sc,
                                   outer_vtx,
                                   transformValue=((outer_jnt, 1 - ratio * count), (inner_jnt, ratio * count)))
                    mc.skinPercent(sc,
                                   inner_vtx,
                                   transformValue=((outer_jnt, ratio * count), (inner_jnt, 1 - ratio * count)))
                    count += 1

        lt = zip(
            [self.outer_upper_way[0], self.outer_upper_way[-1]],
            [self.inner_upper_way[0], self.inner_upper_way[-1]],
            [
                [self.outer_upper_jnts[0], self.outer_lower_jnts[0]],
                [self.outer_upper_jnts[-1], self.outer_lower_jnts[-1]]],
            [
                [self.inner_upper_jnts[0], self.inner_upper_jnts[0]],
                [self.inner_upper_jnts[-1], self.inner_upper_jnts[-1]]
            ]
        )
        for outer_vtx, inner_vtx, outer_jnts, inner_jnts in lt:
            mc.skinPercent(sc, outer_vtx, transformValue=((outer_jnts[0], 0.5), (outer_jnts[1], 0.5)))
            mc.skinPercent(sc, inner_vtx, transformValue=((inner_jnts[0], 0.5), (inner_jnts[1], 0.5)))
            outer_edges = polygon.convert_component(outer_vtx, edge=True)
            inner_edges = polygon.convert_component(inner_vtx, edge=True)

            outer_edges = [int(x) for x in polygon.get_component_index(outer_edges) if x not in outer_edge_loop]
            inner_edges = [int(x) for x in polygon.get_component_index(inner_edges) if x not in inner_edge_loop]

            loop0 = set(mc.polySelect(mesh, query=True, edgeLoopPath=(outer_edges[0], inner_edges[0])))
            loop1 = set(mc.polySelect(mesh, query=True, edgeLoopPath=(outer_edges[0], inner_edges[1])))
            loop2 = set(mc.polySelect(mesh, query=True, edgeLoopPath=(outer_edges[1], inner_edges[0])))
            loop3 = set(mc.polySelect(mesh, query=True, edgeLoopPath=(outer_edges[1], inner_edges[1])))

            intersection = loop0 & loop1 & loop2 & loop3
            skinned_vertices.extend([outer_vtx, inner_vtx])

            count = 1
            ratio = 0.5 / len(intersection)
            while intersection and count < len(intersection):
                outer_edges = set(polygon.convert_component(outer_vtx, edge=True, to_string=False))
                inner_edges = set(polygon.convert_component(inner_vtx, edge=True, to_string=False))

                outer_edge = outer_edges & intersection
                inner_edge = inner_edges & intersection

                intersection -= outer_edge
                intersection -= inner_edge

                outer_vertices = set(
                    polygon.convert_component(mesh + ".e[" + str(outer_edge.pop()) + "]", vertex=True))
                inner_vertices = set(
                    polygon.convert_component(mesh + ".e[" + str(inner_edge.pop()) + "]", vertex=True))

                outer_vtx = (outer_vertices - set([outer_vtx])).pop()
                inner_vtx = (inner_vertices - set([inner_vtx])).pop()
                skinned_vertices.extend([outer_vtx, inner_vtx])

                mc.skinPercent(sc,
                               outer_vtx,
                               transformValue=(
                                   (outer_jnts[0], 0.5 - ratio * count),
                                   (outer_jnts[1], 0.5 - ratio * count),
                                   (inner_jnts[0], ratio * count),
                                   (inner_jnts[1], ratio * count)
                               )
                               )
                mc.skinPercent(sc,
                               inner_vtx,
                               transformValue=(
                                   (outer_jnts[0], ratio * count),
                                   (outer_jnts[1], ratio * count),
                                   (inner_jnts[0], 0.5 - ratio * count),
                                   (inner_jnts[1], 0.5 - ratio * count)
                               )
                               )
                count += 1

        # outer falloff skinning
        falloff = 6
        outer_upper_way = self.outer_upper_way
        outer_lower_way = self.outer_lower_way
        inner_upper_way = self.inner_upper_way
        inner_lower_way = self.inner_lower_way

        for _ in range(falloff):
            result = []
            for way in [outer_upper_way, outer_lower_way, inner_upper_way, inner_lower_way]:
                new_vertices = []
                for w in way:
                    edges = polygon.convert_component(w, edge=True)
                    vertices = polygon.convert_component(edges, vertex=True)
                    vertex = [x for x in vertices if x not in skinned_vertices]
                    new_vertices.append(vertex[0])
                result.append(new_vertices)

            outer_upper_way = result[0]
            outer_lower_way = result[1]
            inner_upper_way = result[2]
            inner_lower_way = result[3]

            skinned_vertices.extend(outer_upper_way)
            skinned_vertices.extend(outer_lower_way)
            skinned_vertices.extend(inner_upper_way)
            skinned_vertices.extend(inner_lower_way)

            outer_upper_zip = outer_upper_way, self.outer_upper_jnts
            outer_lower_zip = outer_lower_way, self.outer_lower_jnts
            inner_upper_zip = inner_upper_way, self.inner_upper_jnts
            inner_lower_zip = inner_lower_way, self.inner_lower_jnts
            for way, jnts in [outer_upper_zip, outer_lower_zip, inner_upper_zip, inner_lower_zip]:
                for x, jnt in enumerate(jnts):
                    way_index = x + 1
                    mc.skinPercent(sc, way[way_index], transformValue=((jnt, 1)))

            mc.skinPercent(sc,
                           outer_upper_way[0],
                           transformValue=((self.outer_upper_jnts[0], 0.5), (self.outer_lower_jnts[0], 0.5)))
            mc.skinPercent(sc,
                           inner_upper_way[0],
                           transformValue=((self.inner_upper_jnts[0], 0.5), (self.inner_lower_jnts[0], 0.5)))
            mc.skinPercent(sc,
                           outer_upper_way[-1],
                           transformValue=((self.outer_upper_jnts[-1], 0.5), (self.outer_lower_jnts[-1], 0.5)))
            mc.skinPercent(sc,
                           inner_upper_way[-1],
                           transformValue=((self.inner_upper_jnts[-1], 0.5), (self.inner_lower_jnts[-1], 0.5)))

        # inner falloff skinning
        mc.sets(skinned_vertices, edit=True, addElement=skinned_sets)

    def connections(self, context):
        super().connections(context)
