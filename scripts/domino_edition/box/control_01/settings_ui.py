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
        Form.resize(328, 521)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.leaf_joint_checkBox = QCheckBox(self.groupBox)
        self.leaf_joint_checkBox.setObjectName(u"leaf_joint_checkBox")

        self.gridLayout_3.addWidget(self.leaf_joint_checkBox, 2, 0, 1, 1)

        self.uni_scale_checkBox = QCheckBox(self.groupBox)
        self.uni_scale_checkBox.setObjectName(u"uni_scale_checkBox")

        self.gridLayout_3.addWidget(self.uni_scale_checkBox, 3, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 7, 0, 1, 1)

        self.icon_comboBox = QComboBox(self.groupBox)
        self.icon_comboBox.addItem("")
        self.icon_comboBox.setObjectName(u"icon_comboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon_comboBox.sizePolicy().hasHeightForWidth())
        self.icon_comboBox.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.icon_comboBox, 7, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 6, 0, 1, 1)

        self.nothing_checkBox = QCheckBox(self.groupBox)
        self.nothing_checkBox.setObjectName(u"nothing_checkBox")

        self.gridLayout_3.addWidget(self.nothing_checkBox, 0, 0, 1, 1)

        self.ctl_size_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.ctl_size_doubleSpinBox.setObjectName(u"ctl_size_doubleSpinBox")
        self.ctl_size_doubleSpinBox.setMinimum(0.010000000000000)
        self.ctl_size_doubleSpinBox.setMaximum(999.000000000000000)
        self.ctl_size_doubleSpinBox.setValue(1.000000000000000)

        self.gridLayout_3.addWidget(self.ctl_size_doubleSpinBox, 6, 1, 1, 1)

        self.joint_checkBox = QCheckBox(self.groupBox)
        self.joint_checkBox.setObjectName(u"joint_checkBox")

        self.gridLayout_3.addWidget(self.joint_checkBox, 1, 0, 1, 1)

        self.neutral_rotation_checkBox = QCheckBox(self.groupBox)
        self.neutral_rotation_checkBox.setObjectName(u"neutral_rotation_checkBox")

        self.gridLayout_3.addWidget(self.neutral_rotation_checkBox, 4, 0, 1, 1)

        self.mirror_behaviour_checkBox = QCheckBox(self.groupBox)
        self.mirror_behaviour_checkBox.setObjectName(u"mirror_behaviour_checkBox")

        self.gridLayout_3.addWidget(self.mirror_behaviour_checkBox, 5, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.rotate_pushButton = QPushButton(self.groupBox_2)
        self.rotate_pushButton.setObjectName(u"rotate_pushButton")

        self.gridLayout.addWidget(self.rotate_pushButton, 0, 1, 1, 1)

        self.tx_checkBox = QCheckBox(self.groupBox_2)
        self.tx_checkBox.setObjectName(u"tx_checkBox")

        self.gridLayout.addWidget(self.tx_checkBox, 1, 0, 1, 1)

        self.sy_checkBox = QCheckBox(self.groupBox_2)
        self.sy_checkBox.setObjectName(u"sy_checkBox")

        self.gridLayout.addWidget(self.sy_checkBox, 2, 2, 1, 1)

        self.ty_checkBox = QCheckBox(self.groupBox_2)
        self.ty_checkBox.setObjectName(u"ty_checkBox")

        self.gridLayout.addWidget(self.ty_checkBox, 2, 0, 1, 1)

        self.tz_checkBox = QCheckBox(self.groupBox_2)
        self.tz_checkBox.setObjectName(u"tz_checkBox")

        self.gridLayout.addWidget(self.tz_checkBox, 3, 0, 1, 1)

        self.ry_checkBox = QCheckBox(self.groupBox_2)
        self.ry_checkBox.setObjectName(u"ry_checkBox")

        self.gridLayout.addWidget(self.ry_checkBox, 2, 1, 1, 1)

        self.sx_checkBox = QCheckBox(self.groupBox_2)
        self.sx_checkBox.setObjectName(u"sx_checkBox")

        self.gridLayout.addWidget(self.sx_checkBox, 1, 2, 1, 1)

        self.rx_checkBox = QCheckBox(self.groupBox_2)
        self.rx_checkBox.setObjectName(u"rx_checkBox")

        self.gridLayout.addWidget(self.rx_checkBox, 1, 1, 1, 1)

        self.sz_checkBox = QCheckBox(self.groupBox_2)
        self.sz_checkBox.setObjectName(u"sz_checkBox")

        self.gridLayout.addWidget(self.sz_checkBox, 3, 2, 1, 1)

        self.translate_pushButton = QPushButton(self.groupBox_2)
        self.translate_pushButton.setObjectName(u"translate_pushButton")

        self.gridLayout.addWidget(self.translate_pushButton, 0, 0, 1, 1)

        self.scale_pushButton = QPushButton(self.groupBox_2)
        self.scale_pushButton.setObjectName(u"scale_pushButton")

        self.gridLayout.addWidget(self.scale_pushButton, 0, 2, 1, 1)

        self.rz_checkBox = QCheckBox(self.groupBox_2)
        self.rz_checkBox.setObjectName(u"rz_checkBox")

        self.gridLayout.addWidget(self.rz_checkBox, 3, 1, 1, 1)

        self.ro_checkBox = QCheckBox(self.groupBox_2)
        self.ro_checkBox.setObjectName(u"ro_checkBox")

        self.gridLayout.addWidget(self.ro_checkBox, 4, 1, 1, 1)

        self.ro_comboBox = QComboBox(self.groupBox_2)
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.setObjectName(u"ro_comboBox")

        self.gridLayout.addWidget(self.ro_comboBox, 5, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.remove_pushButton = QPushButton(self.groupBox_3)
        self.remove_pushButton.setObjectName(u"remove_pushButton")

        self.gridLayout_2.addWidget(self.remove_pushButton, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.add_pushButton = QPushButton(self.groupBox_3)
        self.add_pushButton.setObjectName(u"add_pushButton")

        self.gridLayout_2.addWidget(self.add_pushButton, 0, 1, 1, 1)

        self.listWidget = QListWidget(self.groupBox_3)
        self.listWidget.setObjectName(u"listWidget")

        self.gridLayout_2.addWidget(self.listWidget, 0, 0, 3, 1)


        self.verticalLayout.addWidget(self.groupBox_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.leaf_joint_checkBox.setText(QCoreApplication.translate("Form", u"Leaf Joint", None))
        self.uni_scale_checkBox.setText(QCoreApplication.translate("Form", u"Uni Scale", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Icon", None))
        self.icon_comboBox.setItemText(0, QCoreApplication.translate("Form", u"cube", None))

        self.label.setText(QCoreApplication.translate("Form", u"Ctl Size", None))
        self.nothing_checkBox.setText(QCoreApplication.translate("Form", u"Nothing", None))
        self.joint_checkBox.setText(QCoreApplication.translate("Form", u"Joint", None))
        self.neutral_rotation_checkBox.setText(QCoreApplication.translate("Form", u"Neutral Rotation", None))
        self.mirror_behaviour_checkBox.setText(QCoreApplication.translate("Form", u"Mirror Behaviour", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Keyable", None))
        self.rotate_pushButton.setText(QCoreApplication.translate("Form", u"Rotate", None))
        self.tx_checkBox.setText(QCoreApplication.translate("Form", u"tx", None))
        self.sy_checkBox.setText(QCoreApplication.translate("Form", u"sy", None))
        self.ty_checkBox.setText(QCoreApplication.translate("Form", u"ty", None))
        self.tz_checkBox.setText(QCoreApplication.translate("Form", u"tz", None))
        self.ry_checkBox.setText(QCoreApplication.translate("Form", u"ry", None))
        self.sx_checkBox.setText(QCoreApplication.translate("Form", u"sx", None))
        self.rx_checkBox.setText(QCoreApplication.translate("Form", u"rx", None))
        self.sz_checkBox.setText(QCoreApplication.translate("Form", u"sz", None))
        self.translate_pushButton.setText(QCoreApplication.translate("Form", u"Translate", None))
        self.scale_pushButton.setText(QCoreApplication.translate("Form", u"Scale", None))
        self.rz_checkBox.setText(QCoreApplication.translate("Form", u"rz", None))
        self.ro_checkBox.setText(QCoreApplication.translate("Form", u"ro", None))
        self.ro_comboBox.setItemText(0, QCoreApplication.translate("Form", u"xyz", None))
        self.ro_comboBox.setItemText(1, QCoreApplication.translate("Form", u"yzx", None))
        self.ro_comboBox.setItemText(2, QCoreApplication.translate("Form", u"zxy", None))
        self.ro_comboBox.setItemText(3, QCoreApplication.translate("Form", u"xzy", None))
        self.ro_comboBox.setItemText(4, QCoreApplication.translate("Form", u"yxz", None))
        self.ro_comboBox.setItemText(5, QCoreApplication.translate("Form", u"zyx", None))

        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"Space Switch", None))
        self.remove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
        self.add_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
    # retranslateUi

