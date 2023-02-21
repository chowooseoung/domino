# domino
from domino.edition.ui import CommonPieceSettings


class Settings(CommonPieceSettings):
    title_name = "Finger 02 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        self.resize_window()
