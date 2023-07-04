# domino
from domino.assembler.ui import CommonComponentSettings

# gui
from PySide2 import QtWidgets, QtCore
from . import settings_ui


class IndividualSettings(QtWidgets.QWidget, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(IndividualSettings, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(CommonComponentSettings):
    title_name = "Wire 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_spinBox(
            ui.division_spinBox,
            "division")
        self.ui_funcs.install_spinBox(
            ui.turning_point_doubleSpinBox,
            "turning_point")
        self.ui_funcs.install_curve_btn(
            ui.wire_curve_lineEdit,
            ui.select_wire_curve_pushButton,
            "wire_curve")
        self.ui_funcs.install_spinBox(
            ui.up_normal_x_doubleSpinBox,
            "up_normal_x")
        self.ui_funcs.install_spinBox(
            ui.up_normal_y_doubleSpinBox,
            "up_normal_y")
        self.ui_funcs.install_spinBox(
            ui.up_normal_z_doubleSpinBox,
            "up_normal_z")

        self.ui_funcs.install_parent_btn(
            ui.head_parent_lineEdit,
            ui.add_head_parent_pushButton,
            "head_parent")
        self.ui_funcs.install_spinBox(
            ui.head_range_spinBox,
            "head_range")

        self.ui_funcs.install_parent_btn(
            ui.tail_parent_lineEdit,
            ui.add_tail_parent_pushButton,
            "tail_parent")
        self.ui_funcs.install_spinBox(
            ui.tail_range_spinBox,
            "tail_range")

        self.ui_funcs.install_checkBox(
            ui.fk_path_checkBox,
            "fk_path")

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 400)
            self.resize(size)
