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


class Room:
    def __init__(self, name, x, y, w, h, overview, fpv, combo):
        fpv.setCurrentIndex(1)
        self.roomName = name
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.ovRoomView = QtWidgets.QFrame(overview)
        self.ovRoomView.setGeometry(
            QtCore.QRect(self.x, self.y, self.width, self.height)
        )
        font = QtGui.QFont()
        font.setKerning(True)
        self.ovRoomView.setFont(font)
        self.ovRoomView.setFrameShape(QtWidgets.QFrame.Box)
        self.ovRoomView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ovRoomView.setLineWidth(1)
        self.ovRoomView.setObjectName(name)
        self.roomTab = QtWidgets.QWidget()
        fpv.addTab(self.roomTab, name)
        self.tabRoomView = QtWidgets.QFrame(self.roomTab)
        self.tabRoomScale = 1
        if self.width < 600 and self.height < 480:
            if self.width / 600 > self.height / 480:
                self.tabRoomScale = int(600 / self.width)
            else:
                self.tabRoomScale = int(480 / self.height)
        self.tabRoomView.setGeometry(
            QtCore.QRect(
                20, 20, self.width * self.tabRoomScale, self.height * self.tabRoomScale
            )
        )
        font = QtGui.QFont()
        font.setKerning(True)
        self.tabRoomView.setFont(font)
        self.tabRoomView.setFrameShape(QtWidgets.QFrame.Box)
        self.tabRoomView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tabRoomView.setLineWidth(1)
        self.tabRoomView.setObjectName(name)
        combo.addItem(name)
        fpv.setCurrentIndex(0)

    def tabViewResize(self):
        self.tabRoomScale = 1
        if self.width < 600 and self.height < 480:
            if self.width / 600 > self.height / 480:
                self.tabRoomScale = int(600 / self.width)
            else:
                self.tabRoomScale = int(480 / self.height)
        self.tabRoomView.setGeometry(
            QtCore.QRect(
                20, 20, self.width * self.tabRoomScale, self.height * self.tabRoomScale
            )
        )


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
        # self.floorplanView.removeTab(1)
        # self.r1.setLineWidth(0)
        # self.rooms.append(Room('Room 1', 20, 20, 120, 80, self.overviewTab, self.floorplanView, self.roomOptionsComboBox))

    def saveFloorplan(self):
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
        """
        self.r3 = QtWidgets.QFrame(self.overviewTab)
        self.r3.setGeometry(QtCore.QRect(100, 100, 301, 181))
        font = QtGui.QFont()
        font.setKerning(True)
        self.r3.setFont(font)
        self.r3.setFrameShape(QtWidgets.QFrame.Box)
        self.r3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.r3.setLineWidth(1)
        self.r3.setObjectName(newRoomText)
        self.floorplanView.setCurrentIndex(0)

        self.room = QtWidgets.QWidget()
        self.room.setObjectName(newRoomText)
        self.roomFull = QtWidgets.QFrame(self.room)
        self.roomFull.setGeometry(QtCore.QRect(20, 20, 600, 480))
        font = QtGui.QFont()
        font.setKerning(True)
        self.roomFull.setFont(font)
        self.roomFull.setFrameShape(QtWidgets.QFrame.Box)
        self.roomFull.setFrameShadow(QtWidgets.QFrame.Plain)
        self.roomFull.setLineWidth(1)
        self.roomFull.setObjectName(newRoomText + "_full")
        self.floorplanView.addTab(self.room, newRoomText)
        self.rooms.append(self.room)
        """

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
