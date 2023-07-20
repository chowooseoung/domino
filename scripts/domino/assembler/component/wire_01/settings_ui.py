# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(316, 288)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.turning_point_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.turning_point_doubleSpinBox.setObjectName(u"turning_point_doubleSpinBox")
        self.turning_point_doubleSpinBox.setMaximum(1.000000000000000)
        self.turning_point_doubleSpinBox.setSingleStep(0.050000000000000)
        self.turning_point_doubleSpinBox.setValue(0.500000000000000)

        self.gridLayout.addWidget(self.turning_point_doubleSpinBox, 1, 1, 1, 3)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)

        self.tail_range_spinBox = QSpinBox(self.groupBox)
        self.tail_range_spinBox.setObjectName(u"tail_range_spinBox")
        self.tail_range_spinBox.setMaximum(999)
        self.tail_range_spinBox.setValue(1)

        self.gridLayout.addWidget(self.tail_range_spinBox, 10, 1, 1, 3)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 9, 0, 1, 1)

        self.tail_parent_lineEdit = QLineEdit(self.groupBox)
        self.tail_parent_lineEdit.setObjectName(u"tail_parent_lineEdit")
        self.tail_parent_lineEdit.setReadOnly(False)

        self.gridLayout.addWidget(self.tail_parent_lineEdit, 9, 1, 1, 2)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.division_spinBox = QSpinBox(self.groupBox)
        self.division_spinBox.setObjectName(u"division_spinBox")
        self.division_spinBox.setMinimum(1)
        self.division_spinBox.setMaximum(999)

        self.gridLayout.addWidget(self.division_spinBox, 0, 1, 1, 3)

        self.add_head_parent_pushButton = QPushButton(self.groupBox)
        self.add_head_parent_pushButton.setObjectName(u"add_head_parent_pushButton")

        self.gridLayout.addWidget(self.add_head_parent_pushButton, 7, 3, 1, 1)

        self.select_wire_curve_pushButton = QPushButton(self.groupBox)
        self.select_wire_curve_pushButton.setObjectName(u"select_wire_curve_pushButton")

        self.gridLayout.addWidget(self.select_wire_curve_pushButton, 3, 3, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 10, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 11, 2, 1, 1)

        self.head_range_spinBox = QSpinBox(self.groupBox)
        self.head_range_spinBox.setObjectName(u"head_range_spinBox")
        self.head_range_spinBox.setMaximum(999)
        self.head_range_spinBox.setValue(1)

        self.gridLayout.addWidget(self.head_range_spinBox, 8, 1, 1, 3)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 6, 0, 1, 4)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 8, 0, 1, 1)

        self.add_tail_parent_pushButton = QPushButton(self.groupBox)
        self.add_tail_parent_pushButton.setObjectName(u"add_tail_parent_pushButton")

        self.gridLayout.addWidget(self.add_tail_parent_pushButton, 9, 3, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.up_normal_x_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.up_normal_x_doubleSpinBox.setObjectName(u"up_normal_x_doubleSpinBox")
        self.up_normal_x_doubleSpinBox.setDecimals(1)
        self.up_normal_x_doubleSpinBox.setMaximum(1.000000000000000)

        self.horizontalLayout_2.addWidget(self.up_normal_x_doubleSpinBox)

        self.up_normal_y_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.up_normal_y_doubleSpinBox.setObjectName(u"up_normal_y_doubleSpinBox")
        self.up_normal_y_doubleSpinBox.setDecimals(1)
        self.up_normal_y_doubleSpinBox.setMaximum(1.000000000000000)

        self.horizontalLayout_2.addWidget(self.up_normal_y_doubleSpinBox)

        self.up_normal_z_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.up_normal_z_doubleSpinBox.setObjectName(u"up_normal_z_doubleSpinBox")
        self.up_normal_z_doubleSpinBox.setDecimals(1)
        self.up_normal_z_doubleSpinBox.setMaximum(1.000000000000000)

        self.horizontalLayout_2.addWidget(self.up_normal_z_doubleSpinBox)


        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 1, 1, 3)

        self.head_parent_lineEdit = QLineEdit(self.groupBox)
        self.head_parent_lineEdit.setObjectName(u"head_parent_lineEdit")
        self.head_parent_lineEdit.setReadOnly(False)

        self.gridLayout.addWidget(self.head_parent_lineEdit, 7, 1, 1, 2)

        self.fk_path_checkBox = QCheckBox(self.groupBox)
        self.fk_path_checkBox.setObjectName(u"fk_path_checkBox")

        self.gridLayout.addWidget(self.fk_path_checkBox, 5, 0, 1, 1)

        self.curve_comboBox = QComboBox(self.groupBox)
        self.curve_comboBox.setObjectName(u"curve_comboBox")

        self.gridLayout.addWidget(self.curve_comboBox, 3, 1, 1, 2)


        self.horizontalLayout.addWidget(self.groupBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Head Parent", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Division", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Up Curve Normal", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Tail Parent", None))
        self.label.setText(QCoreApplication.translate("Form", u"Wire Curve", None))
        self.add_head_parent_pushButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.select_wire_curve_pushButton.setText(QCoreApplication.translate("Form", u"Select", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Tail Range", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Turning Point", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Head Range", None))
        self.add_tail_parent_pushButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.fk_path_checkBox.setText(QCoreApplication.translate("Form", u"Fk Path", None))
    # retranslateUi

