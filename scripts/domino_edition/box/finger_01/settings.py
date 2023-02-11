# domino
from domino_edition.ui import CommonPieceSettings

# gui


class Settings(CommonPieceSettings):
    title_name = "Finger 01 Settings"

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)

        self.resize_window()
