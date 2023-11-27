from PyQt5 import QtCore, QtGui, QtWidgets, QtTest

from PyQt5.QtCore import QObject, QThread, pyqtSignal, QRectF, QPointF
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush, QImage, QPixmap

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsEllipseItem,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QGraphicsItem,
    QMessageBox,
    QGraphicsView,
    QFileDialog,
)
import sys
import time
import datetime
import json
import os
import Common.Primitives as Primitives
from Common.Util import Vec2
import Common.Colors as Colors

import Common.Robot as Robot
import Simulation.AI as AI
import numpy as np
import math
import shutil
import matplotlib.pyplot as plt


import Simulator.SimulationCore as SimulationCore


from Views.ui_sim import Ui_SimWindow

# from FloorPlanDesigner.openFPD import fpdWindowApp
import FloorPlanDesigner.openFPD as OpenFPD
import IntroWindow.openIntro as OpenIntro


class RectangleItem(QGraphicsItem):
    def __init__(self, x, y, width, height, isRoom):
        super().__init__()
        self.rect = QRectF(x, y, width, height)

        self.x = x
        self.y = y
        self._brush = QBrush(QColor(230, 255, 230) if isRoom else QColor(255, 100, 100))

    def setBrush(self, brush):
        self._brush = brush
        self.update()

    def boundingRect(self):
        return self.rect

    def paint(self, painter=None, style=None, widget=None):
        painter.fillRect(self.rect, self._brush)


class CircleItem(QGraphicsItem):
    def __init__(self, x, y, radius):
        super().__init__()
        self.rect = QRectF(x - radius, y - radius, 2 * radius, 2 * radius)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setBrush(QColor(0, 0, 200))  # Set the fill color
        painter.drawEllipse(self.rect)


class RobotSprite(QGraphicsItem):
    def __init__(self, x, y, radius, wRadius, facing, parent=None):
        super(RobotSprite, self).__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

        # Create three QGraphicsEllipseItems as child items
        self.center_circle = QGraphicsEllipseItem(0, 0, 2 * radius, 2 * radius, self)
        self.center_circle.setPos(-radius, -radius)
        l = (2 / 3) * radius - wRadius

        g = (2 / 3) * radius + wRadius
        self.left_circle = QGraphicsEllipseItem(0, 0, 2 * wRadius, 2 * wRadius, self)
        self.left_circle.setPos(-g, l)
        self.right_circle = QGraphicsEllipseItem(0, 0, 2 * wRadius, 2 * wRadius, self)
        self.right_circle.setPos(l, l)
        self.setRotation(facing)
        self.center_circle.setBrush(QColor(0, 0, 255))
        self.left_circle.setBrush(QColor(0, 0, 255))
        self.right_circle.setBrush(QColor(0, 0, 255))

    def paint(self, painter, option, widget):
        pass

    def boundingRect(self):
        # Return a QRectF that contains all child items
        return self.childrenBoundingRect()

    def setRadius(self, radius, wRadius):
        # Set the radius of the circles
        self.center_circle.setRect(0, 0, 2 * radius, 2 * radius)
        self.center_circle.setPos(-radius, -radius)
        l = (2 / 3) * radius - wRadius
        g = (2 / 3) * radius + wRadius
        self.left_circle.setRect(0, 0, 2 * wRadius, 2 * wRadius)
        self.left_circle.setPos(-g, l)
        self.right_circle.setRect(-0, 0, 2 * wRadius, 2 * wRadius)
        self.right_circle.setPos(l, l)


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

        self.simSpeedOptions = [1, 5, 50]
        self.simSpeedIndex = 0
        self.SimSpeed = 1
        self.Robot = None
        self.RobotRenderObject = None
        self.dirtRenderObject = None
        self.maxT = 30
        self.simulationRunning = False

        self.fileName = None

        self.dirt = None
        self.StartDirt = 0
        self.floorplansDir = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/Floor Plans/"
        )
        self.lastRunsDir = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Old Runs/"
        )

        self.graphicsView.scene = QGraphicsScene()
        self.graphicsView.setScene(self.graphicsView.scene)

        self.robotSizeChange()
        self.sliderChange()

    # Create a worker class to run the simulation in a seperate thread
    class Worker(QObject):
        finished = pyqtSignal()
        frameUpdated = pyqtSignal(float)
        simulationError = pyqtSignal()

        def __init__(self, parent):
            super().__init__()
            self.parent = parent

        def run(self):
            """Simulation thread/run loop"""
            self.parent.Robot = self.parent.InstanceRobot()
            Sim = None

            # If there are invalid parameters it ends the thread and emits a warning
            try:
                tl, br = self.parent.BoundingBox()
                Sim = SimulationCore.Simulation(
                    self.parent.shapes,
                    self.parent.dirt,
                    self.parent.InstanceAI(),
                    self.parent.Robot,
                    tl,
                )
            except RuntimeError:
                self.simulationError.emit()
                self.finished.emit()
                return
            T = 0
            # Render Update Ideal Framerate
            dT = 1 / 60
            lastTime = time.time()

            lastSimTime = time.time()
            while self.parent.simulationRunning:
                if (time.time() - lastSimTime) > (1 / (20 * self.parent.SimSpeed)):
                    # Read the simulation rate to control the run loop
                    T += (
                        1 / 20
                    )  # flat internal assumed 60 simulation steps per simulation second
                    Sim.update(1 / 20)
                    if T > self.parent.maxT:
                        break
                    lastSimTime = time.time()

                if (time.time() - lastTime) > dT:
                    lastTime = time.time()
                    self.frameUpdated.emit(T)

            self.finished.emit()

    def robotSizeChange(self):
        if self.RobotRenderObject:
            self.RobotRenderObject.radius = self.DiameterSlide.value() / 2
            self.RobotRenderObject.setRadius(
                self.DiameterSlide.value() * 0.254 / 2,
                self.WhiskerSlide.value() * 0.254 / 2,
            )

    def sliderChange(self):
        self.Stat_Diameter.setText(
            "{} in ({:.2f} cm)".format(
                self.DiameterSlide.value() / 10, self.DiameterSlide.value() * 0.254
            )
        )
        self.Stat_VacuumWidth.setText(
            "{} in ({:.2f} cm)".format(
                self.VacWidthSlide.value() / 10, self.VacWidthSlide.value() * 0.254
            )
        )
        self.Stat_VacEff.setText("{}%".format(self.EfficiencySlide.value()))
        self.Stat_Whisker.setText(
            "{} in ({:.2f} cm)".format(
                self.WhiskerSlide.value() / 10, self.WhiskerSlide.value() * 0.254
            )
        )
        self.Stat_WhiskerEfficiency.setText("{}%".format(self.WhiskerEffSlide.value()))
        self.Stat_Speed.setText(
            "{} in/s ({:.2f} cm)".format(
                self.SpeedSlide.value(), self.SpeedSlide.value() * 2.54
            )
        )
        self.Stat_BatteryLife.setText("{} min".format(self.BatteryLifeSlide.value()))

        self.maxT = self.BatteryLifeSlide.value() * 60

    def loadVacuum(self):
        """
        Loads a vacuum from a file selected by the user using a file dialog.
        The vacuum is stored in a JSON file format.
        """
        opts = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Robot Settings - Save Robot",
            self.floorplansDir,
            "Robot settings file (*.rbt)",
            options=opts,
        )
        # TODO load diameter and vac width seperately
        if fileName:
            with open(fileName, "r") as inFile:
                fp = json.load(inFile)
                self.SpeedSlide.setValue(fp[0]),
                self.WhiskerSlide.setValue(fp[1]),
                self.DiameterSlide.setValue(fp[2]),
                self.EfficiencySlide.setValue(fp[3]),
                self.BatteryLifeSlide.setValue(fp[4]),
                self.WhiskerEffSlide.setValue(fp[5])

    def saveVacuum(self):
        opts = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Robot Settings - Save Robot",
            self.floorplansDir,
            "Robot settings file (*.rbt)",
            options=opts,
        )
        if fileName:
            if ".rbt" not in fileName:
                fileName = fileName + ".rbt"
            fp = [
                self.SpeedSlide.value(),
                self.WhiskerSlide.value(),
                self.DiameterSlide.value(),
                self.EfficiencySlide.value(),
                self.BatteryLifeSlide.value(),
                self.WhiskerEffSlide.value(),
            ]

            jsonObj = json.dumps(fp)
            with open(fileName, "w") as outFile:
                outFile.write(jsonObj)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error Saving Robot File")
            msg.setWindowTitle("Save Error")
            msg.exec_()

    def simSpeedChange(self):
        self.simSpeedIndex = (self.simSpeedIndex + 1) % len(self.simSpeedOptions)
        self.SimSpeed = self.simSpeedOptions[self.simSpeedIndex]
        self.SimSpeedButton.setText(str(self.SimSpeed) + "x")

    def updateFrame(self, T):
        tl, br = self.BoundingBox()
        self.RobotRenderObject.setPos(
            self.Robot.pos[0] + tl.x, self.Robot.pos[1] + tl.y
        )
        self.RobotRenderObject.setRotation((self.Robot.facing * 180) / math.pi)
        self.dirtRenderObject.setPixmap(self.getDirtPixmap())
        h = int(T / 3600)
        m = int(T / 60) % 60
        s = int(T) % 60
        # Adds leading zeros, there is probably a better way of doing this TODO
        htext = "0" + str(h) if h < 10 else str(h)
        mtext = "0" + str(m) if m < 10 else str(m)
        stext = "0" + str(s) if s < 10 else str(s)

        self.Stat_SimulationTime.setText(htext + ":" + mtext + ":" + stext)

    def simulateErrorMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Sorry! It looks like you can't put the Robot there")
        msg.setInformativeText(
            "The robot has to be in a room, and not on a piece of furniture"
        )
        msg.setWindowTitle("Error")
        msg.exec_()

    def openFPD(self):
        self.fpds.append(OpenFPD.fpdWindowApp())
        self.fpds[-1].show()

    def openMain(self):
        self.main.append(OpenIntro.mainWindowApp())
        self.main[-1].show()

    def completeMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Simulation Complete")
        msg.setInformativeText(
            f'Simulation at {datetime.datetime.now()}\n\tUsing Algorithm {self.PathAlgorithmBox.currentText()}\n\tOn floorplan "{self.fileName}"\n\tWith floor type {self.FloorTypeBox.currentText()}\n\tTotal Percentage cleaned: {100 * round(1-(np.sum(self.dirt)/self.StartDirt), 2)}%\n\tFinal duration {self.Stat_SimulationTime.text()}'
        )
        msg.setWindowTitle("Simulation Comlete")
        # Create a button and add it to the message box
        button = QPushButton("Save Run")
        msg.addButton(button, QMessageBox.AcceptRole)

        # Connect a function to the button's clicked signal
        button.clicked.connect(self.saveRun)
        msg.exec_()

    def beginSimulation(self):
        if self.simulationRunning:
            self.simulationRunning = False
            self.SimulationButton.setText("Simulate")
        else:
            """Simulation initialization logic"""
            # Check to see if all values are valid for starting the simulation:
            if len(self.shapes):
                tl, br = self.BoundingBox()
                self.dirt = np.zeros(
                    (math.ceil(abs(tl.x - br.x)), math.ceil(abs(tl.y - br.y))),
                    dtype=np.uint8,
                )

                # Generates dirt tile objects and puts them in the rendering window.
                for x in range(len(self.dirt)):
                    for y in range(len(self.dirt[0])):
                        self.dirt[x, y] = (
                            Primitives.PrimitiveInclusion(self.shapes, Vec2(x, y) + tl)
                            * 200
                        )
                        # CreatSe a QImage from the numpy array
                self.dirt = np.rot90(self.dirt)
                self.dirt = np.flipud(self.dirt)
                # Create a QThread object
                self.thread = QThread()
                # Create a worker object
                self.worker = self.Worker(self)
                # Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.completeMessage)

                self.worker.frameUpdated.connect(self.updateFrame)
                self.worker.simulationError.connect(self.simulateErrorMessage)

                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)

                # Start the thread
                self.thread.start()
                self.simulationRunning = True
                self.SimulationButton.setText("Stop Simulation")
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
                msg.setInformativeText("Make sure you have a floor plan loaded")
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
        tl, br = self.BoundingBox()
        p = self.RobotRenderObject.pos()
        return Robot.Robot(
            Vec2(p.x() - tl.x, p.y() - tl.y),
            0,
            diameter=self.DiameterSlide.value() * 0.254,
            maxSpeed=self.SpeedSlide.value() * 2.54,
            whisker_length=self.WhiskerSlide.value() * 0.254,
            efficiency=self.EfficiencySlide.value() / 100,
            whisker_eff=self.WhiskerEffSlide.value() / 100,
            vaccum_width=self.VacWidthSlide.value() * 0.254,
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

        sizeConversion = 182  # was 182

        if fileName:
            self.graphicsView.scene.clear()
            self.shapes = []
            with open(fileName, "r") as inFile:
                fp = json.load(inFile)
                for item in fp:
                    # Read the values from the JSON file
                    x = int(item["x1"])
                    y = int(item["y1"])
                    w = int(item["width"])
                    h = int(item["height"])

                    # If it is a room, add it to the list of shapes as an inclusion primitive
                    # If it is a or another type for furniture, add it to the list of shapes as an exclusion primitive
                    if item["type"] == "Room":
                        self.shapes.append(
                            Primitives.Rectangle(Vec2(x, y), Vec2(x + w, y + h), False)
                        )
                    else:
                        self.shapes.append(
                            Primitives.Rectangle(Vec2(x, y), Vec2(x + w, y + h), True)
                        )
                    # TODO deal with not rectangles for rendering
                    # This renders the rectangle to the screen
                    rect = RectangleItem(
                        x, y, w, h, item["type"] == "Room"
                    )  # parameters are x, y, width, height
                    if item["type"] != "Room":
                        rect.setZValue(2)
                    # Add the rectangle to the scene
                    self.graphicsView.scene.addItem(rect)

            # Initializes dirt 2D array, zeros are temporary

            tl, br = self.BoundingBox()
            self.dirt = np.zeros(
                (math.ceil(abs(tl.x - br.x)), math.ceil(abs(tl.y - br.y))),
                dtype=np.uint8,
            )

            # Generates dirt tile objects and puts them in the rendering window.
            for x in range(len(self.dirt)):
                for y in range(len(self.dirt[0])):
                    self.dirt[x, y] = (
                        Primitives.PrimitiveInclusion(self.shapes, Vec2(x, y) + tl)
                        * 200
                    )
                    # CreatSe a QImage from the numpy array
            self.StartDirt = np.sum(self.dirt)
            self.dirt = np.rot90(self.dirt)
            self.dirt = np.flipud(self.dirt)
            # Create a QGraphicsPixmapItem from the QPixmap
            pixmap_item = QGraphicsPixmapItem(self.getDirtPixmap())
            pixmap_item.setPos(tl[0], tl[1])
            # Add the pixmap item to the scene
            self.dirtRenderObject = pixmap_item
            self.graphicsView.scene.addItem(self.dirtRenderObject)
            self.RobotRenderObject = RobotSprite(0, 0, 16, 4, 0)
            self.graphicsView.scene.addItem(self.RobotRenderObject)
            self.robotSizeChange()
            self.fileName = fileName

    def getDirtPixmap(self):
        # Convert the 2D alpha_values array into a 3D array with 4 channels (RGBA)
        image_data = np.zeros(
            (self.dirt.shape[0], self.dirt.shape[1], 4), dtype=np.uint8
        )

        image_data[..., 3] = self.dirt

        # Create a QImage from the numpy array
        image = QImage(
            image_data.data,
            image_data.shape[1],
            image_data.shape[0],
            QImage.Format_RGBA8888,
        )

        # Create a QPixmap from the QImage
        pixmap = QPixmap.fromImage(image)
        return pixmap

    def connectButtons(self):
        # self.BacktoMainButton.clicked.connect(self.openMain)
        # self.EditFloorPlanButton.clicked.connect(self.openFPD)
        self.SimulationButton.clicked.connect(self.beginSimulation)
        self.LoadFloorPlanButton.clicked.connect(self.loadFloorPlan)

        self.DiameterSlide.valueChanged.connect(self.robotSizeChange)
        self.WhiskerSlide.valueChanged.connect(self.robotSizeChange)

        self.DiameterSlide.valueChanged.connect(self.sliderChange)
        self.VacWidthSlide.valueChanged.connect(self.sliderChange)
        self.EfficiencySlide.valueChanged.connect(self.sliderChange)
        self.WhiskerSlide.valueChanged.connect(self.sliderChange)
        self.WhiskerEffSlide.valueChanged.connect(self.sliderChange)
        self.SpeedSlide.valueChanged.connect(self.sliderChange)
        self.BatteryLifeSlide.valueChanged.connect(self.sliderChange)

        self.VacuumLoadButton.clicked.connect(self.loadVacuum)
        self.VacuumSaveButton.clicked.connect(self.saveVacuum)
        self.SimSpeedButton.clicked.connect(self.simSpeedChange)

        # self.SimSpeedButton.clicked.connect()
        # self.VacuumLoadButton.clicked.connect()
        # self.VacuumSaveButton.clicked.connect()

    def getWindowImage(self):
        view = QGraphicsView(self.graphicsView.scene)

        # Render the scene to a QImage
        image = QImage(view.viewport().size(), QImage.Format_ARGB32)
        painter = QPainter(image)
        view.viewport().render(painter)
        painter.end()

        return image

    def saveRun(self):
        opts = QFileDialog.Options()
        folderName = QFileDialog.getExistingDirectory(
            self,
            "Save Run",
            self.lastRunsDir,
            options=opts,
        )
        os.mkdir(
            folderName := (
                folderName
                + "/"
                + str(datetime.datetime.now()).split(".")[0].replace(":", "-")
            )
        )

        rb = [
            self.SpeedSlide.value(),
            self.WhiskerSlide.value(),
            self.DiameterSlide.value(),
            self.EfficiencySlide.value(),
            self.BatteryLifeSlide.value(),
            self.WhiskerEffSlide.value(),
        ]

        jsonObj = json.dumps(rb)
        with open(folderName + "/Robot_Settings.rbt", "w") as outFile:
            outFile.write(jsonObj)
        with open(folderName + "/Message.txt", "w") as outFile:
            outFile.write(
                f'Simulation at {datetime.datetime.now()}\n\tUsing Algorithm {self.PathAlgorithmBox.currentText()}\n\tOn floorplan "{self.fileName}"\n\tWith floor type {self.FloorTypeBox.currentText()}\n\tTotal Percentage cleaned: {100 * round(1-(np.sum(self.dirt)/self.StartDirt), 2)}%\n\tFinal duration {self.Stat_SimulationTime.text()}'
            )

        with open(self.fileName, "rb") as src, open(
            folderName + "/Floor_Plan.fpd", "wb"
        ) as dest:
            shutil.copyfileobj(src, dest)

        # Visualize the dirtienes using a pie chart
        plt.pie(
            [np.sum(self.dirt), self.StartDirt - np.sum(self.dirt)],
            labels=["Dirt", "Clean"],
            colors=["saddlebrown", "limegreen"],
            autopct="%1.1f%%",
        )
        plt.savefig(folderName + "/Dirt_Pie.png")

        # Render the scene to a png
        # This has to be done this way because the floorplan may be larger than the window
        area = self.graphicsView.scene.sceneRect()
        image = QImage(int(area.width()), int(area.height()), QImage.Format_ARGB32)
        painter = QPainter(image)
        image.fill(QtCore.Qt.white)
        self.graphicsView.scene.render(painter)
        painter.end()

        image.save(folderName + "/Result_Image.png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = simWindowApp()
    win.show()
    app.exec()
