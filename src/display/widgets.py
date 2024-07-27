from PyQt5 import QtCore, QtGui, QtWidgets
from utils import constants as cst


class ClickableLabel(QtWidgets.QLabel):
    def __init__(self, name: str, parent=None):
        """
        Initializes an instance of the class with the given name and parent widget.

        Parameters:
            name (str): The name of the widget.
            parent (QWidget, optional): The parent widget. Defaults to None.

        Returns:
            None
        """
        super().__init__(parent)
        self.setObjectName(name)
        self.setStyleSheet(
            "#%s{background-color: transparent;}" % name
        )

    def mousePressEvent(self, event):
        self.clicked.emit()

    clicked = QtCore.pyqtSignal()


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setupUi(self, name, title="default title", parent=None):
        self.main = QtWidgets.QWidget(parent)
        self.main.resize(1600, 900)
        self.main.setObjectName(name)
        self.back = ClickableLabel(self.main)
        self.back.setObjectName("back")
        self.back.setStyleSheet(
            "#back{border-image:url($MAIN)}".replace(
                "$MAIN", cst.BACK_BUTTON.replace("\\", "/")
            )
        )
        self.back.setGeometry(0, 0, *cst.BUTTON_SIZE)
        self.main.setWindowTitle(title)

    def close(self):
        super().close()


# TODO: title and other widgets
