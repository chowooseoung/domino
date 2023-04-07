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
        Form.resize(329, 165)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.mirror_behaviour_checkBox = QCheckBox(self.groupBox)
        self.mirror_behaviour_checkBox.setObjectName(u"mirror_behaviour_checkBox")

        self.gridLayout.addWidget(self.mirror_behaviour_checkBox, 2, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_6 = QGroupBox(Form)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_6 = QGridLayout(self.groupBox_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.aim_space_switch_remove_pushButton = QPushButton(self.groupBox_6)
        self.aim_space_switch_remove_pushButton.setObjectName(u"aim_space_switch_remove_pushButton")

        self.gridLayout_6.addWidget(self.aim_space_switch_remove_pushButton, 1, 1, 1, 1)

        self.aim_space_switch_add_pushButton = QPushButton(self.groupBox_6)
        self.aim_space_switch_add_pushButton.setObjectName(u"aim_space_switch_add_pushButton")

        self.gridLayout_6.addWidget(self.aim_space_switch_add_pushButton, 0, 1, 1, 1)

        self.aim_space_switch_listWidget = QListWidget(self.groupBox_6)
        self.aim_space_switch_listWidget.setObjectName(u"aim_space_switch_listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aim_space_switch_listWidget.sizePolicy().hasHeightForWidth())
        self.aim_space_switch_listWidget.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.aim_space_switch_listWidget, 0, 0, 3, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_4, 2, 1, 2, 1)


        self.verticalLayout.addWidget(self.groupBox_6)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.mirror_behaviour_checkBox.setText(QCoreApplication.translate("Form", u"Mirror Behaviour", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"Aim Space Switch", None))
        self.aim_space_switch_remove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
        self.aim_space_switch_add_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
    # retranslateUi

