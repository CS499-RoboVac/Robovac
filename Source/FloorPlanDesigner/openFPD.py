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

from Views.ui_fpd import Ui_FPDWindow


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


class fpdWindowApp(QMainWindow, Ui_FPDWindow):
    def __init__(self, parent=None):
        super(fpdWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.numRooms = 1
        self.rooms = []
        # self.rooms.append(Room('Room 1', 20, 20, 120, 80, self.overviewTab, self.floorplanView, self.roomOptionsComboBox))

    def saveFloorplan(self):
        _translate = QtCore.QCoreApplication.translate
        self.saveFloorplanButton.setText(_translate("MainWindow", "Floorplan Saved!"))

    def loadFloorplan(self):
        1
 
    def newFloorplan(self):
        1

    def updateRoomDimensions(self):
        for room in self.rooms:
            if room.roomName == self.roomOptionsComboBox.currentText():
                self.floorplanView.setCurrentIndex(1)
                room.ovRoomView.move(
                    int(self.roomXBox.value()), (self.roomYBox.value())
                )
                room.ovRoomView.resize(
                    int(self.roomWBox.value()), (self.roomHBox.value())
                )
                self.floorplanView.setCurrentIndex(0)

    def updateRoomOptions(self):
        for room in self.rooms:
            if room.roomName == self.roomOptionsComboBox.currentText():
                self.roomXBox.setProperty("value", room.x)
                self.roomYBox.setProperty("value", room.y)
                self.roomWBox.setProperty("value", room.width)
                self.roomHBox.setProperty("value", room.height)

    def addRoom(self):
        newRoomText = self.textEdit.toPlainText()
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
        self.roomOptionsComboBox.currentIndexChanged.connect(self.updateRoomOptions)
        self.roomXBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomYBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomWBox.valueChanged.connect(self.updateRoomDimensions)
        self.roomHBox.valueChanged.connect(self.updateRoomDimensions)
