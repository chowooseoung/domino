# domino
from domino.core import menu
from domino.edition.api import utils

# built-ins
import os

cb_manager = """import domino.edition.ui
domino.edition.ui.open_manager()"""

cb_settings = """import domino.edition.ui
domino.edition.ui.open_settings()"""

cb_build_from_selection_guide = """import domino.edition.api.lib
import pymel.core as pm
selected = pm.ls(selection=True)
if selected:
    domino.edition.api.lib.create_rig(guide=selected[0])"""

cb_build_from_selection_rig = """import domino.edition.api.lib
import pymel.core as pm
selected = pm.ls(selection=True)
if selected:
    domino.edition.api.lib.create_rig(rig=selected[0])"""

cb_extract_guide_from_rig = """import domino.edition.api.lib
domino.edition.api.lib.extract_guide_from_rig()"""

cb_extract_ctl_shapes = """import domino.edition.api.lib
import pymel.core as pm
selected = pm.ls(selection=True)
if selected:
    domino.edition.api.lib.extract_ctl_shapes(selected)"""

cb_save_guide = """import domino.edition.api.lib
domino.edition.api.lib.save()"""

cb_load_guide = """import domino.edition.api.lib
domino.edition.api.lib.load(guide=True, rig=False)"""


def install():
    commands = (
        ("Manager", cb_manager, ""),
        ("Settings", cb_settings, ""),
        ("Extract ctl shapes", cb_extract_ctl_shapes, ""),
        ("---", None),
        ("Build from selection(Guide)", cb_build_from_selection_guide, ""),
        ("Build from selection(Rig)", cb_build_from_selection_rig, ""),
        ("Extract Guide from Rig", cb_extract_guide_from_rig, ""),
        ("---", None),
        ("Save Guide", cb_save_guide, ""),
        ("Load Guide", cb_load_guide, ""),
        ("---", None),
        (None, templates_menu),
    )
    menu.add("Domino Edition", commands)


cb_load_template = """import domino.edition.api.lib
domino.edition.api.lib.load(r"{path}", True, False)"""


def templates_menu(parent_menu_id):
    template_dir = os.getenv(utils.DOMINO_TEMPLATE_DIR, None)
    template_list = os.listdir(template_dir)
    template_path_list = [os.path.normpath(os.path.join(template_dir, x)) for x in template_list]
    commands = []
    for i, name in enumerate(template_list):
        commands.append((name.split(".")[0], cb_load_template.format(path=template_path_list[i])))
    menu.add("Templates", commands, parent_menu_id)
