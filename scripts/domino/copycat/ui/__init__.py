# ui
from . import main

# domino
from domino.lib import utils


def open_ui():
    utils.show_dialog(main.CopyCat, parent=None)
