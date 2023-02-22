# maya
from pymel import core as pm

# built-ins
import os
import json
from xml.etree import ElementTree


def load_interface(interface_file, map_file, definition, prefix="interface"):
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
    pm.importFile(interface_file, namespace=":")

    with open(map_file, "r") as f:
        map_data = json.load(f)

    skip_t = ["tx", "ty", "tz"]
    skip_r = ["rx", "ry", "rz"]
    for interface, data in map_data["match"].items():
        for rig, match_obj in data.items():
            pm.matchTransform(interface, match_obj, position=True, rotation=True)
    for interface, data in map_data["connector"].items():
        for rig, cons_attrs in data.items():
            pm.parentConstraint(interface,
                                rig,
                                skipTranslate=list(set(skip_t) - set(cons_attrs)),
                                skipRotate=list(set(skip_r) - set(cons_attrs)),
                                maintainOffset=True)
    interface_root = pm.PyNode(interface).getParent(generations=-1)
    pm.makeIdentity(interface_root, apply=True, rotate=True)

    tree = ElementTree.parse(definition)
    match_list = tree.getroot()[0]
    character = pm.mel.eval('hikCreateCharacter("interface");')

    n = 0
    for li in match_list:
        if li.attrib["value"]:
            if prefix:
                interface_node = f"{prefix}_{li.attrib['value']}"
            else:
                interface_node = li.attrib['value']
            if pm.objExists(interface_node):
                pm.mel.eval(f'hikSetCharacterObject("{interface_node}", "{character}", {n}, 0);')
        n += 1


def load_mocap(file, definition, prefix="mocap"):
    if not (os.path.exists(file) and os.path.exists(definition)):
        return 0
    pm.importFile(file, namespace=":")

    tree = ElementTree.parse(definition)
    match_list = tree.getroot()[0]
    character = pm.mel.eval('hikCreateCharacter("mocap");')

    n = 0
    for li in match_list:
        if li.attrib["value"]:
            if prefix:
                mocap_node = f"{prefix}_{li.attrib['value']}"
            else:
                mocap_node = li.attrib["value"]
            if pm.objExists(mocap_node):
                pm.mel.eval(f'hikSetCharacterObject("{mocap_node}", "{character}", {n}, 0);')
        n += 1


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


def bake_anim():
    pass


def export(file):
    pass
