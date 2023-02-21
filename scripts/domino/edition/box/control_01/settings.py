# domino
from domino.edition.ui import CommonPieceSettings

# gui
from PySide2 import QtWidgets
from . import settings_ui


class IndividualSettings(QtWidgets.QWidget, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(IndividualSettings, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(CommonPieceSettings):
    title_name = "Control_01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        ui = IndividualSettings(self.common_settings)
        self.common_settings.toolBox.addItem(ui,
                                             "Individual Settings")
        self.resize_window()

        self.ui_funcs.install_checkBox(
            ui.nothing_checkBox,
            "nothing")
        self.ui_funcs.install_checkBox(
            ui.joint_checkBox,
            "jnt_rig")
        self.ui_funcs.install_checkBox(
            ui.leaf_joint_checkBox,
            "leaf_jnt")
        self.ui_funcs.install_checkBox(
            ui.uni_scale_checkBox,
            "uni_scale")
        self.ui_funcs.install_checkBox(
            ui.neutral_rotation_checkBox,
            "neutral_rotation")
        self.ui_funcs.install_checkBox(
            ui.mirror_behaviour_checkBox,
            "mirror_behaviour")
        self.ui_funcs.install_spinBox(
            ui.ctl_size_doubleSpinBox,
            "ctl_size")
        self.ui_funcs.install_comboBox(
            ui.icon_comboBox,
            "icon")

        self.ui_funcs.install_checkBox(
            ui.tx_checkBox,
            "k_tx")
        self.ui_funcs.install_checkBox(
            ui.ty_checkBox,
            "k_ty")
        self.ui_funcs.install_checkBox(
            ui.tz_checkBox,
            "k_tz")
        self.ui_funcs.install_checkBox(
            ui.rx_checkBox,
            "k_rx")
        self.ui_funcs.install_checkBox(
            ui.ry_checkBox,
            "k_ry")
        self.ui_funcs.install_checkBox(
            ui.rz_checkBox,
            "k_rz")
        self.ui_funcs.install_checkBox(
            ui.ro_checkBox,
            "k_ro")
        self.ui_funcs.install_checkBox(
            ui.sx_checkBox,
            "k_sx")
        self.ui_funcs.install_checkBox(
            ui.sy_checkBox,
            "k_sy")
        self.ui_funcs.install_checkBox(
            ui.sz_checkBox,
            "k_sz")
        self.ui_funcs.install_comboBox(
            ui.ro_comboBox,
            "default_rotate_order")

        self.ui_funcs.install_space_switch_listWidget(
            ui.listWidget,
            ui.add_pushButton,
            ui.remove_pushButton,
            "space_switch_array")

        self.ui_funcs.install_checkBox_toggle_pushButton(
            ui.translate_pushButton,
            [ui.tx_checkBox, ui.ty_checkBox, ui.tz_checkBox])
        self.ui_funcs.install_checkBox_toggle_pushButton(
            ui.rotate_pushButton,
            [ui.rx_checkBox, ui.ry_checkBox, ui.rz_checkBox, ui.ro_checkBox])
        self.ui_funcs.install_checkBox_toggle_pushButton(
            ui.scale_pushButton,
            [ui.sx_checkBox, ui.sy_checkBox, ui.sz_checkBox])
