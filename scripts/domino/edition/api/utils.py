# built-ins
import os
import sys
import json
import importlib.util

# domino
from ...core import log
from . import piece

# maya
from pymel import core as pm

# gui
from PySide2 import (QtWidgets,
                     QtCore)

DOMINO_DEFAULT_EDITION = "DOMINO_DEFAULT_EDITION"
DOMINO_CUSTOM_EDITION = "DOMINO_CUSTOM_EDITION"
DOMINO_TEMPLATE_DIR = "DOMINO_TEMPLATE_DIR"
DOMINO_SUB_PIECE_DIR = "DOMINO_SUB_PIECE_DIR"


def collect_piece(guide, rig, datas, include_assembly=False):
    modules = []
    argument = []
    if guide or rig:
        containers = []
        if guide:
            if include_assembly and guide not in pm.ls(assemblies=True):
                containers.append(pm.PyNode(guide).getParent(generations=-1))
            containers.extend(pm.ls(guide, dagObjects=True, type="dagContainer"))
        elif rig:
            containers = pm.listRelatives(rig, children=True, type="transform")
            containers = [x for x in containers if x.hasAttr("d_id")]
        for container in containers:
            module_name = container.attr("piece").get()
            modules.append(import_piece_module(module_name))
        argument.extend([{"node": n} for n in containers])
    elif datas:
        for data in datas:
            modules.append(import_piece_module(data["piece"]))
        argument.extend([{"data": data} for data in datas])

    pieces = []
    for index, mod in enumerate(modules):
        p = get_piece_attr(mod)
        if p is None:
            log.Logger.error(f"Empty Module {mod}")
            raise RuntimeError(f"{collect_piece.__name__!r}")
        pieces.append(p(**argument[index]))
    for p in pieces:
        p.ddata.parent = pieces
    return pieces


def register_editions():
    dir_name = os.path.dirname(__file__)
    os.environ[DOMINO_DEFAULT_EDITION] = os.path.join(dir_name, "..", "box")
    custom_edition_dir = os.getenv(DOMINO_CUSTOM_EDITION, None)
    if custom_edition_dir and custom_edition_dir not in sys.path:
        log.Logger.info(f"append custom edition path '{custom_edition_dir}'")
        sys.path.append(custom_edition_dir)
    if os.getenv(DOMINO_TEMPLATE_DIR, None) is None:
        os.environ[DOMINO_TEMPLATE_DIR] = os.path.normpath(os.path.join(dir_name, "..", "..", "..", "..", "templates"))


def import_piece_module(name):
    box_dir = "domino.edition.box"
    custom_dir = os.getenv(DOMINO_CUSTOM_EDITION, None)
    try:
        module = importlib.import_module(f"{box_dir}.{name}")
        importlib.reload(module)
    except ModuleNotFoundError:
        base_dir = None
        for d in os.listdir(custom_dir):
            if d == "__pycache__" or not os.path.isdir(os.path.join(custom_dir, d)):
                continue
            if name in os.listdir(os.path.join(custom_dir, d)):
                base_dir = d
            if base_dir:
                break
        try:
            module = importlib.import_module(f"{base_dir}.{name}")
            importlib.reload(module)
        except ModuleNotFoundError:
            raise ModuleNotFoundError(f"'{name}' don't exists")
    return module


def import_piece_settings(name):
    box_dir = "domino.edition.box"
    custom_dir = os.getenv(DOMINO_CUSTOM_EDITION, None)
    try:
        module = importlib.import_module(f"{box_dir}.{name}.settings")
        importlib.reload(module)
    except ModuleNotFoundError:
        base_dir = None
        for d in os.listdir(custom_dir):
            if d == "__pycache__" or not os.path.isdir(os.path.join(custom_dir, d)):
                continue
            if name in os.listdir(os.path.join(custom_dir, d)):
                base_dir = d
            if base_dir:
                break
        try:
            module = importlib.import_module(f"{base_dir}.{name}.settings")
            importlib.reload(module)
        except ModuleNotFoundError:
            raise ModuleNotFoundError(f"'{name}.settings' don't exists")
    return module.Settings


def reload_module(module):
    if module.__name__ in sys.modules:
        del sys.modules[module.__name__]
    sys.modules[module.__name__] = module


def get_piece_attr(mod):
    for attr in dir(mod):
        p = getattr(mod, attr)
        if type(p) == type(type):
            if issubclass(p, piece.AbstractPiece):
                return p


def import_dotfile(dotfile):
    with open(dotfile, "r") as f:
        data = json.load(f)
    return data


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
