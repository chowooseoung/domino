# domino
from .core import log
from domino import menu
from domino.edition.api import utils as edition_utils
from domino.motion_capture.api import utils as motion_capture_utils

__version__ = [1, 0, 0]
__version_str__ = ". ".join([str(x) for x in __version__])


def install():
    log.Logger.info("Domino Installing...")

    edition_utils.register_editions()  # DOMINO_DEFAULT_EDITION, DOMINO_CUSTOM_EDITION, DOMINO_TEMPLATE_DIR
    motion_capture_utils.register_motion_capture()  #
    menu.install()
