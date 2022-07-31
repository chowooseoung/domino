# domino
from domino_edition.ui import CommonPieceSettings

# gui
from PySide2 import QtCore


class Settings(CommonPieceSettings):
    title_name = "Shoulder_01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        self.resize_window()

    def resize_window(self):
        index = self.common_settings.toolBox.currentIndex()
        if index == 0:
            size = QtCore.QSize(370, 564)
            self.resize(size)
