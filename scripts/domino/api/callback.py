# maya
from pymel import core as pm

# domino
from . import attribute


def space_switch(source_ctls, target_ctl, host, switch_attr_name="space_switch"):
    """
    source_ctls : switch source objects
    target_ctl : domino controller
    host : ui host
    """
    # add host 
    enum_name = ["this"] + [x.nodeName() for x in source_ctls]
    match_attr_name = switch_attr_name + "_match"
    attribute.add(host,
                  match_attr_name,
                  "enum",
                  enumName=enum_name,
                  channelBox=True)

    container = pm.container(query=True, findContainer=host)
    root = pm.PyNode(pm.container(container, query=True, publishAsRoot=True))

    d_id = root.attr("d_id").get()
    script_node = pm.createNode("script")
    attribute.add(script_node,
                  "root",
                  "message")
    attribute.add(script_node,
                  "d_id",
                  "string",
                  value=d_id)
    script_node.attr("sourceType").set(1)
    script_node.attr("scriptType").set(0)

    host = host.fullPathName()
    target_ctl = target_ctl.fullPathName()
    script_code = \
        f"""import maya.cmds as mc
import maya.api.OpenMaya as om2


class SpaceSwitch:

    def __init__(self, namespace):
        if namespace:
            namespace += ":"
        self.host = "{host}"
        self.host = "|".join([namespace + x for x in self.host.split("|")][1:])

        self.ctl = "{target_ctl}"
        self.ctl = "|".join([namespace + x for x in self.ctl.split("|")][1:])

        self.match_attr = "{match_attr_name}"
        self.switch_attr = "{switch_attr_name}"

    def switch(self):
        current_time = mc.currentTime(query=True)
        destination_value = mc.getAttr(self.host + "." + self.match_attr)
        temp_obj = mc.createNode("transform", name="SPACESWITCHTEMP")
        mc.matchTransform(temp_obj, self.ctl, position=True, rotation=True)
        mc.setKeyframe(self.ctl, attribute=["tx", "ty", "tz", "rx", "ry", "rz"], time=current_time - 1)
        mc.setAttr(self.host + "." + self.switch_attr, destination_value)
        mc.setKeyframe(self.host, attribute=self.switch_attr)
        mc.matchTransform(self.ctl, temp_obj, position=True, rotation=True)
        mc.setKeyframe(self.ctl, attribute=["tx", "ty", "tz", "rx", "ry", "rz"])
        mc.delete(temp_obj)

    def space_switch(self):
        mc.undoInfo(openChunk=True)
        
        try:
            selected = mc.ls(selection=True)
            value = mc.getAttr(self.host + "." + self.match_attr)
            if value not in {range(len(enum_name) + 1)}:
                return
            switch_value = mc.getAttr(self.host + "." + self.switch_attr)
            if value != switch_value:
                self.switch()
            mc.select(selected)
        except Exception as e:
            print(e)
        finally:
            mc.undoInfo(closeChunk=True)
            

def cb_run(msg, plug1, plug2, client_data):
    if msg != 2056:
        return
    if plug1.partialName(includeNodeName=False) != "{match_attr_name}":
        return
    client_data.space_switch()


def register_cb(namespace):
    if namespace:
        namespace += ":"
    target_node = "{host}"
    target_node = "|".join([namespace + x for x in target_node.split("|")][1:])
    sel_list = om2.MGlobal.getSelectionListByName(target_node)
    node_dag = sel_list.getDagPath(0)
    node_obj = sel_list.getDependNode(0)
    cb_id = om2.MNodeMessage.addAttributeChangedCallback(node_obj,
                                                         cb_run,
                                                         clientData=SpaceSwitch(namespace))
    return (node_dag, cb_id)


def run_space_switch_callback():
    global domino_character_cb_registry
    global domino_character_namespace_registry

    d_id = "{d_id}"

    script_nodes = [x for x in mc.ls(type="script") if mc.objExists(x + ".d_id")]
    script_nodes = [x for x in script_nodes if mc.getAttr(x + ".d_id") == d_id]

    if not script_nodes:
        return None

    for sc_node in script_nodes:
        namespace = mc.ls(sc_node, showNamespace=True)[1]
        namespace = "" if namespace == ":" else namespace
        if namespace not in domino_character_namespace_registry:
            try:
                domino_character_cb_registry.append(register_cb(namespace))
            except:
                domino_character_cb_registry = []
                domino_character_cb_registry.append(register_cb(namespace))
run_space_switch_callback()"""
    pm.scriptNode(script_node, edit=True, beforeScript=script_code)
    return script_node


def match_ik_fk():
    pass
