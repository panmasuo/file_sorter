import logging

# configure logging before anything else
logging.basicConfig(
    filename="logs.log",
    filemode='a',
    level=logging.DEBUG,
    format="[%(levelname)s %(name)s:%(lineno)d] [%(thread)d] %(message)s"
)

# imports for loggers
from exif._image import logger as exif_logger
from hachoir.core import config as hachor_config
from hachoir.core.log import Logger as hachoir_logger

hachor_config.quiet = True  # suppress hachoir log messages
hachoir_logger.error = hachoir_logger.info  # monkey patch the error function

exif_logger.setLevel(logging.CRITICAL)  # suppress exif log messages
