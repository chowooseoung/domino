# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pose_manager_ui.ui'
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
        Dialog.resize(341, 218)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 3)

        self.add_pushButton = QPushButton(Dialog)
        self.add_pushButton.setObjectName(u"add_pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_pushButton.sizePolicy().hasHeightForWidth())
        self.add_pushButton.setSizePolicy(sizePolicy)
        self.add_pushButton.setMinimumSize(QSize(50, 0))

        self.gridLayout.addWidget(self.add_pushButton, 0, 1, 1, 1)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAutoFillBackground(False)

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.delete_pushButton = QPushButton(Dialog)
        self.delete_pushButton.setObjectName(u"delete_pushButton")
        sizePolicy.setHeightForWidth(self.delete_pushButton.sizePolicy().hasHeightForWidth())
        self.delete_pushButton.setSizePolicy(sizePolicy)
        self.delete_pushButton.setMinimumSize(QSize(50, 0))

        self.gridLayout.addWidget(self.delete_pushButton, 0, 2, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.add_pushButton.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"pose name", None))
        self.delete_pushButton.setText(QCoreApplication.translate("Dialog", u"Delete", None))
    # retranslateUi

