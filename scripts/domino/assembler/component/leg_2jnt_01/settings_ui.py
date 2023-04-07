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
        Form.resize(320, 607)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.guide_orient_ankle_checkBox = QCheckBox(self.groupBox)
        self.guide_orient_ankle_checkBox.setObjectName(u"guide_orient_ankle_checkBox")

        self.gridLayout.addWidget(self.guide_orient_ankle_checkBox, 5, 0, 1, 1)

        self.fk_ik_horizontalSlider = QSlider(self.groupBox)
        self.fk_ik_horizontalSlider.setObjectName(u"fk_ik_horizontalSlider")
        self.fk_ik_horizontalSlider.setMaximum(100)
        self.fk_ik_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fk_ik_horizontalSlider, 0, 1, 1, 1)

        self.fk_ik_spinBox = QSpinBox(self.groupBox)
        self.fk_ik_spinBox.setObjectName(u"fk_ik_spinBox")
        self.fk_ik_spinBox.setMaximum(100)

        self.gridLayout.addWidget(self.fk_ik_spinBox, 0, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.upper_division_spinBox = QSpinBox(self.groupBox)
        self.upper_division_spinBox.setObjectName(u"upper_division_spinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upper_division_spinBox.sizePolicy().hasHeightForWidth())
        self.upper_division_spinBox.setSizePolicy(sizePolicy)
        self.upper_division_spinBox.setMinimum(1)

        self.horizontalLayout.addWidget(self.upper_division_spinBox)

        self.lower_division_spinBox = QSpinBox(self.groupBox)
        self.lower_division_spinBox.setObjectName(u"lower_division_spinBox")
        sizePolicy.setHeightForWidth(self.lower_division_spinBox.sizePolicy().hasHeightForWidth())
        self.lower_division_spinBox.setSizePolicy(sizePolicy)
        self.lower_division_spinBox.setMinimum(1)

        self.horizontalLayout.addWidget(self.lower_division_spinBox)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 2)

        self.max_stretch_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.max_stretch_doubleSpinBox.setObjectName(u"max_stretch_doubleSpinBox")

        self.gridLayout.addWidget(self.max_stretch_doubleSpinBox, 1, 1, 1, 2)

        self.support_knee_jnt_checkBox = QCheckBox(self.groupBox)
        self.support_knee_jnt_checkBox.setObjectName(u"support_knee_jnt_checkBox")

        self.gridLayout.addWidget(self.support_knee_jnt_checkBox, 6, 0, 1, 1)

        self.squash_stretch_pushButton = QPushButton(self.groupBox)
        self.squash_stretch_pushButton.setObjectName(u"squash_stretch_pushButton")

        self.gridLayout.addWidget(self.squash_stretch_pushButton, 7, 0, 1, 3)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(Form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalSpacer_2 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 2, 1, 2, 1)

        self.pv_to_ik_space_switch_pushButton = QPushButton(self.groupBox_4)
        self.pv_to_ik_space_switch_pushButton.setObjectName(u"pv_to_ik_space_switch_pushButton")

        self.gridLayout_4.addWidget(self.pv_to_ik_space_switch_pushButton, 3, 0, 1, 1)

        self.ik_space_switch_add_pushButton = QPushButton(self.groupBox_4)
        self.ik_space_switch_add_pushButton.setObjectName(u"ik_space_switch_add_pushButton")

        self.gridLayout_4.addWidget(self.ik_space_switch_add_pushButton, 0, 1, 1, 1)

        self.ik_space_switch_remove_pushButton = QPushButton(self.groupBox_4)
        self.ik_space_switch_remove_pushButton.setObjectName(u"ik_space_switch_remove_pushButton")

        self.gridLayout_4.addWidget(self.ik_space_switch_remove_pushButton, 1, 1, 1, 1)

        self.ik_space_switch_listWidget = QListWidget(self.groupBox_4)
        self.ik_space_switch_listWidget.setObjectName(u"ik_space_switch_listWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ik_space_switch_listWidget.sizePolicy().hasHeightForWidth())
        self.ik_space_switch_listWidget.setSizePolicy(sizePolicy1)

        self.gridLayout_4.addWidget(self.ik_space_switch_listWidget, 0, 0, 3, 1)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(Form)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_5 = QGridLayout(self.groupBox_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.pv_space_switch_listWidget = QListWidget(self.groupBox_5)
        self.pv_space_switch_listWidget.setObjectName(u"pv_space_switch_listWidget")
        sizePolicy1.setHeightForWidth(self.pv_space_switch_listWidget.sizePolicy().hasHeightForWidth())
        self.pv_space_switch_listWidget.setSizePolicy(sizePolicy1)

        self.gridLayout_5.addWidget(self.pv_space_switch_listWidget, 0, 0, 3, 1)

        self.pv_space_switch_remove_pushButton = QPushButton(self.groupBox_5)
        self.pv_space_switch_remove_pushButton.setObjectName(u"pv_space_switch_remove_pushButton")

        self.gridLayout_5.addWidget(self.pv_space_switch_remove_pushButton, 1, 1, 1, 1)

        self.pv_space_switch_add_pushButton = QPushButton(self.groupBox_5)
        self.pv_space_switch_add_pushButton.setObjectName(u"pv_space_switch_add_pushButton")

        self.gridLayout_5.addWidget(self.pv_space_switch_add_pushButton, 0, 1, 1, 1)

        self.ik_to_pv_space_switch_pushButton = QPushButton(self.groupBox_5)
        self.ik_to_pv_space_switch_pushButton.setObjectName(u"ik_to_pv_space_switch_pushButton")

        self.gridLayout_5.addWidget(self.ik_to_pv_space_switch_pushButton, 3, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_3, 2, 1, 2, 1)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(Form)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_6 = QGridLayout(self.groupBox_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.pin_space_switch_remove_pushButton = QPushButton(self.groupBox_6)
        self.pin_space_switch_remove_pushButton.setObjectName(u"pin_space_switch_remove_pushButton")

        self.gridLayout_6.addWidget(self.pin_space_switch_remove_pushButton, 1, 1, 1, 1)

        self.pin_space_switch_add_pushButton = QPushButton(self.groupBox_6)
        self.pin_space_switch_add_pushButton.setObjectName(u"pin_space_switch_add_pushButton")

        self.gridLayout_6.addWidget(self.pin_space_switch_add_pushButton, 0, 1, 1, 1)

        self.pin_space_switch_listWidget = QListWidget(self.groupBox_6)
        self.pin_space_switch_listWidget.setObjectName(u"pin_space_switch_listWidget")
        sizePolicy1.setHeightForWidth(self.pin_space_switch_listWidget.sizePolicy().hasHeightForWidth())
        self.pin_space_switch_listWidget.setSizePolicy(sizePolicy1)

        self.gridLayout_6.addWidget(self.pin_space_switch_listWidget, 0, 0, 3, 1)

        self.ik_to_pin_space_switch_pushButton = QPushButton(self.groupBox_6)
        self.ik_to_pin_space_switch_pushButton.setObjectName(u"ik_to_pin_space_switch_pushButton")

        self.gridLayout_6.addWidget(self.ik_to_pin_space_switch_pushButton, 3, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_4, 2, 1, 2, 1)


        self.verticalLayout.addWidget(self.groupBox_6)


        self.retranslateUi(Form)
        self.fk_ik_horizontalSlider.valueChanged.connect(self.fk_ik_spinBox.setValue)
        self.fk_ik_spinBox.valueChanged.connect(self.fk_ik_horizontalSlider.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Max Stretch", None))
        self.label.setText(QCoreApplication.translate("Form", u"Fk / IK", None))
        self.guide_orient_ankle_checkBox.setText(QCoreApplication.translate("Form", u"Guide Orient Ankle", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Division", None))
        self.support_knee_jnt_checkBox.setText(QCoreApplication.translate("Form", u"Support Knee Jnt", None))
        self.squash_stretch_pushButton.setText(QCoreApplication.translate("Form", u"Squash Stretch Edit", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"IK Space Switch", None))
        self.pv_to_ik_space_switch_pushButton.setText(QCoreApplication.translate("Form", u"Copy from Pv Space Switch Array", None))
        self.ik_space_switch_add_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.ik_space_switch_remove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"Pv Space Switch", None))
        self.pv_space_switch_remove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
        self.pv_space_switch_add_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.ik_to_pv_space_switch_pushButton.setText(QCoreApplication.translate("Form", u"Copy from IK Space Switch Array", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"Pin Space Switch", None))
        self.pin_space_switch_remove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
        self.pin_space_switch_add_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.ik_to_pin_space_switch_pushButton.setText(QCoreApplication.translate("Form", u"Copy from IK Space Switch Array", None))
    # retranslateUi

