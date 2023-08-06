# gui
import uuid

from PySide2 import QtWidgets, QtCore, QtGui
from . import common_component_settings_ui, jnt_name_setting_ui, manager_ui, pose_manager_ui

# built-ins
from functools import partial
import os
import json

# maya
from maya import cmds as mc
from maya import mel
from maya.api import OpenMaya as om2

# domino
from domino import assembler
from domino.lib.color import MAYA_OVERRIDE_COLOR
from domino.lib import attribute, log, hierarchy, utils
from domino import DOMINO_CUSTOM_COMPONENT


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
        root = self.ui_funcs.root
        if root:
            name = root.split("|")[-1]
            self.setWindowTitle(self.title_name + " " + name)


class UiFunctionSet:

    def __init__(self, ui):
        self.ui = ui
        self._root = None

    @property
    def root(self):
        if self._root is None:
            root = mc.ls(selection=True, type="transform", long=True)
            if root and mc.attributeQuery("is_guide", node=root[0], exists=True):
                if mc.nodeType(root[0]) != "dagContainer":
                    root = [hierarchy.get_parent(root[0], type="dagContainer")]
                selection_list = om2.MSelectionList()
                selection_list.add(root[0])
                self._root = selection_list.getDagPath(0)
        if not mc.objExists(self._root.fullPathName()):
            self.ui.close()
            return None
        return self._root.fullPathName()

    def get_attr_from_root(self, attr):
        at = mc.attributeQuery(attr, node=self.root, attributeType=True)
        if at == "enum":
            return mc.getAttr(self.root + "." + attr, asString=True)
        elif at == "typed":
            return mc.getAttr(self.root + "." + attr) or ""
        return mc.getAttr(self.root + "." + attr)

    def set_attr_to_root(self, attr, value):
        at = mc.attributeQuery(attr, node=self.root, attributeType=True)
        if at == "typed":
            mc.setAttr(self.root + "." + attr, value, type="string")
        elif at == "enum":
            en = mc.attributeQuery(attr, node=self.root, listEnum=True)[0]
            enum_names = en.split(":")
            index = enum_names.index(value)
            mc.setAttr(self.root + "." + attr, index)
        else:
            if isinstance(value, (list, tuple)):
                mc.setAttr(self.root + "." + attr, *value)
            else:
                mc.setAttr(self.root + "." + attr, value)

    def is_valid_identifier(self, name, side, index):
        valid_identifier = True
        if self.root in mc.ls(long=True, assemblies=True):
            return valid_identifier
        assembly = hierarchy.get_parent(self.root, generations=-1)
        containers = mc.ls(assembly, dagObjects=True, type="dagContainer", long=True)
        containers.remove(self.root)
        for c in containers[1:]:
            c_name = mc.getAttr(c + ".name")
            c_side = mc.getAttr(c + ".side", asString=True)
            c_index = mc.getAttr(c + ".index")
            if name == c_name and side == c_side and index == c_index:
                valid_identifier = False
                break
        return valid_identifier

    def edit_space_switch(self, orig, new):
        node = hierarchy.get_parent(self.root, generations=-1)
        if node is None:
            node = self.root
        roots = mc.ls(node, dagObjects=True, type="dagContainer")
        for root in roots:
            ud_attrs = mc.listAttr(root, userDefined=True)
            for attr in ud_attrs:
                if attr.endswith("switch_array"):
                    orig_str = mc.getAttr(root + "." + attr) or ""
                    new_str = orig_str.replace(orig, new)
                    mc.setAttr(root + "." + attr, new_str, type="string")

    def update_name_lineEdit(self, l_edit, target_attr):
        orig_name = self.get_attr_from_root(target_attr)
        new_name = l_edit.text()
        if orig_name != new_name:
            try:
                mc.undoInfo(openChunk=True)
                is_assembly = self.get_attr_from_root("component") == "assembly"
                if not is_assembly:
                    side = self.get_attr_from_root("side")
                    index = self.get_attr_from_root("index")
                    is_valid = self.is_valid_identifier(new_name, side, index)
                    orig_identifier = "{0}_{1}_{2}".format(orig_name, side, index)
                    new_identifier = "{0}_{1}_{2}".format(new_name, side, index)
                else:
                    is_valid = self.is_valid_identifier(new_name, "", "")
                    orig_identifier = orig_name
                    new_identifier = new_name
                if not is_valid:
                    l_edit.setText(orig_name)
                else:
                    self.set_attr_to_root(target_attr, new_name)
                    comp = assembler.Component()
                    comp.pull_data_from_node(self.root)
                    guide = assembler.Guide(component=comp, root=self.root)
                    guide.rename()
                    self.edit_space_switch(orig_identifier, new_identifier)
                self.ui.setup_window_title()
            finally:
                mc.undoInfo(closeChunk=True)

    def install_name_lineEdit(self, l_edit, target_attr):
        l_edit.setText(self.get_attr_from_root(target_attr))
        l_edit.editingFinished.connect(
            partial(self.update_name_lineEdit,
                    l_edit=l_edit,
                    target_attr=target_attr))

    def update_side_comboBox(self, c_box, target_attr):
        orig_side = self.get_attr_from_root(target_attr)
        new_side = c_box.currentText()
        if orig_side != new_side:
            try:
                mc.undoInfo(openChunk=True)
                name = self.get_attr_from_root("name")
                index = self.get_attr_from_root("index")
                is_valid = self.is_valid_identifier(name, new_side, index)
                orig_identifier = "{0}_{1}_{2}".format(name, orig_side, index)
                new_identifier = "{0}_{1}_{2}".format(name, new_side, index)
                if not is_valid:
                    c_box.setCurrentText(orig_side)
                else:
                    self.set_attr_to_root(target_attr, new_side)
                    comp = assembler.Component()
                    comp.pull_data_from_node(self.root)
                    guide = assembler.Guide(component=comp, root=self.root)
                    guide.rename()
                    self.edit_space_switch(orig_identifier, new_identifier)
                self.ui.setup_window_title()
            finally:
                mc.undoInfo(closeChunk=True)

    def install_side_comboBox(self, c_box, target_attr):
        c_box.setCurrentText(self.get_attr_from_root(target_attr))
        c_box.currentTextChanged.connect(
            lambda _: self.update_side_comboBox(
                c_box=c_box,
                target_attr=target_attr))

    def update_index_spinBox(self, s_box, target_attr):
        orig_index = self.get_attr_from_root(target_attr)
        new_index = s_box.value()
        if orig_index != new_index:
            try:
                mc.undoInfo(openChunk=True)
                name = self.get_attr_from_root("name")
                side = self.get_attr_from_root("side")
                is_valid = self.is_valid_identifier(name, side, new_index)
                orig_identifier = "{0}_{1}_{2}".format(name, side, orig_index)
                new_identifier = "{0}_{1}_{2}".format(name, side, new_index)
                if not is_valid:
                    s_box.setValue(orig_index)
                else:
                    self.set_attr_to_root(target_attr, new_index)
                    comp = assembler.Component()
                    comp.pull_data_from_node(self.root)
                    guide = assembler.Guide(component=comp, root=self.root)
                    guide.rename()
                    self.edit_space_switch(orig_identifier, new_identifier)
                self.ui.setup_window_title()
            finally:
                mc.undoInfo(closeChunk=True)

    def install_index_spinBox(self, s_box, target_attr):
        s_box.setValue(int(self.get_attr_from_root(target_attr)))
        s_box.valueChanged.connect(
            lambda _: self.update_index_spinBox(
                s_box=s_box,
                target_attr=target_attr))

    def update_spinBox(self, s_box, target_attr, _factor, *args):
        orig_value = self.get_attr_from_root(target_attr)
        new_value = s_box.value() / _factor
        if orig_value != new_value:
            try:
                mc.undoInfo(openChunk=True)
                self.set_attr_to_root(target_attr, new_value)
            finally:
                mc.undoInfo(closeChunk=True)

    def install_spinBox(self, s_box, target_attr, factor=1):
        s_box.setValue(self.get_attr_from_root(target_attr) / factor)
        s_box.valueChanged.connect(
            partial(self.update_spinBox,
                    s_box,
                    target_attr,
                    factor))

    def update_lineEdit(self, l_edit, target_attr):
        orig_value = self.get_attr_from_root(target_attr)
        new_value = l_edit.text()
        if orig_value != new_value:
            try:
                mc.undoInfo(openChunk=True)
                self.set_attr_to_root(target_attr, new_value)
            finally:
                mc.undoInfo(closeChunk=True)

    def install_lineEdit(self, l_edit, target_attr):
        l_edit.setText(self.get_attr_from_root(target_attr))
        l_edit.editingFinished.connect(
            partial(self.update_lineEdit,
                    l_edit=l_edit,
                    target_attr=target_attr))

    def update_comboBox(self, c_box, target_attr, *args):
        orig_value = self.get_attr_from_root(target_attr)
        new_value = c_box.currentText()
        if orig_value != new_value:
            try:
                mc.undoInfo(openChunk=True)
                self.set_attr_to_root(target_attr, new_value)
            finally:
                mc.undoInfo(closeChunk=True)

    def install_comboBox(self, c_box, target_attr):
        c_box.setCurrentText(self.get_attr_from_root(target_attr))
        c_box.currentTextChanged.connect(
            partial(self.update_comboBox,
                    c_box,
                    target_attr))

    def update_checkBox(self, c_box, target_attr, *args):
        orig_value = self.get_attr_from_root(target_attr)
        new_value = c_box.isChecked()
        if orig_value != new_value:
            try:
                mc.undoInfo(openChunk=True)
                self.set_attr_to_root(target_attr, new_value)
            finally:
                mc.undoInfo(closeChunk=True)

    def install_checkBox(self, c_box, target_attr):
        c_box.setChecked(self.get_attr_from_root(target_attr))
        c_box.stateChanged.connect(
            lambda _: self.update_checkBox(
                c_box=c_box,
                target_attr=target_attr))

    def update_slider(self, slider, target_attr, factor, *args):
        orig_value = self.get_attr_from_root(target_attr)
        new_value = slider.value() * factor
        if orig_value != new_value:
            try:
                mc.undoInfo(openChunk=True)
                self.set_attr_to_root(target_attr, new_value)
            finally:
                mc.undoInfo(closeChunk=True)

    def install_slider(self, slider, target_attr, factor=1):
        slider.setValue(int(self.get_attr_from_root(target_attr) / factor))
        slider.valueChanged.connect(
            partial(self.update_slider,
                    slider,
                    target_attr,
                    factor))

    def update_textEdit(self, t_edit, target_attr):
        orig_value = self.get_attr_from_root(target_attr)
        new_value = t_edit.toPlainText()
        if orig_value != new_value:
            try:
                mc.undoInfo(openChunk=True)
                self.set_attr_to_root(target_attr, new_value)
                s = t_edit.document().size()
                t_edit.setFixedHeight(s.height() + 4)
            finally:
                mc.undoInfo(closeChunk=True)

    def install_textEdit(self, t_edit, target_attr):
        txt = self.get_attr_from_root(target_attr)
        t_edit.setPlainText(txt)
        font = t_edit.document().defaultFont()
        font_metrices = QtGui.QFontMetrics(font)
        txt_size = font_metrices.size(0, t_edit.toPlainText())
        t_edit.setFixedHeight(txt_size.height() + 12)
        t_edit.textChanged.connect(
            partial(self.update_textEdit,
                    t_edit,
                    target_attr))

    def use_rgb_color_checkBox(self,
                               use_rgb_c_box,
                               btn,
                               slider,
                               s_box,
                               rgb_attr,
                               index_attr,
                               *args):
        is_rgb = use_rgb_c_box.isChecked()
        if not is_rgb:
            slider.setVisible(False)
            s_box.setVisible(True)
            index = self.get_attr_from_root(index_attr)
            rgb = [float(x / 255) for x in MAYA_OVERRIDE_COLOR[index]]
            color = mc.colorManagementConvert(toDisplaySpace=rgb)
            self.update_rgb_color_btn(btn, color)
            s_box.setValue(index)
        else:
            slider.setVisible(True)
            s_box.setVisible(False)
            rgb = self.get_attr_from_root(rgb_attr)[0]
            color = mc.colorManagementConvert(toDisplaySpace=rgb)
            h_value = sorted(rgb)[2]
            if not h_value:
                color = (0, 0, 0)
            self.update_rgb_color_btn(btn, color)
            slider.setValue(h_value * 100)

    def rgb_color_btn(self, use_rgb_c_box, btn, target_attr):
        if not use_rgb_c_box.isChecked():
            return 0
        pos = QtGui.QCursor.pos()
        mc.colorEditor(rgb=self.get_attr_from_root(target_attr)[0], mini=True, position=(pos.x() - 200, pos.y() - 120))
        if mc.colorEditor(query=True, result=True):
            rgb = mc.colorEditor(query=True, rgb=True)
            self.set_attr_to_root(target_attr, rgb)
            color = mc.colorManagementConvert(toDisplaySpace=rgb)
            self.update_rgb_color_btn(btn, color)

    def rgb_color_slider(self, btn, target_attr, value):
        rgb = self.get_attr_from_root(target_attr)[0]
        hsv_value = sorted(rgb)[2]
        if hsv_value:
            new_rgb = tuple(i / (hsv_value / 1.0) * (value / 100) for i in rgb)
        else:
            new_rgb = tuple((1.0 * (value / 100), 1.0 * (value / 100), 1.0 * (value / 100)))
        self.update_rgb_color_btn(btn, new_rgb)
        try:
            mc.undoInfo(openChunk=True)
            self.set_attr_to_root(target_attr, new_rgb)
        finally:
            mc.undoInfo(closeChunk=True)

    def rgb_color_spinBox(self, s_box, btn, target_attr, value):
        self.update_spinBox(s_box, target_attr, 1)
        rgb = [float(x / 255) for x in MAYA_OVERRIDE_COLOR[value]]
        color = mc.colorManagementConvert(toDisplaySpace=rgb)
        self.update_rgb_color_btn(btn, color)

    def update_rgb_color_btn(self, btn, color):
        color = ", ".join([str(c * 255) for c in color])
        btn.setStyleSheet("* {background-color: rgb(" + color + ")}")

    def install_color_widgets(self,
                              use_rgb_c_box,
                              btn,
                              slider,
                              s_box,
                              rgb_attr,
                              index_attr):
        self.use_rgb_color_checkBox(use_rgb_c_box, btn, slider, s_box, rgb_attr, index_attr)
        use_rgb_c_box.clicked.connect(
            partial(self.use_rgb_color_checkBox,
                    use_rgb_c_box,
                    btn,
                    slider,
                    s_box,
                    rgb_attr,
                    index_attr))
        btn.clicked.connect(
            partial(self.rgb_color_btn,
                    use_rgb_c_box,
                    btn,
                    rgb_attr))
        s_box.valueChanged.connect(
            partial(self.rgb_color_spinBox,
                    s_box,
                    btn,
                    index_attr))
        slider.valueChanged.connect(
            partial(self.rgb_color_slider,
                    btn,
                    rgb_attr))

    def reset_values(self, widgets, values):
        for index, widget in enumerate(widgets):
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.setText(values[index])
                widget.editingFinished.emit()
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.setCurrentText(values[index])
            elif isinstance(widget, QtWidgets.QSpinBox):
                widget.setValue(values[index])

    def add_space_switch_listWidget(self, list_widget, target_attr):
        items = mc.ls(selection=True, long=True)
        registered_items = [i.text() for i in list_widget.findItems("", QtCore.Qt.MatchContains)]
        if registered_items and not registered_items[0]:
            list_widget.takeItem(0)

        for item in items:
            if not mc.attributeQuery("is_ctl", node=item, exists=True):
                continue

            plugs = mc.listConnections(item + ".message", destination=True, source=False, plugs=True)
            root, attr = \
                [x.split(".") for x in plugs if mc.attributeQuery("component", node=x.split(".")[0], exists=True)][0]

            if mc.getAttr(root + ".component") == "assembly":
                identifier = mc.getAttr(root + ".name")
            else:
                name = mc.getAttr(root + ".name")
                side = mc.getAttr(root + ".side", asString=True)
                index = str(mc.getAttr(root + ".index"))

                identifier = "_".join([name, side, index])

            index = str(attribute.get_index(attr))
            data = index + " | " + identifier
            if data in registered_items:
                log.Logger.warning("The object: %s, is already in the list." % item.split("|")[-1])
            else:
                value = self.get_attr_from_root(target_attr)
                value += "," + data if value else data
                try:
                    mc.undoInfo(openChunk=True)
                    self.set_attr_to_root(target_attr, value)
                finally:
                    mc.undoInfo(closeChunk=True)
        self.update_space_switch_listWidget(list_widget, target_attr)

    def remove_space_switch_listWidget(self, list_widget, target_attr):
        for item in list_widget.selectedItems():
            value = self.get_attr_from_root(target_attr).split(",")
            value.remove(item.text())
            try:
                mc.undoInfo(openChunk=True)
                self.set_attr_to_root(target_attr, ",".join(value))
            finally:
                mc.undoInfo(closeChunk=True)
        self.update_space_switch_listWidget(list_widget, target_attr)

    def update_space_switch_listWidget(self, list_widget, target_attr):
        """Update the string attribute with values separated by commas"""
        data = self.get_attr_from_root(target_attr)
        list_widget.clear()
        registered_items = [i.text() for i in list_widget.findItems("", QtCore.Qt.MatchContains)]
        if registered_items and not registered_items[0]:
            list_widget.takeItem(0)
        for d in data.split(","):
            list_widget_item = QtWidgets.QListWidgetItem()
            list_widget_item.setText(d)
            list_widget.addItem(list_widget_item)

    def copy_space_switch_listWidget(self, list_widget, source_attr, target_attr):
        source_data = self.get_attr_from_root(source_attr)
        self.set_attr_to_root(target_attr, source_data)
        self.update_space_switch_listWidget(list_widget, target_attr)

    def install_space_switch_listWidget(self,
                                        list_widget,
                                        add_btn,
                                        remove_btn,
                                        target_attr):
        self.update_space_switch_listWidget(list_widget, target_attr)
        add_btn.clicked.connect(
            partial(self.add_space_switch_listWidget,
                    list_widget,
                    target_attr))
        remove_btn.clicked.connect(
            partial(self.remove_space_switch_listWidget,
                    list_widget,
                    target_attr))

    def add_container_lineEdit(self, line_edit, target_attr):
        selected = mc.ls(selection=True)
        containers = [container for container in selected if mc.attributeQuery("is_guide", node=container, exists=True)]
        if not containers:
            self.set_attr_to_root(target_attr, "")
            line_edit.setText("")
            return None

        data = []
        for container in containers:
            if mc.getAttr(container + ".component") == "assembly":
                continue

            name = mc.getAttr(container + ".name")
            side = mc.getAttr(container + ".side", asString=True)
            index = str(mc.getAttr(container + ".index"))
            data.append("_".join([name, side, index]))

        self.set_attr_to_root(target_attr, ",".join(data))
        self.update_container_lineEdit(line_edit, target_attr)

    def update_container_lineEdit(self, line_edit, target_attr):
        line_edit.setText("")
        data = self.get_attr_from_root(target_attr)
        line_edit.setText(data)

    def install_container_lineEdit(self, line_edit, btn, target_attr):
        self.update_container_lineEdit(line_edit, target_attr)
        btn.clicked.connect(
            partial(self.add_container_lineEdit,
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
        mc.select(self.root)
        mel.eval("GraphEditor;")

    def update_listWidget(self, list_widget, target_attr):
        items_list = [i for i in list_widget.findItems("", QtCore.Qt.MatchContains)]
        if items_list and not items_list[0]:
            list_widget.takeItem(0)
        items_data = ",".join([i.text() for i in items_list])
        self.set_attr_to_root(target_attr, items_data)

    def remove_items_listWidget(self, list_widget, target_attr):
        for item in list_widget.selectedItems():
            list_widget.takeItem(list_widget.row(item))
        if target_attr:
            self.update_listWidget(list_widget, target_attr)

    def init_listWidget(self, list_widget, target_attr):
        # initialize
        items = [list_widget.item(i) for i in range(list_widget.count())]
        for item in items:
            list_widget.takeItem(list_widget.row(item))

        data = self.get_attr_from_root(target_attr)
        items_data = data.split(",")
        for d in items_data:
            list_widget.addItem(d)

    def select_curve_btn(self, combobox, target_attr, role):
        combobox.clear()
        orig_curves = mc.listConnections(self.root + "." + target_attr, source=True, destination=False)
        if orig_curves:
            mc.delete(orig_curves)

        selection = mc.ls(selection=True)
        if not selection:
            return

        is_multi = mc.attributeQuery(target_attr, node=self.root, multi=True)
        if not is_multi:
            selection = [selection[0]]
            target_attrs = [target_attr]
        else:
            target_attrs = [target_attr + "[{0}]".format(i) for i in range(len(selection))]

        model = combobox.model()
        i = 0
        for sel, target_attr in zip(selection, target_attrs):
            shape = mc.listRelatives(sel, shapes=True, fullPath=True)[0]
            if mc.nodeType(shape) != "nurbsCurve":
                return

            new_shape = mc.duplicateCurve(shape, name=str(uuid.uuid4()), constructionHistory=False)
            new_shape = mc.parent(new_shape, self.root)[0]
            shape = mc.listRelatives(new_shape, shapes=True)[0]

            mc.connectAttr(shape + ".worldSpace[0]", self.root + "." + target_attr, force=True)
            mc.setAttr(shape + ".dispHull", 1)
            mc.setAttr(shape + ".dispCV", 1)
            mc.setAttr(new_shape + ".overrideEnabled", 1)
            mc.setAttr(new_shape + ".overrideDisplayType", 2)

            item = QtGui.QStandardItem()
            item.setText(str(i))
            item.setData(new_shape, role)
            model.appendRow(item)
            i += 1

    def install_curve_btn(self, combobox, btn, target_attr, role=QtCore.Qt.UserRole):
        source = mc.listConnections(self.root + "." + target_attr, source=True, destination=False) or []
        combobox.clear()
        model = combobox.model()
        for i, s in enumerate(source):
            item = QtGui.QStandardItem()
            item.setText(str(i))
            item.setData(s, role)
            model.appendRow(item)

        combobox.activated.connect(lambda: mc.select(combobox.currentData(role)))

        btn.clicked.connect(
            partial(self.select_curve_btn,
                    combobox,
                    target_attr,
                    role))

    def update_parent_comp_btn(self, line_edit, target_attr):
        line_edit.setText(self.get_attr_from_root(target_attr))

    def add_parent_comp_btn(self, line_edit, target_attr):
        selection = mc.ls(selection=True, long=True)
        if not selection:
            return
        if not mc.attributeQuery("is_guide", node=selection[0], exists=True):
            return

        root = selection[0]
        if mc.getAttr(root + ".component") == "assembly":
            identifier = mc.getAttr(root + ".name")
        else:
            name = mc.getAttr(root + ".name")
            side = mc.getAttr(root + ".side", asString=True)
            index = str(mc.getAttr(root + ".index"))
            identifier = "_".join([name, side, index])

        self.set_attr_to_root(target_attr, identifier)
        self.update_parent_comp_btn(line_edit, target_attr)

    def install_parent_comp_btn(self, line_edit, btn, target_attr):
        self.update_parent_comp_btn(line_edit, target_attr)
        btn.clicked.connect(
            partial(self.add_parent_comp_btn,
                    line_edit,
                    target_attr))


class CommonComponentSettingUI(QtWidgets.QWidget, common_component_settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(CommonComponentSettingUI, self).__init__(parent=parent)
        self.setupUi(self)


class CommonComponentSettings(DominoDialog):

    def __init__(self, parent=None):
        super(CommonComponentSettings, self).__init__(parent=parent)
        self.setObjectName("DominoComponentSettings")

        self.ui_funcs = UiFunctionSet(ui=self)
        self.visibilitySignal.connect(self.setup_window_title)

        self.v_layout = QtWidgets.QVBoxLayout(self)

        self.common_settings = CommonComponentSettingUI(self)
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

        self.ui_funcs.install_checkBox(
            ui.create_jnt_checkBox,
            "create_jnt")
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

        self.ui_funcs.install_container_lineEdit(
            ui.container_lineEdit,
            ui.select_container_pushButton,
            "asset_container")

    def resize_window(self):
        index = self.common_settings.toolBox.currentIndex()
        if index == 0:
            size = QtCore.QSize(370, 550)
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
        jointNames = (mc.getAttr(self.root.fullPathName() + ".jnt_names") or "").split(",")
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
        mc.setAttr(self.root.fullPathName() + ".jnt_names", value, type="string")

        self.tableWidget.setVerticalHeaderLabels(
            [str(i) for i in range(len(jointNames))])

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
        self.component_listView.setAcceptDrops(False)
        self.component_listView.setDragEnabled(True)
        self.component_listView.setDropIndicatorShown(False)


class Manager(ManagerUI):
    _role = 17

    def __init__(self, parent=None):
        super(Manager, self).__init__(parent=parent)

        self.proxy_model = QtCore.QSortFilterProxyModel(self)
        self.component_listView.setModel(self.proxy_model)
        self.component_listView.setDragEnabled(False)
        indent = QtGui.QFontMetricsF(self.description_textEdit.font()).horizontalAdvance("    ")
        self.description_textEdit.document().setIndentWidth(indent)

        self.create_connections()
        self.refresh_listView()

    def create_connections(self):
        model = self.component_listView.selectionModel()
        model.selectionChanged.connect(self.refresh_description)

        self.settings_pushButton.clicked.connect(partial(open_settings))
        self.extract_ctl_shapes_pushButton.clicked.connect(self.extract_ctl_shapes)
        self.copy_pushButton.clicked.connect(self.copy_guide)
        self.mirror_pushButton.clicked.connect(self.mirror_guide)
        self.build_pushButton.clicked.connect(self.build_from_guide)
        self.search_lineEdit.textChanged.connect(self.search)
        self.component_listView.doubleClicked.connect(self.draw_guide)

    def refresh_listView(self):
        comp = {}
        default_component_dir = os.path.join(os.path.dirname(assembler.__file__), "component")
        default_component = {
            "default":
                {x: None for x in sorted(os.listdir(default_component_dir)) if
                 os.path.isdir(os.path.join(default_component_dir, x))}
        }
        if "__pycache__" in default_component["default"]:
            del default_component["default"]["__pycache__"]
        comp.update(default_component)

        custom_component_dirs = os.getenv(DOMINO_CUSTOM_COMPONENT, None)
        if custom_component_dirs:
            dir_list = [os.path.join(custom_component_dirs, x) for x in os.listdir(custom_component_dirs)
                        if os.path.isdir(os.path.join(custom_component_dirs, x))]
            for d in dir_list:
                base_name = os.path.basename(d)
                custom_component = {
                    base_name: {x: None for x in sorted(os.listdir(d)) if os.path.isdir(os.path.join(d, x))}
                }
                if "__pycache__" in custom_component[base_name]:
                    del custom_component[base_name]["__pycache__"]
                for x in custom_component[base_name].copy():
                    if x in comp["default"].keys():
                        del custom_component[base_name][x]
                        log.Logger.warning(f"Already exists component '{x}'")
                        continue
                comp.update(custom_component)

        for k in comp:
            for name in comp[k].copy():
                mod = assembler.import_component_module(name)
                comp[k][name] = {"author": mod.Author}

        del comp["default"]["assembly"]
        self.model = QtGui.QStandardItemModel(self)
        for repo in comp:
            for name, author in comp[repo].items():
                item = QtGui.QStandardItem(name)
                item.setData(author, self._role)
                self.model.appendRow(item)
        self.proxy_model.setSourceModel(self.model)

    def refresh_description(self):
        item = self.component_listView.selectedIndexes()
        if item:
            name = item[0].data()
            data = item[0].data(self._role)
            author = data["author"]
            text = f"{author.description}\n"
            text += "- - -\n"
            text += f"component : {name}\n\n"
            text += f"madeBy : {author.madeBy}\n\n"
            text += f"contact : {author.contact}\n\n"
            text += f"version : {'{}. {}. {}'.format(*author.version)}\n\n"
        else:
            text = ""
        self.description_textEdit.setMarkdown(text)

    def search(self, text):
        reg_exp = QtCore.QRegExp(text,
                                 QtCore.Qt.CaseInsensitive,
                                 QtCore.QRegExp.Wildcard)
        self.proxy_model.setFilterRegExp(reg_exp)
        self.description_textEdit.setPlainText("")

    def extract_ctl_shapes(self):
        selected = mc.ls(selection=True)
        if selected:
            try:
                mc.undoInfo(openChunk=True)
                assembler.extract_shape(selected)
            finally:
                mc.undoInfo(closeChunk=True)

    def copy_guide(self):
        selected = mc.ls(selection=True)
        if selected:
            try:
                mc.undoInfo(openChunk=True)
                assembler.copy_guide(selected[0])
            finally:
                mc.undoInfo(closeChunk=True)

    def mirror_guide(self):
        selected = mc.ls(selection=True)
        if selected:
            try:
                mc.undoInfo(openChunk=True)
                assembler.mirror_guide(selected[0])
            finally:
                mc.undoInfo(closeChunk=True)

    def build_from_guide(self):
        selected = mc.ls(selection=True)
        if selected:
            try:
                mc.undoInfo(openChunk=True)
                assembler.create_rig(guide=selected[0])
            finally:
                mc.undoInfo(closeChunk=True)

    def draw_guide(self):
        item = self.component_listView.selectedIndexes()
        if item:
            try:
                selection = mc.ls(sl=1)
                mc.undoInfo(openChunk=True)
                name = item[0].data()
                assembler.add_guide(selection[0] if selection else None, name)
            finally:
                mc.undoInfo(closeChunk=True)


class PoseManagerUI(QtWidgets.QDialog, pose_manager_ui.Ui_Dialog):
    ui_name = "PoseManagerUI"

    def __init__(self, parent=None):
        super(PoseManagerUI, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Pose Manager")
        self.setObjectName(self.ui_name)


class PoseManager(PoseManagerUI):
    POSE_ROLE = QtCore.Qt.UserRole + 33

    def __init__(self, parent=None, root=None):
        super(PoseManager, self).__init__(parent=parent)
        self._root = root
        self.create_connections()
        self.refresh_listWidget()

    @property
    def root(self):
        if not mc.objExists(self._root):
            self.close()
        return self._root

    def get_pose_data(self):
        return json.loads(mc.getAttr(self.root + ".pose_json").replace("'", "\""))

    def add_pose_data(self, new_pose):
        original_data = self.get_pose_data()
        original_data[new_pose[0]] = new_pose[1]
        mc.setAttr(self.root + ".pose_json", json.dumps(original_data), type="string")

    def create_connections(self):
        self.add_pushButton.clicked.connect(self.add_pose)
        self.delete_pushButton.clicked.connect(self.delete_pose)
        self.listWidget.doubleClicked.connect(self.go_to_pose)

    def add_pose(self):
        pose_name = self.lineEdit.text()
        if pose_name:
            self.add_pose_data([pose_name, attribute.collect_attr(mc.ls(selection=True))])
            self.go_to_pose("neutral")
            self.refresh_listWidget()

    def delete_pose(self):
        pose_data = self.get_pose_data()
        items = self.listWidget.selectedItems()
        for item in items:
            pose = item.data(QtCore.Qt.DisplayRole)
            del pose_data[pose]
        mc.setAttr(self.root + ".pose_json", json.dumps(pose_data), type="string")
        self.refresh_listWidget()

    def go_to_pose(self, pose):
        if isinstance(pose, QtCore.QModelIndex):
            pose_data = pose.data(self.POSE_ROLE)
        else:
            pose_data = self.get_pose_data()[pose]
        attribute.apply_attr(pose_data)

    def refresh_listWidget(self):
        pose_data = self.get_pose_data()

        self.listWidget.clear()

        for pose, data in pose_data.items():
            item = QtWidgets.QListWidgetItem(pose)
            item.setData(self.POSE_ROLE, data)
            self.listWidget.addItem(item)


def open_manager():
    utils.show_dialog(Manager, parent=None)


def open_settings():
    selected = mc.ls(selection=True)
    if not selected:
        return 0
    if not mc.attributeQuery("component", node=selected[0], exists=True):
        return 0
    ui = assembler.import_component_module(mc.getAttr(selected[0] + ".component"), ui=True)
    if ui is not None:
        utils.show_dialog(ui.Settings, parent=None)


def open_pose_manager():
    selected = mc.ls(selection=True, type="transform")
    if not selected:
        return 0
    top = hierarchy.get_parent(selected[0], generations=-1)
    if not mc.attributeQuery("assembly_node", node=top, exists=True):
        return 0
    assembly_root = mc.listConnections(top + ".assembly_node", source=False, destination=True)[0]
    utils.show_dialog(PoseManager, parent=None, root=assembly_root)
