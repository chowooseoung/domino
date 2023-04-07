# domino
from domino.assembler.ui import CommonComponentSettings

# gui
from PySide2 import QtWidgets


# class IndividualSettings(QtWidgets.QWidget, settings_ui.Ui_Form):
#
#     def __init__(self, parent=None):
#         super(IndividualSettings, self).__init__(parent=parent)
#         self.setupUi(self)


class Settings(CommonComponentSettings):
    title_name = "Metacarpal 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        # ui = IndividualSettings(self.common_settings)
        # self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()
