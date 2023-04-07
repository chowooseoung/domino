# domino
from domino.assembler.ui import CommonComponentSettings

# gui
from PySide2 import QtCore


class Settings(CommonComponentSettings):
    title_name = "Clavicle_01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        self.resize_window()
