import utils.constants
import utils.core
from utils.logger import get_log

log = get_log()


class CLI:
    """The CLI display class."""

    def __init__(self):
        pass

    def start(self):
        """The main function to start the CLI display."""
        log.info("Starting CLI display...")
        utils.core.rdesk()
