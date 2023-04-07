# maya
from maya import cmds as mc

# domino
from domino.lib import attribute

# built-ins
import uuid

base_callback = """import maya.cmds as mc
import maya.api.OpenMaya as om2
import traceback


def destroy_cb(*args):  # all callback clear
    global domino_destroy_new_id
    global domino_destroy_open_id
    global domino_destroy_remove_ref_id
    global domino_destroy_unload_ref_id
    global domino_character_cb_registry
    global domino_character_namespace_registry
        
    try:
        for array in domino_character_cb_registry:
            om2.MNodeMessage.removeCallback(array[1])
        om2.MSceneMessage.removeCallback(domino_destroy_new_id)
        om2.MSceneMessage.removeCallback(domino_destroy_open_id)
        om2.MSceneMessage.removeCallback(domino_destroy_remove_ref_id)
        om2.MSceneMessage.removeCallback(domino_destroy_unload_ref_id)
        del domino_character_cb_registry
        del domino_character_namespace_registry
        del domino_destroy_new_id
        del domino_destroy_open_id
        del domino_destroy_remove_ref_id
        del domino_destroy_unload_ref_id
    except:
        traceback.print_exc()


def refresh_registry(*argc):  # refresh registry at reference unload, remove
    global domino_character_cb_registry
    global domino_character_namespace_registry

    remove_list = []
    for ns in domino_character_namespace_registry:
        if not mc.namespaceInfo(ns, listNamespace=True):
            remove_list.append(ns)
    for rm in remove_list:
        domino_character_namespace_registry.remove(rm)
    for array in domino_character_cb_registry:
        if array[0].fullPathName() == "":
            om2.MNodeMessage.removeCallback(array[1])
    domino_character_cb_registry = [x for x in domino_character_cb_registry if x[0].fullPathName() != ""]


def run_callback_root():
    global domino_script_node_id_registry
    global domino_destroy_id
    global domino_character_namespace_registry
    try:
        domino_character_namespace_registry
    except:
        domino_character_namespace_registry = []
    domino_script_node_id_registry = []

    component_id = '{component_id}'
    
    root_sets = []
    for o_set in mc.ls(type="objectSet"):
        plugs = mc.listConnections(o_set + ".message", destination=True, source=False, plugs=True) or []
        for plug in plugs:
            if plug.endswith("root_sets"):
                root_sets.append(o_set)

    roots = [y for s in root_sets for y in mc.sets(s, query=True)]
    roots = [r for r in roots if mc.getAttr(r + ".component_id") == component_id]

    if "" in domino_character_namespace_registry:
        domino_character_namespace_registry.remove("")
    if not roots:
        return
    for root in roots:
        callback_root = mc.listConnections(root + ".message",
                                           destination=True,
                                           source=False,
                                           type="script")
        namespace = mc.ls(root, showNamespace=True)[1]
        namespace = "" if namespace == ":" else namespace
        if callback_root and namespace not in domino_character_namespace_registry:
            callbacks = mc.listConnections(callback_root[0] + ".callbacks",
                                           destination=True,
                                           source=False,
                                           type="script")
            for cb in callbacks:
                mc.scriptNode(cb, executeBefore=True)
            domino_character_namespace_registry.append(namespace)

run_callback_root()
try:
    om2.MSceneMessage.removeCallback(domino_destroy_new_id)
except:
    pass
finally:
    domino_destroy_new_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterNew, destroy_cb)

try:
    om2.MSceneMessage.removeCallback(domino_destroy_open_id)
except:
    pass
finally:
    domino_destroy_open_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterOpen, destroy_cb)

try:
    om2.MSceneMessage.removeCallback(domino_destroy_remove_ref_id)
except:
    pass
finally:
    domino_destroy_remove_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterRemoveReference, refresh_registry)

try:
    om2.MSceneMessage.removeCallback(domino_destroy_unload_ref_id)
except:
    pass
finally:
    domino_destroy_unload_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterUnloadReference, refresh_registry)"""


def create_script_node(component_id):
    sn = mc.createNode("script")
    script_node_id = str(uuid.uuid4())
    attribute.add_attr(sn, longName="component_id", type="string")
    mc.setAttr(sn + ".component_id", component_id, type="string")
    attribute.add_attr(sn, longName="sn_id", type="string")
    mc.setAttr(sn + ".sn_id", script_node_id, type="string")
    return sn, script_node_id


def space_switch(source_ctls, target_ctl, host, switch_attr_name="space_switch"):
    """
    source_ctls : switch source objects
    target_ctl : domino controller
    host : ui host
    """
    # add host 
    enum_name = ["this"] + [x.split("|")[-1] for x in source_ctls]
    match_attr_name = switch_attr_name + "_match"
    attribute.add_attr(host, longName=match_attr_name, type="enum", enumName=":".join(enum_name))
    mc.setAttr(host + "." + match_attr_name, channelBox=True)

    outputs = mc.listConnections(host + ".message", source=False, destination=True, plugs=True)
    root = [x.split(".")[0] for x in outputs if x.endswith(".host")][0]

    component_id = mc.getAttr(root + ".component_id")
    script_node, script_node_id = create_script_node(component_id)
    attribute.add_attr(script_node, longName="root", type="message")
    mc.setAttr(script_node + ".sourceType", 1)
    mc.setAttr(script_node + ".scriptType", 0)

    host = mc.ls(host, long=True)[0]
    target_ctl = mc.ls(target_ctl, long=True)[0]
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
        mc.setKeyframe(self.host, attribute=[self.switch_attr], time=current_time - 1)
        mc.setAttr(self.host + "." + self.switch_attr, destination_value)
        mc.setKeyframe(self.host, attribute=self.switch_attr)
        mc.matchTransform(self.ctl, temp_obj, position=True, rotation=True)
        mc.setKeyframe(self.ctl, attribute=["tx", "ty", "tz", "rx", "ry", "rz"])
        mc.delete(temp_obj)

    def space_switch(self):
        try:
            mc.undoInfo(openChunk=True)
            selected = mc.ls(selection=True)
            value = mc.getAttr(self.host + "." + self.match_attr)
            if value not in {range(len(enum_name) + 1)}:
                return
            switch_value = mc.getAttr(self.host + "." + self.switch_attr)
            if value != switch_value:
                self.switch()
        except Exception as e:
            print(e)
        finally:
            mc.select(selected)
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
    global domino_script_node_id_registry
    global domino_character_namespace_registry

    component_id = "{component_id}"
    sn_id = "{script_node_id}"
    script_nodes = [x for x in mc.ls(type="script") if mc.objExists(x + ".component_id")]
    script_nodes = [x for x in script_nodes if mc.getAttr(x + ".component_id") == component_id]
    script_nodes = [x for x in script_nodes if mc.getAttr(x + ".sn_id") == sn_id]

    if not script_nodes:
        return None
    for sc_node in script_nodes:
        namespace = mc.ls(sc_node, showNamespace=True)[1]
        namespace = "" if namespace == ":" else namespace
        script_node_id = mc.getAttr(sc_node + ".sn_id")
        if namespace not in domino_character_namespace_registry and script_node_id not in domino_script_node_id_registry:
            try:
                domino_character_cb_registry.append(register_cb(namespace))
            except:
                domino_character_cb_registry = []
                domino_character_cb_registry.append(register_cb(namespace))
            domino_script_node_id_registry.append(script_node_id)
run_space_switch_callback()"""
    mc.scriptNode(script_node, edit=True, beforeScript=script_code)
    return script_node
