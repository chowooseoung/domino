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
    title_name = "Eyelid 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_container_lineEdit(
            ui.eye_lineEdit,
            ui.eye_pushButton,
            "eye_component")
        self.ui_funcs.install_mesh_lineEdit(
            ui.mesh_lineEdit,
            ui.mesh_pushButton,
            "mesh")

        self.ui_funcs.install_checkBox(
            ui.skin_checkBox,
            "auto_skinning")

        self.ui_funcs.install_index_lineEdit(
            ui.eyelid_vertex_loop_lineEdit,
            ui.eyelid_vertex_loop_pushButton,
            "eyelid_vertex_loop")
        self.ui_funcs.install_index_lineEdit(
            ui.eyelid_outer_vertex_lineEdit,
            ui.eyelid_outer_vertex_pushButton,
            "eyelid_outer_vertex")
        self.ui_funcs.install_index_lineEdit(
            ui.eyelid_inner_vertex_lineEdit,
            ui.eyelid_inner_vertex_pushButton,
            "eyelid_inner_vertex")
        self.ui_funcs.install_index_lineEdit(
            ui.eye_hole_vertex_loop_lineEdit,
            ui.eye_hole_vertex_loop_pushButton,
            "eye_hole_vertex_loop")
        self.ui_funcs.install_index_lineEdit(
            ui.eye_hole_outer_vertex_lineEdit,
            ui.eye_hole_outer_vertex_pushButton,
            "eye_hole_outer_vertex")
        self.ui_funcs.install_index_lineEdit(
            ui.eye_hole_inner_vertex_lineEdit,
            ui.eye_hole_inner_vertex_pushButton,
            "eye_hole_inner_vertex")

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 474)
            self.resize(size)
