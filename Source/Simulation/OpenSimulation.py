from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QFileDialog
)

import sys
import time
import sys
import json

import Common.Primitives as Primitives
from Common.Util import Vec2
import Common.Colors as Colors
import Simulation.AI as AI
import Simulator.SimulationCore as SimulationCore 

from Views.ui_sim import Ui_SimWindow

# from FloorPlanDesigner.openFPD import fpdWindowApp
import FloorPlanDesigner.openFPD as OpenFPD
import IntroWindow.openIntro as OpenIntro

class simWindowApp(QMainWindow, Ui_SimWindow):
    def __init__(self, parent=None):
        super(simWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.fpds = []
        self.oprs = []
        self.main = []
        self.shapes = []
        #MAKE SPEED VALUE HERE TODO
        self.SimSpeed = 1

    def drawShapes(self, qp):
        #Right now now everything is a rectangle TODO 
        for shape in self.shapes:
            # Eventually a check will need to be performed to see which shape it is, this is placeholder for that
            if type(shape) == Primitives.rectangle:
                # Render rectangle
                # Rectangle Fill
                qp.setBrush(Colors.GRAY)
                width = shape.maxCorner.x - shape.minCorner.x
                height = shape.maxCorner.y - shape.minCorner.y
                qp.drawRect(shape.minCorner.x, shape.minCorner.y, width, height)

    def paintEvent(self, e):
            qp = QPainter()
            qp.begin(self)
            self.drawShapes(qp)
            qp.end()

    # Create a worker class to run the simulation in a seperate thread
    class Worker(QObject):
        def __init__(self, parent):
            self.parent = parent
        finished = pyqtSignal()
        def run(self):
            """Simulation thread/run loop"""
            # Use the currently loaded floor plan?
            Sim = Simulation()
            while(True):
                # Read the simulation rate to control the run loop
                dT = self.parent.SimSpeed
                
                pass
            self.finished.emit()

    def openFPD(self):
        self.fpds.append(OpenFPD.fpdWindowApp())
        self.fpds[-1].show()

    def openMain(self):
        self.main.append(OpenIntro.mainWindowApp())
        self.main[-1].show()

    def beginSimulation(self):
        """Simulation initialization logic"""
        floorplanloaded = True #TODO figure out this check
        # Check to see if all values are valid for starting the simulation:
        if (floorplanloaded):
            # Create a QThread object
            self.thread = QThread()
            # Create a worker object
            self.worker = self.Worker(self)
            # Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            
            # Start the thread
            self.thread.start()

            self.SimulationButton.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.SimulationButton.setEnabled(True)
            )
            self.thread.finished.connect(
                lambda: self.SimulationButton.setText("Finished Simulation")
            )
        else:
            # Emit failure message because a condition was not met
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Simulation Parameter Invalid or Floor Plan not loaded")
            msg.setInformativeText('TMP, replace with informative information')
            msg.setWindowTitle("Error")
            msg.exec_()
            pass

    def loadFloorPlan(self):
        """
        Loads a floorplan from a file selected by the user using a file dialog.
        The floorplan is stored in a JSON file format.
        """
        opts = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Floorplan Designer - Load Floorplan",
            self.floorplansDir,
            "Floor Plan Designer Files (*.fpd)",
            options=opts,
        )
        if fileName:
            self.shapes = []
            with open(fileName, "r") as inFile:
                fp = json.load(inFile)

            for key in fp.keys():
                # The fact that there is a hard coded dimension like this hurts my soul
                x = int(int(fp[key]["x1"]) / 182)
                y = int(int(fp[key]["y1"]) / 182)
                w = int(int(fp[key]["width"]) / 182)
                h = int(int(fp[key]["height"]) / 182)
                furniture = fp[key]["furniture"] # What even is this parameter???
                # EVERYTHING IS A RECTANGLE YAY\s TODO
                # EVERYTHING IS AN INCLUSION YAY (eventually there will need to be a conditional on the isExclusion variable)
                isExclusion = False # TODO
                self.shapes.append(Primitives.Rectangle(Vec2(x,y),Vec2(x+w,y+h),isExclusion))    

    def connectButtons(self):
        self.BacktoMainButton.clicked.connect(self.openMain)
        self.EditFloorPlanButton.clicked.connect(self.openFPD)
        self.SimulationButton.clicked.connect(self.beginSimulation)
        self.LoadFloorPlanButton.clicked.connect(self.loadFloorPlan)
        # self.SimSpeedButton.clicked.connect()
        # self.VacuumLoadButton.clicked.connect()
        # self.VacuumSaveButton.clicked.connect()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = simWindowApp()
    win.show()
    app.exec()
