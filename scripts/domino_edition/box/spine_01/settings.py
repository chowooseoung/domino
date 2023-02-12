# domino
from domino_edition.ui import CommonPieceSettings

# gui
from PySide2 import QtWidgets, QtCore
from . import settings_ui


class IndividualSettings(QtWidgets.QWidget, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(IndividualSettings, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(CommonPieceSettings):
    title_name = "Spine_01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui,
                                             "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_spinBox(
            ui.division_spinBox,
            "division")

        self.ui_funcs.install_spinBox(
            ui.position_spinBox,
            "position",
            0.01)
        self.ui_funcs.install_slider(
            ui.position_horizontalSlider,
            "position",
            0.01)

        self.ui_funcs.install_spinBox(
            ui.hip_position_spinBox,
            "hip_position",
            0.01)
        self.ui_funcs.install_slider(
            ui.hip_position_horizontalSlider,
            "hip_position",
            0.01)

        self.ui_funcs.install_spinBox(
            ui.stretch_spinBox,
            "max_stretch",
            0.01)
        self.ui_funcs.install_slider(
            ui.stretch_horizontalSlider,
            "max_stretch",
            0.01)

        self.ui_funcs.install_spinBox(
            ui.squash_spinBox,
            "max_squash",
            0.01)
        self.ui_funcs.install_slider(
            ui.squash_horizontalSlider,
            "max_squash",
            0.01)

        ui.squash_stretch_pushButton.clicked.connect(self.ui_funcs.open_graph_editor)

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 300)
            self.resize(size)
