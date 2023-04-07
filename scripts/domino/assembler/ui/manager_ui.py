# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manager_ui.ui'
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
        Dialog.resize(275, 462)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.extract_ctl_shapes_pushButton = QPushButton(self.groupBox)
        self.extract_ctl_shapes_pushButton.setObjectName(u"extract_ctl_shapes_pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extract_ctl_shapes_pushButton.sizePolicy().hasHeightForWidth())
        self.extract_ctl_shapes_pushButton.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.extract_ctl_shapes_pushButton, 0, 0, 1, 1)

        self.copy_pushButton = QPushButton(self.groupBox)
        self.copy_pushButton.setObjectName(u"copy_pushButton")
        sizePolicy.setHeightForWidth(self.copy_pushButton.sizePolicy().hasHeightForWidth())
        self.copy_pushButton.setSizePolicy(sizePolicy)
        self.copy_pushButton.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.copy_pushButton, 0, 1, 1, 1)

        self.mirror_pushButton = QPushButton(self.groupBox)
        self.mirror_pushButton.setObjectName(u"mirror_pushButton")
        sizePolicy.setHeightForWidth(self.mirror_pushButton.sizePolicy().hasHeightForWidth())
        self.mirror_pushButton.setSizePolicy(sizePolicy)
        self.mirror_pushButton.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.mirror_pushButton, 0, 2, 1, 1)

        self.settings_pushButton = QPushButton(self.groupBox)
        self.settings_pushButton.setObjectName(u"settings_pushButton")
        sizePolicy.setHeightForWidth(self.settings_pushButton.sizePolicy().hasHeightForWidth())
        self.settings_pushButton.setSizePolicy(sizePolicy)
        self.settings_pushButton.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.settings_pushButton, 1, 0, 1, 1)

        self.build_pushButton = QPushButton(self.groupBox)
        self.build_pushButton.setObjectName(u"build_pushButton")
        sizePolicy.setHeightForWidth(self.build_pushButton.sizePolicy().hasHeightForWidth())
        self.build_pushButton.setSizePolicy(sizePolicy)
        self.build_pushButton.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.build_pushButton, 1, 1, 1, 2)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox1 = QGroupBox(Dialog)
        self.groupBox1.setObjectName(u"groupBox1")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.search_lineEdit = QLineEdit(self.groupBox1)
        self.search_lineEdit.setObjectName(u"search_lineEdit")

        self.verticalLayout_2.addWidget(self.search_lineEdit)

        self.component_listView = QListView(self.groupBox1)
        self.component_listView.setObjectName(u"component_listView")
        self.component_listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.component_listView.setAlternatingRowColors(True)
        self.component_listView.setMovement(QListView.Snap)
        self.component_listView.setWordWrap(False)

        self.verticalLayout_2.addWidget(self.component_listView)

        self.description_textEdit = QTextEdit(self.groupBox1)
        self.description_textEdit.setObjectName(u"description_textEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.description_textEdit.sizePolicy().hasHeightForWidth())
        self.description_textEdit.setSizePolicy(sizePolicy1)
        self.description_textEdit.setMinimumSize(QSize(0, 0))
        self.description_textEdit.setMaximumSize(QSize(16777215, 124))
        self.description_textEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.description_textEdit)


        self.verticalLayout.addWidget(self.groupBox1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Command", None))
        self.extract_ctl_shapes_pushButton.setText(QCoreApplication.translate("Dialog", u"Ext. Shape", None))
        self.copy_pushButton.setText(QCoreApplication.translate("Dialog", u"Copy", None))
        self.mirror_pushButton.setText(QCoreApplication.translate("Dialog", u"Mirror", None))
        self.settings_pushButton.setText(QCoreApplication.translate("Dialog", u"Settings", None))
        self.build_pushButton.setText(QCoreApplication.translate("Dialog", u"Build", None))
        self.groupBox1.setTitle(QCoreApplication.translate("Dialog", u"List", None))
        self.search_lineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Search", None))
    # retranslateUi

