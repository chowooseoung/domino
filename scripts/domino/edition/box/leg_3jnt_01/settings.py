# domino
from domino.edition.ui import CommonPieceSettings

# gui
from PySide2 import QtWidgets, QtCore
from . import settings_ui


class IndividualSettings(QtWidgets.QWidget, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(IndividualSettings, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(CommonPieceSettings):
    title_name = "Leg 3 Jnt 01 Settings"

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
            ui.division1_spinBox,
            "division1")
        self.ui_funcs.install_spinBox(
            ui.division2_spinBox,
            "division2")
        self.ui_funcs.install_spinBox(
            ui.division3_spinBox,
            "division3")
        self.ui_funcs.install_spinBox(
            ui.max_stretch_doubleSpinBox,
            "max_stretch")

        self.ui_funcs.install_checkBox(
            ui.spring_solver_checkBox,
            "spring_solver")

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

        ui.squash_stretch_pushButton.clicked.connect(self.ui_funcs.open_graph_editor)

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 585)
            self.resize(size)
