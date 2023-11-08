from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QRectF
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


class Room(QGraphicsItem):
    def __init__(self, x, y, width, height, name, color=QColor(224, 222, 209)):
        """
        Width and height are in CM (one cm is one pixel I think)
        """
        super().__init__()
        self.name = name
        self.color = color
        self.selected = False
        self.rect = QRectF(x, y, width, height)

    from PyQt5.QtGui import QPen

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

    def changePositon(self, x, y):
        self.rect = QRectF(x, y, self.rect.width(), self.rect.height())

    def changeSize(self, width, height):
        self.rect = QRectF(self.rect.x(), self.rect.y(), width, height)
