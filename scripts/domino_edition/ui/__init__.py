# gui
from PySide2 import (QtWidgets,
                     QtCore,
                     QtGui)
from . import (common_piece_settings_ui,
               jnt_name_setting_ui,
               manager_ui)

# built-ins
from functools import partial
import os

# maya
from pymel import core as pm

# domino
from domino_edition.api import (utils,
                                lib)
from domino_edition.api.piece import (Identifier,
                                      find_guide_from_identifier)
from domino.api.color import MAYA_OVERRIDE_COLOR
from domino.api import log


class DominoDialog(QtWidgets.QDialog):
    visibilitySignal = QtCore.Signal(int)

    def showEvent(self, event):
        self.visibilitySignal.emit(0)
        super(DominoDialog, self).showEvent(event)

    def closeEvent(self, event):
        self.visibilitySignal.emit(1)
        super(DominoDialog, self).closeEvent(event)

    def hideEvent(self, event):
        self.visibilitySignal.emit(2)
        super(DominoDialog, self).hideEvent(event)

    def setup_window_title(self):
        name = self.ui_funcs._root.nodeName()
        self.setWindowTitle(f"{self.title_name} ({name})")


class UiFunctionSet:

    def __init__(self, ui):
        self.ui = ui
        self._root = None
        self._piece = None
        self._pieces = None
        self.closed = True
        self.ui.visibilitySignal.connect(self.initialize)

    @property
    def root(self):
        if self._root is None:
            root = pm.ls(selection=True, type="transform")
            if root:
                has_d_id = root[0].hasAttr("d_id")
                has_is_guide = root[0].hasAttr("is_domino_guide")
                if has_d_id and has_is_guide:
                    self._root = root[0]
        if not pm.objExists(self._root):
            self.ui.close()
            return None
        return self._root

    @property
    def piece(self):
        if self._root and self._piece is None:
            self._piece = utils.collect_piece(guide=self._root.fullPathName(),
                                              rig=None,
                                              datas=None)[0]
        return self._piece

    @property
    def pieces(self):
        if self._root:
            assembly = self._root.getParent(generations=-1)
            self._pieces = utils.collect_piece(guide=assembly,
                                               rig=None,
                                               datas=None)
        return self._pieces

    def initialize(self, state):
        if state == 0 and self.closed:
            self._root = None
            self._piece = None
            self._pieces = None
            self.closed = False
            log.Logger.info(f"root : {self.root.nodeName()}")
        elif state in [1, 2]:
            self.closed = True

    def get_attr_from_piece(self, attr):
        at = pm.attributeQuery(attr, node=self._root, attributeType=True)
        if at == "enum":
            return pm.getAttr(f"{self._root}.{attr}", asString=True)
        return pm.getAttr(f"{self._root}.{attr}")

    def set_attr_to_piece(self, attr, value):
        at = pm.attributeQuery(attr, node=self._root, attributeType=True)
        if at == "typed":
            pm.setAttr(f"{self._root}.{attr}",
                       value,
                       type="string")
        elif at == "enum":
            en = pm.attributeQuery(attr,
                                   node=self._root,
                                   listEnum=True)[0]
            enum_names = en.split(":")
            index = enum_names.index(value)
            pm.setAttr(f"{self._root}.{attr}", index)
        else:
            if isinstance(value, (list, tuple)):
                pm.setAttr(f"{self._root}.{attr}", *value)
            else:
                pm.setAttr(f"{self._root}.{attr}", value)

    def is_valid_identifier(self, name, side, index):
        valid_identifier = True
        if self._root in pm.ls(assemblies=True):
            return valid_identifier
        assembly = self._root.getParent(generations=-1)
        containers = pm.ls(assembly,
                           dagObjects=True,
                           type="dagContainer")
        containers.remove(self._root)
        for container in containers[1:]:
            d_name = container.attr("name").get()
            d_side = container.attr("side").get(asString=True)
            d_index = container.attr("index").get()
            if name == d_name and \
                    side == d_side and \
                    index == d_index:
                valid_identifier = False
                break
        return valid_identifier

    def update_name_lineEdit(self, state, l_edit, target_attr):
        if state == 0:  # show
            l_edit.setText(self.get_attr_from_piece(target_attr))
        elif state in [-1, 1, 2]:  # default, hide, close
            with pm.UndoChunk():
                new_name = l_edit.text()
                if self.get_attr_from_piece("module") != "assembly_01":
                    side = self.get_attr_from_piece("side")
                    index = self.get_attr_from_piece("index")
                    valid_identifier = self.is_valid_identifier(
                        new_name, side, index)
                else:
                    valid_identifier = self.is_valid_identifier(
                        new_name, "", "")
                if not valid_identifier:
                    l_edit.setText(self.get_attr_from_piece(target_attr))
                else:
                    self.set_attr_to_piece(target_attr, new_name)
                    self.piece.ddata.sync()
                    self.piece.ddata.sync(True)
                self.ui.setup_window_title()

    def install_name_lineEdit(self, l_edit, target_attr):
        self.ui.visibilitySignal.connect(
            partial(self.update_name_lineEdit,
                    l_edit=l_edit,
                    target_attr=target_attr))
        l_edit.editingFinished.connect(
            partial(self.update_name_lineEdit,
                    state=-1,
                    l_edit=l_edit,
                    target_attr=target_attr))

    def update_side_comboBox(self, state, c_box, target_attr):
        if state == 0:  # show
            c_box.setCurrentText(self.get_attr_from_piece(target_attr))
        elif state in [-1, 1, 2]:  # default, hide, close
            with pm.UndoChunk():
                name = self.get_attr_from_piece("name")
                new_side = c_box.currentText()
                index = self.get_attr_from_piece("index")
                valid_identifier = self.is_valid_identifier(name,
                                                            new_side,
                                                            index)
                if not valid_identifier:
                    c_box.setCurrentText(self.get_attr_from_piece(target_attr))
                else:
                    self.set_attr_to_piece(target_attr, new_side)
                    self.piece.ddata.sync()
                    self.piece.ddata.sync(True)
                self.ui.setup_window_title()

    def install_side_comboBox(self, c_box, target_attr):
        self.ui.visibilitySignal.connect(
            partial(self.update_side_comboBox,
                    c_box=c_box,
                    target_attr=target_attr))
        c_box.currentTextChanged.connect(
            lambda _: self.update_side_comboBox(
                state=-1,
                c_box=c_box,
                target_attr=target_attr))

    def update_index_spinBox(self, state, s_box, target_attr):
        if state == 0:  # show
            s_box.setValue(self.get_attr_from_piece(target_attr))
        elif state in [-1, 1, 2]:  # default, hide, close
            with pm.UndoChunk():
                name = self.get_attr_from_piece("name")
                side = self.get_attr_from_piece("side")
                new_index = s_box.value()
                valid_identifier = self.is_valid_identifier(name,
                                                            side,
                                                            new_index)
                if not valid_identifier:
                    s_box.setValue(self.get_attr_from_piece(target_attr))
                else:
                    self.set_attr_to_piece(target_attr, new_index)
                    self.piece.ddata.sync()
                    self.piece.ddata.sync(True)
                self.ui.setup_window_title()

    def install_index_spinBox(self, s_box, target_attr):
        self.ui.visibilitySignal.connect(
            partial(self.update_index_spinBox,
                    s_box=s_box,
                    target_attr=target_attr))
        s_box.valueChanged.connect(
            lambda _: self.update_index_spinBox(
                state=-1,
                s_box=s_box,
                target_attr=target_attr))

    def update_spinBox(self, s_box, target_attr, _factor, state, *args):
        if state == 0:  # show
            s_box.setValue(self.get_attr_from_piece(target_attr) / _factor)
        elif state in [-1, 1, 2]:  # default, hide, close
            with pm.UndoChunk():
                self.set_attr_to_piece(target_attr, s_box.value() * _factor)

    def install_spinBox(self, s_box, target_attr, factor=1):
        self.ui.visibilitySignal.connect(
            partial(self.update_spinBox,
                    s_box,
                    target_attr,
                    factor))
        s_box.valueChanged.connect(
            partial(self.update_spinBox,
                    s_box,
                    target_attr,
                    factor,
                    -1))

    def update_lineEdit(self, state, l_edit, target_attr):
        if state == 0:  # show
            l_edit.setText(self.get_attr_from_piece(target_attr))
        elif state in [-1, 1, 2]:  # default, hide, close
            with pm.UndoChunk():
                name = l_edit.text()
                self.set_attr_to_piece(target_attr, name)

    def install_lineEdit(self, l_edit, target_attr):
        self.ui.visibilitySignal.connect(
            partial(self.update_lineEdit,
                    l_edit=l_edit,
                    target_attr=target_attr))
        l_edit.editingFinished.connect(
            partial(self.update_lineEdit,
                    state=-1,
                    l_edit=l_edit,
                    target_attr=target_attr))

    def update_comboBox(self, c_box, target_attr, state, *args):
        if state == 0:  # show
            c_box.setCurrentText(self.get_attr_from_piece(target_attr))
        elif state in [-1, 1, 2]:  # default, hide, close
            with pm.UndoChunk():
                value = c_box.currentText()
                self.set_attr_to_piece(target_attr, value)

    def install_comboBox(self, c_box, target_attr):
        self.ui.visibilitySignal.connect(
            partial(self.update_comboBox,
                    c_box,
                    target_attr))
        c_box.currentTextChanged.connect(
            partial(self.update_comboBox,
                    c_box,
                    target_attr,
                    -1))

    def update_checkBox(self, state, c_box, target_attr):
        if state == 0:  # show
            c_box.setChecked(self.get_attr_from_piece(target_attr))
        elif state in [-1, 1, 2]:  # default, hide, close
            with pm.UndoChunk():
                self.set_attr_to_piece(target_attr, c_box.isChecked())

    def install_checkBox(self, c_box, target_attr):
        self.ui.visibilitySignal.connect(
            partial(self.update_checkBox,
                    c_box=c_box,
                    target_attr=target_attr))
        c_box.stateChanged.connect(
            lambda _: self.update_checkBox(
                state=-1,
                c_box=c_box,
                target_attr=target_attr))

    def update_slider(self, slider, target_attr, factor, state, *args):
        if state == 0:  # show
            slider.setValue(int(self.get_attr_from_piece(target_attr) / factor))
        elif state in [-1, 1, 2]:  # default, hide, close
            with pm.UndoChunk():
                self.set_attr_to_piece(target_attr, slider.value() * factor)

    def install_slider(self, slider, target_attr, factor=1):
        self.ui.visibilitySignal.connect(
            partial(self.update_slider,
                    slider,
                    target_attr,
                    factor))
        slider.valueChanged.connect(
            partial(self.update_slider,
                    slider,
                    target_attr,
                    factor,
                    -1))

    def update_textEdit(self, t_edit, target_attr, state):
        if state == 0:  # show
            t_edit.setPlainText(self.get_attr_from_piece(target_attr))
        elif state in [-1, 1, 2]:  # default, hide, close
            with pm.UndoChunk():
                self.set_attr_to_piece(target_attr, t_edit.toPlainText())
                s = t_edit.document().size()
                t_edit.setFixedHeight(s.height() + 4)

    def install_textEdit(self, t_edit, target_attr):
        self.ui.visibilitySignal.connect(
            partial(self.update_textEdit,
                    t_edit,
                    target_attr))
        t_edit.textChanged.connect(
            partial(self.update_textEdit,
                    t_edit,
                    target_attr,
                    -1))

    def use_rgb_color_checkBox(self,
                               use_rgb_c_box,
                               btn,
                               slider,
                               s_box,
                               rgb_attr,
                               index_attr,
                               state,
                               *args):
        is_rgb = use_rgb_c_box.isChecked()
        if not is_rgb:
            slider.setVisible(False)
            s_box.setVisible(True)
        else:
            slider.setVisible(True)
            s_box.setVisible(False)
        if state == 0:  # show
            if is_rgb:
                rgb = self.get_attr_from_piece(rgb_attr)
                color = pm.colorManagementConvert(
                    toDisplaySpace=rgb)
                h_value = sorted(rgb)[2]
                if not h_value:
                    color = (0, 0, 0)
                color = ", ".join([str(c * 255) for c in color])
                btn.setStyleSheet("* {background-color: rgb(" + color + ")}")
                slider.setValue(h_value * 100)
            else:
                index = self.get_attr_from_piece(index_attr)
                rgb = [float(x / 255)
                       for x in MAYA_OVERRIDE_COLOR[index]]
                color = pm.colorManagementConvert(
                    toDisplaySpace=rgb)
                color = ",".join([str(c * 255) for c in color])
                btn.setStyleSheet("* {background-color: rgb(" + color + ")}")
                value = self.get_attr_from_piece(index_attr)
                s_box.setValue(value)

    def rgb_color_btn(self, use_rgb_c_box, target_attr):
        if not use_rgb_c_box.isChecked():
            return 0
        pm.colorEditor(rgb=self.get_attr_from_piece(target_attr))
        if pm.colorEditor(query=True, result=True):
            rgb = pm.colorEditor(query=True, rgb=True)
            self.set_attr_to_piece(target_attr, rgb)
            self.ui.visibilitySignal.emit(0)

    def rgb_color_slider(self, target_attr, value):
        rgb = self.get_attr_from_piece(target_attr)
        hsv_value = sorted(rgb)[2]
        if hsv_value:
            new_rgb = tuple(i / (hsv_value / 1.0) * (value / 100)
                            for i in rgb)
        else:
            new_rgb = tuple((1.0 * (value / 100),
                             1.0 * (value / 100),
                             1.0 * (value / 100)))
        self.set_attr_to_piece(target_attr, new_rgb)
        self.ui.visibilitySignal.emit(0)

    def install_color_widgets(self,
                              use_rgb_c_box,
                              btn,
                              slider,
                              s_box,
                              rgb_attr,
                              index_attr):
        self.ui.visibilitySignal.connect(
            partial(self.use_rgb_color_checkBox,
                    use_rgb_c_box,
                    btn,
                    slider,
                    s_box,
                    rgb_attr,
                    index_attr))

        use_rgb_c_box.clicked.connect(
            partial(self.use_rgb_color_checkBox,
                    use_rgb_c_box,
                    btn,
                    slider,
                    s_box,
                    rgb_attr,
                    index_attr,
                    0))

        btn.clicked.connect(
            partial(self.rgb_color_btn,
                    use_rgb_c_box,
                    rgb_attr))

        s_box.valueChanged.connect(
            partial(self.update_spinBox,
                    s_box,
                    index_attr,
                    -1))

        slider.valueChanged.connect(
            partial(self.rgb_color_slider,
                    rgb_attr))

    def reset_values(self, target_attrs, values):
        for index, attr in enumerate(target_attrs):
            self.set_attr_to_piece(attr, values[index])
        self.ui.visibilitySignal.emit(0)

    def toggle_values(self, target_attrs, values):
        pass

    def add_space_switch_listWidget(self, list_widget, target_attr):
        items = pm.ls(selection=True, long=True)
        registered_items = [i.text() for i in
                            list_widget.findItems("", QtCore.Qt.MatchContains)]
        if registered_items and not registered_items[0]:
            list_widget.takeItem(0)

        for item in items:
            if not item.hasAttr("is_domino_ctl"):
                continue

            ctl_attr = pm.listConnections(f"{item}.message",
                                          destination=True,
                                          source=False,
                                          plugs=True)[0]
            root = ctl_attr.node()
            if root.attr("module").get() == "assembly_01":
                identifier = \
                    Identifier.to_str(root.attr("name").get(), None, None)
            else:
                name = root.attr("name").get()
                side = root.attr("side").get(asString=True)
                index = root.attr("index").get()
                identifier = \
                    Identifier.to_str(name, side, index)
            index = ctl_attr.index()
            data = f"{index} | {identifier}"
            if data in registered_items:
                log.Logger.warning("The object: %s, is already in the list." %
                                   item.split("|")[-1])
            else:
                value = self.get_attr_from_piece(target_attr)
                value += f",{data}" if value else data
                with pm.UndoChunk():
                    self.set_attr_to_piece(target_attr, value)
        self.ui.visibilitySignal.emit(-1)

    def remove_space_switch_listWidget(self, list_widget, target_attr):
        for item in list_widget.selectedItems():
            value = self.get_attr_from_piece(target_attr).split(",")
            value.remove(item.text())
            with pm.UndoChunk():
                self.set_attr_to_piece(target_attr, ",".join(value))
        self.ui.visibilitySignal.emit(-1)

    def update_space_switch_listWidget(self, list_widget, target_attr, state):
        """Update the string attribute with values separated by commas"""
        data = self.get_attr_from_piece(target_attr)
        list_widget.clear()
        registered_items = [i.text() for i in
                            list_widget.findItems("", QtCore.Qt.MatchContains)]
        if registered_items and not registered_items[0]:
            list_widget.takeItem(0)
        for d in data.split(","):
            list_widget_item = QtWidgets.QListWidgetItem()
            list_widget_item.setText(d)
            list_widget.addItem(list_widget_item)

    def install_space_switch_listWidget(self,
                                        list_widget,
                                        add_btn,
                                        remove_btn,
                                        target_attr):
        self.ui.visibilitySignal.connect(
            partial(self.update_space_switch_listWidget,
                    list_widget,
                    target_attr))

        add_btn.clicked.connect(
            partial(self.add_space_switch_listWidget,
                    list_widget,
                    target_attr))

        remove_btn.clicked.connect(
            partial(self.remove_space_switch_listWidget,
                    list_widget,
                    target_attr))

    def add_host_lineEdit(self, line_edit, target_attr):
        selected = pm.ls(selection=True)
        if not selected:
            self.set_attr_to_piece(target_attr, "")
            line_edit.setText("")
            return 0

        if not selected[0].hasAttr("is_domino_guide"):
            return 0
        guide = selected[0]

        name = guide.attr("name").get()
        side = guide.attr("side").get(asString=True)
        index = guide.attr("index").get()
        self.set_attr_to_piece(target_attr, Identifier.to_str(name, side, index))
        self.update_host_lineEdit(line_edit, target_attr, 0)

    def update_host_lineEdit(self, line_edit, target_attr, state):
        line_edit.setText("")
        top_node = self.root.getParent(generations=-1)

        identifier = self.get_attr_from_piece(target_attr)
        guide = find_guide_from_identifier(top_node, identifier)
        if guide:
            line_edit.setText(guide.strip())

    def install_host_lineEdit(self, line_edit, btn, target_attr):
        self.ui.visibilitySignal.connect(
            partial(self.update_host_lineEdit,
                    line_edit,
                    target_attr))

        btn.clicked.connect(
            partial(self.add_host_lineEdit,
                    line_edit,
                    target_attr))

    def toggle_checkBox_clicked_pushButton(self, c_boxes):
        for box in c_boxes:
            if box.isChecked():
                box.setChecked(False)
            else:
                box.setChecked(True)

    def install_checkBox_toggle_pushButton(self, btn, c_boxes):
        btn.clicked.connect(partial(self.toggle_checkBox_clicked_pushButton, c_boxes))

    def open_graph_editor(self):
        pm.select(self.root)
        pm.mel.eval("GraphEditor;")


class CommonPieceSettingUI(QtWidgets.QWidget, common_piece_settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(CommonPieceSettingUI, self).__init__(parent=parent)
        self.setupUi(self)


class CommonPieceSettings(DominoDialog):

    def __init__(self, parent=None):
        super(CommonPieceSettings, self).__init__(parent=parent)
        self.setObjectName("DominoPieceSettings")

        self.ui_funcs = UiFunctionSet(ui=self)
        self.visibilitySignal.connect(self.setup_window_title)

        self.v_layout = QtWidgets.QVBoxLayout(self)

        self.common_settings = CommonPieceSettingUI(self)
        ui = self.common_settings
        ui.toolBox.currentChanged.connect(self.resize_window)
        self.v_layout.addWidget(ui)

        self.ui_funcs.install_name_lineEdit(
            ui.name_lineEdit,
            "name")
        self.ui_funcs.install_side_comboBox(
            ui.side_comboBox,
            "side")
        self.ui_funcs.install_index_spinBox(
            ui.index_spinBox,
            "index")

        self.ui_funcs.install_spinBox(
            ui.ref_index_spinBox,
            "custom_ref_index")
        self.ui_funcs.install_spinBox(
            ui.orientX_spinBox,
            "offset_orient_x")
        self.ui_funcs.install_spinBox(
            ui.orientY_spinBox,
            "offset_orient_y")
        self.ui_funcs.install_spinBox(
            ui.orientZ_spinBox,
            "offset_orient_z")

        ui.custom_jnt_name_pushButton.clicked.connect(
            partial(utils.show_dialog,
                    JntNameSetting,
                    self))

        self.ui_funcs.install_checkBox(
            ui.override_colors_checkBox,
            "override_colors")
        self.ui_funcs.install_checkBox(
            ui.use_RGB_colors_checkBox,
            "use_RGB_colors")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.color_ik_pushButton,
            ui.color_rgb_ik_horizontalSlider,
            ui.color_ik_spinBox,
            "RGB_ik",
            "color_ik")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.color_fk_pushButton,
            ui.color_rgb_fk_horizontalSlider,
            ui.color_fk_spinBox,
            "RGB_fk",
            "color_fk")

        self.ui_funcs.install_host_lineEdit(
            ui.host_lineEdit,
            ui.select_host_pushButton,
            "host")

    def resize_window(self):
        index = self.common_settings.toolBox.currentIndex()
        if index == 0:
            size = QtCore.QSize(370, 530)
        else:
            size = self.common_settings.toolBox.currentWidget().sizeHint()
        self.resize(size)


class JntNameSetting(DominoDialog, jnt_name_setting_ui.Ui_Dialog):
    attributeChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super(JntNameSetting, self).__init__(parent=parent)
        self.root = parent.ui_funcs._root

        self.setupUi(self)
        self.setWindowTitle("Custom Joint Name Settings")
        self.setObjectName("JntNameSettings")
        self.tableWidget.setHorizontalHeaderLabels(["jnt names"])

        self.populate_controls()
        self.apply_names()
        self.create_connections()

    def populate_controls(self):
        jointNames = self.root.attr("jnt_names").get().split(",")
        if jointNames[-1]:
            jointNames.append("")

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        for i, name in enumerate(jointNames):
            self.tableWidget.insertRow(i)
            item = QtWidgets.QTableWidgetItem(name.strip())
            self.tableWidget.setItem(i, 0, item)

    def create_connections(self):
        self.tableWidget.cellChanged.connect(self.update_name)
        self.tableWidget.itemActivated.connect(self.tableWidget.editItem)

        self.add_pushButton.clicked.connect(self.add)
        self.remove_pushButton.clicked.connect(self.remove)
        self.remove_all_pushButton.clicked.connect(self.remove_all)

        self.up_pushButton.clicked.connect(lambda: self.up_down(-1))
        self.down_pushButton.clicked.connect(lambda: self.up_down(1))

    def apply_names(self):
        jointNames = []
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            jointNames.append(item.text())

        value = ",".join(jointNames[0:-1])
        self.root.attr("jnt_names").set(value)

        self.tableWidget.setVerticalHeaderLabels(
            [str(i) for i in range(len(jointNames))])

        self.attributeChanged.emit()

    def add(self):
        row = max(0, self.tableWidget.currentRow() or 0)
        self.tableWidget.insertRow(row)
        item = QtWidgets.QTableWidgetItem("")
        self.tableWidget.setItem(row, 0, item)
        self.tableWidget.setCurrentCell(row, 0)
        self.apply_names()

    def remove(self):
        row = self.tableWidget.currentRow()
        if row + 1 < self.tableWidget.rowCount() > 1:
            self.tableWidget.removeRow(row)
            self.apply_names()
            self.tableWidget.setCurrentCell(row, 0)

    def remove_all(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(""))
        self.tableWidget.setCurrentCell(0, 0)
        self.apply_names()

    def up_down(self, step):
        row = self.tableWidget.currentRow()
        if row + step < 0:
            return
        item1 = self.tableWidget.item(row, 0).text()
        item2 = self.tableWidget.item(row + step, 0).text()
        self.tableWidget.item(row, 0).setText(item2)
        self.tableWidget.item(row + step, 0).setText(item1)
        self.tableWidget.setCurrentCell(row + step, 0)

    def update_name(self, row, column):
        item = self.tableWidget.item(row, column)
        if row == self.tableWidget.rowCount() - 1 and item.text():
            self.tableWidget.insertRow(row + 1)
            self.tableWidget.setItem(
                row + 1, 0, QtWidgets.QTableWidgetItem(""))
        self.apply_names()
        self.tableWidget.setCurrentCell(row + 1, 0)
        self.tableWidget.editItem(self.tableWidget.currentItem())


class ManagerUI(QtWidgets.QDialog, manager_ui.Ui_Dialog):
    ui_name = "DominoManagerUI"

    def __init__(self, parent=None):
        super(ManagerUI, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Domino Manager")
        self.setObjectName(self.ui_name)
        self.piece_listView.setAcceptDrops(False)
        self.piece_listView.setDragEnabled(True)
        self.piece_listView.setDropIndicatorShown(False)


class Manager(ManagerUI):
    _role = 17

    def __init__(self, parent=None):
        super(Manager, self).__init__(parent=parent)

        self.proxy_model = QtCore.QSortFilterProxyModel(self)
        self.piece_listView.setModel(self.proxy_model)
        self.piece_listView.setDragEnabled(False)

        self.create_connections()
        self.refresh_listView()

    def create_connections(self):
        model = self.piece_listView.selectionModel()
        model.selectionChanged.connect(self.refresh_description)

        self.settings_pushButton.clicked.connect(partial(open_settings))
        self.copy_pushButton.clicked.connect(self.copy_guide)
        self.mirror_pushButton.clicked.connect(self.mirror_guide)
        self.build_pushButton.clicked.connect(self.build_from_guide)
        self.search_lineEdit.textChanged.connect(self.search)
        self.piece_listView.doubleClicked.connect(self.draw_guide)

    def refresh_listView(self):
        pieces = {}
        box_dir = os.getenv("DOMINO_DEFAULT_EDITION", None)
        custom_edition_dirs = os.getenv("DOMINO_CUSTOM_EDITION", None)

        box_pieces = {"domino_edition.box":
                          {x: None for x in os.listdir(box_dir) if os.path.isdir(os.path.join(box_dir, x))}
                      }
        if "__pycache__" in box_pieces["domino_edition.box"]:
            del box_pieces["domino_edition.box"]["__pycache__"]
        pieces.update(box_pieces)

        if custom_edition_dirs:
            print(custom_edition_dirs)
            dir_list = [os.path.join(custom_edition_dirs, x) for x in os.listdir(custom_edition_dirs)
                        if os.path.isdir(os.path.join(custom_edition_dirs, x))]
            print(dir_list)
            for d in dir_list:
                base_name = os.path.basename(d)
                custom_pieces = {base_name: {x: None for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))}}
                if "__pycache__" in custom_pieces[base_name]:
                    del custom_pieces[base_name]["__pycache__"]
                for x in custom_pieces[base_name].copy():
                    if x in pieces["domino_edition.box"].keys():
                        del custom_pieces[base_name][x]
                        log.Logger.warning(f"Already exists piece '{x}'")
                        continue
                pieces.update(custom_pieces)

        for k in pieces:
            for name in pieces[k].copy():
                p_mod = utils.import_piece_module(name)
                identifier = None
                for _i in dir(p_mod):
                    temp = getattr(p_mod, _i)
                    if type(temp) == type(type):
                        if issubclass(getattr(p_mod, _i), Identifier):
                            identifier = temp
                            break
                pieces[k][name] = {"identifier": identifier}

        del pieces["domino_edition.box"]["assembly_01"]
        self.model = QtGui.QStandardItemModel(self)
        for repo in pieces:
            for name, identifier in pieces[repo].items():
                item = QtGui.QStandardItem(name)
                item.setData(identifier, self._role)
                self.model.appendRow(item)
        self.proxy_model.setSourceModel(self.model)

    def refresh_description(self):
        item = self.piece_listView.selectedIndexes()
        if item:
            name = item[0].data()
            data = item[0].data(self._role)
            identifier = data["identifier"]
            text = f"{identifier.description}\n"
            text += "- - -\n"
            text += f"piece : {name}\n\n"
            text += f"madeBy : {identifier.madeBy}\n\n"
            text += f"contact : {identifier.contact}\n\n"
            text += f"version : {'{}. {}. {}'.format(*identifier.version)}\n\n"
        else:
            text = ""
        self.description_textEdit.setMarkdown(text)

    def search(self, text):
        reg_exp = QtCore.QRegExp(text,
                                 QtCore.Qt.CaseInsensitive,
                                 QtCore.QRegExp.Wildcard)
        self.proxy_model.setFilterRegExp(reg_exp)
        self.description_textEdit.setPlainText("")

    def copy_guide(self):
        selected = pm.ls(sl=1)
        if selected:
            with pm.UndoChunk():
                lib.copy_guide(selected[0])

    def mirror_guide(self):
        selected = pm.ls(sl=1)
        if selected:
            with pm.UndoChunk():
                lib.mirror_guide(selected[0])

    def build_from_guide(self):
        selected = pm.ls(selection=True)
        if selected:
            with pm.UndoChunk():
                lib.create_rig(guide=selected[0])

    def draw_guide(self):
        item = self.piece_listView.selectedIndexes()
        if item:
            with pm.UndoChunk():
                name = item[0].data()
                lib.create_guide(name)


def open_manager():
    utils.show_dialog(Manager, parent=None)


def open_settings():
    selected = pm.ls(selection=True)
    if not selected:
        return 0
    if not pm.attributeQuery("module", node=selected[0], exists=True):
        return 0
    ui = utils.import_piece_settings(selected[0].attr("module").get())
    if ui is not None:
        utils.show_dialog(ui, parent=None)
