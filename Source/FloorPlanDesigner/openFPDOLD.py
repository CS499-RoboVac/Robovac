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
from Common.Room import Room



# class fpdWindowApp(QMainWindow, Ui_FPDWindow):
#     """
#     A class representing the Floor Plan Designer application window.

#     Inherits from QMainWindow and Ui_FPDWindow.

#     Attributes:
#     - numRooms (int): The number of rooms in the floor plan.
#     - rooms (list): A list of Room objects representing the rooms in the floor plan.
#     - floorplansDir (str): The directory where floor plan files are saved.

#     Methods:
#     - __init__(self, parent=None): Initializes the fpdWindowApp object.
#     - saveFloorplan(self): Saves the current floor plan to a file.
#     - loadFloorplan(self): Loads a floor plan from a file.
#     - newFloorplan(self): Clears the current floor plan and starts a new one.
#     - updateRoomDimensions(self): Updates the dimensions of a selected room in the floor plan.
#     """


class fpdWindowApp(QMainWindow, Ui_FPDWindow):
    def __init__(self, parent=None, isLoad=False):
        super(fpdWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.numRooms = 0
        self.rooms = []
        self.door_count = 0
        self.floorplansDir = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/Floor Plans/"
        )
        if not isLoad: 
            self.addRoom("livingRoom")

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
            self.floorplanView.setCurrentIndex(0)
            with open(fileName, "r") as inFile:
                fp = json.load(inFile)
            # self, name, x, y, w, h, overview, fpv, combo
            i = self.floorplanView.count()
            while i > 0:
                self.floorplanView.removeTab(i)
                i -= 1
            for room in self.rooms:
                room.__del__()
            self.rooms.clear()
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
            self.floorplanView.setCurrentIndex(1)
            self.floorplanView.setCurrentIndex(0)

    def newFloorplan(self):
        """
        Completely resets the floorplan designer application.
        """
        i = self.floorplanView.count()
        while i > 0:
            self.floorplanView.removeTab(i)
            i -= 1
        for room in self.rooms:
            room.__del__()
        self.rooms.clear()
        self.overviewTab
        self.floorplanView
        self.roomOptionsComboBox.clear()
        self.addRoom("livingRoom")
        

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
                # If the room name contains "Door", then it is a door and should be rendered below all other rooms.
                # If the room name does not contain "Door", then it is a normal room and should be rendered above all
                # other rooms.
                # If the room name does not contain "Door", then it's minimum size is 20x20.
                if "Door" in self.rooms[roomIndex].roomName:
                    self.rooms[roomIndex].ovRoomView.lower()
                else:
                    if self.rooms[roomIndex].width < 20:
                        self.rooms[roomIndex].width = 20
                        self.roomWBox.setValue(20)
                    if self.rooms[roomIndex].height < 20:
                        self.rooms[roomIndex].height = 20
                        self.roomHBox.setValue(20)
                    self.rooms[roomIndex].ovRoomView.raise_()

            roomIndex += 1
        self.floorplanView.setCurrentIndex(0)

    def addRoom(self, roomName=None):
        """
        Adds a new room to the floorplan.

        Retrieves the new room name from the textEdit widget and checks if it already exists in the floorplan.
        If the room name is unique, a new Room object is created and added to the floorplan.

        Args:
            None

        Returns:
            None
        """
        if roomName is None:
            newRoomText = self.textEdit.toPlainText()
        else:
            newRoomText = roomName
            # If the type of the room name is not a string, then set it to a default value.
            if type(newRoomText) != str:
                newRoomText = "Room " + str(self.numRooms)

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
            self.roomOptionsComboBox.setCurrentIndex(len(self.rooms) - 1)

    def addDoor(self):
        """
        Adds a door to the floorplan.
        A door is a 5x5 room that is brown in color.
        It is also rendered below all other rooms.
        """
        self.door_count += 1
        self.floorplanView.setCurrentIndex(1)
        door = Room(
            "Door" + str(self.door_count),
            100,
            100,
            5,
            5,
            self.overviewTab,
            self.floorplanView,
            self.roomOptionsComboBox,
            "rgb(139, 69, 19)",
        )

        self.rooms.append(door)
        self.roomOptionsComboBox.setCurrentIndex(len(self.rooms) - 1)

    def on_room_selected(self):
        """
        This function is called whenever the user selects a new room
        from the roomOptionsComboBox.
        Updates the room options and the rest of the GUI based on the current selection in the roomOptionsComboBox.
        Also handles any other housekeeping tasks that need to be done when a new room is selected.

        Removes the border from all rooms, then adds a border to the currently selected room.

        Sets the values of the roomXBox, roomYBox, roomWBox, and roomHBox widgets to the values of the
        currently selected room in the self.rooms list.
        Args:
            self: The FloorPlanDesigner object.

        Returns:
            None
        """
        # Find the room that is currently selected in the combo box.
        try:
            selected_room = self.rooms[self.roomOptionsComboBox.currentIndex()]
        except:
            # If there are no rooms, then return.
            # This occurs on startup.
            return

        # Set all rooms to have no line width.
        for room in self.rooms:
            room.ovRoomView.setLineWidth(0)

        # Set the selected room to have a line width of 1.
        selected_room.set_line_width(1)

        self.roomXBox.blockSignals(True)
        self.roomYBox.blockSignals(True)
        self.roomWBox.blockSignals(True)
        self.roomHBox.blockSignals(True)

        self.roomXBox.setProperty("value", selected_room.x)
        self.roomYBox.setProperty("value", selected_room.y)
        self.roomWBox.setProperty("value", selected_room.width)
        self.roomHBox.setProperty("value", selected_room.height)

        self.roomXBox.blockSignals(False)
        self.roomYBox.blockSignals(False)
        self.roomWBox.blockSignals(False)
        self.roomHBox.blockSignals(False)

    def connectButtons(self):
        self.addRoomButton.clicked.connect(self.addRoom)
        self.addDoorButton.clicked.connect(self.addDoor)
        self.saveFloorplanButton.clicked.connect(self.saveFloorplan)
        self.loadFloorplanButton.clicked.connect(self.loadFloorplan)
        self.newFloorplanButton.clicked.connect(self.newFloorplan)
        self.roomOptionsComboBox.currentIndexChanged.connect(self.on_room_selected)
        self.roomOptionsComboBox.highlighted.connect(self.on_room_selected)
        self.roomXBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomYBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomWBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomHBox.valueChanged.connect(self.updateRoomDimensions)
