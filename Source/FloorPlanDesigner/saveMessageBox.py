from PyQt5.QtWidgets import QMessageBox

class SaveMessageBox(QMessageBox):
    """
    A custom message box with Yes, No, and Cancel buttons.
    The X button behaves like the Cancel button, so the cancelbtn function should also close the message box.
    """
    def __init__(self, parent=None, message="Save Floorplan?", title="Save Floorplan?", yesbtn=None, nobtn=None, cancelbtn=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Question)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        self.setDefaultButton(QMessageBox.Yes)
        self.connectButtons(yesbtn, nobtn, cancelbtn)
        

    def connectButtons(self, yesbtn, nobtn, cancelbtn):
        self.yesbtn = yesbtn
        self.nobtn = nobtn
        self.cancelbtn = cancelbtn
        # if the user clicks the yes button, return 1
        self.button(QMessageBox.Yes).clicked.connect(yesbtn)
        # if the user clicks the X button, return -1
        self.button(QMessageBox.Cancel).clicked.connect(cancelbtn)
        # if the user clicks the no button, return 0
        self.button(QMessageBox.No).clicked.connect(nobtn)
        
    def closeEvent(self, event):
        # Override the close behavior here
        self.cancelbtn()
        
