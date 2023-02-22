# maya
from pymel import core as pm

# domino
from domino.core import icon

dt = pm.datatypes


def tag(obj, parent):
    pm.controller(obj)
    control_tag = pm.PyNode(pm.controller(obj, query=True)[0])
    control_tag.attr("visibilityMode").set(1)
    if parent:
        parent_control_tag = pm.PyNode(pm.controller(parent, query=True)[0])
        parent_control_tag.attr("cycleWalkSibling").set(True)
        pm.connectAttr(parent_control_tag.attr("prepopulate"),
                       control_tag.attr("prepopulate"), force=True)

        attr = parent_control_tag.attr("children")
        num = attr.getNumElements()
        if num == attr.numConnectedElements():
            index = num
        else:
            for i in range(num):
                if not attr[i].inputs():
                    index = num
        pm.disconnectAttr(control_tag.attr("parent"))
        pm.connectAttr(control_tag.attr("parent"),
                       parent_control_tag.attr("children")[index])


def npo(obj, name=None):
    if name is None:
        name = str(obj) + "_npo"

    parent = obj.getParent()
    _npo = pm.createNode("transform", name=name, parent=parent)
    pm.matchTransform(_npo, obj, position=True, rotation=True, scale=True)
    pm.parent(obj, _npo)
    return _npo


def child(obj, name=None, shape="cube", **kwargs):
    if name is None:
        name = str(obj) + "_child"

    ctl = icon.create(parent=obj,
                      name=name,
                      shape=shape,
                      color=dt.Color(1, 1, 0),
                      m=obj.getMatrix(worldSpace=True),
                      **kwargs)
    return ctl


def get_child_controller(obj):
    child = pm.controller(obj, query=True, children=True)
    children = []
    while child is not None:
        children.extend(child)
        tags = []
        for c in child:
            tags.extend(pm.listConnections(c, type="controller"))
        child = pm.controller(tags, query=True, children=True)
    return children
