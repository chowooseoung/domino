# domino
from domino.assembler.ui import CommonComponentSettings
from domino.lib import matrix

# gui
from PySide2 import QtWidgets, QtCore
from . import settings_ui

# maya
from maya import cmds as mc


class IndividualSettings(QtWidgets.QWidget, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(IndividualSettings, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(CommonComponentSettings):
    title_name = "Lip 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_container_lineEdit(
            ui.head_lineEdit,
            ui.head_pushButton,
            "head_component")
        self.ui_funcs.install_container_lineEdit(
            ui.jaw_lineEdit,
            ui.jaw_pushButton,
            "jaw_component")
        self.ui_funcs.install_mesh_lineEdit(
            ui.mesh_lineEdit,
            ui.mesh_pushButton,
            "mesh")

        self.ui_funcs.install_checkBox(
            ui.skin_checkBox,
            "auto_skinning")

        self.ui_funcs.install_index_lineEdit(
            ui.outer_edge_loop_lineEdit,
            ui.outer_edge_loop_pushButton,
            "outer_edge_loop")
        self.ui_funcs.install_index_lineEdit(
            ui.outer_upper_vertex_lineEdit,
            ui.outer_upper_vertex_pushButton,
            "outer_upper_vertex")
        self.ui_funcs.install_index_lineEdit(
            ui.outer_lower_vertex_lineEdit,
            ui.outer_lower_vertex_pushButton,
            "outer_lower_vertex")
        self.ui_funcs.install_index_lineEdit(
            ui.inner_edge_loop_lineEdit,
            ui.inner_edge_loop_pushButton,
            "inner_edge_loop")
        self.ui_funcs.install_index_lineEdit(
            ui.inner_upper_vertex_lineEdit,
            ui.inner_upper_vertex_pushButton,
            "inner_upper_vertex")
        self.ui_funcs.install_index_lineEdit(
            ui.inner_lower_vertex_lineEdit,
            ui.inner_lower_vertex_pushButton,
            "inner_lower_vertex")

        ui.mirror_pushButton.clicked.connect(self.mirror_guide_pos)

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(370, 474)
            self.resize(size)

    def mirror_guide_pos(self):
        selected = mc.ls(selection=True)
        if not selected:
            return
        mirror_table = {
            "3": "4",
            "4": "3",
            "5": "6",
            "6": "5",
            "7": "8",
            "8": "7"
        }

        mc.undoInfo(openChunk=True)
        for sel in selected:
            if not mc.objExists(sel + ".is_guide"):
                continue
            parent = mc.listRelatives(sel, parent=True)[0]
            if not mc.objExists(parent + ".is_guide"):
                continue
            if mc.getAttr(parent + ".component") != "lip_01":
                continue
            for plug in mc.listConnections(sel + ".worldMatrix[0]", source=False, destination=True, plugs=True):
                if "anchors" not in plug:
                    continue
                index = plug.split("[")[-1].split("]")[0]
                if index not in mirror_table:
                    break
                m = matrix.get_matrix(sel)
                mirror_m = matrix.get_mirror_matrix(m)
                mirror_index = mirror_table[index]
                target = mc.listConnections(plug.replace(index, mirror_index), source=True, destination=False)[0]
                matrix.set_matrix(target, mirror_m)
                break
        mc.undoInfo(closeChunk=True)
