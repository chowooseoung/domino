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
    title_name = "Feather 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_checkBox(
            ui.primary_checkBox,
            "primary")
        self.ui_funcs.install_checkBox(
            ui.primary_coverts_checkBox,
            "primary_coverts")
        self.ui_funcs.install_checkBox(
            ui.primary_under_checkBox,
            "primary_under")
        self.ui_funcs.install_checkBox(
            ui.secondary_checkBox,
            "secondary")
        self.ui_funcs.install_checkBox(
            ui.secondary_coverts_checkBox,
            "secondary_coverts")
        self.ui_funcs.install_checkBox(
            ui.secondary_under_checkBox,
            "secondary_under")
        self.ui_funcs.install_checkBox(
            ui.tertiary_checkBox,
            "tertiary")

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 266)
            self.resize(size)
