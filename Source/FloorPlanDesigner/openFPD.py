from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QRectF, Qt
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
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
import Common.Room as Room
from Common.Util import Vec2
import Common.Colors as Colors
import numpy as np
import math
import random

from Views.ui_fpd import Ui_FPDWindow
from Common.Util import cm_to_ft, ft_to_cm


class fpdWindowApp(QMainWindow, Ui_FPDWindow):
    def __init__(self, parent=None):
        super(fpdWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.main = []

        self.floorplansDir = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/Floor Plans/"
        )

        self.FPDGraphicsView.scene = QGraphicsScene()
        self.FPDGraphicsView.setScene(self.FPDGraphicsView.scene)
        self.FPDGraphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.FPDGraphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def populateRoomOptions(self):
        """
        Populates the room options combo box with the names of the rooms in the floorplan.

        This function loops through the list of rooms in the floorplan and adds the name of each room
        to the room options combo box.

        Args:
            self: The FloorPlanDesigner object.

        Returns:
            None.
        """

        # remove all of the items in the combo box
        self.roomOptionsComboBox.clear()

        # Add the names of the rooms to the combo box
        for room in self.FPDGraphicsView.scene.items():
            self.roomOptionsComboBox.addItem(room.name)

    def addRoom(self):
        """
        Adds a room to the floorplan.
        The room is added at the position (0, 0) with a width and height 10 feet.
        """
        roomname = self.textEdit.toPlainText()
        roomcount = len(
            [
                item
                for item in self.FPDGraphicsView.scene.items()
                if ("Door" not in item.name)
            ]
        )
        if (roomname == "") or (type(roomname) != str):
            roomname = "Room " + str(roomcount + 1)
        room = Room.Room(0, 0, ft_to_cm(10), ft_to_cm(10), roomname)
        room.setZValue(0)
        self.FPDGraphicsView.scene.addItem(room)
        self.populateRoomOptions()

    def addDoor(self):
        """
        Adds a door to the floorplan.
        The door is added at the position (0, 0) with a width and height 2 feet.
        """
        # Find how many doors are in the scene
        doors = len(
            [
                door
                for door in self.FPDGraphicsView.scene.items()
                if ("Door" in door.name)
            ]
        )
        doorname = "Door " + str(doors + 1)
        door = Room.Room(
            0, 0, ft_to_cm(2), ft_to_cm(2), doorname, color=QColor(139, 69, 19)
        )
        door.setZValue(1)
        self.FPDGraphicsView.scene.addItem(door)
        self.populateRoomOptions()

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
            self.FPDGraphicsView.scene.clear()
            with open(fileName, "r") as inFile:
                fp = json.load(inFile)

            for key in fp.keys():
                # Read the values from the JSON file
                x = int(fp[key]["x1"])
                y = int(fp[key]["y1"])
                w = int(fp[key]["width"])
                h = int(fp[key]["height"])
                name = fp[key]["Room Name"]
                furniture = fp[key]["furniture"]  # What even is this parameter???
                # This renders the rectangle to the screen
                room = Room.Room(x, y, w, h, name)  # parameters are x, y, width, height

                # If the room is a door, change the color to brown, and set it's Z to 2
                if "Door" in name:
                    room.color = QColor(139, 69, 19)
                    room.setZValue(2)

                # Add the rectangle to the scene
                self.FPDGraphicsView.scene.addItem(room)
        self.populateRoomOptions()

    def saveFloorPlan(self):
        """
        Saves the floorplan to a file selected by the user using a file dialog.
        The floorplan is stored in a JSON file format.
        """
        _translate = QtCore.QCoreApplication.translate
        if len(self.FPDGraphicsView.scene.items()) == 0:
            return

        opts = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Floorplan Designer - Save Floorplan",
            self.floorplansDir,
            "Floor Plan Designer Files (*.fpd)",
            options=opts,
        )
        if fileName:
            if ".fpd" not in fileName:
                fileName = fileName + ".fpd"
            fp = dict()
            for room in self.FPDGraphicsView.scene.items():
                fp[room.name] = {
                    "Room Name": room.name,
                    "x1": room.x(),
                    "y1": room.y(),
                    "width": room.rect.width(),
                    "height": room.rect.height(),
                    "furniture": "",
                }
            if self.validateFloorPlan(fp):
                jsonObj = json.dumps(fp)
                with open(fileName, "w") as outFile:
                    outFile.write(jsonObj)
                self.saveFloorplanButton.setText("Floorplan Saved!")
                QtTest.QTest.qWait(5000)
                self.saveFloorplanButton.setText("Save Floorplan")
            else:
                self.saveFloorplanButton.setText("Error - Floorplan Not Valid!")
                QtTest.QTest.qWait(5000)
                self.saveFloorplanButton.setText("Save Floorplan")
        else:
            self.saveFloorplanButton.setText("Error - Floorplan Not Saved!")
            QtTest.QTest.qWait(5000)
            self.saveFloorplanButton.setText("Save Floorplan")

    def createNewFloorPlan(self):
        """
        Empties the current floorplan and creates a new floorplan.
        Which is really just deleting all of the items in the scene.
        """
        self.FPDGraphicsView.scene.clear()
        self.populateRoomOptions()

        # Set the room values to the default values
        self.roomWBox.setValue(10)
        self.roomHBox.setValue(10)

    def updateRoomDimensions(self):
        """
        Updates the dimensions of a room in the floorplan.

        This function updates the dimensions of a room in the floorplan based on the values entered in the GUI.
        It loops through the list of rooms to find the room with the same name as the selected room in the
        room options combo box. Once the room is found, it updates the position and size of the room.

        Args:
            self: The FloorPlanDesigner object.

        Returns:
            None.
        """
        roomName = self.roomOptionsComboBox.currentText()
        for room in self.FPDGraphicsView.scene.items():
            if roomName == room.name:
                room.changeSize(
                    ft_to_cm(self.roomWBox.value()), ft_to_cm(self.roomHBox.value())
                )
                self.FPDGraphicsView.scene.update()

    def onRoomSelected(self):
        """
        Updates the room options combo box when a room is selected.

        This function updates the room options combo box when a room is selected. It updates the values
        in the room options combo box to match the values of the selected room.

        It also highlights the selected room in the floorplan by giving it an outline.

        Args:
            self: The FloorPlanDesigner object.

        Returns:
            None.
        """
        roomName = self.roomOptionsComboBox.currentText()

        for room in self.FPDGraphicsView.scene.items():
            if roomName == room.name:
                self.roomWBox.blockSignals(True)
                self.roomHBox.blockSignals(True)
                
                self.roomWBox.setValue(cm_to_ft(room.rect.width()))
                self.roomHBox.setValue(cm_to_ft(room.rect.height()))

                self.roomWBox.blockSignals(False)
                self.roomHBox.blockSignals(False)

                room.selected = True
                room.setZValue(room.zValue() + 1)
            else:
                room.selected = False
                room.setZValue(room.zValue() - 1)
            self.FPDGraphicsView.scene.update()

    def connectButtons(self):
        # Load, new, and save buttons
        self.loadFloorplanButton.clicked.connect(self.loadFloorPlan)
        self.newFloorplanButton.clicked.connect(self.createNewFloorPlan)
        self.saveFloorplanButton.clicked.connect(self.saveFloorPlan)

        # Add room and add Door
        self.addRoomButton.clicked.connect(self.addRoom)
        self.addDoorButton.clicked.connect(self.addDoor)

        # Connect the room options combo box to the onRoomSelected function
        self.roomOptionsComboBox.currentIndexChanged.connect(self.onRoomSelected)
        self.roomOptionsComboBox.highlighted.connect(self.onRoomSelected)

        # Modify room dimensions
        self.roomWBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomHBox.valueChanged.connect(self.updateRoomDimensions)

    def validateFloorPlan(self, fp):
        fpc = {Primitives.Rectangle(Vec2(v["x1"], v["y1"]), Vec2(v["x1"]+v["width"], v["y1"]+v["height"]), False) : False for k,v in fp.items()}
        fpc[next(iter(fpc.keys()))]=True
        TurnedThisRound = True
        while TurnedThisRound:
            TurnedThisRound = False
            for S in fpc.keys():
                if not fpc[S]:
                    for C in fpc.keys():
                        if fpc[C]:
                            if S&C or C&S:
                                fpc[S]=True
                                TurnedThisRound = True
                                break
        return all([v for v in fpc.values()])
