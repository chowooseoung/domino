# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(457, 247)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.target_rig_file_lineEdit = QLineEdit(self.groupBox)
        self.target_rig_file_lineEdit.setObjectName(u"target_rig_file_lineEdit")

        self.gridLayout.addWidget(self.target_rig_file_lineEdit, 0, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.interface_comboBox = QComboBox(self.groupBox)
        self.interface_comboBox.setObjectName(u"interface_comboBox")

        self.gridLayout.addWidget(self.interface_comboBox, 1, 1, 1, 1)

        self.load_rig_pushButton = QPushButton(self.groupBox)
        self.load_rig_pushButton.setObjectName(u"load_rig_pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_rig_pushButton.sizePolicy().hasHeightForWidth())
        self.load_rig_pushButton.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.load_rig_pushButton, 0, 2, 3, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.motion_directory_lineEdit = QLineEdit(self.groupBox_2)
        self.motion_directory_lineEdit.setObjectName(u"motion_directory_lineEdit")

        self.gridLayout_2.addWidget(self.motion_directory_lineEdit, 1, 1, 1, 1)

        self.motion_definition_comboBox = QComboBox(self.groupBox_2)
        self.motion_definition_comboBox.setObjectName(u"motion_definition_comboBox")

        self.gridLayout_2.addWidget(self.motion_definition_comboBox, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.export_directory_lineEdit = QLineEdit(self.groupBox_3)
        self.export_directory_lineEdit.setObjectName(u"export_directory_lineEdit")

        self.gridLayout_3.addWidget(self.export_directory_lineEdit, 0, 1, 1, 1)

        self.export_pushButton = QPushButton(self.groupBox_3)
        self.export_pushButton.setObjectName(u"export_pushButton")

        self.gridLayout_3.addWidget(self.export_pushButton, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Rig", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Target Rig File", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Interface File", None))
        self.load_rig_pushButton.setText(QCoreApplication.translate("Dialog", u"Load", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Motion", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Motion Directory", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Definition", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Export", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Export Directory", None))
        self.export_pushButton.setText(QCoreApplication.translate("Dialog", u"Export", None))
    # retranslateUi

