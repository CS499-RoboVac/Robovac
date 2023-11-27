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
from Common.Util import cm_to_ft, ft_to_cm, Vec2
from FloorPlanDesigner.saveMessageBox import SaveMessageBox


class fpdWindowApp(QMainWindow, Ui_FPDWindow):
    def resetGraphicsScene(self):
        """
        Resets the graphics scene to its default state, by clearing the scene and creating a new scene.
        """
        self.FPDGraphicsView.scene = QGraphicsScene()
        self.FPDGraphicsView.setScene(self.FPDGraphicsView.scene)
        self.FPDGraphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.FPDGraphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def __init__(self, parent=None):
        super(fpdWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.main = []
        # Flag to indicate whether the floorplan has been changed since the last save
        self.changed = False

        self.floorplansDir = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/Floor Plans/"
        )

        # Create the graphics scene
        self.resetGraphicsScene()

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
            if type(room) == Room.Room:
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
        self.changed = True

    def addChest(self):
        chestCount = len(
            [
                item
                for item in self.FPDGraphicsView.scene.items()
                if (type(item) == Room.Chest)
            ]
        )
        chestName = "Chest " + str(chestCount + 1)
        chest = Room.Chest(0, 0, ft_to_cm(3), ft_to_cm(1), chestName)
        chest.setZValue(3)
        self.FPDGraphicsView.scene.addItem(chest)
        self.changed = True

    def addFurniture(self):
        self.changed = True
        pass

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
        door.setZValue(5)
        self.FPDGraphicsView.scene.addItem(door)
        self.populateRoomOptions()
        self.changed = True

    def Helper01(self, fp):
        """
        Helper method to process and render items from a floor plan.

        Args:
            fp (list): List of items in the floor plan.

        Returns:
            None
        """
        for item in fp:
            # Read the values from the JSON file
            x = int(item["x1"])
            y = int(item["y1"])
            w = int(item["width"])
            h = int(item["height"])
            name = item["Room Name"]
            typeString = item["type"]
            # First, add the rooms and furniture to the scene
            if typeString == "Room":
                # This renders the rooms to the screen
                room = Room.Room(x, y, w, h, name)  # parameters are x, y, width, height
                # If the room is a door, change the color to brown, and set its Z to 2
                if "Door" in name:
                    room.color = QColor(139, 69, 19)
                    room.setZValue(0)
                self.FPDGraphicsView.scene.addItem(room)
            elif typeString == "Chest":
                # This renders the chests to the screen
                chest = Room.Chest(x, y, w, h, name)
                chest.setZValue(3)
                self.FPDGraphicsView.scene.addItem(chest)

    def loadFloorPlan(self):
        """
        Loads a floorplan from a file selected by the user using a file dialog.
        The floorplan is stored in a JSON file format.
        """
        # Check if the user wants to save the current floorplan
        result = self.savePrompt()
        if result == -1:
            return

        opts = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Floorplan Designer - Load Floorplan",
            self.floorplansDir,
            "Floor Plan Designer Files (*.fpd)",
            options=opts,
        )
        if fileName:
            self.resetGraphicsScene()
            with open(fileName, "r") as inFile:
                fp = json.load(inFile)

            self.Helper01(fp)
            # self.Helper01(fp, True)

        self.populateRoomOptions()
        self.floorplanIsSavedSet()

    def saveFloorPlan(self, calledFromSavePrompt=False):
        """
        Saves the floorplan to a file selected by the user using a file dialog.
        The floorplan is stored in a JSON file format.
        Returns: 0 if the floorplan was not saved, 1 if the floorplan was saved
        """
        _translate = QtCore.QCoreApplication.translate
        # If there are no rooms in the floorplan, don't do anything
        if len(self.FPDGraphicsView.scene.items()) == 0:
            return 0

        # Create the floorplan dictionary to be saved
        fp = list()
        for room in self.FPDGraphicsView.scene.items():
            fp.append(
                {
                    "Room Name": room.name,
                    "x1": room.x(),
                    "y1": room.y(),
                    "width": room.rect.width(),
                    "height": room.rect.height(),
                    "type": type(room).__name__,
                }
            )

        # If the floorplan is not valid, don't save it, and display an error message
        if not self.validateFloorPlan(fp):
            # Pop up a message box to tell the user that the floorplan is not valid
            message = "The floorplan is not valid. Please make sure that all rooms are connected."
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText(message)
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            return 0

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

            jsonObj = json.dumps(fp)
            with open(fileName, "w") as outFile:
                outFile.write(jsonObj)
                QtTest.QTest.qWait(1)
            self.saveFloorplanButton.setText("Floorplan Saved!")
            self.floorplanIsSavedSet()
            # If this function was called from the exit button we don't want to wait
            if calledFromSavePrompt:
                self.saveFloorplanButton.setText("Save Floorplan")
                return 1
            QtTest.QTest.qWait(5000)
            self.saveFloorplanButton.setText("Save Floorplan")
        else:
            self.saveFloorplanButton.setText("Error - Floorplan Not Saved!")
            QtTest.QTest.qWait(5000)
            self.saveFloorplanButton.setText("Save Floorplan")
            return 0

    def savePrompt(self, exitAfter=False):
        """
        Makes sure that the floorplan is saved before doing something that would cause the floorplan to be lost.
        asks the user if they want to save the floorplan if it has been changed,
        and then closes the floorplan designer if exitAfter is True.
        Args:
            self: The FloorPlanDesigner object.
            exitAfter (bool): Flag indicating whether to exit the floorplan designer after saving or not saving.
        Returns:
            1 if the floorplan was saved, 0 if the floorplan was not saved, and -1 if the operation was cancelled.
        """
        self.returnVal = 0
        # If there is nothing in the scene, don't do anything
        if len(self.FPDGraphicsView.scene.items()) == 0:
            if exitAfter:
                self.close()
            return self.returnVal

        # Update the changed flag
        self.floorplanHasBeenChangedCheck()

        # If the floorplan has not been changed, don't do anything
        if not self.changed:
            if exitAfter:
                self.close()
            return self.returnVal

        # If the floorplan has been changed, ask the user if they want to save it

        def yesbtn(i):
            # Save the floorplan
            if self.saveFloorPlan(calledFromSavePrompt=True) == 1:
                self.returnVal = 1
            else:
                # The floorplan could not be saved for some reason
                # So we don't want to close the floorplan designer
                self.returnVal = -1
            # Close the message box
            self.msg.hide()

            # Close the floorplan designer
            if exitAfter and self.returnVal == 1:
                self.close()

        def nobtn():
            self.returnVal = 0
            # Close the message box
            self.msg.hide()
            if exitAfter:
                self.close()

        def cancelbtn():
            self.returnVal = -1
            # Close the message box
            self.msg.hide()

        if self.changed:
            # Pop up a message box to ask the user if they want to save the floorplan
            message = "Do you want to save the current floorplan?\n\nAny unsaved changes will be lost."
            self.msg = SaveMessageBox(
                message=message, yesbtn=yesbtn, nobtn=nobtn, cancelbtn=cancelbtn
            )
            self.msg.exec_()

        return self.returnVal

    def createNewFloorPlan(self):
        """
        Empties the current floorplan and creates a new floorplan.
        Which is really just deleting all of the items in the scene.
        """
        # Check if the user wants to save the current floorplan
        if self.savePrompt() == -1:
            return

        # Clear the scene
        self.resetGraphicsScene()
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
            if type(room) == Room.Room and roomName == room.name:
                self.roomWBox.blockSignals(True)
                self.roomHBox.blockSignals(True)

                self.roomWBox.setValue(cm_to_ft(room.rect.width()))
                self.roomHBox.setValue(cm_to_ft(room.rect.height()))

                self.roomWBox.blockSignals(False)
                self.roomHBox.blockSignals(False)

                room.selected = True
                room.setZValue(0)
            else:
                room.selected = False
                room.setZValue(0)
            self.FPDGraphicsView.scene.update()

    def floorplanHasBeenChangedCheck(self):
        """
        Checks to see if a room has been changed.
        """
        # Loop through the list of objects in the floorplan,
        # and check to see if any of them have been changed
        for object in self.FPDGraphicsView.scene.items():
            # Check if the object has a hasChanged attribute
            if hasattr(object, "hasChanged") and object.hasChanged:
                self.changed = True
                return

    def floorplanIsSavedSet(self):
        """
        Checks to see if a room has been changed.
        """
        # Loop through the list of objects in the floorplan,
        # and check to see if any of them have been changed
        for object in self.FPDGraphicsView.scene.items():
            # Check if the object has a hasChanged attribute
            if hasattr(object, "hasChanged"):
                object.hasChanged = False
        self.changed = False

    def connectButtons(self):
        # Load, new, and save buttons
        self.loadFloorplanButton.clicked.connect(self.loadFloorPlan)
        self.newFloorplanButton.clicked.connect(self.createNewFloorPlan)
        self.saveFloorplanButton.clicked.connect(self.saveFloorPlan)

        # Add room and add Door
        self.addRoomButton.clicked.connect(self.addRoom)
        self.addDoorButton.clicked.connect(self.addDoor)
        self.addChestButton.clicked.connect(self.addChest)
        self.addFurnitureButton.clicked.connect(self.addFurniture)

        # Connect the room options combo box to the onRoomSelected function
        self.roomOptionsComboBox.currentIndexChanged.connect(self.onRoomSelected)
        self.roomOptionsComboBox.highlighted.connect(self.onRoomSelected)

        # Modify room dimensions
        self.roomWBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomHBox.valueChanged.connect(self.updateRoomDimensions)

        # Exit the floorplan designer
        self.BackButton.clicked.connect(self.close)

    def closeEvent(self, event):
        """
        This function is called when the user tries to close the window.
        """
        if self.savePrompt(exitAfter=True) == -1:
            event.ignore()
        else:
            return super().closeEvent(event)

    def validateFloorPlan(self, fp):
        if len(fp) == 1:
            return True
        fpc = {
            Primitives.Rectangle(
                Vec2(v["x1"], v["y1"]),
                Vec2(v["x1"] + v["width"], v["y1"] + v["height"]),
                False,
            ): False
            for v in fp
            if v["type"] == "Room"
        }
        fpc[next(iter(fpc.keys()))] = True
        TurnedThisRound = True
        while TurnedThisRound:
            TurnedThisRound = False
            for S in fpc.keys():
                if not fpc[S]:
                    for C in fpc.keys():
                        if fpc[C]:
                            if S & C or C & S:
                                fpc[S] = True
                                TurnedThisRound = True
                                break
        return all([v for v in fpc.values()])
