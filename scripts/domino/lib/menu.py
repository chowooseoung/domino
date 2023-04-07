# maya
from maya import cmds as mc

menu_id = "Domino"


def create(menu_id=menu_id):
    if mc.menu(menu_id, exists=True):
        mc.deleteUI(menu_id)

    mc.menu(menu_id,
            parent="MayaWindow",
            tearOff=True,
            allowOptionBoxes=True,
            label=menu_id)
    return menu_id


def add(label, commands, parent=menu_id, image=""):
    m = mc.menuItem(parent=parent,
                    subMenu=True,
                    tearOff=True,
                    label=label,
                    image=image)
    for c in commands:
        if len(c) == 3:
            label, command, img = c
        else:
            label, command = c
            img = ""
        if not command:
            mc.menuItem(divider=True)
            continue
        if not label:
            command(m)
            mc.setParent(m, menu=True)
            continue
        mc.menuItem(label=label, command=command, image=img)
    return m


def divide(parent=menu_id):
    mc.menuItem(divider=True, parent=parent)
