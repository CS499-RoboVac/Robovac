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
    QGraphicsEllipseItem,
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
        return f'{type(self).__name__}"{self.name}" self.pos: ({self.pos().x()}, {self.pos().y()}) rect: ({self.rect.x()}, {self.rect.y()}, {self.rect.width()}, {self.rect.height()})'

    def __str__(self) -> str:
        return f'{type(self).__name__}"{self.name}" where rect is ({self.rect.x()}, {self.rect.y()}, {self.rect.width()}, {self.rect.height()}) \n and self.pos is ({self.pos().x()}, {self.pos().y()})'


# Chest class, inherits from Room it's basically the same thing, but with a different color
class Chest(Room):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name, QColor(100, 100, 0))


class TableLeg(Room):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name, QColor(33, 39, 209))

    def paint(self, painter, option, widget):
        if self.selected:
            painter.setPen(QColor(0, 0, 0))
        else:
            pen = QPen()
            pen.setStyle(QtCore.Qt.NoPen)
            painter.setPen(pen)

        painter.setBrush(self.color)  # Set the fill color
        painter.drawEllipse(self.rect)


# TableTop class, This is like a room, but it's semitransparent and it has 4 TableLeg objects
class TableTop(Room):
    def __init__(self, x, y, width, height, name, tableLegs=None):
        super().__init__(x, y, width, height, name, QColor(33, 39, 209))
        if tableLegs is None:
            # If we don't have any tableLegs, we create them
            self.tableLegs = [
                TableLeg(x, y, 10, 10, f"{name} Leg1"),
                TableLeg(x + width - 10, y, 10, 10, f"{name} Leg2"),
                TableLeg(x, y + height - 10, 10, 10, f"{name} Leg3"),
                TableLeg(x + width - 10, y + height - 10, 10, 10, f"{name} Leg4"),
            ]
        else:
            # If we do have tableLegs, we set them to the ones we have
            self.tableLegs = tableLegs

    def paint(self, painter, option, widget):
        if self.selected:
            painter.setPen(QColor(0, 0, 0))
        else:
            pen = QPen()
            pen.setStyle(QtCore.Qt.NoPen)
            painter.setPen(pen)

        painter.setBrush(self.color)
        painter.setOpacity(0.5)
        painter.drawRect(self.rect)

    def changeSize(self, width, height):
        """
        Changes the size of the table top, and moves the table legs to the correct position
        based on the new size of the table top
        """
        super().changeSize(width, height)
        self.tableLegs[0].setPos(self.pos().x(), self.pos().y())
        self.tableLegs[1].setPos(
            self.pos().x() + self.rect.width() - 10, self.pos().y()
        )
        self.tableLegs[2].setPos(
            self.pos().x(), self.pos().y() + self.rect.height() - 10
        )
        self.tableLegs[3].setPos(
            self.pos().x() + self.rect.width() - 10,
            self.pos().y() + self.rect.height() - 10,
        )

    def itemChange(self, change, value):
        """
        When this item is moved, we update the flag to indicate that it has been Changed
        """
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.hasChanged = True
            # We also have to move the tableLegs
            self.tableLegs[0].setPos(self.pos().x(), self.pos().y())
            self.tableLegs[1].setPos(
                self.pos().x() + self.rect.width() - 10, self.pos().y()
            )
            self.tableLegs[2].setPos(
                self.pos().x(), self.pos().y() + self.rect.height() - 10
            )
            self.tableLegs[3].setPos(
                self.pos().x() + self.rect.width() - 10,
                self.pos().y() + self.rect.height() - 10,
            )

        return super().itemChange(change, value)
