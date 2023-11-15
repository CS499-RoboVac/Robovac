from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsPixmapItem,
    QFileDialog,
    QGraphicsScene,
)
import sys
import os
from Views.ui_opr import Ui_OPRWindow

# from FloorPlanDesigner.openFPD import fpdWindowApp
import FloorPlanDesigner.openFPD as OpenFPD
import IntroWindow.openIntro as OpenIntro


class oprWindowApp(QMainWindow, Ui_OPRWindow):
    def __init__(self, parent=None):
        super(oprWindowApp, self).__init__(parent)
        self.setupUi(self)
        self.connectButtons()
        self.fpds = []
        self.sims = []
        self.main = []
        self.graphicsView.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.graphicsView.scene)

    def openFPD(self):
        self.fpds.append(OpenFPD.fpdWindowApp())
        self.fpds[-1].show()

    def openMain(self):
        self.main.append(OpenIntro.mainWindowApp())
        self.main[-1].show()

    def connectButtons(self):
        self.openFileButton.clicked.connect(self.loadFolder)
        # self.EditFloorPlanButton.clicked.connect(self.openFPD)

    def loadFolder(self):
        opts = QFileDialog.Options()
        folderName = QFileDialog.getExistingDirectory(
            self,
            "Load Run",
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Old Runs/",
            options=opts,
        )
        fileName = folderName + "/Result_Image.png"
        pixmap = QPixmap(fileName)
        if not pixmap.isNull():
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.graphicsView.scene.addItem(pixmap_item)
        with open(folderName + "/Message.txt") as f:
            Message = f.read()
            self.plainTextEdit.setPlainText(Message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = simWindowApp()
    win.show()
    app.exec()
