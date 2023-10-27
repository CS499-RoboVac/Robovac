from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)

import sys
import json
import os

from Views.ui_fpd import Ui_FPDWindow
from Common.FloorTile import FloorTile
from Common.Room import Room

class fpdWindowApp(QMainWindow, Ui_FPDWindow):
    """
    A class representing the Floor Plan Designer application window.

    Inherits from QMainWindow and Ui_FPDWindow.

    Attributes:
    - numRooms (int): The number of rooms in the floor plan.
    - rooms (list): A list of Room objects representing the rooms in the floor plan.
    - floorplansDir (str): The directory where floor plan files are saved.

    Methods:
    - __init__(self, parent=None): Initializes the fpdWindowApp object.
    - saveFloorplan(self): Saves the current floor plan to a file.
    - loadFloorplan(self): Loads a floor plan from a file.
    - newFloorplan(self): Clears the current floor plan and starts a new one.
    - updateRoomDimensions(self): Updates the dimensions of a selected room in the floor plan.
    """
class fpdWindowApp(QMainWindow, Ui_FPDWindow):
    def __init__(self, parent=None):
        super(fpdWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.numRooms = 1
        self.rooms = []
        self.floorplansDir = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/Floor Plans/"
        )

    def saveFloorplan(self):
            """
            Saves the current floorplan to a file in JSON format. The file is selected by the user
            using a file dialog. The floorplan is saved as a dictionary with the following keys:
            - Room Name: the name of the room
            - x1: the x-coordinate of the top-left corner of the room
            - x2: the x-coordinate of the bottom-right corner of the room
            - y1: the y-coordinate of the top-left corner of the room
            - y2: the y-coordinate of the bottom-right corner of the room
            - width: the width of the room
            - height: the height of the room
            - furniture: a string representing the furniture in the room (currently not implemented)
            """
            _translate = QtCore.QCoreApplication.translate
            # *************************************************************
            #
            # **************   NEEDS UPDATING, TEMPORARY   ****************
            #
            # *************************************************************
            # adding some temporary boo-boo math here
            # assuming size of floorplan is 600 units wide by 480 units tall
            # this is based on current FloorPlan tab size, using math to adjust
            # this ratio to fit the 8000 square foot requirement per the project requirements
            # for this ratio to be 8000 sqft, 600*480 = 288000 / 36 = 8000
            # 600 / 6 = 100 foot wide x 480 / 6 = 80 foot tall
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
                roomCount = 1
                for room in self.rooms:
                    key = str(roomCount)
                    fp[key] = dict()
                    fp[key]["Room Name"] = room.roomName
                    fp[key]["x1"] = 182 * room.x
                    fp[key]["x2"] = 182 * (room.x + room.width)
                    fp[key]["y1"] = 182 * room.y
                    fp[key]["y2"] = 182 * (room.y * room.height)
                    fp[key]["width"] = 182 * room.width
                    fp[key]["height"] = 182 * room.height
                    fp[key]["furniture"] = ""
                    roomCount += 1
                jsonObj = json.dumps(fp)
                with open(fileName, "w") as outFile:
                    outFile.write(jsonObj)
                self.saveFloorplanButton.setText(
                    _translate("MainWindow", "Floorplan Saved!")
                )
                QtTest.QTest.qWait(5000)
                self.saveFloorplanButton.setText(_translate("MainWindow", "Save Floorplan"))
            else:
                self.saveFloorplanButton.setText(
                    _translate("MainWindow", "Error - Floorplan Not Saved!")
                )
                QtTest.QTest.qWait(5000)
                self.saveFloorplanButton.setText(_translate("MainWindow", "Save Floorplan"))

    def loadFloorplan(self):
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
            self.floorplanView.setCurrentIndex(1)
            with open(fileName, "r") as inFile:
                fp = json.load(inFile)
            # self, name, x, y, w, h, overview, fpv, combo
            i = self.floorplanView.count()
            while i > 1:
                self.floorplanView.removeTab(i)
                i -= 1
            for room in self.rooms:
                room.ovRoomView.setLineWidth(0)
            self.rooms.clear()
            self.numRooms = 1
            self.overviewTab
            self.floorplanView
            self.roomOptionsComboBox.clear()
            for key in fp.keys():
                n = fp[key]["Room Name"]
                x = int(int(fp[key]["x1"]) / 182)
                y = int(int(fp[key]["y1"]) / 182)
                w = int(int(fp[key]["width"]) / 182)
                h = int(int(fp[key]["height"]) / 182)
                furniture = fp[key]["furniture"]
                self.rooms.append(
                    Room(
                        n,
                        x,
                        y,
                        w,
                        h,
                        self.overviewTab,
                        self.floorplanView,
                        self.roomOptionsComboBox,
                    )
                )
            self.floorplanView.setCurrentIndex(0)

    def newFloorplan(self):
        """
        Clears the room options combo box, sets the current index of the floorplan view to 1, 
        sets the number of rooms to 1, removes all tabs from the floorplan view except the first one, 
        and clears the list of rooms. Also sets the line width of each room's ovRoomView to 0.
        """
        self.roomOptionsComboBox.clear()
        self.floorplanView.setCurrentIndex(1)
        self.numRooms = 1
        for room in self.rooms:
            room.ovRoomView.setLineWidth(0)
        self.rooms.clear()
        i = self.floorplanView.count()
        while i > 1:
            self.floorplanView.removeTab(i)
            i -= 1
        self.floorplanView.setCurrentIndex(0)

    def updateRoomDimensions(self):
        """
        Updates the dimensions of a room in the floorplan.

        This function updates the dimensions of a room in the floorplan based on the values entered in the GUI.
        It first sets the current index of the floorplan view to 1, then loops through the list of rooms to find
        the room with the same name as the selected room in the room options combo box. Once the room is found,
        it updates the position and size of the room's view, as well as the x, y, width, and height attributes
        of the room object. Finally, it calls the tabViewResize() method of the room object to resize the tab view
        for the room. The function then sets the current index of the floorplan view back to 0.

        Args:
            self: The FloorPlanDesigner object.

        Returns:
            None.
        """
        self.floorplanView.setCurrentIndex(1)
        roomIndex = 0
        for room in self.rooms:
            if room.roomName == self.roomOptionsComboBox.currentText():
                self.floorplanView.setCurrentIndex(1)
                room.ovRoomView.move(
                    int(self.roomXBox.value()), (self.roomYBox.value())
                )
                room.ovRoomView.resize(
                    int(self.roomWBox.value()), (self.roomHBox.value())
                )
                self.rooms[roomIndex].x = self.roomXBox.value()
                self.rooms[roomIndex].y = self.roomYBox.value()
                self.rooms[roomIndex].width = self.roomWBox.value()
                self.rooms[roomIndex].height = self.roomHBox.value()
                self.rooms[roomIndex].tabViewResize()
            roomIndex += 1
        self.floorplanView.setCurrentIndex(0)

    def updateRoomOptions(self):
        """
        Updates the room options in the GUI based on the current selection in the roomOptionsComboBox.

        This function sets the values of the roomXBox, roomYBox, roomWBox, and roomHBox widgets to the values of the
        currently selected room in the self.rooms list. This function is called whenever the user selects a new room
        from the roomOptionsComboBox.

        Args:
            self: The FloorPlanDesigner object.

        Returns:
            None
        """
        self.roomXBox.blockSignals(True)
        self.roomYBox.blockSignals(True)
        self.roomWBox.blockSignals(True)
        self.roomHBox.blockSignals(True)

        for room in self.rooms:
            if room.roomName == self.roomOptionsComboBox.currentText():
                self.roomXBox.setProperty("value", room.x)
                self.roomYBox.setProperty("value", room.y)
                self.roomWBox.setProperty("value", room.width)
                self.roomHBox.setProperty("value", room.height)

        self.roomXBox.blockSignals(False)
        self.roomYBox.blockSignals(False)
        self.roomWBox.blockSignals(False)
        self.roomHBox.blockSignals(False)

    def addRoom(self):
            """
            Adds a new room to the floorplan.

            Retrieves the new room name from the textEdit widget and checks if it already exists in the floorplan.
            If the room name is unique, a new Room object is created and added to the floorplan.

            Args:
                None

            Returns:
                None
            """
            newRoomText = self.textEdit.toPlainText()
            self.textEdit.setText("")
            dupeFlag = False
            for room in self.rooms:
                if room.roomName == newRoomText or newRoomText == "":
                    dupeFlag = True
            if not dupeFlag:
                self.floorplanView.setCurrentIndex(1)
                self.rooms.append(
                    Room(
                        newRoomText,
                        100,
                        100,
                        300,
                        180,
                        self.overviewTab,
                        self.floorplanView,
                        self.roomOptionsComboBox,
                    )
                )

    def connectButtons(self):
        self.addRoomButton.clicked.connect(self.addRoom)
        self.saveFloorplanButton.clicked.connect(self.saveFloorplan)
        self.loadFloorplanButton.clicked.connect(self.loadFloorplan)
        self.newFloorplanButton.clicked.connect(self.newFloorplan)
        self.roomOptionsComboBox.currentIndexChanged.connect(self.updateRoomOptions)
        self.roomXBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomYBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomWBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomHBox.valueChanged.connect(self.updateRoomDimensions)
