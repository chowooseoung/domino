# domino
import sys

from domino.core.api import log
from domino.edition.api import naming
from domino.edition.api.utils import DOMINO_SUB_PIECE_DIR
from ...api import lib

# built-ins
from functools import partial
import os
import subprocess

# gui
from domino.edition.ui import (DominoDialog,
                               UiFunctionSet)
from . import settings_ui
from PySide2 import (QtWidgets,
                     QtCore,
                     QtGui)

# maya
from pymel import core as pm


class Settings(DominoDialog, settings_ui.Ui_Dialog):
    title_name = "Assembly Settings"

    green_brush = QtGui.QColor(0, 160, 0)
    red_brush = QtGui.QColor(180, 0, 0)
    white_brush = QtGui.QColor(255, 255, 255)
    white_down_brush = QtGui.QColor(160, 160, 160)
    orange_brush = QtGui.QColor(240, 160, 0)

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)
        self.setupUi(self)
        self.ui_funcs = UiFunctionSet(ui=self)
        ui = self

        self.setObjectName("DominoAssemblySettings")
        self.resize_window()
        self.visibilitySignal.connect(self.setup_window_title)
        ui.toolBox.currentChanged.connect(self.resize_window)

        self.ui_funcs.install_comboBox(
            ui.icon_name_comboBox,
            "icon_name")

        self.ui_funcs.install_name_lineEdit(
            ui.rig_name_lineEdit,
            "name")
        self.ui_funcs.install_comboBox(
            ui.mode_comboBox,
            "mode")
        self.ui_funcs.install_comboBox(
            ui.end_point_comboBox,
            "end_point")
        self.ui_funcs.install_textEdit(
            ui.notes_textEdit,
            "publish_notes")

        self.ui_funcs.install_spinBox(
            ui.origin_sub_ctl_count_spinBox,
            "origin_sub_ctl_count")
        self.ui_funcs.install_spinBox(
            ui.origin_ctl_size_doubleSpinBox,
            "origin_ctl_size")

        self.ui_funcs.install_checkBox(
            ui.force_uniform_scale_checkBox,
            "force_uni_scale")
        self.ui_funcs.install_checkBox(
            ui.connect_jnt_checkBox,
            "connect_jnt_rig")

        self.ui_funcs.install_checkBox(
            ui.use_RGB_colors_checkBox,
            "use_RGB_colors")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.left_color_ik_pushButton,
            ui.left_color_ik_horizontalSlider,
            ui.left_color_ik_spinBox,
            "l_RGB_ik",
            "l_color_ik")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.left_color_fk_pushButton,
            ui.left_color_fk_horizontalSlider,
            ui.left_color_fk_spinBox,
            "l_RGB_fk",
            "l_color_fk")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.center_color_ik_pushButton,
            ui.center_color_ik_horizontalSlider,
            ui.center_color_ik_spinBox,
            "c_RGB_ik",
            "c_color_ik")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.center_color_fk_pushButton,
            ui.center_color_fk_horizontalSlider,
            ui.center_color_fk_spinBox,
            "c_RGB_fk",
            "c_color_fk")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.right_color_ik_pushButton,
            ui.right_color_ik_horizontalSlider,
            ui.right_color_ik_spinBox,
            "r_RGB_ik",
            "r_color_ik")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.right_color_fk_pushButton,
            ui.right_color_fk_horizontalSlider,
            ui.right_color_fk_spinBox,
            "r_RGB_fk",
            "r_color_fk")

        self.ui_funcs.install_checkBox(
            ui.run_sub_pieces_checkBox,
            "run_sub_pieces")

        ui.sub_pieces_add_pushButton.clicked.connect(self.add_sub_piece)
        ui.sub_pieces_new_pushButton.clicked.connect(self.new_sub_piece)
        ui.sub_pieces_edit_pushButton.clicked.connect(self.edit_sub_piece)
        ui.sub_pieces_remove_pushButton.clicked.connect(self.delete_sub_piece)
        ui.sub_pieces_run_sel_pushButton.clicked.connect(self.run_sub_piece)

        ui.ctl_name_rule_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    [ui.ctl_name_rule_lineEdit,
                     ui.ctl_description_letter_case_comboBox],
                    [naming.DEFAULT_NAMING_RULE,
                     "default"]))

        ui.jnt_name_rule_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    [ui.jnt_name_rule_lineEdit,
                     ui.jnt_description_letter_case_comboBox],
                    [naming.DEFAULT_NAMING_RULE,
                     "default"]))

        ui.ctl_side_name_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    [ui.l_ctl_side_name_lineEdit,
                     ui.r_ctl_side_name_lineEdit,
                     ui.c_ctl_side_name_lineEdit],
                    [naming.DEFAULT_SIDE_L_NAME,
                     naming.DEFAULT_SIDE_R_NAME,
                     naming.DEFAULT_SIDE_C_NAME]))

        ui.jnt_side_name_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    [ui.l_jnt_side_name_lineEdit,
                     ui.r_jnt_side_name_lineEdit,
                     ui.c_jnt_side_name_lineEdit],
                    [naming.DEFAULT_SIDE_L_NAME,
                     naming.DEFAULT_SIDE_R_NAME,
                     naming.DEFAULT_SIDE_C_NAME]))

        ui.index_padding_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    [ui.ctl_index_padding_spinBox,
                     ui.jnt_index_padding_spinBox],
                    [naming.DEFAULT_CTL_INDEX_PADDING,
                     naming.DEFAULT_JNT_INDEX_PADDING]))

        ui.extensions_name_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    [ui.ctl_extensions_name_lineEdit,
                     ui.jnt_extensions_name_lineEdit],
                    [naming.DEFAULT_CTL_EXT_NAME,
                     naming.DEFAULT_JOINT_EXT_NAME]))

        self.ui_funcs.install_lineEdit(
            ui.ctl_name_rule_lineEdit,
            "ctl_name_rule")

        self.ui_funcs.install_lineEdit(
            ui.jnt_name_rule_lineEdit,
            "jnt_name_rule")

        self.ui_funcs.install_comboBox(
            ui.ctl_description_letter_case_comboBox,
            "ctl_description_letter_case")

        self.ui_funcs.install_comboBox(
            ui.jnt_description_letter_case_comboBox,
            "jnt_description_letter_case")

        self.ui_funcs.install_lineEdit(
            ui.l_ctl_side_name_lineEdit,
            "ctl_left_name")

        self.ui_funcs.install_lineEdit(
            ui.r_ctl_side_name_lineEdit,
            "ctl_right_name")

        self.ui_funcs.install_lineEdit(
            ui.c_ctl_side_name_lineEdit,
            "ctl_center_name")

        self.ui_funcs.install_lineEdit(
            ui.l_jnt_side_name_lineEdit,
            "jnt_left_name")

        self.ui_funcs.install_lineEdit(
            ui.r_jnt_side_name_lineEdit,
            "jnt_right_name")

        self.ui_funcs.install_lineEdit(
            ui.c_jnt_side_name_lineEdit,
            "jnt_center_name")

        self.ui_funcs.install_spinBox(
            ui.ctl_index_padding_spinBox,
            "ctl_index_padding")

        self.ui_funcs.install_spinBox(
            ui.jnt_index_padding_spinBox,
            "jnt_index_padding")

        self.ui_funcs.install_lineEdit(
            ui.ctl_extensions_name_lineEdit,
            "ctl_name_ext")

        self.ui_funcs.install_lineEdit(
            ui.jnt_extensions_name_lineEdit,
            "jnt_name_ext")

        # right click menu
        self.ui_funcs.init_listWidget(ui.sub_pieces_listWidget, "sub_pieces")
        ui.sub_pieces_listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        ui.sub_pieces_listWidget.customContextMenuRequested.connect(partial(self.sub_piece_context_menu))
        ui.sub_pieces_listWidget.installEventFilter(self)

    def resize_window(self):
        index = self.toolBox.currentIndex()
        if index == 0:
            size = QtCore.QSize(370, 605)
            self.resize(size)
        elif index == 1:
            size = QtCore.QSize(370, 510)
            self.resize(size)
        elif index == 2:
            size = QtCore.QSize(370, 574)
            self.resize(size)

    def add_sub_piece(self):
        sub_piece_dir = os.getenv(DOMINO_SUB_PIECE_DIR, "")
        directory = sub_piece_dir if sub_piece_dir else pm.workspace(q=True, rootDirectory=True)

        file_path = pm.fileDialog2(fileMode=1,
                                   startingDirectory=directory,
                                   okc="Add",
                                   fileFilter="Sub piece .py (*.py)")
        if not file_path:
            return
        file_path = file_path[0]
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Quick clean the first empty item
        items_list = [i.text() for i in self.sub_pieces_listWidget.findItems("", QtCore.Qt.MatchContains)]
        if items_list and not items_list[0]:
            self.sub_pieces_listWidget.takeItem(0)

        if sub_piece_dir:
            file_path = os.path.abspath(file_path)
            base_path = os.path.abspath(sub_piece_dir)
            file_path = file_path.replace(base_path, "").replace("\\", "/")
            if file_path.startswith("/"):
                file_path = file_path[1:]

        item_data = file_name + " | " + file_path
        item = QtWidgets.QListWidgetItem(item_data)
        self.sub_pieces_listWidget.addItem(item)
        self.ui_funcs.update_listWidget(self.sub_pieces_listWidget, "sub_pieces")

    def new_sub_piece(self):
        sub_piece_dir = os.getenv(DOMINO_SUB_PIECE_DIR, "")
        directory = sub_piece_dir if sub_piece_dir else pm.workspace(q=True, rootDirectory=True)

        file_path = pm.fileDialog2(fileMode=0,
                                   startingDirectory=directory,
                                   okc="Add",
                                   fileFilter="Sub piece .py (*.py)")
        if not file_path:
            return
        file_path = file_path[0]
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Quick clean the first empty item
        items_list = [i.text() for i in self.sub_pieces_listWidget.findItems("", QtCore.Qt.MatchContains)]
        if items_list and not items_list[0]:
            self.sub_pieces_listWidget.takeItem(0)

        content = """# domino 
import domino_edition.api.piece as p

        
class SubPiece(p.AbstractSubPiece):

    def run(self, context):
        ...
"""
        with open(file_path, "w") as f:
            f.write(content)

        if sub_piece_dir:
            file_path = os.path.abspath(file_path)
            base_path = os.path.abspath(sub_piece_dir)
            file_path = file_path.replace(base_path, "").replace("\\", "/")
            if file_path.startswith("/"):
                file_path = file_path[1:]

        item_data = file_name + " | " + file_path
        item = QtWidgets.QListWidgetItem(item_data)
        self.sub_pieces_listWidget.addItem(item)
        self.ui_funcs.update_listWidget(self.sub_pieces_listWidget, "sub_pieces")

    def edit_sub_piece(self):
        items = self.sub_pieces_listWidget.selectedItems()
        if not items:
            return
        data = items[0].text()
        full_path = data.split(" | ")[-1]

        if full_path:
            try:
                if sys.platform.startswith("darwin"):
                    subprocess.call(("open", full_path))
                elif os.name == "nt":
                    os.startfile(full_path)
                elif os.name == "posix":
                    subprocess.call("xdg-open", full_path)
            except Exception:
                log.Logger.error(f"'{full_path}' can't be find")

    def delete_sub_piece(self):
        for item in self.sub_pieces_listWidget.selectedItems():
            if item.text() in ["objects", "attributes", "operators", "connections", "cleanup"]:
                item.setSelected(False)
        self.ui_funcs.remove_items_listWidget(self.sub_pieces_listWidget, "sub_pieces")

    def run_sub_piece(self):
        items = self.sub_pieces_listWidget.selectedItems()
        if items:
            lib.run_sub_pieces({"run_sub_pieces": True}, [i.text() for i in items])

    def sub_piece_context_menu(self, QPos):
        current_item = self.sub_pieces_listWidget.currentItem()
        if current_item is None:
            return None
        self.sub_piece_menu = QtWidgets.QMenu()
        parent_position = self.sub_pieces_listWidget.mapToGlobal(QtCore.QPoint(0, 0))
        menu_item_01 = self.sub_piece_menu.addAction("Toggle Sub Piece")
        self.sub_piece_menu.addSeparator()
        menu_item_02 = self.sub_piece_menu.addAction("Turn OFF Selected")
        menu_item_03 = self.sub_piece_menu.addAction("Turn ON Selected")
        self.sub_piece_menu.addSeparator()
        menu_item_04 = self.sub_piece_menu.addAction("Turn OFF All")
        menu_item_05 = self.sub_piece_menu.addAction("Turn ON All")

        menu_item_01.triggered.connect(self.toggle_status_sub_piece)
        menu_item_02.triggered.connect(partial(self.set_status_sub_piece, False, True))
        menu_item_03.triggered.connect(partial(self.set_status_sub_piece, True, True))
        menu_item_04.triggered.connect(partial(self.set_status_sub_piece, False, False))
        menu_item_05.triggered.connect(partial(self.set_status_sub_piece, True, False))

        self.sub_piece_menu.move(parent_position + QPos)
        self.sub_piece_menu.show()

    def toggle_status_sub_piece(self):
        items = self.sub_pieces_listWidget.selectedItems()
        for item in items:
            if item.text().startswith("*"):
                item.setText(item.text()[1:])
            else:
                item.setText("*" + item.text())
        self.ui_funcs.update_listWidget(self.sub_pieces_listWidget, "sub_pieces")

    def set_status_sub_piece(self, status, selected):
        if selected:
            items = self.sub_pieces_listWidget.selectedItems()
        else:
            items = [self.sub_pieces_listWidget.item(i) for i in range(self.sub_pieces_listWidget.count())]

        for item in items:
            off = item.text().startswith("*")
            if status and off:
                item.setText(item.text()[1:])
            elif not status and not off:
                item.setText("*" + item.text())
        self.ui_funcs.update_listWidget(self.sub_pieces_listWidget, "sub_pieces")

    def eventFilter(self, sender, event):
        if event.type() == QtCore.QEvent.ChildRemoved:
            if sender == self.sub_pieces_listWidget:
                datas = [i.text() for i in self.sub_pieces_listWidget.selectedItems()]
                const_check = False
                for const in ["objects", "attributes", "operators", "connections", "cleanup"]:
                    if const in datas:
                        const_check = True
                        break
                if const_check:
                    self.ui_funcs.init_listWidget(sender, "sub_pieces")
                else:
                    self.ui_funcs.update_listWidget(sender, "sub_pieces")
            return True
        else:
            return QtWidgets.QDialog.eventFilter(self, sender, event)
