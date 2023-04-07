# maya
from maya import cmds as mc
from maya import mel

# domino
from domino.lib import attribute


def set_current_asset(asset):
    mc.container(asset, edit=True, current=True) if asset else mel.eval("ClearCurrentContainer;")


def add_advanced_asset(parent, name):
    set_current_asset(parent)
    new_container = mc.container(name=name)
    set_current_asset(new_container)
    return new_container


def remove_node_from_asset(node):
    while mc.container(query=True, findContainer=node):
        mc.container(mc.container(query=True, findContainer=node), edit=True, removeNode=node)


def publish_node(node):
    pub_name = node.split("|")[-1]
    asset = mc.container(query=True, findContainer=node)
    mc.containerPublish(asset, publishNode=(pub_name, ""))
    mc.containerPublish(asset, bindNode=(pub_name, node))


def publish_attribute(node):
    publish_attrs = []
    for attr in mc.listAttr(node, userDefined=True, shortNames=True):
        plug = attribute.get_plug(node, attr)
        if plug.isChannelBox or plug.isKeyable:
            publish_attrs.append(attr)

    asset = mc.container(query=True, findContainer=node)
    component_identifier = ""
    if mc.attributeQuery("identifier", node=node, exists=True):
        component_identifier = mc.getAttr(node + ".identifier")
    for attr in publish_attrs:
        publish_name = component_identifier + ("_I_" + attr if attr != "_I" else "")
        mc.container(asset, edit=True, publishName=publish_name)
        mc.container(asset, edit=True, bindAttr=[node + "." + attr, publish_name])
