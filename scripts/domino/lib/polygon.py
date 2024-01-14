# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# domino
from domino.lib import vector

# built-ins
import math


def get_component_index(component):
    for comp in component:
        index = comp.split("[")[-1][:-1]
        if ":" in comp:
            start, end = map(int, index.split(":"))
            yield from [str(i) for i in range(start, end + 1)]
        else:
            yield index


def convert_component(component, vertex=False, edge=False, face=False, uv=False, to_string=True):
    if not isinstance(component, (list, tuple)):
        component = [component]
    mesh = component[0].split(".")[0]

    index_range = get_component_index(mc.polyListComponentConversion(component,
                                                                     fromVertex=True,
                                                                     fromEdge=True,
                                                                     fromFace=True,
                                                                     fromUV=True,
                                                                     toVertex=vertex,
                                                                     toEdge=edge,
                                                                     toFace=face,
                                                                     toUV=uv))
    sorted_index_range = sorted(list(set(index_range)), key=lambda x: int(x))
    if not to_string:
        return [int(x) for x in sorted_index_range]
    if vertex:
        result_component = "vtx"
    elif edge:
        result_component = "e"
    elif face:
        result_component = "f"
    elif uv:
        result_component = "map"
    return [mesh + "." + result_component + "[" + index + "]" for index in sorted_index_range]


def loop_to_way(loop, start_vertex, end_vertex):
    if start_vertex not in loop:
        return [], []
    if end_vertex not in loop:
        return [], []

    way1 = [start_vertex]
    loop.remove(start_vertex)

    def get_ways():
        if loop and end_vertex not in way1:
            edges = mc.polyListComponentConversion(way1[-1], fromVertex=True, toEdge=True)
            for v in convert_component(edges, vertex=True):
                if v in loop:
                    way1.append(v)
                    if v != end_vertex:
                        loop.remove(v)
                    break
            get_ways()

    get_ways()
    return way1

def loop_to_2way(loop, start_vertex, end_vertex):
    """

    Args:
        loop : vertex loop. ["plane1.vtx[1]", ...]
        start_vertex : vtx. "plane1.vtx[1]"
        end_vertex : vtx. "plane1.vtx[10]"
    """
    if start_vertex not in loop:
        return [], []
    if end_vertex not in loop:
        return [], []

    way1 = [start_vertex]
    way2 = [start_vertex]
    loop.remove(start_vertex)

    def get_ways():
        if loop and (end_vertex not in way1 or end_vertex not in way2):
            way_vertexes = []
            if end_vertex not in way1:
                way_vertexes.append([way1, way1[-1]])
            if end_vertex not in way2:
                way_vertexes.append([way2, way2[-1]])
            for way, vtx in way_vertexes:
                edges = mc.polyListComponentConversion(vtx, fromVertex=True, toEdge=True)
                for v in convert_component(edges, vertex=True):
                    if v in loop:
                        way.append(v)
                        if v != end_vertex:
                            loop.remove(v)
                        break
                break
            get_ways()

    get_ways()
    return way1, way2


def point_to_mesh(parent, name, points, up=(0, 0, 1)):
    total_length = 0
    for i in range(len(points)):
        if i == 0:
            continue
        total_length += vector.get_distance(points[i], points[i - 1])
    if total_length > 2:
        up = om2.MVector(up) / math.log2(total_length)
    else:
        up = om2.MVector(up) * 0.05

    crv1 = mc.curve(point=points, name="TEmp1", degree=1)
    crv2 = mc.curve(point=[om2.MVector(p) + up for p in points], name="TEmp2", degree=1)
    crv3 = mc.curve(point=[om2.MVector(p) - up for p in points], name="TEmp3", degree=1)

    mesh = mc.loft([crv2, crv1, crv3],
                   name=name,
                   constructionHistory=0,
                   uniform=1,
                   close=0,
                   autoReverse=1,
                   degree=1,
                   sectionSpans=1,
                   range=0,
                   rebuild=0,
                   polygon=1,
                   reverseSurfaceNormals=True)[0]
    if parent:
        mesh = mc.parent(mesh, parent)[0]
    mc.delete([crv1, crv2 ,crv3])
    return mesh
