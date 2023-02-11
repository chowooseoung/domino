# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'jnt_name_setting_ui.ui'
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
        Dialog.resize(315, 257)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableWidget = QTableWidget(Dialog)
        if (self.tableWidget.columnCount() < 1):
            self.tableWidget.setColumnCount(1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 7, 1)

        self.add_pushButton = QPushButton(Dialog)
        self.add_pushButton.setObjectName(u"add_pushButton")

        self.gridLayout.addWidget(self.add_pushButton, 0, 1, 1, 1)

        self.remove_pushButton = QPushButton(Dialog)
        self.remove_pushButton.setObjectName(u"remove_pushButton")

        self.gridLayout.addWidget(self.remove_pushButton, 1, 1, 1, 1)

        self.remove_all_pushButton = QPushButton(Dialog)
        self.remove_all_pushButton.setObjectName(u"remove_all_pushButton")

        self.gridLayout.addWidget(self.remove_all_pushButton, 2, 1, 1, 1)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 3, 1, 1, 1)

        self.up_pushButton = QPushButton(Dialog)
        self.up_pushButton.setObjectName(u"up_pushButton")

        self.gridLayout.addWidget(self.up_pushButton, 4, 1, 1, 1)

        self.down_pushButton = QPushButton(Dialog)
        self.down_pushButton.setObjectName(u"down_pushButton")

        self.gridLayout.addWidget(self.down_pushButton, 5, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 82, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.add_pushButton.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.remove_pushButton.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.remove_all_pushButton.setText(QCoreApplication.translate("Dialog", u"Remove All", None))
        self.up_pushButton.setText(QCoreApplication.translate("Dialog", u"Up", None))
        self.down_pushButton.setText(QCoreApplication.translate("Dialog", u"Down", None))
    # retranslateUi

