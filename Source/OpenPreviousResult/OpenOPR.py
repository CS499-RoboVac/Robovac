from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsPixmapItem,
    QFileDialog,
    QGraphicsScene,
)
import sys
import os

from cv2 import QT_FONT_NORMAL
from Views.ui_opr import Ui_OPRWindow
from Views.ui_prView import Ui_PRViewWindow
from PyQt5.QtWidgets import QGraphicsView
from Common.ResizableGraphicsView import ResizableGraphicsView

# from FloorPlanDesigner.openFPD import fpdWindowApp
import FloorPlanDesigner.openFPD as OpenFPD
import IntroWindow.openIntro as OpenIntro


class oprWindowApp(QMainWindow, Ui_OPRWindow):
    def __init__(self, parent=None):
        super(oprWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.viewers = []
        
    def connectButtons(self):
        self.openFileButton.clicked.connect(self.loadFolder)
        

    def loadFolder(self):
        opts = QFileDialog.Options()
        folderName = QFileDialog.getExistingDirectory(
            self,
            "Load Run",
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Old Runs/",
            options=opts,
        )

        if folderName:
            # Open the PR viewer window with the folder name passed in
            self.viewers.append(oprViewerWindowApp(folderName))


class oprViewerWindowApp(QMainWindow, Ui_PRViewWindow):
    def __init__(self, folderName, parent=None):
        super(oprViewerWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.folderName = folderName
        self.loadFolder()
        self.show()

    def loadFolder(self):
        # Use ResizableGraphicsView instead of QGraphicsView
        self.runView.setScene(QGraphicsScene())
        self.pieChartView.setScene(QGraphicsScene())
        fileName = self.folderName + "/Result_Image.png"
        # Display the Result Image in the runView GraphicsView
        pixmap = QPixmap(fileName)
        if not pixmap.isNull():
            self.runView.setPixmap(pixmap)
        # Display the Message in the MessageLabel
        with open(self.folderName + "/Message.txt") as f:
            Message = f.read()
            self.MessageLabel.setText(Message)
        # Display the Pie Chart in the pieChartView GraphicsView
        fileName = self.folderName + "/Dirt_Pie.png"
        pixmap = QPixmap(fileName)
        if not pixmap.isNull():
            self.pieChartView.setPixmap(pixmap)

