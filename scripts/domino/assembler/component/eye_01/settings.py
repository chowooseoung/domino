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
    title_name = "Eye 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_checkBox(
            ui.mirror_behaviour_checkBox,
            "mirror_behaviour")

        self.ui_funcs.install_space_switch_listWidget(
            ui.aim_space_switch_listWidget,
            ui.aim_space_switch_add_pushButton,
            ui.aim_space_switch_remove_pushButton,
            "aim_space_switch_array")

        self.ui_funcs.install_checkBox(
            ui.spherical_iris_pupil_rig_checkBox,
            "spherical_iris_pupil_rig")
        self.ui_funcs.install_mesh_lineEdit(
            ui.eyeball_mesh_lineEdit,
            ui.eyeball_mesh_pushButton,
            "eyeball_mesh")
        self.ui_funcs.install_index_lineEdit(
            ui.center_edge_index_lineEdit,
            ui.center_edge_index_pushButton,
            "center_edge_index")
        self.ui_funcs.install_index_lineEdit(
            ui.limbus_edge_index_lineEdit,
            ui.limbus_edge_index_pushButton,
            "limbus_edge_index")
        self.ui_funcs.install_index_lineEdit(
            ui.pupil_edge_index_lineEdit,
            ui.pupil_edge_index_pushButton,
            "pupil_edge_index")
        self.ui_funcs.install_index_lineEdit(
            ui.last_edge_index_lineEdit,
            ui.last_edge_index_pushButton,
            "last_edge_index")

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 500)
            self.resize(size)
