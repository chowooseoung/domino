# domino
from domino_edition.api import naming

# built-ins
from functools import partial

# gui
from domino_edition.ui import (DominoDialog,
                               UiFunctionSet)
from . import (settings_ui,
               character_set_settings_ui)


class Settings(DominoDialog, settings_ui.Ui_Dialog):
    title_name = "Assembly Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)
        self.setupUi(self)
        self.ui_funcs = UiFunctionSet(ui=self)
        ui = self

        self.setObjectName("DominoAssemblySettings")
        self.visibilitySignal.connect(self.setup_window_title)
        self.resize(360, 730)
        ui.toolBox.currentChanged.connect(self.resize_window)

        self.ui_funcs.install_name_lineEdit(
            ui.rig_name_lineEdit,
            "name")
        self.ui_funcs.install_comboBox(
            ui.mode_comboBox,
            "mode")
        self.ui_funcs.install_comboBox(
            ui.end_point_comboBox,
            "end_point")
        self.ui_funcs.install_textEdit(
            ui.notes_textEdit,
            "publish_notes")

        self.ui_funcs.install_spinBox(
            ui.origin_sub_ctl_count_spinBox,
            "origin_sub_ctl_count")
        self.ui_funcs.install_spinBox(
            ui.origin_ctl_size_doubleSpinBox,
            "origin_ctl_size")

        self.ui_funcs.install_checkBox(
            ui.force_uniform_scale_checkBox,
            "force_uni_scale")
        self.ui_funcs.install_checkBox(
            ui.connect_jnt_checkBox,
            "connect_jnt_rig")

        self.ui_funcs.install_checkBox(
            ui.use_RGB_colors_checkBox,
            "use_RGB_colors")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.left_color_ik_pushButton,
            ui.left_color_ik_horizontalSlider,
            ui.left_color_ik_spinBox,
            "l_RGB_ik",
            "l_color_ik")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.left_color_fk_pushButton,
            ui.left_color_fk_horizontalSlider,
            ui.left_color_fk_spinBox,
            "l_RGB_fk",
            "l_color_fk")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.center_color_ik_pushButton,
            ui.center_color_ik_horizontalSlider,
            ui.center_color_ik_spinBox,
            "c_RGB_ik",
            "c_color_ik")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.center_color_fk_pushButton,
            ui.center_color_fk_horizontalSlider,
            ui.center_color_fk_spinBox,
            "c_RGB_fk",
            "c_color_fk")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.right_color_ik_pushButton,
            ui.right_color_ik_horizontalSlider,
            ui.right_color_ik_spinBox,
            "r_RGB_ik",
            "r_color_ik")
        self.ui_funcs.install_color_widgets(
            ui.use_RGB_colors_checkBox,
            ui.right_color_fk_pushButton,
            ui.right_color_fk_horizontalSlider,
            ui.right_color_fk_spinBox,
            "r_RGB_fk",
            "r_color_fk")

        self.ui_funcs.install_checkBox(
            ui.use_character_set_checkBox,
            "use_character_set")
        self.ui_funcs.install_lineEdit(
            ui.character_set_name_lineEdit,
            "character_set")

        self.ui_funcs.install_checkBox(
            ui.run_sub_pieces_checkBox,
            "run_sub_pieces")

        ui.ctl_name_rule_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    ["ctl_name_rule",
                     "ctl_description_letter_case"],
                    [naming.DEFAULT_NAMING_RULE,
                     "default"]))

        ui.jnt_name_rule_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    ['jnt_name_rule',
                     "jnt_description_letter_case"],
                    [naming.DEFAULT_NAMING_RULE,
                     "default"]))

        ui.ctl_side_name_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    ["ctl_left_name",
                     "ctl_right_name",
                     "ctl_center_name"],
                    [naming.DEFAULT_SIDE_L_NAME,
                     naming.DEFAULT_SIDE_R_NAME,
                     naming.DEFAULT_SIDE_C_NAME]))

        ui.jnt_side_name_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    ["jnt_left_name",
                     "jnt_right_name",
                     "jnt_center_name"],
                    [naming.DEFAULT_SIDE_L_NAME,
                     naming.DEFAULT_SIDE_R_NAME,
                     naming.DEFAULT_SIDE_C_NAME]))

        ui.index_padding_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    ["ctl_index_padding",
                     "jnt_index_padding"],
                    [naming.DEFAULT_CTL_INDEX_PADDING,
                     naming.DEFAULT_JNT_INDEX_PADDING]))

        ui.extensions_name_reset_pushButton.clicked.connect(
            partial(self.ui_funcs.reset_values,
                    ["ctl_name_ext",
                     "jnt_name_ext"],
                    [naming.DEFAULT_CTL_EXT_NAME,
                     naming.DEFAULT_JOINT_EXT_NAME]))

        self.ui_funcs.install_lineEdit(
            ui.ctl_name_rule_lineEdit,
            "ctl_name_rule")

        self.ui_funcs.install_lineEdit(
            ui.jnt_name_rule_lineEdit,
            "jnt_name_rule")

        self.ui_funcs.install_comboBox(
            ui.ctl_description_letter_case_comboBox,
            "ctl_description_letter_case")

        self.ui_funcs.install_comboBox(
            ui.jnt_description_letter_case_comboBox,
            "jnt_description_letter_case")

        self.ui_funcs.install_lineEdit(
            ui.l_ctl_side_name_lineEdit,
            "ctl_left_name")

        self.ui_funcs.install_lineEdit(
            ui.r_ctl_side_name_lineEdit,
            "ctl_right_name")

        self.ui_funcs.install_lineEdit(
            ui.c_ctl_side_name_lineEdit,
            "ctl_center_name")

        self.ui_funcs.install_lineEdit(
            ui.l_jnt_side_name_lineEdit,
            "jnt_left_name")

        self.ui_funcs.install_lineEdit(
            ui.r_jnt_side_name_lineEdit,
            "jnt_right_name")

        self.ui_funcs.install_lineEdit(
            ui.c_jnt_side_name_lineEdit,
            "jnt_center_name")

        self.ui_funcs.install_spinBox(
            ui.ctl_index_padding_spinBox,
            "ctl_index_padding")

        self.ui_funcs.install_spinBox(
            ui.jnt_index_padding_spinBox,
            "jnt_index_padding")

        self.ui_funcs.install_lineEdit(
            ui.ctl_extensions_name_lineEdit,
            "ctl_name_ext")

        self.ui_funcs.install_lineEdit(
            ui.jnt_extensions_name_lineEdit,
            "jnt_name_ext")

    def resize_window(self):
        return 0


class CharacterSetSettings(DominoDialog, character_set_settings_ui.Ui_Dialog):
    pass
