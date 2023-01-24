# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'common_piece_settings_ui.ui'
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
        Form.resize(412, 456)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.toolBox = QToolBox(Form)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setStyleSheet(u"QToolBox::tab {\n"
"	border-radius: 1px;\n"
"	color: dark;\n"
"}\n"
"\n"
"QToolBox::tab:selected {\n"
"    color: white;\n"
"}\n"
"\n"
"QToolBox QScrollArea>QWidget>QWidget>QWidget\n"
"{\n"
"	background: rgb(80, 80, 80);\n"
"}")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 394, 412))
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy1)
        self.page.setMinimumSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.page)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.name_lineEdit = QLineEdit(self.groupBox)
        self.name_lineEdit.setObjectName(u"name_lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.name_lineEdit.sizePolicy().hasHeightForWidth())
        self.name_lineEdit.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.name_lineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.side_comboBox = QComboBox(self.groupBox)
        self.side_comboBox.addItem("")
        self.side_comboBox.addItem("")
        self.side_comboBox.addItem("")
        self.side_comboBox.setObjectName(u"side_comboBox")
        sizePolicy.setHeightForWidth(self.side_comboBox.sizePolicy().hasHeightForWidth())
        self.side_comboBox.setSizePolicy(sizePolicy)
        self.side_comboBox.setLayoutDirection(Qt.LeftToRight)
        self.side_comboBox.setFrame(False)

        self.gridLayout.addWidget(self.side_comboBox, 1, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.index_spinBox = QSpinBox(self.groupBox)
        self.index_spinBox.setObjectName(u"index_spinBox")
        sizePolicy.setHeightForWidth(self.index_spinBox.sizePolicy().hasHeightForWidth())
        self.index_spinBox.setSizePolicy(sizePolicy)
        self.index_spinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.index_spinBox.setMaximum(9999)

        self.gridLayout.addWidget(self.index_spinBox, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.page)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.ref_index_spinBox = QSpinBox(self.groupBox_2)
        self.ref_index_spinBox.setObjectName(u"ref_index_spinBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.ref_index_spinBox.sizePolicy().hasHeightForWidth())
        self.ref_index_spinBox.setSizePolicy(sizePolicy4)
        self.ref_index_spinBox.setMinimum(-1)
        self.ref_index_spinBox.setMaximum(999)

        self.gridLayout_2.addWidget(self.ref_index_spinBox, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        sizePolicy4.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy4)

        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)

        self.custom_jnt_name_pushButton = QPushButton(self.groupBox_2)
        self.custom_jnt_name_pushButton.setObjectName(u"custom_jnt_name_pushButton")
        sizePolicy3.setHeightForWidth(self.custom_jnt_name_pushButton.sizePolicy().hasHeightForWidth())
        self.custom_jnt_name_pushButton.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.custom_jnt_name_pushButton, 1, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.groupBox_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setFlat(False)
        self.horizontalLayout = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.orientX_spinBox = QSpinBox(self.groupBox_4)
        self.orientX_spinBox.setObjectName(u"orientX_spinBox")
        sizePolicy3.setHeightForWidth(self.orientX_spinBox.sizePolicy().hasHeightForWidth())
        self.orientX_spinBox.setSizePolicy(sizePolicy3)
        self.orientX_spinBox.setFrame(False)
        self.orientX_spinBox.setMinimum(-360)
        self.orientX_spinBox.setMaximum(360)
        self.orientX_spinBox.setSingleStep(90)
        self.orientX_spinBox.setStepType(QAbstractSpinBox.DefaultStepType)

        self.horizontalLayout.addWidget(self.orientX_spinBox)

        self.orientY_spinBox = QSpinBox(self.groupBox_4)
        self.orientY_spinBox.setObjectName(u"orientY_spinBox")
        sizePolicy3.setHeightForWidth(self.orientY_spinBox.sizePolicy().hasHeightForWidth())
        self.orientY_spinBox.setSizePolicy(sizePolicy3)
        self.orientY_spinBox.setFrame(False)
        self.orientY_spinBox.setMinimum(-360)
        self.orientY_spinBox.setMaximum(360)
        self.orientY_spinBox.setSingleStep(90)

        self.horizontalLayout.addWidget(self.orientY_spinBox)

        self.orientZ_spinBox = QSpinBox(self.groupBox_4)
        self.orientZ_spinBox.setObjectName(u"orientZ_spinBox")
        sizePolicy3.setHeightForWidth(self.orientZ_spinBox.sizePolicy().hasHeightForWidth())
        self.orientZ_spinBox.setSizePolicy(sizePolicy3)
        self.orientZ_spinBox.setFrame(False)
        self.orientZ_spinBox.setProperty("showGroupSeparator", False)
        self.orientZ_spinBox.setMinimum(-360)
        self.orientZ_spinBox.setMaximum(360)
        self.orientZ_spinBox.setSingleStep(90)

        self.horizontalLayout.addWidget(self.orientZ_spinBox)


        self.gridLayout_2.addWidget(self.groupBox_4, 2, 0, 1, 2)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.page)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy5)

        self.gridLayout_3.addWidget(self.label_8, 1, 3, 1, 1)

        self.color_ik_pushButton = QPushButton(self.groupBox_3)
        self.color_ik_pushButton.setObjectName(u"color_ik_pushButton")
        sizePolicy.setHeightForWidth(self.color_ik_pushButton.sizePolicy().hasHeightForWidth())
        self.color_ik_pushButton.setSizePolicy(sizePolicy)
        self.color_ik_pushButton.setMinimumSize(QSize(24, 24))
        self.color_ik_pushButton.setMaximumSize(QSize(24, 24))

        self.gridLayout_3.addWidget(self.color_ik_pushButton, 1, 4, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.color_rgb_ik_horizontalSlider = QSlider(self.groupBox_3)
        self.color_rgb_ik_horizontalSlider.setObjectName(u"color_rgb_ik_horizontalSlider")
        sizePolicy2.setHeightForWidth(self.color_rgb_ik_horizontalSlider.sizePolicy().hasHeightForWidth())
        self.color_rgb_ik_horizontalSlider.setSizePolicy(sizePolicy2)
        self.color_rgb_ik_horizontalSlider.setMinimumSize(QSize(0, 0))
        self.color_rgb_ik_horizontalSlider.setMaximum(100)
        self.color_rgb_ik_horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.color_rgb_ik_horizontalSlider)

        self.color_ik_spinBox = QSpinBox(self.groupBox_3)
        self.color_ik_spinBox.setObjectName(u"color_ik_spinBox")
        sizePolicy2.setHeightForWidth(self.color_ik_spinBox.sizePolicy().hasHeightForWidth())
        self.color_ik_spinBox.setSizePolicy(sizePolicy2)
        self.color_ik_spinBox.setMinimumSize(QSize(0, 0))
        self.color_ik_spinBox.setMaximum(31)

        self.horizontalLayout_3.addWidget(self.color_ik_spinBox)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 5, 1, 1)

        self.override_colors_checkBox = QCheckBox(self.groupBox_3)
        self.override_colors_checkBox.setObjectName(u"override_colors_checkBox")
        sizePolicy2.setHeightForWidth(self.override_colors_checkBox.sizePolicy().hasHeightForWidth())
        self.override_colors_checkBox.setSizePolicy(sizePolicy2)
        self.override_colors_checkBox.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.override_colors_checkBox, 0, 0, 1, 3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.color_rgb_fk_horizontalSlider = QSlider(self.groupBox_3)
        self.color_rgb_fk_horizontalSlider.setObjectName(u"color_rgb_fk_horizontalSlider")
        sizePolicy2.setHeightForWidth(self.color_rgb_fk_horizontalSlider.sizePolicy().hasHeightForWidth())
        self.color_rgb_fk_horizontalSlider.setSizePolicy(sizePolicy2)
        self.color_rgb_fk_horizontalSlider.setMinimumSize(QSize(0, 0))
        self.color_rgb_fk_horizontalSlider.setMaximum(100)
        self.color_rgb_fk_horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.color_rgb_fk_horizontalSlider)

        self.color_fk_spinBox = QSpinBox(self.groupBox_3)
        self.color_fk_spinBox.setObjectName(u"color_fk_spinBox")
        sizePolicy2.setHeightForWidth(self.color_fk_spinBox.sizePolicy().hasHeightForWidth())
        self.color_fk_spinBox.setSizePolicy(sizePolicy2)
        self.color_fk_spinBox.setMinimumSize(QSize(0, 0))
        self.color_fk_spinBox.setMaximum(31)

        self.horizontalLayout_2.addWidget(self.color_fk_spinBox)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)

        self.use_RGB_colors_checkBox = QCheckBox(self.groupBox_3)
        self.use_RGB_colors_checkBox.setObjectName(u"use_RGB_colors_checkBox")
        sizePolicy2.setHeightForWidth(self.use_RGB_colors_checkBox.sizePolicy().hasHeightForWidth())
        self.use_RGB_colors_checkBox.setSizePolicy(sizePolicy2)
        self.use_RGB_colors_checkBox.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.use_RGB_colors_checkBox, 0, 3, 1, 3)

        self.color_fk_pushButton = QPushButton(self.groupBox_3)
        self.color_fk_pushButton.setObjectName(u"color_fk_pushButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.color_fk_pushButton.sizePolicy().hasHeightForWidth())
        self.color_fk_pushButton.setSizePolicy(sizePolicy6)
        self.color_fk_pushButton.setMinimumSize(QSize(24, 24))
        self.color_fk_pushButton.setMaximumSize(QSize(24, 24))

        self.gridLayout_3.addWidget(self.color_fk_pushButton, 1, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        sizePolicy5.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy5)

        self.gridLayout_3.addWidget(self.label_7, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_6 = QGroupBox(self.page)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_4 = QGridLayout(self.groupBox_6)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.select_host_pushButton = QPushButton(self.groupBox_6)
        self.select_host_pushButton.setObjectName(u"select_host_pushButton")
        sizePolicy6.setHeightForWidth(self.select_host_pushButton.sizePolicy().hasHeightForWidth())
        self.select_host_pushButton.setSizePolicy(sizePolicy6)

        self.gridLayout_4.addWidget(self.select_host_pushButton, 0, 2, 2, 1)

        self.host_lineEdit = QLineEdit(self.groupBox_6)
        self.host_lineEdit.setObjectName(u"host_lineEdit")

        self.gridLayout_4.addWidget(self.host_lineEdit, 0, 0, 2, 2)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 2, 0, 1, 3)


        self.verticalLayout.addWidget(self.groupBox_6)

        self.toolBox.addItem(self.page, u"Common Settings")

        self.verticalLayout_2.addWidget(self.toolBox)


        self.retranslateUi(Form)

        self.toolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Piece Identifier", None))
        self.label.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Side", None))
        self.side_comboBox.setItemText(0, QCoreApplication.translate("Form", u"C", None))
        self.side_comboBox.setItemText(1, QCoreApplication.translate("Form", u"L", None))
        self.side_comboBox.setItemText(2, QCoreApplication.translate("Form", u"R", None))

        self.side_comboBox.setPlaceholderText("")
        self.label_3.setText(QCoreApplication.translate("Form", u"Index", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Joint Settings", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Ref Index", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Custom Name", None))
        self.custom_jnt_name_pushButton.setText(QCoreApplication.translate("Form", u"Edit", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Orient Offset", None))
        self.orientZ_spinBox.setSpecialValueText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"Color Settings", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Ik", None))
        self.color_ik_pushButton.setText("")
        self.override_colors_checkBox.setText(QCoreApplication.translate("Form", u"Override Colors", None))
        self.use_RGB_colors_checkBox.setText(QCoreApplication.translate("Form", u"Use RGB Colors", None))
        self.color_fk_pushButton.setText("")
        self.label_7.setText(QCoreApplication.translate("Form", u"Fk", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"Host Settings", None))
        self.select_host_pushButton.setText(QCoreApplication.translate("Form", u"Select", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QCoreApplication.translate("Form", u"Common Settings", None))
    # retranslateUi

