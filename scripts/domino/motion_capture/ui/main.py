# gui
from PySide2 import (QtWidgets, QtCore, QtGui)
from . import main_ui


class MocapUI(QtWidgets.QDialog, main_ui.Ui_Dialog):
    ui_name = "DominoMotionCaptureUI"

    def __init__(self, parent=None):
        super(MocapUI, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Domino Motion Capture")
        self.setObjectName(self.ui_name)


class Mocap(MocapUI):
    pass