# built-ins
import os
import logging


class Logger:

    logger = None
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s',
                                  "%y-%m-%d %H:%M:%S")

    @ classmethod
    def LOGGER(cls):
        if cls.logger is None:
            cls.logger = logging.getLogger("domino")
            cls.logger.propagate = False
            cls.DEBUG(False)

    @ classmethod
    def DEBUG(cls, status):
        if cls.logger:
            handlers = cls.logger.handlers.copy()
            [cls.logger.removeHandler(handle) for handle in handlers]

        cls.logger.setLevel(
            logging.DEBUG) if status else cls.logger.setLevel(logging.INFO)
        cls.logger.info("Set Debug Mode") if status else cls.logger.info(
            "Set Info Mode")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(cls.formatter)
        cls.logger.addHandler(stream_handler)

        if status is True:
            file_handler = logging.FileHandler(os.path.join(
                os.path.expanduser("~"), ".domino.log"))
            file_handler.setFormatter(cls.formatter)
            cls.logger.addHandler(file_handler)

    @ classmethod
    def info(cls, msg):
        cls.logger.info(msg)

    @ classmethod
    def warn(cls, msg):
        cls.logger.warn(msg)

    @ classmethod
    def warning(cls, msg):
        cls.logger.warning(msg)

    @ classmethod
    def error(cls, msg):
        cls.logger.error(msg)

    @ classmethod
    def critical(cls, msg):
        cls.logger.critical(msg)

    @ classmethod
    def debug(cls, msg):
        cls.logger.debug(msg)


Logger.LOGGER()
