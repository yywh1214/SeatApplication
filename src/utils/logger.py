import yaml
import logging.config
import os

from utils.constants import *


def setup_logging(
    default_path: str = LOGGING_SETTINGS,
    default_level: int = logging.INFO,
    env_key: str = "LOG_CFG",
):
    """Setup logging configuration.

    Args:
        default_path (str, optional): The path to log files. Defaults to LOGGING_SETTINGS.
        default_level (int, optional): The level of the log. Defaults to logging.INFO.
        env_key (str, optional): The enviroment var for your settings. Defaults to "LOG_CFG".
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get_log(**kwargs):
    """Create a logger with specified settings.

    Returns:
        logging.Logger: The logger object you can use.
    """
    logger = logging.getLogger(__name__)
    if DEBUG:
        setup_logging(default_level=logging.DEBUG, **kwargs)
        logger.setLevel(logging.DEBUG)
    else:
        setup_logging(**kwargs)
    return logger


if __name__ == "__main__":
    setup_logging()
