# ui
from . import main

# domino
from domino.edition.api import utils


def open_ui():
    utils.show_dialog(main.Imitator, parent=None)
