# built-ins
import sys

# domino
from . import log

# gui
from PySide2 import QtWidgets, QtCore


def reload_domino():
    for mod in sys.modules.copy():
        if mod.startswith("domino"):
            log.Logger.info("[{}.{}] Removing '{}'".format(__name__, sys._getframe().f_code.co_name, sys.modules[mod]))
            del sys.modules[mod]


def reload_module(module):
    if module.__name__ in sys.modules:
        del sys.modules[module.__name__]
    sys.modules[module.__name__] = module


def getMayaMainWindow():
    # get the qApp instance if it exists.
    app = QtWidgets.QApplication.instance()
    mayaWin = next(w for w in app.topLevelWidgets() if w.objectName() == 'MayaWindow')
    return app, mayaWin


def show_dialog(ui, parent, *args, **kwargs):
    app, maya_window = getMayaMainWindow()
    try:
        for c in maya_window.children():
            if isinstance(c, ui):
                c.deleteLater()
    except Exception:
        pass
    if not parent:
        parent = maya_window

    win = ui(parent=parent, *args, **kwargs)
    desktop = app.desktop()
    screen = desktop.screenNumber(desktop.cursor().pos())
    screen_center = desktop.screenGeometry(screen).center()

    win.show()
    win_center = win.rect().center()
    win.move(QtCore.QPoint(desktop.cursor().pos().x(),
                           (screen_center - win_center).y()))
