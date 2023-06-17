# built-ins
import sys
import os

# domino
from .lib import log, menu
from .lib.rigging import quick_menu

__version__ = [1, 0, 0]
__version_str__ = ". ".join([str(x) for x in __version__])

DOMINO_ROOT = "DOMINO_ROOT"

DOMINO_DEFAULT_COMPONENT = "DOMINO_DEFAULT_COMPONENT"
DOMINO_CUSTOM_COMPONENT = "DOMINO_CUSTOM_COMPONENT"

DOMINO_CUSTOM_STEP_DIR = "DOMINO_CUSTOM_STEP_DIR"

DOMINO_RIG_TEMPLATE_DIR = "DOMINO_RIG_TEMPLATE_DIR"
DOMINO_COPYCAT_TEMPLATE_DIR = "DOMINO_COPYCAT_TEMPLATE_DIR"


def register_domino():
    dir_name = os.path.dirname(__file__)
    os.environ[DOMINO_ROOT] = os.path.join(dir_name, "..", "..")


def register_manager():
    domino_root = os.getenv(DOMINO_ROOT, None)
    os.environ[DOMINO_DEFAULT_COMPONENT] = "domino.assembler.component"
    custom_component_dir = os.getenv(DOMINO_CUSTOM_COMPONENT, None)
    if custom_component_dir and custom_component_dir not in sys.path:
        log.Logger.info(f"append custom component path '{custom_component_dir}'")
        sys.path.append(custom_component_dir)
    if os.getenv(DOMINO_RIG_TEMPLATE_DIR, None) is None:
        os.environ[DOMINO_RIG_TEMPLATE_DIR] = os.path.normpath(os.path.join(domino_root, "rig_templates"))


def register_motion_capture():
    domino_root = os.getenv(DOMINO_ROOT, None)
    if os.getenv(DOMINO_COPYCAT_TEMPLATE_DIR, None) is None:
        os.environ[DOMINO_COPYCAT_TEMPLATE_DIR] = os.path.normpath(os.path.join(domino_root, "copycat_templates"))


def install():
    log.Logger.info("Domino Installing...")

    register_domino()
    register_manager()  # DOMINO_DEFAULT_EDITION, DOMINO_CUSTOM_EDITION, DOMINO_TEMPLATE_DIR
    register_motion_capture()  #
    menu_install()


def menu_install():
    menu.create()

    # quick menu checkbox
    quick_menu.install(menu.menu_id)

    # manager
    manager_menu()

    # ---
    menu.divide(menu.menu_id)

    # RiggingTools
    rigging_menu()

    # MotionCaptureTools
    motion_capture_menu()

    # ---
    menu.divide(menu.menu_id)

    # Utils
    utils_menu()


cb_manager = """import domino.assembler.ui as assembler_ui
assembler_ui.open_manager()"""

cb_settings = """import domino.assembler.ui as assembler_ui
assembler_ui.open_settings()"""

cb_build_from_selection_guide = """import domino.assembler as assembler
from maya import cmds as mc
selected = mc.ls(selection=True)
if selected:
    assembler.create_rig(guide=selected[0])"""

cb_build_from_selection_rig = """import domino.assembler as assembler
from maya import cmds as mc
selected = mc.ls(selection=True)
if selected:
    assembler.create_rig(rig=selected[0])"""

cb_extract_guide_from_rig = """import domino.assembler as assembler
assembler.extract_guide_from_rig()"""

cb_extract_ctl_shapes = """import domino.assembler as assembler
from maya import cmds as mc
selected = mc.ls(selection=True)
if selected:
    assembler.extract_shape(selected)"""

cb_save_guide = """import domino.assembler.io as assembler_io
assembler_io.dump()"""

cb_load_guide = """import domino.assembler.io as assembler_io
assembler_io.load(guide=True, rig=False)"""


def manager_menu():
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


cb_load_template = """import domino.assembler.io
domino.assembler.io.load(r"{path}", True, False)"""


def templates_menu(parent_menu_id):
    template_dir = os.getenv(DOMINO_RIG_TEMPLATE_DIR, None)
    template_list = os.listdir(template_dir)
    template_path_list = [os.path.normpath(os.path.join(template_dir, x)) for x in template_list]
    commands = []
    for i, name in enumerate(template_list):
        commands.append((name.split(".")[0], cb_load_template.format(path=template_path_list[i])))
    menu.add("Templates", commands, parent_menu_id)


cb_pose_manager_ui = """import domino.assembler.ui as assembler_ui
assembler_ui.open_pose_manager()"""


def rigging_menu():
    command = (
        ("Pose Manager", cb_pose_manager_ui, ""),
    )
    menu.add("Rigging Tools", command)


cb_copycat_ui = """import domino.copycat.ui
domino.copycat.ui.open_ui()"""


def motion_capture_menu():
    commands = (
        ("CopyCat UI", cb_copycat_ui, ""),
    )
    menu.add("Motion Capture Tools", commands)


cb_reload_domino = """import domino.lib.utils
domino.lib.utils.reload_domino()"""

cb_reinstall_menu = """import domino
domino.menu_install()"""


def utils_menu():
    commands = (
        ("Reload Domino", cb_reload_domino, ""),
        ("ReInstall Menu", cb_reinstall_menu, ""),
    )
    menu.add("Utils", commands)
