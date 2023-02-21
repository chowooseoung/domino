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
        Form.resize(187, 84)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.connector_comboBox = QComboBox(self.groupBox)
        self.connector_comboBox.addItem("")
        self.connector_comboBox.addItem("")
        self.connector_comboBox.setObjectName(u"connector_comboBox")

        self.gridLayout.addWidget(self.connector_comboBox, 2, 1, 1, 2)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.roll_angle_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.roll_angle_doubleSpinBox.setObjectName(u"roll_angle_doubleSpinBox")
        self.roll_angle_doubleSpinBox.setMinimum(-360.000000000000000)
        self.roll_angle_doubleSpinBox.setMaximum(360.000000000000000)

        self.gridLayout.addWidget(self.roll_angle_doubleSpinBox, 3, 1, 1, 2)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.connector_comboBox.setItemText(0, QCoreApplication.translate("Form", u"default", None))
        self.connector_comboBox.setItemText(1, QCoreApplication.translate("Form", u"leg_2jnt_01", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"Connector", None))
        self.label.setText(QCoreApplication.translate("Form", u"Roll Angle", None))
    # retranslateUi

