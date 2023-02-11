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
        Form.resize(337, 123)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_4 = QGroupBox(Form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalSpacer_2 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 2, 1, 2, 1)

        self.head_aim_switch_add_pushButton = QPushButton(self.groupBox_4)
        self.head_aim_switch_add_pushButton.setObjectName(u"head_aim_switch_add_pushButton")

        self.gridLayout_4.addWidget(self.head_aim_switch_add_pushButton, 0, 1, 1, 1)

        self.head_aim_switch_remove_pushButton = QPushButton(self.groupBox_4)
        self.head_aim_switch_remove_pushButton.setObjectName(u"head_aim_switch_remove_pushButton")

        self.gridLayout_4.addWidget(self.head_aim_switch_remove_pushButton, 1, 1, 1, 1)

        self.head_aim_switch_listWidget = QListWidget(self.groupBox_4)
        self.head_aim_switch_listWidget.setObjectName(u"head_aim_switch_listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.head_aim_switch_listWidget.sizePolicy().hasHeightForWidth())
        self.head_aim_switch_listWidget.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.head_aim_switch_listWidget, 0, 0, 3, 1)


        self.verticalLayout.addWidget(self.groupBox_4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Head Aim Switch", None))
        self.head_aim_switch_add_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.head_aim_switch_remove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
    # retranslateUi

