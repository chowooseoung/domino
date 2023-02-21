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


cb_add_blended_jnt = """import domino.edition.api.lib
domino.edition.api.lib.add_blended_jnt()"""

cb_add_support_jnt = """import domino.edition.api.lib
domino.edition.api.lib.add_support_jnt()"""

cb_pose_manager_ui = """import domino.edition.ui
domino.edition.ui.open_pose_manager()"""


def rigging_menu():
    command = (
        ("Add Blended Joint", cb_add_blended_jnt, ""),
        ("Add Support Joint", cb_add_support_jnt, ""),
        ("---", None),
        ("Pose Manager", cb_pose_manager_ui, "")
    )
    menu.add("Rigging Tools", command)


cb_motion_capture_ui = """import domino.motion_capture.ui
domino.motion_capture.ui.open_ui()"""


def motion_capture_menu():
    commands = (
        ("MotionCapture UI", cb_motion_capture_ui, ""),
    )
    menu.add("Motion Capture Tools", commands)
