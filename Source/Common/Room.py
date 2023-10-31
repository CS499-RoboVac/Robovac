# imports
from PyQt5 import QtCore, QtGui, QtWidgets

class Room:
    
    def tabViewResize(self):
        """
        Resizes the tab view of the room based on the room's dimensions.

        Args:
        - None

        Returns:
        - None
        """
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

    def __init__(self, name, x, y, w, h, overview, fpv, combo):
        """
        Initializes a Room object with the given parameters.

        Args:
        - name (str): the name of the room
        - x (int): the x-coordinate of the room's top-left corner
        - y (int): the y-coordinate of the room's top-left corner
        - w (int): the width of the room
        - h (int): the height of the room
        - overview (QtWidgets.QWidget): the widget that displays an overview of the floor plan
        - fpv (QtWidgets.QTabWidget): the tab widget that displays the room's details
        - combo (QtWidgets.QComboBox): the combo box that displays the list of rooms

        Returns:
        - None
        """
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
        self.tabViewResize()
        font = QtGui.QFont()
        font.setKerning(True)
        self.tabRoomView.setFont(font)
        self.tabRoomView.setFrameShape(QtWidgets.QFrame.Box)
        self.tabRoomView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tabRoomView.setLineWidth(1)
        self.tabRoomView.setObjectName(name)
        combo.addItem(name)
        fpv.setCurrentIndex(0)
