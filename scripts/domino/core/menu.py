# maya
from pymel import core as pm

menu_id = "Domino"


def create(menu_id=menu_id):
    if pm.menu(menu_id, exists=True):
        pm.deleteUI(menu_id)

    pm.menu(menu_id,
            parent="MayaWindow",
            tearOff=True,
            allowOptionBoxes=True,
            label=menu_id)
    return menu_id


def add(label, commands, parent=menu_id, image=""):
    m = pm.menuItem(parent=parent,
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
            pm.menuItem(divider=True)
            continue
        if not label:
            command(m)
            pm.setParent(m, menu=True)
            continue
        pm.menuItem(label=label, command=command, image=img)
    return m


def divide(parent=menu_id):
    pm.menuItem(divider=True, parent=parent)


cb_reload_domino = """import domino.core.utils
domino.core.utils.reload_domino()"""

cb_reinstall_menu = """import domino.menu
domino.menu.install()"""


def install_utils():
    commands = (
        ("Reload Domino", cb_reload_domino, ""),
        ("ReInstall Menu", cb_reinstall_menu, ""),
    )
    add("Utils", commands)
