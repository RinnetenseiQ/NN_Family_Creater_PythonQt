# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Predict_c2d_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PredictC2DWindow(object):
    def setupUi(self, PredictC2DWindow):
        PredictC2DWindow.setObjectName("PredictC2DWindow")
        PredictC2DWindow.resize(914, 635)
        self.centralwidget = QtWidgets.QWidget(PredictC2DWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 611, 521))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        PredictC2DWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PredictC2DWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 914, 25))
        self.menubar.setObjectName("menubar")
        PredictC2DWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PredictC2DWindow)
        self.statusbar.setObjectName("statusbar")
        PredictC2DWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PredictC2DWindow)
        QtCore.QMetaObject.connectSlotsByName(PredictC2DWindow)

    def retranslateUi(self, PredictC2DWindow):
        _translate = QtCore.QCoreApplication.translate
        PredictC2DWindow.setWindowTitle(_translate("PredictC2DWindow", "MainWindow"))
        self.label.setText(_translate("PredictC2DWindow", "TextLabel"))
