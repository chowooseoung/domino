# domino
from domino.assembler.ui import CommonComponentSettings

# gui
from PySide2 import QtWidgets, QtCore
from . import settings_ui

# built-ins
from functools import partial


class IndividualSettings(QtWidgets.QWidget, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(IndividualSettings, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(CommonComponentSettings):
    title_name = "Leg 2 Jnt 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_spinBox(
            ui.fk_ik_spinBox,
            "fk_ik",
            0.01)
        self.ui_funcs.install_slider(
            ui.fk_ik_horizontalSlider,
            "fk_ik",
            0.01)

        self.ui_funcs.install_spinBox(
            ui.upper_division_spinBox,
            "upper_division")
        self.ui_funcs.install_spinBox(
            ui.lower_division_spinBox,
            "lower_division")
        self.ui_funcs.install_spinBox(
            ui.max_stretch_doubleSpinBox,
            "max_stretch")

        self.ui_funcs.install_checkBox(
            ui.guide_orient_ankle_checkBox,
            "guide_orient_ankle")
        self.ui_funcs.install_checkBox(
            ui.support_knee_jnt_checkBox,
            "support_knee_jnt")

        self.ui_funcs.install_space_switch_listWidget(
            ui.ik_space_switch_listWidget,
            ui.ik_space_switch_add_pushButton,
            ui.ik_space_switch_remove_pushButton,
            "ik_space_switch_array")
        self.ui_funcs.install_space_switch_listWidget(
            ui.pv_space_switch_listWidget,
            ui.pv_space_switch_add_pushButton,
            ui.pv_space_switch_remove_pushButton,
            "pv_space_switch_array")
        self.ui_funcs.install_space_switch_listWidget(
            ui.pin_space_switch_listWidget,
            ui.pin_space_switch_add_pushButton,
            ui.pin_space_switch_remove_pushButton,
            "pin_space_switch_array")

        ui.squash_stretch_pushButton.clicked.connect(self.ui_funcs.open_graph_editor)

        ui.pv_to_ik_space_switch_pushButton.clicked.connect(
            partial(self.ui_funcs.copy_space_switch_listWidget,
                    ui.ik_space_switch_listWidget,
                    "pv_space_switch_array",
                    "ik_space_switch_array"))
        ui.ik_to_pin_space_switch_pushButton.clicked.connect(
            partial(self.ui_funcs.copy_space_switch_listWidget,
                    ui.pin_space_switch_listWidget,
                    "ik_space_switch_array",
                    "pin_space_switch_array"))
        ui.ik_to_pv_space_switch_pushButton.clicked.connect(
            partial(self.ui_funcs.copy_space_switch_listWidget,
                    ui.pv_space_switch_listWidget,
                    "ik_space_switch_array",
                    "pv_space_switch_array"))

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 755)
            self.resize(size)
