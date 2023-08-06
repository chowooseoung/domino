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
        Form.resize(289, 192)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.primary_checkBox = QCheckBox(self.groupBox)
        self.primary_checkBox.setObjectName(u"primary_checkBox")

        self.verticalLayout.addWidget(self.primary_checkBox)

        self.primary_coverts_checkBox = QCheckBox(self.groupBox)
        self.primary_coverts_checkBox.setObjectName(u"primary_coverts_checkBox")

        self.verticalLayout.addWidget(self.primary_coverts_checkBox)

        self.primary_under_checkBox = QCheckBox(self.groupBox)
        self.primary_under_checkBox.setObjectName(u"primary_under_checkBox")

        self.verticalLayout.addWidget(self.primary_under_checkBox)

        self.secondary_checkBox = QCheckBox(self.groupBox)
        self.secondary_checkBox.setObjectName(u"secondary_checkBox")

        self.verticalLayout.addWidget(self.secondary_checkBox)

        self.secondary_coverts_checkBox = QCheckBox(self.groupBox)
        self.secondary_coverts_checkBox.setObjectName(u"secondary_coverts_checkBox")

        self.verticalLayout.addWidget(self.secondary_coverts_checkBox)

        self.secondary_under_checkBox = QCheckBox(self.groupBox)
        self.secondary_under_checkBox.setObjectName(u"secondary_under_checkBox")

        self.verticalLayout.addWidget(self.secondary_under_checkBox)

        self.tertiary_checkBox = QCheckBox(self.groupBox)
        self.tertiary_checkBox.setObjectName(u"tertiary_checkBox")

        self.verticalLayout.addWidget(self.tertiary_checkBox)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.primary_checkBox.setText(QCoreApplication.translate("Form", u"Primary", None))
        self.primary_coverts_checkBox.setText(QCoreApplication.translate("Form", u"Primary Coverts", None))
        self.primary_under_checkBox.setText(QCoreApplication.translate("Form", u"Primary Under", None))
        self.secondary_checkBox.setText(QCoreApplication.translate("Form", u"Secondary", None))
        self.secondary_coverts_checkBox.setText(QCoreApplication.translate("Form", u"Secondary Coverts", None))
        self.secondary_under_checkBox.setText(QCoreApplication.translate("Form", u"Secondary Under", None))
        self.tertiary_checkBox.setText(QCoreApplication.translate("Form", u"Tertiary", None))
    # retranslateUi

