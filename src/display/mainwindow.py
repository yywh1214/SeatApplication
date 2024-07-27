import os
from PyQt5 import QtWidgets, QtCore

from utils.constants import *
from utils.logger import get_log
from display.widgets import ClickableLabel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.logger = get_log()
        super().__init__()
        self.setupUi("main")
        self.logger.info("Showing main window...")
        self.show()

    def setupUi(self, name):
        self.main = QtWidgets.QWidget()
        self.main.resize(1600, 900)
        self.main.setObjectName(name)
        self.main.setWindowTitle("Seat Application")
        self.logger.debug(f"current dir: {os.getcwd()}")
        self.logger.debug(f"opening {BACKGROUND_PICTURE}")
        self.main.setStyleSheet(
            "#main{border-image:url($MAIN)}".replace(
                "$MAIN", BACKGROUND_PICTURE
            )
        )
        self.logger.info(f"Creating labels...")
        # TODO: create labels with a dict
        raise NotImplementedError
        self.main.show()
