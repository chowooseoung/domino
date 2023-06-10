# maya
from maya import cmds as mc

# domino
from domino.lib import matrix, hierarchy, icon, attribute


def add_npo(node, name, offset_parent_matrix=False):
    name = name if name else node + "_npo"
    npo = mc.createNode("transform", name=name, parent=hierarchy.get_parent(node))
    m = matrix.get_matrix(node, world_space=True)
    matrix.set_matrix(npo, m, world_space=True, offset_parent_matrix=offset_parent_matrix)
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
    check_lock_attr = [mc.getAttr(node + "." + attr, lock=True) for attr in attrs]
    [mc.setAttr(node + "." + attr, lock=False) for attr in attrs]
    node = mc.parent(node, npo)[0]
    [mc.setAttr(node + "." + attr, lock=True) for i, attr in enumerate(attrs) if check_lock_attr[i] == 1]
    return npo, node


def add_ctl(parent, name, m, parent_ctl=None, attrs=(), mirror_config=(0,) * 9, shape_args=None, **config):
    ctl = icon.create(parent=parent, name=name, m=m, **shape_args)
    matrix.set_matrix(ctl, m)
    attach_tag(ctl, parent_ctl)

    mc.addAttr(ctl, longName="is_ctl", attributeType="bool", keyable=False)

    lock_hide_attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
    [lock_hide_attrs.remove(x) for x in attrs]
    [mc.setAttr(ctl + "." + attr, lock=True) for attr in lock_hide_attrs]
    [mc.setAttr(ctl + "." + attr, keyable=False) for attr in lock_hide_attrs]

    if config:
        attribute.add_attr(ctl, longName="component_root", type="message")
        attribute.add_attr(ctl, longName="component_host", type="message")
        # Required to publish attribute.
        attribute.add_attr(ctl, longName="identifier", type="string")
        mc.setAttr(ctl + ".identifier", config["identifier"], type="string")
        # Required to use mirror pose.
        attribute.add_attr(ctl, longName="mirror_ctl_name", type="string")
        mc.setAttr(ctl + ".mirror_ctl_name", config["mirror_ctl_name"], type="string")
    # Required to use rbf manager.
    # Required to use mirror pose.
    attribute.add_mirror_config_channels(ctl, mirror_config)
    return ctl


def add_placeholder(parent, name, offset=(0, 0, 0)):
    ph = mc.createNode("transform", name=name, parent=parent)
    mc.setAttr(ph + ".rotate", *offset)
    return ph


def attach_tag(node, parent=None):
    mc.controller(node)
    control_tag = mc.controller(node, query=True)[0]
    mc.setAttr(control_tag + ".visibilityMode", 1)
    if parent:
        parent_control_tag = mc.controller(parent, query=True)[0]
        mc.setAttr(parent_control_tag + ".cycleWalkSibling", True)
        mc.connectAttr(parent_control_tag + ".prepopulate", control_tag + ".prepopulate", force=True)

        plug = attribute.get_plug(parent_control_tag, "children")
        num = plug.numElements()
        index = 0
        if num == plug.numConnectedElements():
            index = num
        else:
            for i in range(num):
                if not mc.listConnections(parent_control_tag + ".children[{}]".format(i), source=True,
                                          destination=False):
                    index = num
        for x in mc.listConnections(control_tag + ".parent", source=False, destination=True, plugs=True) or []:
            mc.disconnectAttr(control_tag + ".parent", x)
        mc.connectAttr(control_tag + ".parent", parent_control_tag + ".children[{}]".format(index))


def get_children(node):
    def get_child_tag(n):
        tag = mc.controller(n, query=True)[0]
        return mc.listConnections(tag + ".children", source=True, destination=False) or []

    def get_ctl_object(tag):
        return mc.listConnections(tag + ".controllerObject", source=True, destination=False) or []

    child_tags = get_child_tag(node)
    child = [y for t in child_tags for y in get_ctl_object(t)]
    children = []
    while child is not None:
        children.extend(child)
        tags = []
        for c in child:
            tags.extend(get_child_tag(c))
        child = list([y for t in tags for y in get_ctl_object(t)]) or None
    return children


def get_parent(node):
    tag = mc.controller(node, query=True)[0]
    parent = mc.listConnections(tag + ".parent", source=False, destination=True)
    if parent:
        return mc.listConnections(parent[0] + ".controllerObject", source=True, destination=True)[0]
