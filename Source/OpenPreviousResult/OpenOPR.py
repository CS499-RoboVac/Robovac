from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
)
import sys
from Views.ui_opr import Ui_OPRWindow

# from FloorPlanDesigner.openFPD import fpdWindowApp
import FloorPlanDesigner.openFPD as OpenFPD
import IntroWindow.openIntro as OpenIntro


class oprWindowApp(QMainWindow, Ui_OPRWindow):
    def __init__(self, parent=None):
        super(oprWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.fpds = []
        self.sims = []
        self.main = []

    def openFPD(self):
        self.fpds.append(OpenFPD.fpdWindowApp())
        self.fpds[-1].show()

    def openMain(self):
        self.main.append(OpenIntro.mainWindowApp())
        self.main[-1].show()

    def connectButtons(self):
        self.BackButton.clicked.connect(self.openMain)
        # self.EditFloorPlanButton.clicked.connect(self.openFPD)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = simWindowApp()
    win.show()
    app.exec()
