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
        Form.resize(316, 205)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.position_horizontalSlider = QSlider(self.groupBox)
        self.position_horizontalSlider.setObjectName(u"position_horizontalSlider")
        self.position_horizontalSlider.setMaximum(100)
        self.position_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.position_horizontalSlider, 0, 2, 1, 1)

        self.stretch_horizontalSlider = QSlider(self.groupBox)
        self.stretch_horizontalSlider.setObjectName(u"stretch_horizontalSlider")
        self.stretch_horizontalSlider.setMinimum(1)
        self.stretch_horizontalSlider.setMaximum(999)
        self.stretch_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.stretch_horizontalSlider, 2, 2, 1, 1)

        self.stretch_spinBox = QSpinBox(self.groupBox)
        self.stretch_spinBox.setObjectName(u"stretch_spinBox")
        self.stretch_spinBox.setMinimum(1)
        self.stretch_spinBox.setMaximum(999)

        self.gridLayout.addWidget(self.stretch_spinBox, 2, 3, 1, 1)

        self.squash_horizontalSlider = QSlider(self.groupBox)
        self.squash_horizontalSlider.setObjectName(u"squash_horizontalSlider")
        self.squash_horizontalSlider.setMinimum(1)
        self.squash_horizontalSlider.setMaximum(100)
        self.squash_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.squash_horizontalSlider, 3, 2, 1, 1)

        self.division_spinBox = QSpinBox(self.groupBox)
        self.division_spinBox.setObjectName(u"division_spinBox")
        self.division_spinBox.setMinimum(1)
        self.division_spinBox.setMaximum(999)

        self.gridLayout.addWidget(self.division_spinBox, 4, 2, 1, 2)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.position_spinBox = QSpinBox(self.groupBox)
        self.position_spinBox.setObjectName(u"position_spinBox")
        self.position_spinBox.setMaximum(100)

        self.gridLayout.addWidget(self.position_spinBox, 0, 3, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 2)

        self.squash_stretch_pushButton = QPushButton(self.groupBox)
        self.squash_stretch_pushButton.setObjectName(u"squash_stretch_pushButton")

        self.gridLayout.addWidget(self.squash_stretch_pushButton, 5, 0, 1, 4)

        self.squash_spinBox = QSpinBox(self.groupBox)
        self.squash_spinBox.setObjectName(u"squash_spinBox")
        self.squash_spinBox.setMinimum(1)
        self.squash_spinBox.setMaximum(100)

        self.gridLayout.addWidget(self.squash_spinBox, 3, 3, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 1, 1, 3)

        self.hip_position_horizontalSlider = QSlider(self.groupBox)
        self.hip_position_horizontalSlider.setObjectName(u"hip_position_horizontalSlider")
        self.hip_position_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.hip_position_horizontalSlider, 1, 2, 1, 1)

        self.hip_position_spinBox = QSpinBox(self.groupBox)
        self.hip_position_spinBox.setObjectName(u"hip_position_spinBox")

        self.gridLayout.addWidget(self.hip_position_spinBox, 1, 3, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(Form)
        self.position_horizontalSlider.valueChanged.connect(self.position_spinBox.setValue)
        self.position_spinBox.valueChanged.connect(self.position_horizontalSlider.setValue)
        self.stretch_horizontalSlider.valueChanged.connect(self.stretch_spinBox.setValue)
        self.stretch_spinBox.valueChanged.connect(self.stretch_horizontalSlider.setValue)
        self.squash_horizontalSlider.valueChanged.connect(self.squash_spinBox.setValue)
        self.squash_spinBox.valueChanged.connect(self.squash_horizontalSlider.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("Form", u"Max Stretch", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Division", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Hip Position", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Max Squash", None))
        self.squash_stretch_pushButton.setText(QCoreApplication.translate("Form", u"Squash & Stretch Edit", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Position", None))
    # retranslateUi

