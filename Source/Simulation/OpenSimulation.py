from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QRectF, QPointF
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush, QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QGraphicsPixmapItem, 
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QGraphicsItem,
    QMessageBox,
    QFileDialog,
)

import sys
import time
import json
import os
import Common.Primitives as Primitives
from Common.Util import Vec2
import Common.Colors as Colors
import Common.Robot as Robot
import Simulation.AI as AI
import numpy as np
import math

import Simulator.SimulationCore as SimulationCore

from Views.ui_sim import Ui_SimWindow

# from FloorPlanDesigner.openFPD import fpdWindowApp
import FloorPlanDesigner.openFPD as OpenFPD
import IntroWindow.openIntro as OpenIntro


class RectangleItem(QGraphicsItem):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = QRectF(x, y, width, height)
        self.x=x
        self.y=y
        self._brush = QBrush(QColor(200, 0, 0))

    def setBrush(self, brush):
        self._brush = brush
        self.update()
        
    def boundingRect(self):
        return self.rect

    def paint(self, painter=None, style=None, widget=None):
        painter.fillRect(self.rect, self._brush)

class DirtTile(RectangleItem):
    def __init__(self, x, y, IsDirty):
        TileSize = 1 #adjust here
        super().__init__(x, y, TileSize, TileSize)
        self.Dirtiness = 128*IsDirty
        self.setBrush(QBrush(QColor(100, 100, 100, self.Dirtiness)))

    def updateColor(self):
        self.setBrush(QBrush(QColor(100, 100, 100, self.Dirtiness)))


class CircleItem(QGraphicsItem):
    def __init__(self, x, y, radius):
        super().__init__()
        self.rect = QRectF(x - radius, y - radius, 2*radius, 2*radius)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setBrush(QColor(0, 0, 200))  # Set the fill color
        painter.drawEllipse(self.rect)

class RobotSprite(QGraphicsItem):
    def __init__(self, x, y, radius, wRadius, facing):
        super().__init__()
        self.radius = radius
        self.whiskerRadius = wRadius
        self.facing = facing

        self.x = x
        self.y = y

        self.rect = QRectF(x - radius, y - radius, 2*radius, 2*radius)
        self.whiskers = [QRectF(x - self.whiskerRadius, y - self.whiskerRadius, 2*self.whiskerRadius, 2*self.whiskerRadius) for wh in range(2)]
        pos = Vec2(self.x, self.y)
        for i, wh in enumerate(self.whiskers):
            p = pos + Vec2((-1)**i * self.radius*2/3, self.radius*2/3)
            wh.setRect(p.x - self.whiskerRadius, p.y - self.whiskerRadius, 2*self.whiskerRadius, 2*self.whiskerRadius)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

        self.setPos(100,100)


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.x = value.x()
            self.y = value.y()
        return super().itemChange(change, value)
        
    def boundingRect(self):
        return self.rect

    def updateRobot(self, robot):
        for i, wh in enumerate(robot.whiskers):
            center = robot.pos + wh.pos.turn(robot.facing)
            self.whiskers[i].moveCenter(QPointF(center.x,center.y))
            
        self.rect.moveCenter(QPointF(center.x, center.y))

    def updateDimensions(self):
        self.rect.setRect(self.x - self.radius, self.y - self.radius, 2*self.radius, 2*self.radius)
        pos = Vec2(self.x, self.y)
        for i, wh in enumerate(self.whiskers):
            p = pos + Vec2((-1)**i * self.radius*2/3, self.radius*2/3)
            wh.setRect(p.x - self.whiskerRadius, p.y - self.whiskerRadius, 2*self.whiskerRadius, 2*self.whiskerRadius)

    def paint(self, painter, option, widget):
        painter.setBrush(QColor(0, 150, 200))  # Set the fill color
        painter.drawEllipse(self.rect)
        painter.setBrush(QColor(255, 255, 255))
        for wh in self.whiskers:
            painter.drawEllipse(wh)


from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRectF

class simWindowApp(QMainWindow, Ui_SimWindow):
    def __init__(self, parent=None):
        super(simWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.fpds = []
        self.oprs = []
        self.main = []
        self.shapes = []
        self.dirtRender = None
        # MAKE SPEED VALUE HERE TODO
        self.SimSpeed = 1
        self.Robot = None
        self.RobotRenderObject = None
        self.dirt = None
        self.floorplansDir = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/Floor Plans/"
        )

        self.WhiskerSlide.setRange(1,10)
        self.WhiskerEffSlide.setRange(0,1)
        self.SpeedSlide.setRange(1,30)
        self.DiameterSlide.setRange(10,30)
        self.EfficiencySlide.setRange(0,1)
        

        self.graphicsView.scene = QGraphicsScene()
        self.graphicsView.setScene(self.graphicsView.scene)

    # Create a worker class to run the simulation in a seperate thread
    class Worker(QObject):
        finished = pyqtSignal()
        
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

        def run(self):
            """Simulation thread/run loop"""
            self.parent.robot = self.parent.InstanceRobot()
                    
            Sim = SimulationCore.Simulation(self.parent.shapes, self.parent.dirt, self.parent.InstanceAI(), self.parent.robot)

            MaxT = 5
            T=0
            while True:
                # Read the simulation rate to control the run loop
                T += 1/60 #flat internal assumed 60fps 
                Sim.update(1/60)
                if T>MaxT:
                    break
                time.sleep(1/60)
                self.parent.RobotRenderObject.updateRobot(self.parent.robot)
                self.parent.graphicsView.update()
                
            self.finished.emit()

    def robotSizeChange(self):
        if self.RobotRenderObject:
            self.RobotRenderObject.radius = self.DiameterSlide.value()/2
            self.RobotRenderObject.updateDimensions()
            self.graphicsView.update()

    def openFPD(self):
        self.fpds.append(OpenFPD.fpdWindowApp())
        self.fpds[-1].show()

    def openMain(self):
        self.main.append(OpenIntro.mainWindowApp())
        self.main[-1].show()

    def beginSimulation(self):
        """Simulation initialization logic"""
        # Check to see if all values are valid for starting the simulation:
        if len(self.shapes):
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
            self.thread.finished.connect(lambda: self.SimulationButton.setEnabled(True))
            self.thread.finished.connect(
                lambda: self.SimulationButton.setText("Finished Simulation")
            )
        else:
            # Emit failure message because a condition was not met
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Simulation Parameter Invalid or Floor Plan not loaded")
            msg.setInformativeText("TMP, replace with informative information")
            msg.setWindowTitle("Error")
            msg.exec_()
            pass

    def InstanceAI(self):
        textSelected = self.PathAlgorithmBox.currentText()
        if textSelected == "Random Bounce":
            return AI.RandomBounceAI(self.Robot)
        elif textSelected == "Random Walk":
            return AI.BiasedRandomAI(self.Robot)
        elif textSelected == "Snake":
            return AI.SnakeAI(self.Robot)
        else:
            return AI.SpiralAI(self.Robot)
    
    def InstanceRobot(self):
        p = self.RobotRenderObject.pos()
        return Robot.Robot(
            Vec2(p.x(), p.y()),
            0,
            diameter=self.DiameterSlide.value(),
            maxSpeed=self.SpeedSlide.value(),
            whisker_length=self.WhiskerSlide.value(),
            efficiency=self.EfficiencySlide.value(),
            whisker_eff=self.WhiskerEffSlide.value()
            )

    def BoundingBox(self):
        """returns bounds of the whole floorplan, as top-left and bottom-right Vec2s"""
        left = min(self.shapes, key=lambda s: s.BoundingBox()[0].x).BoundingBox()[0].x
        top = min(self.shapes, key=lambda s: s.BoundingBox()[0].y).BoundingBox()[0].y
        right = max(self.shapes, key=lambda s: s.BoundingBox()[1].x).BoundingBox()[1].x
        bottom = max(self.shapes, key=lambda s: s.BoundingBox()[1].y).BoundingBox()[1].y
        return (Vec2(left, top), Vec2(right, bottom))        
        
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

        sizeConversion = 182 # was 182

        if fileName:
            self.graphicsView.scene.clear()
            self.shapes = []
            with open(fileName, "r") as inFile:
                fp = json.load(inFile)

            for key in fp.keys():
                # The fact that there is a hard coded dimension like this hurts my soul
                x = int(int(fp[key]["x1"]) / sizeConversion)
                y = int(int(fp[key]["y1"]) / sizeConversion)
                w = int(int(fp[key]["width"]) / sizeConversion)
                h = int(int(fp[key]["height"]) / sizeConversion)
                furniture = fp[key]["furniture"]  # What even is this parameter???
                # EVERYTHING IS A RECTANGLE YAY\s TODO
                # EVERYTHING IS AN INCLUSION YAY (eventually there will need to be a conditional on the isExclusion variable)
                isExclusion = False  # TODO
                self.shapes.append(
                    Primitives.Rectangle(Vec2(x, y), Vec2(x + w, y + h), isExclusion)
                )
                # TODO deal with not rectangles for rendering
                # This renders the rectangle to the screen
                rect = RectangleItem(x, y, w, h)  # parameters are x, y, width, height
                # Add the rectangle to the scene
                self.graphicsView.scene.addItem(rect)
        
            # Initializes dirt 2D array, zeros are temporary
            
            tl, br = self.BoundingBox()
            self.dirt = np.zeros((math.ceil(abs(tl.x - br.x)), math.ceil(abs(tl.y - br.y))),dtype=np.uint8)
            
            # Generates dirt tile objects and puts them in the rendering window.
            for x in range(len(self.dirt)):
                for y in range(len(self.dirt[0])):
                    self.dirt[x, y] = Primitives.PrimitiveInclusion(self.shapes, Vec2(x, y)+tl)*128
                    # Create a QImage from the numpy array

            self.dirt = np.rot90(self.dirt)
            self.dirt = np.flipud(self.dirt)
            # Convert the 2D alpha_values array into a 3D array with 4 channels (RGBA)
            image_data = np.zeros((self.dirt.shape[0], self.dirt.shape[1], 4), dtype=np.uint8)

            image_data[..., 3] = self.dirt

            # Create a QImage from the numpy array
            image = QImage(image_data.data, image_data.shape[1], image_data.shape[0], QImage.Format_RGBA8888)

            # Create a QPixmap from the QImage
            pixmap = QPixmap.fromImage(image)

            # Create a QGraphicsPixmapItem from the QPixmap
            pixmap_item = QGraphicsPixmapItem(pixmap)
            pixmap_item.setPos(tl[0], tl[1])

            # Add the pixmap item to the scene
            self.graphicsView.scene.addItem(pixmap_item)
            self.RobotRenderObject = RobotSprite(0,0,16,4,0)
            self.graphicsView.scene.addItem(self.RobotRenderObject)

    
    def connectButtons(self):
        self.BacktoMainButton.clicked.connect(self.openMain)
        self.EditFloorPlanButton.clicked.connect(self.openFPD)
        self.SimulationButton.clicked.connect(self.beginSimulation)
        self.LoadFloorPlanButton.clicked.connect(self.loadFloorPlan)
        self.DiameterSlide.valueChanged.connect(self.robotSizeChange)
        self.WhiskerSlide.valueChanged.connect(self.robotSizeChange)
        # self.SimSpeedButton.clicked.connect()
        # self.VacuumLoadButton.clicked.connect()
        # self.VacuumSaveButton.clicked.connect()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = simWindowApp()
    win.show()
    app.exec()
