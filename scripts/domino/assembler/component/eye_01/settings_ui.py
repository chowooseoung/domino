# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_uizYiuCj.ui'
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
        Form.resize(323, 379)
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

        self.aim_space_switch_listWidget = QListWidget(self.groupBox_6)
        self.aim_space_switch_listWidget.setObjectName(u"aim_space_switch_listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aim_space_switch_listWidget.sizePolicy().hasHeightForWidth())
        self.aim_space_switch_listWidget.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.aim_space_switch_listWidget, 0, 0, 3, 1)

        self.aim_space_switch_add_pushButton = QPushButton(self.groupBox_6)
        self.aim_space_switch_add_pushButton.setObjectName(u"aim_space_switch_add_pushButton")

        self.gridLayout_6.addWidget(self.aim_space_switch_add_pushButton, 0, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_4, 2, 1, 2, 1)


        self.verticalLayout.addWidget(self.groupBox_6)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pupil_edge_index_pushButton = QPushButton(self.groupBox_2)
        self.pupil_edge_index_pushButton.setObjectName(u"pupil_edge_index_pushButton")

        self.gridLayout_2.addWidget(self.pupil_edge_index_pushButton, 4, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 5, 0, 1, 1)

        self.center_edge_index_lineEdit = QLineEdit(self.groupBox_2)
        self.center_edge_index_lineEdit.setObjectName(u"center_edge_index_lineEdit")

        self.gridLayout_2.addWidget(self.center_edge_index_lineEdit, 2, 1, 1, 1)

        self.limbus_edge_index_lineEdit = QLineEdit(self.groupBox_2)
        self.limbus_edge_index_lineEdit.setObjectName(u"limbus_edge_index_lineEdit")

        self.gridLayout_2.addWidget(self.limbus_edge_index_lineEdit, 3, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 4, 0, 1, 1)

        self.last_edge_index_pushButton = QPushButton(self.groupBox_2)
        self.last_edge_index_pushButton.setObjectName(u"last_edge_index_pushButton")

        self.gridLayout_2.addWidget(self.last_edge_index_pushButton, 5, 2, 1, 1)

        self.pupil_edge_index_lineEdit = QLineEdit(self.groupBox_2)
        self.pupil_edge_index_lineEdit.setObjectName(u"pupil_edge_index_lineEdit")

        self.gridLayout_2.addWidget(self.pupil_edge_index_lineEdit, 4, 1, 1, 1)

        self.eyeball_mesh_pushButton = QPushButton(self.groupBox_2)
        self.eyeball_mesh_pushButton.setObjectName(u"eyeball_mesh_pushButton")

        self.gridLayout_2.addWidget(self.eyeball_mesh_pushButton, 1, 2, 1, 1)

        self.center_edge_index_pushButton = QPushButton(self.groupBox_2)
        self.center_edge_index_pushButton.setObjectName(u"center_edge_index_pushButton")

        self.gridLayout_2.addWidget(self.center_edge_index_pushButton, 2, 2, 1, 1)

        self.limbus_edge_index_pushButton = QPushButton(self.groupBox_2)
        self.limbus_edge_index_pushButton.setObjectName(u"limbus_edge_index_pushButton")

        self.gridLayout_2.addWidget(self.limbus_edge_index_pushButton, 3, 2, 1, 1)

        self.last_edge_index_lineEdit = QLineEdit(self.groupBox_2)
        self.last_edge_index_lineEdit.setObjectName(u"last_edge_index_lineEdit")

        self.gridLayout_2.addWidget(self.last_edge_index_lineEdit, 5, 1, 1, 1)

        self.eyeball_mesh_lineEdit = QLineEdit(self.groupBox_2)
        self.eyeball_mesh_lineEdit.setObjectName(u"eyeball_mesh_lineEdit")

        self.gridLayout_2.addWidget(self.eyeball_mesh_lineEdit, 1, 1, 1, 1)

        self.spherical_iris_pupil_rig_checkBox = QCheckBox(self.groupBox_2)
        self.spherical_iris_pupil_rig_checkBox.setObjectName(u"spherical_iris_pupil_rig_checkBox")

        self.gridLayout_2.addWidget(self.spherical_iris_pupil_rig_checkBox, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)


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
        self.groupBox_2.setTitle("")
        self.pupil_edge_index_pushButton.setText(QCoreApplication.translate("Form", u"Select", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Last Edge Index", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Limbus Edge Index", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Center Edge Index", None))
        self.label.setText(QCoreApplication.translate("Form", u"Eyeball Mesh", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Pupil Edge Index", None))
        self.last_edge_index_pushButton.setText(QCoreApplication.translate("Form", u"Select", None))
        self.eyeball_mesh_pushButton.setText(QCoreApplication.translate("Form", u"Select", None))
        self.center_edge_index_pushButton.setText(QCoreApplication.translate("Form", u"Select", None))
        self.limbus_edge_index_pushButton.setText(QCoreApplication.translate("Form", u"Select", None))
        self.spherical_iris_pupil_rig_checkBox.setText(QCoreApplication.translate("Form", u"Spherical Iris Pupil Rig", None))
    # retranslateUi

