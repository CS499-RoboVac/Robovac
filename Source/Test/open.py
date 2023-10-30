from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QGraphicsView,
    QGraphicsScene
)
import sys


# switch new2/new/window as needed 
# new2 added sensible sizing to graphic view and fixed size to vertical menu
import new2 as windows

class simWindowApp(QMainWindow, windows.Ui_MainWindow):
    def __init__(self, parent=None):
        super(simWindowApp, self).__init__(parent)
        self.setupUi(self)

    
    
        # self.SimulationButton.clicked.connect()
        # self.LoadFloorPlanButton.clicked.connect()
        # self.SimSpeedButton.clicked.connect()
        # self.VacuumLoadButton.clicked.connect()
        # self.VacuumSaveButton.clicked.connect()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = simWindowApp()
    win.show()
    app.exec()