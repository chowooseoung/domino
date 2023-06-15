# built-ins
import json
import os

# domino
from domino.lib import hierarchy
from domino import DOMINO_RIG_TEMPLATE_DIR
from domino import assembler, log

# maya
from maya import cmds as mc


def dump(file_path=None):
    node = mc.ls(selection=True)
    if not node:
        return None

    if file_path is None:
        file_path = mc.fileDialog2(caption="Save Domino guide",
                                   startingDirectory=os.getenv(DOMINO_RIG_TEMPLATE_DIR, None),
                                   fileFilter="Domino Guide (*.domino)",
                                   fileMode=0)
        if file_path:
            file_path = file_path[0]
        else:
            return None

    node = node[0] if hierarchy.is_assembly(node[0]) else hierarchy.get_parent(node[0], generations=-1)
    if mc.attributeQuery("is_guide", node=node, exists=True):
        node_hierarchy = assembler.get_guide_hierarchy(node, full_path=True)
    elif mc.attributeQuery("is_rig", node=node, exists=True):
        assembly_node = mc.listConnections(node + ".assembly_node", source=False, destination=True)[0]
        node_hierarchy = assembler.get_rig_hierarchy(assembly_node)
    else:
        return None

    comp = assembler.convert_node_to_component(node_hierarchy)
    data = assembler.convert_component_to_data(comp)

    log.Logger.info("Save Guide : `{0}`".format(file_path))
    with open(file_path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load(file_path=None, guide=False, rig=True, context=None):
    if context is None:
        context = {}
    if file_path is None:
        file_path = mc.fileDialog2(caption="Load Domino guide",
                                   startingDirectory=os.getenv(DOMINO_RIG_TEMPLATE_DIR, None),
                                   fileFilter="Domino Guide (*.domino)",
                                   fileMode=1)
        if file_path:
            file_path = file_path[0]
        else:
            return None

    with open(file_path, "r") as f:
        data = json.load(f)

    if guide:
        log.Logger.info("Load Guide : `{0}`".format(file_path))
        assembler.create_guide(data)
    if rig:
        log.Logger.info("Load Rig : `{0}`".format(file_path))
        assembler.create_rig(data=data, context=context)
