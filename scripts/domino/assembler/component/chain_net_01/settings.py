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
    title_name = "Chain Net 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_checkBox(
            ui.guide_orientation_checkBox,
            "guide_orientation")
        self.ui_funcs.install_spinBox(
            ui.division_spinBox,
            "division")
        self.ui_funcs.install_comboBox(
            ui.degree_comboBox,
            "degree")

        self.ui_funcs.install_container_lineEdit(
            ui.master_a_lineEdit,
            ui.master_a_pushButton,
            "master_a")
        self.ui_funcs.install_container_lineEdit(
            ui.master_b_lineEdit,
            ui.master_b_pushButton,
            "master_b")
        self.ui_funcs.install_spinBox(
            ui.blend_spinBox,
            "blend",
            0.01)
        self.ui_funcs.install_slider(
            ui.blend_horizontalSlider,
            "blend",
            0.01)

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 300)
            self.resize(size)
