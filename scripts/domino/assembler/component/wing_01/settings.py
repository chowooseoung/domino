# domino
from domino.assembler.ui import CommonComponentSettings

# gui
from PySide2 import QtWidgets, QtCore
from . import settings_ui


class IndividualSettings(QtWidgets.QWidget, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(IndividualSettings, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(CommonComponentSettings):
    title_name = "Wing 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui, "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_spinBox(
            ui.extrude_offset_doubleSpinBox,
            "extrude_offset")

        self.ui_funcs.install_curve_btn(
            ui.primary_curve1_comboBox,
            ui.primary_curve1_pushButton,
            "primary_curve1")
        self.ui_funcs.install_curve_btn(
            ui.primary_curve2_comboBox,
            ui.primary_curve2_pushButton,
            "primary_curve2")
        self.ui_funcs.install_curve_btn(
            ui.primary_coverts_curve1_comboBox,
            ui.primary_coverts_curve1_pushButton,
            "primary_coverts_curve1")
        self.ui_funcs.install_curve_btn(
            ui.primary_coverts_curve2_comboBox,
            ui.primary_coverts_curve2_pushButton,
            "primary_coverts_curve2")
        self.ui_funcs.install_curve_btn(
            ui.primary_under_coverts_curve1_comboBox,
            ui.primary_under_coverts_curve1_pushButton,
            "primary_under_coverts_curve1")
        self.ui_funcs.install_curve_btn(
            ui.primary_under_coverts_curve2_comboBox,
            ui.primary_under_coverts_curve2_pushButton,
            "primary_under_coverts_curve2")
        self.ui_funcs.install_curve_btn(
            ui.secondary_curve1_comboBox,
            ui.secondary_curve1_pushButton,
            "secondary_curve1")
        self.ui_funcs.install_curve_btn(
            ui.secondary_curve2_comboBox,
            ui.secondary_curve2_pushButton,
            "secondary_curve2")
        self.ui_funcs.install_curve_btn(
            ui.secondary_coverts_curve1_comboBox,
            ui.secondary_coverts_curve1_pushButton,
            "secondary_coverts_curve1")
        self.ui_funcs.install_curve_btn(
            ui.secondary_coverts_curve2_comboBox,
            ui.secondary_coverts_curve2_pushButton,
            "secondary_coverts_curve2")
        self.ui_funcs.install_curve_btn(
            ui.secondary_under_coverts_curve1_comboBox,
            ui.secondary_under_coverts_curve1_pushButton,
            "secondary_under_coverts_curve1")
        self.ui_funcs.install_curve_btn(
            ui.secondary_under_coverts_curve2_comboBox,
            ui.secondary_under_coverts_curve2_pushButton,
            "secondary_under_coverts_curve2")
        self.ui_funcs.install_curve_btn(
            ui.tertiary_curve1_comboBox,
            ui.tertiary_curve1_pushButton,
            "tertiary_curve1")
        self.ui_funcs.install_curve_btn(
            ui.tertiary_curve2_comboBox,
            ui.tertiary_curve2_pushButton,
            "tertiary_curve2")

    def resize_window(self):
        super(Settings, self).resize_window()
        index = self.common_settings.toolBox.currentIndex()
        if index == 1:
            size = QtCore.QSize(440, 580)
            self.resize(size)
