import typing
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QRectF, Qt
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
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

# Import random for random numbers
import random
from Common.Util import Vec2


class Room(QGraphicsItem):
    def __init__(self, x, y, width, height, name, color=QColor(224, 222, 209)):
        """
        Width and height are in CM (one cm is one pixel I think)
        """
        self.hasChanged = False
        super().__init__()
        self.name = name
        self.color = color
        self.selected = False
        # We have to set the rect's x and y so things are drawn correctly when we set the position
        # but we don't actually want the rect's position to be different, so we set it back to 0, 0
        self.rect = QRectF(x, y, width, height)
        self.setPos(x, y)
        self.rect = QRectF(0, 0, width, height)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        # self.setFlag(QGraphicsItem.ItemIsSelectable)
        # self.setAcceptHoverEvents(True)
        
    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        if self.selected:
            painter.setPen(QColor(0, 0, 0))
        else:
            pen = QPen()
            pen.setStyle(QtCore.Qt.NoPen)
            painter.setPen(pen)

        painter.setBrush(self.color)  # Set the fill color
        painter.drawRect(self.rect)

    def changeSize(self, width, height):
        self.rect = QRectF(self.rect.x(), self.rect.y(), width, height)

    def itemSaved(self):
        """
        When this item is saved, we update the flag to indicate that it has been saved
        """
        self.hasChanged = False


    def itemChange(self, change, value):
        """
        When this item is moved, we update the flag to indicate that it has been Changed
        """
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.hasChanged = True
            
        return super().itemChange(change, value)
    
    def __repr__(self) -> str:
                return f"{type(self).__name__}\"{self.name}\" self.pos: ({self.pos().x()}, {self.pos().y()}) rect: ({self.rect.x()}, {self.rect.y()}, {self.rect.width()}, {self.rect.height()})"
    
    def __str__(self) -> str:
        return f"{type(self).__name__}\"{self.name}\" where rect is ({self.rect.x()}, {self.rect.y()}, {self.rect.width()}, {self.rect.height()}) \n and self.pos is ({self.pos().x()}, {self.pos().y()})"
    

# Chest class, inherits from Room it's basically the same thing, but with a different color
class Chest(Room):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name, QColor(100, 100, 0))
    

class Table(QGraphicsItem):
    def __init__(self, pos, dim, parent):
        super(Chest, self).__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.hasChanged = False
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.rect = QRectF(0, 0, dim.x, dim.y)
        self.setPos(pos.x, pos.y)
        self.name = ""
        self.corners = []

    def paint(self, painter, option, widget):
        painter.setBrush(QColor(100, 100, 0))  # Set the fill color
        painter.drawRect(self.rect)

    def boundingRect(self):
        return self.rect
    
    def itemSaved(self):
        """
        When this item is saved, we update the flag to indicate that it has been saved
        """
        self.hasChanged = False

    def itemChange(self, change, value):
        """
        When this item is moved, we update the flag to indicate that it has been Changed
        """
        if self.hasChanged is False and change == QGraphicsItem.ItemPositionHasChanged:
            self.hasChanged = True
        return super().itemChange(change, value)
