# built-ins
import os


DOMINO_MOTION_DIR = "DOMINO_MOTION_CAPTURE_DIR"


def register_motion_capture():
    dir_name = os.path.dirname(__file__)
    if os.getenv(DOMINO_MOTION_DIR, None) is None:
        os.environ[DOMINO_MOTION_DIR] = os.path.normpath(os.path.join(dir_name, "..", "..", "..", "..", "motioncapture"))
