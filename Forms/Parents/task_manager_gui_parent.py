# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task_manager_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QueueWindow(object):
    def setupUi(self, QueueWindow):
        QueueWindow.setObjectName("QueueWindow")
        QueueWindow.resize(772, 607)
        self.centralwidget = QtWidgets.QWidget(QueueWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 301, 531))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(290, 10, 21, 531))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(320, 10, 451, 22))
        self.comboBox.setObjectName("comboBox")
        self.optimizin_output_TE = QtWidgets.QTextEdit(self.centralwidget)
        self.optimizin_output_TE.setGeometry(QtCore.QRect(320, 40, 451, 541))
        self.optimizin_output_TE.setReadOnly(True)
        self.optimizin_output_TE.setObjectName("optimizin_output_TE")
        self.errorneous_output_TE = QtWidgets.QTextEdit(self.centralwidget)
        self.errorneous_output_TE.setGeometry(QtCore.QRect(100, 600, 101, 91))
        self.errorneous_output_TE.setReadOnly(True)
        self.errorneous_output_TE.setObjectName("errorneous_output_TE")
        self.chr_output_TE = QtWidgets.QTextEdit(self.centralwidget)
        self.chr_output_TE.setGeometry(QtCore.QRect(10, 600, 91, 91))
        self.chr_output_TE.setReadOnly(True)
        self.chr_output_TE.setObjectName("chr_output_TE")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 540, 301, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clear_Btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.clear_Btn.setObjectName("clear_Btn")
        self.horizontalLayout.addWidget(self.clear_Btn)
        self.pause_Btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pause_Btn.setObjectName("pause_Btn")
        self.horizontalLayout.addWidget(self.pause_Btn)
        self.plots_Btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.plots_Btn.setObjectName("plots_Btn")
        self.horizontalLayout.addWidget(self.plots_Btn)
        QueueWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(QueueWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 772, 25))
        self.menubar.setObjectName("menubar")
        QueueWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(QueueWindow)
        self.statusbar.setObjectName("statusbar")
        QueueWindow.setStatusBar(self.statusbar)

        self.retranslateUi(QueueWindow)
        QtCore.QMetaObject.connectSlotsByName(QueueWindow)

    def retranslateUi(self, QueueWindow):
        _translate = QtCore.QCoreApplication.translate
        QueueWindow.setWindowTitle(_translate("QueueWindow", "Task Manager"))
        self.clear_Btn.setText(_translate("QueueWindow", "Clear"))
        self.pause_Btn.setText(_translate("QueueWindow", "Pause"))
        self.plots_Btn.setText(_translate("QueueWindow", "Plots"))
