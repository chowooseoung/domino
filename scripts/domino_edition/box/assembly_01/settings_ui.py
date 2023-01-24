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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(390, 583)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.toolBox = QToolBox(Dialog)
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
"QToolBox QScrollArea>QWidget>QWidget\n"
"{\n"
"	background: rgb(80, 80, 80);\n"
"}")
        self.toolBox.setFrameShadow(QFrame.Raised)
        self.rig_page = QWidget()
        self.rig_page.setObjectName(u"rig_page")
        self.rig_page.setGeometry(QRect(0, 0, 372, 493))
        self.verticalLayout = QVBoxLayout(self.rig_page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.rig_page)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.end_point_comboBox = QComboBox(self.groupBox)
        self.end_point_comboBox.addItem("")
        self.end_point_comboBox.addItem("")
        self.end_point_comboBox.addItem("")
        self.end_point_comboBox.addItem("")
        self.end_point_comboBox.addItem("")
        self.end_point_comboBox.addItem("")
        self.end_point_comboBox.setObjectName(u"end_point_comboBox")

        self.gridLayout_3.addWidget(self.end_point_comboBox, 2, 1, 1, 2)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.mode_comboBox = QComboBox(self.groupBox)
        self.mode_comboBox.addItem("")
        self.mode_comboBox.addItem("")
        self.mode_comboBox.addItem("")
        self.mode_comboBox.setObjectName(u"mode_comboBox")

        self.gridLayout_3.addWidget(self.mode_comboBox, 1, 1, 1, 2)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_3.addWidget(self.label_12, 2, 0, 1, 1)

        self.rig_name_lineEdit = QLineEdit(self.groupBox)
        self.rig_name_lineEdit.setObjectName(u"rig_name_lineEdit")

        self.gridLayout_3.addWidget(self.rig_name_lineEdit, 0, 1, 1, 2)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.notes_textEdit = QTextEdit(self.groupBox)
        self.notes_textEdit.setObjectName(u"notes_textEdit")

        self.gridLayout_3.addWidget(self.notes_textEdit, 3, 0, 1, 3)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(self.rig_page)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_5.addWidget(self.label_11, 1, 0, 1, 1)

        self.origin_ctl_size_doubleSpinBox = QDoubleSpinBox(self.groupBox_4)
        self.origin_ctl_size_doubleSpinBox.setObjectName(u"origin_ctl_size_doubleSpinBox")
        self.origin_ctl_size_doubleSpinBox.setMinimum(0.000000000000000)
        self.origin_ctl_size_doubleSpinBox.setMaximum(100.000000000000000)
        self.origin_ctl_size_doubleSpinBox.setSingleStep(0.200000000000000)

        self.gridLayout_5.addWidget(self.origin_ctl_size_doubleSpinBox, 1, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)

        self.origin_sub_ctl_count_spinBox = QSpinBox(self.groupBox_4)
        self.origin_sub_ctl_count_spinBox.setObjectName(u"origin_sub_ctl_count_spinBox")

        self.gridLayout_5.addWidget(self.origin_sub_ctl_count_spinBox, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.rig_page)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.force_uniform_scale_checkBox = QCheckBox(self.groupBox_5)
        self.force_uniform_scale_checkBox.setObjectName(u"force_uniform_scale_checkBox")

        self.verticalLayout_2.addWidget(self.force_uniform_scale_checkBox)

        self.connect_jnt_checkBox = QCheckBox(self.groupBox_5)
        self.connect_jnt_checkBox.setObjectName(u"connect_jnt_checkBox")

        self.verticalLayout_2.addWidget(self.connect_jnt_checkBox)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.groupBox_3 = QGroupBox(self.rig_page)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.left_color_ik_pushButton = QPushButton(self.groupBox_3)
        self.left_color_ik_pushButton.setObjectName(u"left_color_ik_pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_color_ik_pushButton.sizePolicy().hasHeightForWidth())
        self.left_color_ik_pushButton.setSizePolicy(sizePolicy)
        self.left_color_ik_pushButton.setMinimumSize(QSize(24, 24))
        self.left_color_ik_pushButton.setMaximumSize(QSize(24, 24))

        self.gridLayout_2.addWidget(self.left_color_ik_pushButton, 2, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_7, 0, 7, 1, 3)

        self.right_color_fk_horizontalSlider = QSlider(self.groupBox_3)
        self.right_color_fk_horizontalSlider.setObjectName(u"right_color_fk_horizontalSlider")
        self.right_color_fk_horizontalSlider.setMaximum(100)
        self.right_color_fk_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.right_color_fk_horizontalSlider, 1, 8, 1, 1)

        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)

        self.left_color_ik_horizontalSlider = QSlider(self.groupBox_3)
        self.left_color_ik_horizontalSlider.setObjectName(u"left_color_ik_horizontalSlider")
        self.left_color_ik_horizontalSlider.setMaximum(100)
        self.left_color_ik_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.left_color_ik_horizontalSlider, 2, 2, 1, 1)

        self.right_color_ik_pushButton = QPushButton(self.groupBox_3)
        self.right_color_ik_pushButton.setObjectName(u"right_color_ik_pushButton")
        sizePolicy.setHeightForWidth(self.right_color_ik_pushButton.sizePolicy().hasHeightForWidth())
        self.right_color_ik_pushButton.setSizePolicy(sizePolicy)
        self.right_color_ik_pushButton.setMinimumSize(QSize(24, 24))
        self.right_color_ik_pushButton.setMaximumSize(QSize(24, 24))

        self.gridLayout_2.addWidget(self.right_color_ik_pushButton, 2, 7, 1, 1)

        self.left_color_fk_pushButton = QPushButton(self.groupBox_3)
        self.left_color_fk_pushButton.setObjectName(u"left_color_fk_pushButton")
        sizePolicy.setHeightForWidth(self.left_color_fk_pushButton.sizePolicy().hasHeightForWidth())
        self.left_color_fk_pushButton.setSizePolicy(sizePolicy)
        self.left_color_fk_pushButton.setMinimumSize(QSize(24, 24))
        self.left_color_fk_pushButton.setMaximumSize(QSize(24, 24))

        self.gridLayout_2.addWidget(self.left_color_fk_pushButton, 1, 1, 1, 1)

        self.left_color_ik_spinBox = QSpinBox(self.groupBox_3)
        self.left_color_ik_spinBox.setObjectName(u"left_color_ik_spinBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.left_color_ik_spinBox.sizePolicy().hasHeightForWidth())
        self.left_color_ik_spinBox.setSizePolicy(sizePolicy1)
        self.left_color_ik_spinBox.setMaximum(31)

        self.gridLayout_2.addWidget(self.left_color_ik_spinBox, 2, 3, 1, 1)

        self.left_color_fk_horizontalSlider = QSlider(self.groupBox_3)
        self.left_color_fk_horizontalSlider.setObjectName(u"left_color_fk_horizontalSlider")
        self.left_color_fk_horizontalSlider.setMaximum(100)
        self.left_color_fk_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.left_color_fk_horizontalSlider, 1, 2, 1, 1)

        self.left_color_fk_spinBox = QSpinBox(self.groupBox_3)
        self.left_color_fk_spinBox.setObjectName(u"left_color_fk_spinBox")
        sizePolicy1.setHeightForWidth(self.left_color_fk_spinBox.sizePolicy().hasHeightForWidth())
        self.left_color_fk_spinBox.setSizePolicy(sizePolicy1)
        self.left_color_fk_spinBox.setMaximum(31)

        self.gridLayout_2.addWidget(self.left_color_fk_spinBox, 1, 3, 1, 1)

        self.center_color_fk_horizontalSlider = QSlider(self.groupBox_3)
        self.center_color_fk_horizontalSlider.setObjectName(u"center_color_fk_horizontalSlider")
        self.center_color_fk_horizontalSlider.setMaximum(100)
        self.center_color_fk_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.center_color_fk_horizontalSlider, 1, 5, 1, 1)

        self.center_color_ik_horizontalSlider = QSlider(self.groupBox_3)
        self.center_color_ik_horizontalSlider.setObjectName(u"center_color_ik_horizontalSlider")
        self.center_color_ik_horizontalSlider.setMaximum(100)
        self.center_color_ik_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.center_color_ik_horizontalSlider, 2, 5, 1, 1)

        self.center_color_fk_spinBox = QSpinBox(self.groupBox_3)
        self.center_color_fk_spinBox.setObjectName(u"center_color_fk_spinBox")
        sizePolicy1.setHeightForWidth(self.center_color_fk_spinBox.sizePolicy().hasHeightForWidth())
        self.center_color_fk_spinBox.setSizePolicy(sizePolicy1)
        self.center_color_fk_spinBox.setMaximum(31)

        self.gridLayout_2.addWidget(self.center_color_fk_spinBox, 1, 6, 1, 1)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)

        self.right_color_ik_horizontalSlider = QSlider(self.groupBox_3)
        self.right_color_ik_horizontalSlider.setObjectName(u"right_color_ik_horizontalSlider")
        self.right_color_ik_horizontalSlider.setMaximum(100)
        self.right_color_ik_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.right_color_ik_horizontalSlider, 2, 8, 1, 1)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_5, 0, 1, 1, 3)

        self.center_color_fk_pushButton = QPushButton(self.groupBox_3)
        self.center_color_fk_pushButton.setObjectName(u"center_color_fk_pushButton")
        sizePolicy.setHeightForWidth(self.center_color_fk_pushButton.sizePolicy().hasHeightForWidth())
        self.center_color_fk_pushButton.setSizePolicy(sizePolicy)
        self.center_color_fk_pushButton.setMinimumSize(QSize(24, 24))
        self.center_color_fk_pushButton.setMaximumSize(QSize(24, 24))

        self.gridLayout_2.addWidget(self.center_color_fk_pushButton, 1, 4, 1, 1)

        self.center_color_ik_pushButton = QPushButton(self.groupBox_3)
        self.center_color_ik_pushButton.setObjectName(u"center_color_ik_pushButton")
        sizePolicy.setHeightForWidth(self.center_color_ik_pushButton.sizePolicy().hasHeightForWidth())
        self.center_color_ik_pushButton.setSizePolicy(sizePolicy)
        self.center_color_ik_pushButton.setMinimumSize(QSize(24, 24))
        self.center_color_ik_pushButton.setMaximumSize(QSize(24, 24))

        self.gridLayout_2.addWidget(self.center_color_ik_pushButton, 2, 4, 1, 1)

        self.right_color_fk_pushButton = QPushButton(self.groupBox_3)
        self.right_color_fk_pushButton.setObjectName(u"right_color_fk_pushButton")
        sizePolicy.setHeightForWidth(self.right_color_fk_pushButton.sizePolicy().hasHeightForWidth())
        self.right_color_fk_pushButton.setSizePolicy(sizePolicy)
        self.right_color_fk_pushButton.setMinimumSize(QSize(24, 24))
        self.right_color_fk_pushButton.setMaximumSize(QSize(24, 24))

        self.gridLayout_2.addWidget(self.right_color_fk_pushButton, 1, 7, 1, 1)

        self.right_color_ik_spinBox = QSpinBox(self.groupBox_3)
        self.right_color_ik_spinBox.setObjectName(u"right_color_ik_spinBox")
        sizePolicy1.setHeightForWidth(self.right_color_ik_spinBox.sizePolicy().hasHeightForWidth())
        self.right_color_ik_spinBox.setSizePolicy(sizePolicy1)
        self.right_color_ik_spinBox.setMaximum(31)

        self.gridLayout_2.addWidget(self.right_color_ik_spinBox, 2, 9, 1, 1)

        self.right_color_fk_spinBox = QSpinBox(self.groupBox_3)
        self.right_color_fk_spinBox.setObjectName(u"right_color_fk_spinBox")
        sizePolicy1.setHeightForWidth(self.right_color_fk_spinBox.sizePolicy().hasHeightForWidth())
        self.right_color_fk_spinBox.setSizePolicy(sizePolicy1)
        self.right_color_fk_spinBox.setMaximum(31)

        self.gridLayout_2.addWidget(self.right_color_fk_spinBox, 1, 9, 1, 1)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_6, 0, 4, 1, 3)

        self.center_color_ik_spinBox = QSpinBox(self.groupBox_3)
        self.center_color_ik_spinBox.setObjectName(u"center_color_ik_spinBox")
        sizePolicy1.setHeightForWidth(self.center_color_ik_spinBox.sizePolicy().hasHeightForWidth())
        self.center_color_ik_spinBox.setSizePolicy(sizePolicy1)
        self.center_color_ik_spinBox.setMaximum(31)

        self.gridLayout_2.addWidget(self.center_color_ik_spinBox, 2, 6, 1, 1)

        self.use_RGB_colors_checkBox = QCheckBox(self.groupBox_3)
        self.use_RGB_colors_checkBox.setObjectName(u"use_RGB_colors_checkBox")

        self.gridLayout_2.addWidget(self.use_RGB_colors_checkBox, 3, 0, 1, 5)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.toolBox.addItem(self.rig_page, u"Rig Settings")
        self.sub_piece_page = QWidget()
        self.sub_piece_page.setObjectName(u"sub_piece_page")
        self.sub_piece_page.setGeometry(QRect(0, 0, 172, 211))
        self.gridLayout_4 = QGridLayout(self.sub_piece_page)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalSpacer_2 = QSpacerItem(20, 46, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 7, 1, 1, 1)

        self.sub_pieces_new_pushButton = QPushButton(self.sub_piece_page)
        self.sub_pieces_new_pushButton.setObjectName(u"sub_pieces_new_pushButton")

        self.gridLayout_4.addWidget(self.sub_pieces_new_pushButton, 3, 1, 1, 1)

        self.sub_pieces_listWidget = QListWidget(self.sub_piece_page)
        QListWidgetItem(self.sub_pieces_listWidget)
        QListWidgetItem(self.sub_pieces_listWidget)
        QListWidgetItem(self.sub_pieces_listWidget)
        QListWidgetItem(self.sub_pieces_listWidget)
        QListWidgetItem(self.sub_pieces_listWidget)
        self.sub_pieces_listWidget.setObjectName(u"sub_pieces_listWidget")

        self.gridLayout_4.addWidget(self.sub_pieces_listWidget, 2, 0, 6, 1)

        self.sub_pieces_run_sel_pushButton = QPushButton(self.sub_piece_page)
        self.sub_pieces_run_sel_pushButton.setObjectName(u"sub_pieces_run_sel_pushButton")

        self.gridLayout_4.addWidget(self.sub_pieces_run_sel_pushButton, 6, 1, 1, 1)

        self.sub_pieces_add_pushButton = QPushButton(self.sub_piece_page)
        self.sub_pieces_add_pushButton.setObjectName(u"sub_pieces_add_pushButton")

        self.gridLayout_4.addWidget(self.sub_pieces_add_pushButton, 2, 1, 1, 1)

        self.run_sub_pieces_checkBox = QCheckBox(self.sub_piece_page)
        self.run_sub_pieces_checkBox.setObjectName(u"run_sub_pieces_checkBox")

        self.gridLayout_4.addWidget(self.run_sub_pieces_checkBox, 0, 0, 1, 2)

        self.sub_pieces_edit_pushButton = QPushButton(self.sub_piece_page)
        self.sub_pieces_edit_pushButton.setObjectName(u"sub_pieces_edit_pushButton")

        self.gridLayout_4.addWidget(self.sub_pieces_edit_pushButton, 4, 1, 1, 1)

        self.sub_pieces_remove_pushButton = QPushButton(self.sub_piece_page)
        self.sub_pieces_remove_pushButton.setObjectName(u"sub_pieces_remove_pushButton")

        self.gridLayout_4.addWidget(self.sub_pieces_remove_pushButton, 5, 1, 1, 1)

        self.search_lineEdit = QLineEdit(self.sub_piece_page)
        self.search_lineEdit.setObjectName(u"search_lineEdit")

        self.gridLayout_4.addWidget(self.search_lineEdit, 1, 0, 1, 2)

        self.toolBox.addItem(self.sub_piece_page, u"Sub Piece Settings")
        self.name_rule_page = QWidget()
        self.name_rule_page.setObjectName(u"name_rule_page")
        self.name_rule_page.setGeometry(QRect(0, 0, 313, 452))
        self.gridLayout_8 = QGridLayout(self.name_rule_page)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.groupBox_6 = QGroupBox(self.name_rule_page)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ctl_name_rule_lineEdit = QLineEdit(self.groupBox_6)
        self.ctl_name_rule_lineEdit.setObjectName(u"ctl_name_rule_lineEdit")

        self.horizontalLayout.addWidget(self.ctl_name_rule_lineEdit)

        self.ctl_name_rule_reset_pushButton = QPushButton(self.groupBox_6)
        self.ctl_name_rule_reset_pushButton.setObjectName(u"ctl_name_rule_reset_pushButton")
        sizePolicy.setHeightForWidth(self.ctl_name_rule_reset_pushButton.sizePolicy().hasHeightForWidth())
        self.ctl_name_rule_reset_pushButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.ctl_name_rule_reset_pushButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_13 = QLabel(self.groupBox_6)
        self.label_13.setObjectName(u"label_13")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.label_13)

        self.ctl_description_letter_case_comboBox = QComboBox(self.groupBox_6)
        self.ctl_description_letter_case_comboBox.addItem("")
        self.ctl_description_letter_case_comboBox.addItem("")
        self.ctl_description_letter_case_comboBox.addItem("")
        self.ctl_description_letter_case_comboBox.addItem("")
        self.ctl_description_letter_case_comboBox.setObjectName(u"ctl_description_letter_case_comboBox")
        sizePolicy1.setHeightForWidth(self.ctl_description_letter_case_comboBox.sizePolicy().hasHeightForWidth())
        self.ctl_description_letter_case_comboBox.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.ctl_description_letter_case_comboBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)


        self.gridLayout_8.addWidget(self.groupBox_6, 0, 0, 1, 3)

        self.groupBox_7 = QGroupBox(self.name_rule_page)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.jnt_name_rule_lineEdit = QLineEdit(self.groupBox_7)
        self.jnt_name_rule_lineEdit.setObjectName(u"jnt_name_rule_lineEdit")

        self.horizontalLayout_3.addWidget(self.jnt_name_rule_lineEdit)

        self.jnt_name_rule_reset_pushButton = QPushButton(self.groupBox_7)
        self.jnt_name_rule_reset_pushButton.setObjectName(u"jnt_name_rule_reset_pushButton")
        sizePolicy.setHeightForWidth(self.jnt_name_rule_reset_pushButton.sizePolicy().hasHeightForWidth())
        self.jnt_name_rule_reset_pushButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.jnt_name_rule_reset_pushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_14 = QLabel(self.groupBox_7)
        self.label_14.setObjectName(u"label_14")
        sizePolicy2.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.label_14)

        self.jnt_description_letter_case_comboBox = QComboBox(self.groupBox_7)
        self.jnt_description_letter_case_comboBox.addItem("")
        self.jnt_description_letter_case_comboBox.addItem("")
        self.jnt_description_letter_case_comboBox.addItem("")
        self.jnt_description_letter_case_comboBox.addItem("")
        self.jnt_description_letter_case_comboBox.setObjectName(u"jnt_description_letter_case_comboBox")
        sizePolicy1.setHeightForWidth(self.jnt_description_letter_case_comboBox.sizePolicy().hasHeightForWidth())
        self.jnt_description_letter_case_comboBox.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.jnt_description_letter_case_comboBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.gridLayout_8.addWidget(self.groupBox_7, 1, 0, 1, 3)

        self.groupBox_8 = QGroupBox(self.name_rule_page)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_7 = QGridLayout(self.groupBox_8)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_15 = QLabel(self.groupBox_8)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_7.addWidget(self.label_15, 0, 0, 1, 1)

        self.l_ctl_side_name_lineEdit = QLineEdit(self.groupBox_8)
        self.l_ctl_side_name_lineEdit.setObjectName(u"l_ctl_side_name_lineEdit")
        self.l_ctl_side_name_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.l_ctl_side_name_lineEdit, 0, 1, 1, 1)

        self.label_16 = QLabel(self.groupBox_8)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_7.addWidget(self.label_16, 1, 0, 1, 1)

        self.r_ctl_side_name_lineEdit = QLineEdit(self.groupBox_8)
        self.r_ctl_side_name_lineEdit.setObjectName(u"r_ctl_side_name_lineEdit")
        self.r_ctl_side_name_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.r_ctl_side_name_lineEdit, 1, 1, 1, 1)

        self.label_17 = QLabel(self.groupBox_8)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_7.addWidget(self.label_17, 2, 0, 1, 1)

        self.c_ctl_side_name_lineEdit = QLineEdit(self.groupBox_8)
        self.c_ctl_side_name_lineEdit.setObjectName(u"c_ctl_side_name_lineEdit")
        self.c_ctl_side_name_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.c_ctl_side_name_lineEdit, 2, 1, 1, 1)

        self.ctl_side_name_reset_pushButton = QPushButton(self.groupBox_8)
        self.ctl_side_name_reset_pushButton.setObjectName(u"ctl_side_name_reset_pushButton")

        self.gridLayout_7.addWidget(self.ctl_side_name_reset_pushButton, 3, 1, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_8, 2, 0, 1, 2)

        self.groupBox_9 = QGroupBox(self.name_rule_page)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout_9 = QGridLayout(self.groupBox_9)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label_18 = QLabel(self.groupBox_9)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_9.addWidget(self.label_18, 0, 0, 1, 1)

        self.l_jnt_side_name_lineEdit = QLineEdit(self.groupBox_9)
        self.l_jnt_side_name_lineEdit.setObjectName(u"l_jnt_side_name_lineEdit")
        self.l_jnt_side_name_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.l_jnt_side_name_lineEdit, 0, 1, 1, 1)

        self.label_19 = QLabel(self.groupBox_9)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_9.addWidget(self.label_19, 1, 0, 1, 1)

        self.r_jnt_side_name_lineEdit = QLineEdit(self.groupBox_9)
        self.r_jnt_side_name_lineEdit.setObjectName(u"r_jnt_side_name_lineEdit")
        self.r_jnt_side_name_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.r_jnt_side_name_lineEdit, 1, 1, 1, 1)

        self.label_20 = QLabel(self.groupBox_9)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_9.addWidget(self.label_20, 2, 0, 1, 1)

        self.c_jnt_side_name_lineEdit = QLineEdit(self.groupBox_9)
        self.c_jnt_side_name_lineEdit.setObjectName(u"c_jnt_side_name_lineEdit")
        self.c_jnt_side_name_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.c_jnt_side_name_lineEdit, 2, 1, 1, 1)

        self.jnt_side_name_reset_pushButton = QPushButton(self.groupBox_9)
        self.jnt_side_name_reset_pushButton.setObjectName(u"jnt_side_name_reset_pushButton")

        self.gridLayout_9.addWidget(self.jnt_side_name_reset_pushButton, 3, 1, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_9, 2, 2, 1, 1)

        self.groupBox_10 = QGroupBox(self.name_rule_page)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.formLayout_2 = QFormLayout(self.groupBox_10)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_21 = QLabel(self.groupBox_10)
        self.label_21.setObjectName(u"label_21")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_21)

        self.ctl_index_padding_spinBox = QSpinBox(self.groupBox_10)
        self.ctl_index_padding_spinBox.setObjectName(u"ctl_index_padding_spinBox")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.ctl_index_padding_spinBox)

        self.label_22 = QLabel(self.groupBox_10)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_22)

        self.jnt_index_padding_spinBox = QSpinBox(self.groupBox_10)
        self.jnt_index_padding_spinBox.setObjectName(u"jnt_index_padding_spinBox")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.jnt_index_padding_spinBox)

        self.index_padding_reset_pushButton = QPushButton(self.groupBox_10)
        self.index_padding_reset_pushButton.setObjectName(u"index_padding_reset_pushButton")

        self.formLayout_2.setWidget(2, QFormLayout.SpanningRole, self.index_padding_reset_pushButton)


        self.gridLayout_8.addWidget(self.groupBox_10, 3, 0, 1, 1)

        self.groupBox_11 = QGroupBox(self.name_rule_page)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.gridLayout_6 = QGridLayout(self.groupBox_11)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_23 = QLabel(self.groupBox_11)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_6.addWidget(self.label_23, 0, 0, 1, 1)

        self.ctl_extensions_name_lineEdit = QLineEdit(self.groupBox_11)
        self.ctl_extensions_name_lineEdit.setObjectName(u"ctl_extensions_name_lineEdit")
        self.ctl_extensions_name_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.ctl_extensions_name_lineEdit, 0, 1, 1, 1)

        self.label_24 = QLabel(self.groupBox_11)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_6.addWidget(self.label_24, 1, 0, 1, 1)

        self.jnt_extensions_name_lineEdit = QLineEdit(self.groupBox_11)
        self.jnt_extensions_name_lineEdit.setObjectName(u"jnt_extensions_name_lineEdit")
        self.jnt_extensions_name_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.jnt_extensions_name_lineEdit, 1, 1, 1, 1)

        self.extensions_name_reset_pushButton = QPushButton(self.groupBox_11)
        self.extensions_name_reset_pushButton.setObjectName(u"extensions_name_reset_pushButton")

        self.gridLayout_6.addWidget(self.extensions_name_reset_pushButton, 2, 1, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_11, 3, 1, 1, 2)

        self.verticalSpacer_4 = QSpacerItem(20, 52, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_4, 4, 1, 1, 1)

        self.toolBox.addItem(self.name_rule_page, u"Nameing Rule Settings")

        self.verticalLayout_3.addWidget(self.toolBox)


        self.retranslateUi(Dialog)

        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(4)
        self.mode_comboBox.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Rig Identifier", None))
        self.end_point_comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"all", None))
        self.end_point_comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"objects", None))
        self.end_point_comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"attributes", None))
        self.end_point_comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"operators", None))
        self.end_point_comboBox.setItemText(4, QCoreApplication.translate("Dialog", u"connections", None))
        self.end_point_comboBox.setItemText(5, QCoreApplication.translate("Dialog", u"cleanup", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Mode", None))
        self.mode_comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"DEBUG", None))
        self.mode_comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"WIP", None))
        self.mode_comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"PUB", None))

        self.label_12.setText(QCoreApplication.translate("Dialog", u"End Point", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Name", None))
        self.notes_textEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Publish note", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Ctl Settings", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Origin Ctl Size", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Origin Sub Ctl Count", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"Jnt Settings", None))
        self.force_uniform_scale_checkBox.setText(QCoreApplication.translate("Dialog", u"Force uniform scaling", None))
        self.connect_jnt_checkBox.setText(QCoreApplication.translate("Dialog", u"Use already exists joint", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Color Settings", None))
        self.left_color_ik_pushButton.setText("")
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Right", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Ik", None))
        self.right_color_ik_pushButton.setText("")
        self.left_color_fk_pushButton.setText("")
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Fk", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Left", None))
        self.center_color_fk_pushButton.setText("")
        self.center_color_ik_pushButton.setText("")
        self.right_color_fk_pushButton.setText("")
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Center", None))
        self.use_RGB_colors_checkBox.setText(QCoreApplication.translate("Dialog", u"Use RGB Colors", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.rig_page), QCoreApplication.translate("Dialog", u"Rig Settings", None))
        self.sub_pieces_new_pushButton.setText(QCoreApplication.translate("Dialog", u"New", None))

        __sortingEnabled = self.sub_pieces_listWidget.isSortingEnabled()
        self.sub_pieces_listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.sub_pieces_listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Dialog", u"objects", None));
        ___qlistwidgetitem1 = self.sub_pieces_listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Dialog", u"attributes", None));
        ___qlistwidgetitem2 = self.sub_pieces_listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Dialog", u"operators", None));
        ___qlistwidgetitem3 = self.sub_pieces_listWidget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Dialog", u"connections", None));
        ___qlistwidgetitem4 = self.sub_pieces_listWidget.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("Dialog", u"cleanup", None));
        self.sub_pieces_listWidget.setSortingEnabled(__sortingEnabled)

        self.sub_pieces_run_sel_pushButton.setText(QCoreApplication.translate("Dialog", u"Run. Sel", None))
        self.sub_pieces_add_pushButton.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.run_sub_pieces_checkBox.setText(QCoreApplication.translate("Dialog", u"Run sub pieces", None))
        self.sub_pieces_edit_pushButton.setText(QCoreApplication.translate("Dialog", u"Edit", None))
        self.sub_pieces_remove_pushButton.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.sub_piece_page), QCoreApplication.translate("Dialog", u"Sub Piece Settings", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Dialog", u"Controls Naming Rule", None))
        self.ctl_name_rule_reset_pushButton.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"{description} Letter Case", None))
        self.ctl_description_letter_case_comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"default", None))
        self.ctl_description_letter_case_comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"lower", None))
        self.ctl_description_letter_case_comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"upper", None))
        self.ctl_description_letter_case_comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"capitalize", None))

        self.groupBox_7.setTitle(QCoreApplication.translate("Dialog", u"Joints Naming Rule", None))
        self.jnt_name_rule_reset_pushButton.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"{description} Letter Case", None))
        self.jnt_description_letter_case_comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"default", None))
        self.jnt_description_letter_case_comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"lower", None))
        self.jnt_description_letter_case_comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"upper", None))
        self.jnt_description_letter_case_comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"capitalize", None))

        self.groupBox_8.setTitle(QCoreApplication.translate("Dialog", u"Controls Side Nameing", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Left", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Right", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Center", None))
        self.ctl_side_name_reset_pushButton.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Dialog", u"Joints Side Nameing", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Left", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Right", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Center", None))
        self.jnt_side_name_reset_pushButton.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Dialog", u"Index Padding", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Controls", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Joints", None))
        self.index_padding_reset_pushButton.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Dialog", u"Extensions Naming", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Controls", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"Joints", None))
        self.extensions_name_reset_pushButton.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.name_rule_page), QCoreApplication.translate("Dialog", u"Nameing Rule Settings", None))
    # retranslateUi

