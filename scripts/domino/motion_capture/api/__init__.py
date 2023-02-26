# maya
from pymel import core as pm

# built-ins
import os
import json
from xml.etree import ElementTree

MAYA_LOCATION = os.environ["MAYA_LOCATION"]

# Source Mel Files
pm.mel.eval('source "' + MAYA_LOCATION + '/scripts/others/hikGlobalUtils.mel"')
pm.mel.eval('source "' + MAYA_LOCATION + '/scripts/others/hikCharacterControlsUI.mel"')
pm.mel.eval('source "' + MAYA_LOCATION + '/scripts/others/hikDefinitionOperations.mel"')


def prepare_rig(file):
    pm.newFile(force=True)

    pm.importFile(file, namespace=":")


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
    pm.FBXResetImport()
    pm.mel.eval('FBXImportMode -v "add";')

    new_nodes = pm.importFile(interface_file, returnNewNodes=True, usingNamespaces=True, namespace="interface")
    new_joints = [x for x in new_nodes if x.type() == "joint" or x.type() == "transform"]

    with open(map_file, "r") as f:
        map_data = json.load(f)

    skip_t = ["tx", "ty", "tz"]
    skip_r = ["rx", "ry", "rz"]
    for interface, rig in map_data["match"].items():
        interface_node = f"interface:{interface}"
        pm.matchTransform(interface_node, rig, position=True, rotation=True)
    for interface, data in map_data["connector"].items():
        interface_node = f"interface:{interface}"
        for rig, cons_attrs in data.items():
            argument = {}
            argument["maintainOffset"] = True
            _skip_t = list(set(skip_t) - set(cons_attrs))
            if _skip_t:
                argument["skipTranslate"] = [x[1:] for x in _skip_t]
            _skip_r = list(set(skip_r) - set(cons_attrs))
            if _skip_r:
                argument["skipRotate"] = [x[1:] for x in _skip_r]
            pm.parentConstraint(interface_node, rig, **argument)
    interface_root = new_joints[0].getParent(generations=-1)
    pm.makeIdentity(interface_root, apply=True, rotate=True)

    tree = ElementTree.parse(definition)
    match_list = tree.getroot()[0]
    character = pm.mel.eval('hikCreateCharacter("interfaceCharacter");')

    for n, li in enumerate(match_list):
        if li.attrib["value"]:
            interface_node = f"interface:{li.attrib['value']}"
            if pm.objExists(interface_node):
                pm.mel.eval(f'hikSetCharacterObject("{interface_node}", "{character}", {n}, 0);')

    is_locked = pm.getAttr(character + ".InputCharacterizationLock")
    if not is_locked:
        pm.mel.eval("hikToggleLockDefinition();")


def load_motion(file, definition):
    if not (os.path.exists(file) and os.path.exists(definition)):
        return 0
    pm.mel.eval('FBXImportMode -v "merge";')
    pm.mel.eval(f'FBXImport -f "{file.replace(os.sep, "/")}";')

    tree = ElementTree.parse(definition)
    match_list = tree.getroot()[0]
    character = pm.mel.eval('hikCreateCharacter("motionCharacter");')

    for n, li in enumerate(match_list):
        if li.attrib["value"]:
            motion_node = li.attrib["value"]
            if not pm.objExists(motion_node):
                motion_node = f"{pm.Path(definition).namebase}:{motion_node}"
            if pm.objExists(motion_node):
                pm.mel.eval(f'hikSetCharacterObject("{motion_node}", "{character}", {n}, 0);')
    root = pm.PyNode(motion_node).getParent(generations=-1)
    [x.attr("r").set((0, 0, 0)) for x in pm.ls(root, dagObjects=True)]

    is_locked = pm.getAttr(character + ".InputCharacterizationLock")
    if not is_locked:
        pm.mel.eval("hikToggleLockDefinition();")


def set_source(character, source):
    uiss = pm.lsUI(long=True, type="optionMenuGrp")
    for ui in uiss:
        if "hikCharacterList" in ui:
            ui_hik_character = ui
    pm.optionMenuGrp(ui_hik_character, edit=True, value=character)
    pm.mel.eval('hikUpdateCurrentCharacterFromUI();')
    pm.mel.eval('hikUpdateContextualUI();')

    for ui in uiss:
        if "hikSourceList" in ui:
            ui_hik_source = ui
    pm.optionMenuGrp(ui_hik_source, edit=True, value=f" {source}")
    pm.mel.eval('hikUpdateCurrentSourceFromUI();')
    pm.mel.eval('hikUpdateContextualUI();')


def bake_anim(ctls):
    pass


def export(file, bake=[]):
    if bake:
        bake_anim(bake)
    pm.saveAs(file, force=True)
