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
        Form.resize(196, 84)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.sliding_angle_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.sliding_angle_doubleSpinBox.setObjectName(u"sliding_angle_doubleSpinBox")
        self.sliding_angle_doubleSpinBox.setMinimum(-360.000000000000000)
        self.sliding_angle_doubleSpinBox.setMaximum(360.000000000000000)

        self.gridLayout.addWidget(self.sliding_angle_doubleSpinBox, 1, 1, 1, 2)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.sliding_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.sliding_doubleSpinBox.setObjectName(u"sliding_doubleSpinBox")

        self.gridLayout.addWidget(self.sliding_doubleSpinBox, 0, 1, 1, 2)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("Form", u"Sliding Angle", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Sliding", None))
    # retranslateUi

