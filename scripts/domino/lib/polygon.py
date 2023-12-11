# maya
from maya import cmds as mc


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
