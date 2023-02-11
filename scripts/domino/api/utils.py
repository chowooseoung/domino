# built-ins
import sys

# domino
from . import log


def reload_domino():
    """reload domino module 
    """
    for mod in sys.modules.copy():
        if mod.startswith("domino"):
            log.Logger.info("[{}.{}] Removing '{}'".format(
                __name__, sys._getframe().f_code.co_name, sys.modules[mod]))
            del sys.modules[mod]


def valid():
    """Maya Rigging Scene valid check for publish
    1. naming
    2. sets
    3. modeling version[options]
    """
    pass