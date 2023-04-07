# maya
from maya import cmds as mc


def get_parent(node, generations=1, type=""):
    if type:
        generations = -1
    previous_node = None
    parent = mc.listRelatives(node, parent=True, fullPath=True)
    while parent:
        generations -= 1
        if generations == 0:
            return parent[0]
        if mc.nodeType(parent) == type:
            return parent[0]
        previous_node = parent[0]
        parent = mc.listRelatives(parent[0], parent=True, fullPath=True)
    return previous_node


def is_assembly(node):
    return True if len(mc.ls(node, long=True)[0].split("|")) < 3 else False
