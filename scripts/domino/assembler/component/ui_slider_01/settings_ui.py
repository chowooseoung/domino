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
        Form.resize(329, 278)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.frame_checkBox = QCheckBox(self.groupBox)
        self.frame_checkBox.setObjectName(u"frame_checkBox")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.frame_checkBox)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.size_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.size_doubleSpinBox.setObjectName(u"size_doubleSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.size_doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.size_doubleSpinBox.setSizePolicy(sizePolicy)
        self.size_doubleSpinBox.setSingleStep(0.100000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.size_doubleSpinBox)

        self.plus_x_checkBox = QCheckBox(self.groupBox)
        self.plus_x_checkBox.setObjectName(u"plus_x_checkBox")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.plus_x_checkBox)

        self.minus_x_checkBox = QCheckBox(self.groupBox)
        self.minus_x_checkBox.setObjectName(u"minus_x_checkBox")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.minus_x_checkBox)

        self.plus_y_checkBox = QCheckBox(self.groupBox)
        self.plus_y_checkBox.setObjectName(u"plus_y_checkBox")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.plus_y_checkBox)

        self.minus_y_checkBox = QCheckBox(self.groupBox)
        self.minus_y_checkBox.setObjectName(u"minus_y_checkBox")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.minus_y_checkBox)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_9)

        self.plus_x_name_lineEdit = QLineEdit(self.groupBox)
        self.plus_x_name_lineEdit.setObjectName(u"plus_x_name_lineEdit")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.plus_x_name_lineEdit)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_7)

        self.minus_x_name_lineEdit = QLineEdit(self.groupBox)
        self.minus_x_name_lineEdit.setObjectName(u"minus_x_name_lineEdit")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.minus_x_name_lineEdit)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_10)

        self.plus_y_name_lineEdit = QLineEdit(self.groupBox)
        self.plus_y_name_lineEdit.setObjectName(u"plus_y_name_lineEdit")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.plus_y_name_lineEdit)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_8)

        self.minus_y_name_lineEdit = QLineEdit(self.groupBox)
        self.minus_y_name_lineEdit.setObjectName(u"minus_y_name_lineEdit")

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.minus_y_name_lineEdit)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.frame_checkBox.setText(QCoreApplication.translate("Form", u"Frame", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Size", None))
        self.plus_x_checkBox.setText(QCoreApplication.translate("Form", u"Plus X", None))
        self.minus_x_checkBox.setText(QCoreApplication.translate("Form", u"Minus X", None))
        self.plus_y_checkBox.setText(QCoreApplication.translate("Form", u"Plus Y", None))
        self.minus_y_checkBox.setText(QCoreApplication.translate("Form", u"Minus Y", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Plus X name", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Minus X name", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Plus Y name", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Minus Y name", None))
    # retranslateUi

