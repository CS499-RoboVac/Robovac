# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'floorplandesigner.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FPDWindow(object):
    def setupUi(self, FPDWindow):
        FPDWindow.setObjectName("FPDWindow")
        FPDWindow.resize(1010, 824)
        self.centralwidget = QtWidgets.QWidget(FPDWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.MenuVLayout = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MenuVLayout.sizePolicy().hasHeightForWidth())
        self.MenuVLayout.setSizePolicy(sizePolicy)
        self.MenuVLayout.setObjectName("MenuVLayout")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.MenuVLayout)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.FloorPlanButtonLayout = QtWidgets.QWidget(self.MenuVLayout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FloorPlanButtonLayout.sizePolicy().hasHeightForWidth()
        )
        self.FloorPlanButtonLayout.setSizePolicy(sizePolicy)
        self.FloorPlanButtonLayout.setObjectName("FloorPlanButtonLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.FloorPlanButtonLayout)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.BackButton = QtWidgets.QPushButton(self.FloorPlanButtonLayout)
        self.BackButton.setMinimumSize(QtCore.QSize(100, 0))
        self.BackButton.setObjectName("BackButton")
        self.verticalLayout_6.addWidget(self.BackButton)
        self.newFloorplanButton = QtWidgets.QPushButton(self.FloorPlanButtonLayout)
        self.newFloorplanButton.setObjectName("newFloorplanButton")
        self.verticalLayout_6.addWidget(self.newFloorplanButton)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.saveFloorplanButton = QtWidgets.QPushButton(self.FloorPlanButtonLayout)
        self.saveFloorplanButton.setObjectName("saveFloorplanButton")
        self.horizontalLayout_8.addWidget(self.saveFloorplanButton)
        self.loadFloorplanButton = QtWidgets.QPushButton(self.FloorPlanButtonLayout)
        self.loadFloorplanButton.setObjectName("loadFloorplanButton")
        self.horizontalLayout_8.addWidget(self.loadFloorplanButton)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.verticalLayout_7.addWidget(self.FloorPlanButtonLayout)
        self.AddItemMenuLayout_2 = QtWidgets.QWidget(self.MenuVLayout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.AddItemMenuLayout_2.sizePolicy().hasHeightForWidth()
        )
        self.AddItemMenuLayout_2.setSizePolicy(sizePolicy)
        self.AddItemMenuLayout_2.setObjectName("AddItemMenuLayout_2")
        self.AddItemMenuLayout = QtWidgets.QVBoxLayout(self.AddItemMenuLayout_2)
        self.AddItemMenuLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.AddItemMenuLayout.setObjectName("AddItemMenuLayout")
        self.OverviewTextLabel = QtWidgets.QLabel(self.AddItemMenuLayout_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.OverviewTextLabel.sizePolicy().hasHeightForWidth()
        )
        self.OverviewTextLabel.setSizePolicy(sizePolicy)
        self.OverviewTextLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.OverviewTextLabel.setObjectName("OverviewTextLabel")
        self.AddItemMenuLayout.addWidget(self.OverviewTextLabel)
        self.textEdit = QtWidgets.QTextEdit(self.AddItemMenuLayout_2)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 41))
        self.textEdit.setObjectName("textEdit")
        self.AddItemMenuLayout.addWidget(self.textEdit)
        self.AddItemButtonLayout = QtWidgets.QVBoxLayout()
        self.AddItemButtonLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint
        )
        self.AddItemButtonLayout.setSpacing(5)
        self.AddItemButtonLayout.setObjectName("AddItemButtonLayout")
        self.RoomFurnLayout = QtWidgets.QHBoxLayout()
        self.RoomFurnLayout.setSpacing(6)
        self.RoomFurnLayout.setObjectName("RoomFurnLayout")
        self.addRoomButton = QtWidgets.QPushButton(self.AddItemMenuLayout_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.addRoomButton.sizePolicy().hasHeightForWidth()
        )
        self.addRoomButton.setSizePolicy(sizePolicy)
        self.addRoomButton.setMinimumSize(QtCore.QSize(115, 30))
        self.addRoomButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.addRoomButton.setObjectName("addRoomButton")
        self.RoomFurnLayout.addWidget(self.addRoomButton)
        self.addFurnitureButton = QtWidgets.QPushButton(self.AddItemMenuLayout_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.addFurnitureButton.sizePolicy().hasHeightForWidth()
        )
        self.addFurnitureButton.setSizePolicy(sizePolicy)
        self.addFurnitureButton.setMinimumSize(QtCore.QSize(115, 30))
        self.addFurnitureButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.addFurnitureButton.setObjectName("addFurnitureButton")
        self.RoomFurnLayout.addWidget(self.addFurnitureButton)
        self.AddItemButtonLayout.addLayout(self.RoomFurnLayout)
        self.DoorChestLayout = QtWidgets.QHBoxLayout()
        self.DoorChestLayout.setObjectName("DoorChestLayout")
        self.addDoorButton = QtWidgets.QPushButton(self.AddItemMenuLayout_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.addDoorButton.sizePolicy().hasHeightForWidth()
        )
        self.addDoorButton.setSizePolicy(sizePolicy)
        self.addDoorButton.setMinimumSize(QtCore.QSize(115, 30))
        self.addDoorButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.addDoorButton.setObjectName("addDoorButton")
        self.DoorChestLayout.addWidget(self.addDoorButton)
        self.addChestButton = QtWidgets.QPushButton(self.AddItemMenuLayout_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.addChestButton.sizePolicy().hasHeightForWidth()
        )
        self.addChestButton.setSizePolicy(sizePolicy)
        self.addChestButton.setMinimumSize(QtCore.QSize(115, 30))
        self.addChestButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.addChestButton.setObjectName("addChestButton")
        self.DoorChestLayout.addWidget(self.addChestButton)
        self.AddItemButtonLayout.addLayout(self.DoorChestLayout)
        self.AddItemMenuLayout.addLayout(self.AddItemButtonLayout)
        self.verticalLayout_7.addWidget(self.AddItemMenuLayout_2)
        self.DimensionTextLabel = QtWidgets.QLabel(self.MenuVLayout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.DimensionTextLabel.sizePolicy().hasHeightForWidth()
        )
        self.DimensionTextLabel.setSizePolicy(sizePolicy)
        self.DimensionTextLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.DimensionTextLabel.setObjectName("DimensionTextLabel")
        self.verticalLayout_7.addWidget(self.DimensionTextLabel)
        self.ItemDimVLayout = QtWidgets.QVBoxLayout()
        self.ItemDimVLayout.setObjectName("ItemDimVLayout")
        self.roomOptionsComboBox = QtWidgets.QComboBox(self.MenuVLayout)
        self.roomOptionsComboBox.setEditable(False)
        self.roomOptionsComboBox.setObjectName("roomOptionsComboBox")
        self.ItemDimVLayout.addWidget(self.roomOptionsComboBox)
        self.WidthLayout = QtWidgets.QHBoxLayout()
        self.WidthLayout.setObjectName("WidthLayout")
        self.roomWLabel = QtWidgets.QLabel(self.MenuVLayout)
        self.roomWLabel.setObjectName("roomWLabel")
        self.WidthLayout.addWidget(self.roomWLabel)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.WidthLayout.addItem(spacerItem)
        self.roomWBox = QtWidgets.QSpinBox(self.MenuVLayout)
        self.roomWBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roomWBox.sizePolicy().hasHeightForWidth())
        self.roomWBox.setSizePolicy(sizePolicy)
        self.roomWBox.setMinimumSize(QtCore.QSize(105, 25))
        self.roomWBox.setMinimum(2)
        self.roomWBox.setMaximum(99999999)
        self.roomWBox.setSingleStep(1)
        self.roomWBox.setProperty("value", 10)
        self.roomWBox.setObjectName("roomWBox")
        self.WidthLayout.addWidget(self.roomWBox)
        self.ItemDimVLayout.addLayout(self.WidthLayout)
        self.HeightLayout = QtWidgets.QHBoxLayout()
        self.HeightLayout.setObjectName("HeightLayout")
        self.roomHLabel = QtWidgets.QLabel(self.MenuVLayout)
        self.roomHLabel.setObjectName("roomHLabel")
        self.HeightLayout.addWidget(self.roomHLabel)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.HeightLayout.addItem(spacerItem1)
        self.roomHBox = QtWidgets.QSpinBox(self.MenuVLayout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roomHBox.sizePolicy().hasHeightForWidth())
        self.roomHBox.setSizePolicy(sizePolicy)
        self.roomHBox.setMinimumSize(QtCore.QSize(105, 25))
        self.roomHBox.setMinimum(2)
        self.roomHBox.setMaximum(9999999)
        self.roomHBox.setSingleStep(1)
        self.roomHBox.setProperty("value", 10)
        self.roomHBox.setObjectName("roomHBox")
        self.HeightLayout.addWidget(self.roomHBox)
        self.ItemDimVLayout.addLayout(self.HeightLayout)
        self.verticalLayout_7.addLayout(self.ItemDimVLayout)
        self.SimButtonLayout = QtWidgets.QHBoxLayout()
        self.SimButtonLayout.setObjectName("SimButtonLayout")
        self.verticalLayout_7.addLayout(self.SimButtonLayout)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_7.addItem(spacerItem2)
        self.gridLayout.addWidget(self.MenuVLayout, 0, 0, 1, 1)
        self.GraphicViewVLayout = QtWidgets.QVBoxLayout()
        self.GraphicViewVLayout.setObjectName("GraphicViewVLayout")
        self.FPDTitleHLayout = QtWidgets.QHBoxLayout()
        self.FPDTitleHLayout.setObjectName("FPDTitleHLayout")
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.FPDTitleHLayout.addItem(spacerItem3)
        self.FloorPlanNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.FloorPlanNameLabel.setObjectName("FloorPlanNameLabel")
        self.FPDTitleHLayout.addWidget(self.FloorPlanNameLabel)
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.FPDTitleHLayout.addItem(spacerItem4)
        self.GraphicViewVLayout.addLayout(self.FPDTitleHLayout)
        self.FPDGraphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.FPDGraphicsView.setObjectName("FPDGraphicsView")
        self.GraphicViewVLayout.addWidget(self.FPDGraphicsView)
        self.gridLayout.addLayout(self.GraphicViewVLayout, 0, 1, 1, 1)
        FPDWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(FPDWindow)
        QtCore.QMetaObject.connectSlotsByName(FPDWindow)

    def retranslateUi(self, FPDWindow):
        _translate = QtCore.QCoreApplication.translate
        FPDWindow.setWindowTitle(_translate("FPDWindow", "Floor Plan Designer"))
        self.BackButton.setText(_translate("FPDWindow", "Exit Floor Plan Designer"))
        self.newFloorplanButton.setText(_translate("FPDWindow", "Create New Floorplan"))
        self.saveFloorplanButton.setText(_translate("FPDWindow", "Save Plan"))
        self.loadFloorplanButton.setText(_translate("FPDWindow", "Load Plan"))
        self.OverviewTextLabel.setText(_translate("FPDWindow", "Overview"))
        self.textEdit.setPlaceholderText(_translate("FPDWindow", "Room Name"))
        self.addRoomButton.setText(_translate("FPDWindow", "Add Room"))
        self.addFurnitureButton.setText(_translate("FPDWindow", "Add Table"))
        self.addDoorButton.setText(_translate("FPDWindow", "Add Door"))
        self.addChestButton.setText(_translate("FPDWindow", "Add Chest"))
        self.DimensionTextLabel.setText(_translate("FPDWindow", "Dimension"))
        self.roomWLabel.setText(_translate("FPDWindow", "Item Width"))
        self.roomWBox.setSuffix(_translate("FPDWindow", " ft"))
        self.roomHLabel.setText(_translate("FPDWindow", "Item Height"))
        self.roomHBox.setSuffix(_translate("FPDWindow", " ft"))
        self.FloorPlanNameLabel.setText(_translate("FPDWindow", "Floor Plan:"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    FPDWindow = QtWidgets.QMainWindow()
    ui = Ui_FPDWindow()
    ui.setupUi(FPDWindow)
    FPDWindow.show()
    sys.exit(app.exec_())
