# domino
from domino.assembler.ui import CommonComponentSettings

# gui
from PySide2 import QtWidgets
from . import settings_ui


class IndividualSettings(QtWidgets.QWidget, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(IndividualSettings, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(CommonComponentSettings):
    title_name = "Head 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_space_switch_listWidget(
            ui.head_aim_switch_listWidget,
            ui.head_aim_switch_add_pushButton,
            ui.head_aim_switch_remove_pushButton,
            "aim_space_switch_array")
