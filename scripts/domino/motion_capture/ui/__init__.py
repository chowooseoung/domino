# ui
from . import main

# domino
from domino.edition.api import utils


def show():
    utils.show_dialog(main.Mocap, parent=None)
