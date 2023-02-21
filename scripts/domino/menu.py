# domino
from domino.core.api import menu
from domino.edition.api import quick_menu
from domino.edition.api import menu as edition_menu


def install():
    menu.create()

    # quick menu checkbox
    quick_menu.install(menu.menu_id)

    # Edition
    edition_menu.install()

    # ---
    menu.divide(menu.menu_id)

    # RiggingTools
    rigging_menu()

    # MotionCaptureTools
    motion_capture_menu()

    # ---
    menu.divide(menu.menu_id)

    # Utils
    menu.install_utils()


cb_add_blended_jnt = """import domino_edition.api.lib
domino_edition.api.lib.add_blended_jnt()"""

cb_add_support_jnt = """import domino_edition.api.lib
domino_edition.api.lib.add_support_jnt()"""

cb_pose_manager_ui = """import domino_edition.ui
domino_edition.ui.open_pose_manager()"""


def rigging_menu():
    command = (
        ("Add Blended Joint", cb_add_blended_jnt, ""),
        ("Add Support Joint", cb_add_support_jnt, ""),
        ("---", None),
        ("Pose Manager", cb_pose_manager_ui, "")
    )
    menu.add("Rigging Tools", command)


def motion_capture_menu():
    commands = (
        ("MotionCaptureCmd", "print('TODO')", ""),
    )
    menu.add("Motion Capture Tools", commands)
