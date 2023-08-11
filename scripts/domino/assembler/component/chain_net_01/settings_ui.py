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
        Form.resize(319, 198)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)

        self.blend_horizontalSlider = QSlider(self.groupBox)
        self.blend_horizontalSlider.setObjectName(u"blend_horizontalSlider")
        self.blend_horizontalSlider.setMaximum(100)
        self.blend_horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.blend_horizontalSlider, 2, 2, 1, 1)

        self.guide_orientation_checkBox = QCheckBox(self.groupBox)
        self.guide_orientation_checkBox.setObjectName(u"guide_orientation_checkBox")

        self.gridLayout.addWidget(self.guide_orientation_checkBox, 0, 0, 1, 3)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.blend_spinBox = QSpinBox(self.groupBox)
        self.blend_spinBox.setObjectName(u"blend_spinBox")
        self.blend_spinBox.setMaximum(100)

        self.gridLayout.addWidget(self.blend_spinBox, 2, 3, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)

        self.division_spinBox = QSpinBox(self.groupBox)
        self.division_spinBox.setObjectName(u"division_spinBox")
        self.division_spinBox.setMinimum(2)
        self.division_spinBox.setMaximum(999)

        self.gridLayout.addWidget(self.division_spinBox, 8, 2, 1, 2)

        self.degree_comboBox = QComboBox(self.groupBox)
        self.degree_comboBox.addItem("")
        self.degree_comboBox.addItem("")
        self.degree_comboBox.setObjectName(u"degree_comboBox")

        self.gridLayout.addWidget(self.degree_comboBox, 7, 2, 1, 2)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 1)

        self.master_a_lineEdit = QLineEdit(self.groupBox)
        self.master_a_lineEdit.setObjectName(u"master_a_lineEdit")

        self.gridLayout.addWidget(self.master_a_lineEdit, 5, 2, 1, 1)

        self.master_a_pushButton = QPushButton(self.groupBox)
        self.master_a_pushButton.setObjectName(u"master_a_pushButton")

        self.gridLayout.addWidget(self.master_a_pushButton, 5, 3, 1, 1)

        self.master_b_lineEdit = QLineEdit(self.groupBox)
        self.master_b_lineEdit.setObjectName(u"master_b_lineEdit")

        self.gridLayout.addWidget(self.master_b_lineEdit, 6, 2, 1, 1)

        self.master_b_pushButton = QPushButton(self.groupBox)
        self.master_b_pushButton.setObjectName(u"master_b_pushButton")

        self.gridLayout.addWidget(self.master_b_pushButton, 6, 3, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)
        self.blend_horizontalSlider.valueChanged.connect(self.blend_spinBox.setValue)
        self.blend_spinBox.valueChanged.connect(self.blend_horizontalSlider.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Master A", None))
        self.guide_orientation_checkBox.setText(QCoreApplication.translate("Form", u"Guide Orientation", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Master B", None))
        self.label.setText(QCoreApplication.translate("Form", u"Blend A/B", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Division", None))
        self.degree_comboBox.setItemText(0, QCoreApplication.translate("Form", u"1", None))
        self.degree_comboBox.setItemText(1, QCoreApplication.translate("Form", u"3", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"Degree", None))
        self.master_a_pushButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.master_b_pushButton.setText(QCoreApplication.translate("Form", u"Add", None))
    # retranslateUi

