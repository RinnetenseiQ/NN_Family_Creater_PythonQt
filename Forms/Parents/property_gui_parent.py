# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Property_Dlg.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1043, 563)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(410, 520, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 851, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.toolButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 60, 651, 201))
        self.frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame.setObjectName("frame")
        self.gridLayoutWidget = QtWidgets.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 601, 161))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout.addWidget(self.comboBox_3, 2, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)
        self.frame1 = QtWidgets.QFrame(Dialog)
        self.frame1.setGeometry(QtCore.QRect(660, 60, 341, 201))
        self.frame1.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame1.setObjectName("frame1")
        self.widget = QtWidgets.QWidget(self.frame1)
        self.widget.setGeometry(QtCore.QRect(10, 10, 321, 181))
        self.widget.setObjectName("widget")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Directory"))
        self.toolButton.setText(_translate("Dialog", "..."))
        self.pushButton.setText(_translate("Dialog", "Create"))
        self.label_2.setText(_translate("Dialog", "Create \"Directory\" folder at the specified path "))
        self.label_3.setText(_translate("Dialog", "App Theme"))
        self.label_4.setText(_translate("Dialog", "App Style"))
        self.label_5.setText(_translate("Dialog", "Plot Theme"))
