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
    title_name = "Ui Slider 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_checkBox(
            ui.frame_checkBox,
            "frame")
        self.ui_funcs.install_spinBox(
            ui.size_doubleSpinBox,
            "size")

        self.ui_funcs.install_checkBox(
            ui.plus_x_checkBox,
            "plus_x")
        self.ui_funcs.install_checkBox(
            ui.plus_y_checkBox,
            "plus_y")
        self.ui_funcs.install_checkBox(
            ui.minus_x_checkBox,
            "minus_x")
        self.ui_funcs.install_checkBox(
            ui.minus_y_checkBox,
            "minus_y")

        self.ui_funcs.install_lineEdit(
            ui.plus_x_name_lineEdit,
            "plus_x_name")
        self.ui_funcs.install_lineEdit(
            ui.plus_y_name_lineEdit,
            "plus_y_name")
        self.ui_funcs.install_lineEdit(
            ui.minus_x_name_lineEdit,
            "minus_x_name")
        self.ui_funcs.install_lineEdit(
            ui.minus_y_name_lineEdit,
            "minus_y_name")

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 378)
            self.resize(size)
