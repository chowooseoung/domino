# maya
from pymel import core as pm

# domino
from domino.core import attribute, matrix

# built-ins
import uuid


def create_script_node(d_id):
    sn = pm.createNode("script")
    script_node_id = str(uuid.uuid4())
    attribute.add(sn, "d_id", "string", value=d_id)
    attribute.add(sn, "sn_id", "string", value=script_node_id)
    return sn, script_node_id


def space_switch(source_ctls, target_ctl, host, switch_attr_name="space_switch"):
    """
    source_ctls : switch source objects
    target_ctl : domino controller
    host : ui host
    """
    # add host 
    enum_name = ["this"] + [x.nodeName() for x in source_ctls]
    match_attr_name = switch_attr_name + "_match"
    attribute.add(host, match_attr_name, "enum", enumName=enum_name, channelBox=True)

    container = pm.container(query=True, findContainer=host)
    root = pm.PyNode(pm.container(container, query=True, publishAsRoot=True))

    d_id = root.attr("d_id").get()
    script_node, script_node_id = create_script_node(d_id)
    attribute.add(script_node, "root", "message")
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
        try:
            mc.undoInfo(openChunk=True)
            selected = mc.ls(selection=True)
            value = mc.getAttr(self.host + "." + self.match_attr)
            if value not in {range(len(enum_name) + 1)}:
                return
            switch_value = mc.getAttr(self.host + "." + self.switch_attr)
            if value != switch_value:
                self.switch()
            mc.undoInfo(closeChunk=True)
        except Exception as e:
            mc.undoInfo(closeChunk=True)
            mc.undo()
            print(e)
        finally:
            mc.select(selected)
            

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

    d_id = "{d_id}"
    sn_id = "{script_node_id}"

    script_nodes = [x for x in mc.ls(type="script") if mc.objExists(x + ".d_id")]
    script_nodes = [x for x in script_nodes if mc.getAttr(x + ".d_id") == d_id]
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
    pm.scriptNode(script_node, edit=True, beforeScript=script_code)
    return script_node


def fk_to_ik(_switch, source, target):
    pole_vec_pos = matrix.get_pole_vec_position([x.getTranslation(worldSpace=True) for x in source], 2)
    pole_match_obj = pm.createNode("transform", name="MATCHFKTOIKPOLEVECTEMP")
    pole_match_obj.attr("t").set(pole_vec_pos)
    ik_ctl_m = source[-1].getMatrix(worldSpace=True)

    pm.setAttr(_switch.attr("fk_ik"), 1)
    ik_ctl, pole_vec_ctl = target
    pm.matchTransform(pole_vec_ctl, pole_match_obj, position=True)
    ik_ctl.setMatrix(ik_ctl_m, worldSpace=True)
    pm.delete(pole_match_obj)


def ik_to_fk(_switch, source, target):
    pm.setAttr(_switch.attr("fk_ik"), 0)
    [pm.matchTransform(t, source[i], rotation=True) for i, t in enumerate(target)]


def match_fk_ik(switch, fk_source, ik_source, fk_target, ik_target):
    switch = pm.PyNode(switch)
    if fk_source is not None:
        fk_source = [pm.PyNode(x) for x in fk_source]
    if ik_source is not None:
        ik_source = [pm.PyNode(x) for x in ik_source]
    if fk_target is not None:
        fk_target = [pm.PyNode(x) for x in fk_target]
    if ik_target is not None:
        ik_target = [pm.PyNode(x) for x in ik_target]

    if round(switch.attr("fk_ik").get(), 0):
        ik_to_fk(switch, fk_source, fk_target)
    else:
        fk_to_ik(switch, ik_source, ik_target)
