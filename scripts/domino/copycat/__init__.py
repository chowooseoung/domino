# maya
from maya import cmds as mc
from maya import mel

# built-ins
import os
import json
from xml.etree import ElementTree

# domino
from domino.lib import hierarchy

MAYA_LOCATION = os.environ["MAYA_LOCATION"]

# Source Mel Files
mel.eval('source "' + MAYA_LOCATION + '/scripts/others/hikGlobalUtils.mel"')
mel.eval('source "' + MAYA_LOCATION + '/scripts/others/hikCharacterControlsUI.mel"')
mel.eval('source "' + MAYA_LOCATION + '/scripts/others/hikDefinitionOperations.mel"')


def prepare_rig(file):
    mc.file(newFile=True, force=True)

    mc.file(file, namespace=":", i=True)


def load_interface(interface_file, map_file, definition):
    """
    map file data
    {interface name: {ctl name: parent constraint skip attribute}}

    example
    {"match": {"left_arm": "left_arm_ctl"},
     "connector": {"left_arm": {"left_arm_ctl": ["tx", "ty", "tz", "rx", "ry", "rz"]}}}

    match : interface to ctl
    connector: constraint
    """
    if not (os.path.exists(interface_file) and os.path.exists(map_file) and os.path.exists(definition)):
        return 0
    mel.eval("FBXResetImport();")
    mel.eval('FBXImportMode -v "add";')

    new_nodes = mc.file(interface_file, i=True, returnNewNodes=True, usingNamespaces=True, namespace="interface")
    new_joints = [x for x in new_nodes if mc.nodeType(x) == "joint" or mc.nodeType(x) == "transform"]

    with open(map_file, "r", encoding="UTF-8") as f:
        map_data = json.load(f)

    skip_t = ["tx", "ty", "tz"]
    skip_r = ["rx", "ry", "rz"]
    for interface, rig in map_data["match"].items():
        interface_node = f"interface:{interface}"
        m = mc.xform(rig, query=True, matrix=True, worldSpace=True)
        mc.xform(interface_node, matrix=m, worldSpace=True)
    for interface, data in map_data["connector"].items():
        interface_node = f"interface:{interface}"
        for rig, cons_attrs in data.items():
            argument = {"maintainOffset": True}
            _skip_t = list(set(skip_t) - set(cons_attrs))
            if _skip_t:
                argument["skipTranslate"] = [x[1:] for x in _skip_t]
            _skip_r = list(set(skip_r) - set(cons_attrs))
            if _skip_r:
                argument["skipRotate"] = [x[1:] for x in _skip_r]
            mc.parentConstraint(interface_node, rig, **argument)
    interface_root = hierarchy.get_parent(new_joints[0], generations=-1) or new_joints[0]
    mc.makeIdentity(interface_root, apply=True, rotate=True)

    tree = ElementTree.parse(definition)
    match_list = tree.getroot()[0]
    character = mel.eval('hikCreateCharacter("interfaceCharacter");')

    for n, li in enumerate(match_list):
        if li.attrib["value"]:
            interface_node = f"interface:{li.attrib['value']}"
            if mc.objExists(interface_node):
                mel.eval(f'hikSetCharacterObject("{interface_node}", "{character}", {n}, 0);')

    is_locked = mc.getAttr(character + ".InputCharacterizationLock")
    if not is_locked:
        mel.eval("hikToggleLockDefinition();")


def load_motion(file, definition):
    if not (os.path.exists(file) and os.path.exists(definition)):
        return 0
    namespace = os.path.splitext(os.path.basename(definition))[0]
    mel.eval('FBXImportMode -v "merge";')
    mel.eval(f'FBXImport -f "{file.replace(os.sep, "/")}";')

    tree = ElementTree.parse(definition)
    match_list = tree.getroot()[0]
    character = mel.eval('hikCreateCharacter("motionCharacter");')

    # hip position setup
    hip_node = match_list[1].attrib["value"]  # hip
    if not mc.objExists(hip_node):
        hip_node = f"{namespace}:{hip_node}"
    left_foot_node = match_list[4].attrib["value"]  # left foot
    if not mc.objExists(left_foot_node):
        left_foot_node = f"{namespace}:{left_foot_node}"

    hip_pos = mc.xform(hip_node, query=True, translation=True, worldSpace=True)
    left_foot_pos = mc.xform(left_foot_node, query=True, translation=True, worldSpace=True)
    mc.setAttr(hip_node + ".ty", hip_pos[1] - left_foot_pos[1])

    for n, li in enumerate(match_list):
        if li.attrib["value"]:
            motion_node = li.attrib["value"]
            if not mc.objExists(motion_node):
                motion_node = f"{namespace}:{motion_node}"
            if mc.objExists(motion_node):
                mel.eval(f'hikSetCharacterObject("{motion_node}", "{character}", {n}, 0);')
    root = hierarchy.get_parent(motion_node, generations=-1)
    [mc.setAttr(x + ".r", 0, 0, 0) for x in mc.ls(root, dagObjects=True)]

    is_locked = mc.getAttr(character + ".InputCharacterizationLock")
    if not is_locked:
        mel.eval("hikToggleLockDefinition();")


def set_source(character, source):
    uiss = mc.lsUI(long=True, type="optionMenuGrp")
    for ui in uiss:
        if "hikCharacterList" in ui:
            ui_hik_character = ui
            break
    mc.optionMenuGrp(ui_hik_character, edit=True, value=character)
    mel.eval('hikUpdateCurrentCharacterFromUI();')
    mel.eval('hikUpdateContextualUI();')

    for ui in uiss:
        if "hikSourceList" in ui:
            ui_hik_source = ui
            break
    mc.optionMenuGrp(ui_hik_source, edit=True, value=f" {source}")
    mel.eval('hikUpdateCurrentSourceFromUI();')
    mel.eval('hikUpdateContextualUI();')


def bake_anim(ctls):
    pass


def export(file, bake=[]):
    if bake:
        bake_anim(bake)
    mc.file(rename=file)
    mc.file(save=True, type="mayaAscii")
