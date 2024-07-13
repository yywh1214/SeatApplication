import logging

from utils.constants import *
from utils.logger import get_log
from display.gui import GUI
from display.cli import CLI

log = get_log()


def main():
    log.debug("Current dir: {}".format(PROJECT_DIR))
    log.info("Main starting...")
    log.debug("Current display mode: {}".format(DISPLAY_MODE))
    log.info("Display creating...")
    if DISPLAY_MODE:
        display = GUI()
    else:
        display = CLI()
    log.info("Display create success!")
    log.info("Display starting...")
    display.start()
    log.info("Display start success!")
    log.info("Main file exited with 0")


if __name__ == "__main__":
    main()
