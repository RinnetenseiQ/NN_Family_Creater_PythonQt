import json
import socket
import sys
import time
from collections import deque
from threading import Thread

import qdarkstyle
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtWidgets import QFileDialog, QWidget, QHBoxLayout, QLabel, QPushButton, QProgressBar, QListWidgetItem, \
    QSizePolicy, QToolButton

from Algorithms.GeneticProgram import GeneticProgramProcess
from Forms.Parents.start_page_gui_parent import Ui_StartPageWindow
from Forms.c2d_gui import MainWindow
from Forms.plot_ui import PlotWindow
from Forms.predict_c2d_gui import PredictC2DWindow
from Forms.task_manager_gui import TasksWindow
from Project_controller import Project_controller


class StartPageWindow(QtWidgets.QMainWindow, Ui_StartPageWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()

        self.plots_window = PlotWindow()
        self.setupUi(self)
        self.settings = QSettings()
        self.loadSettings()
        self.initWidgets()

        self.project_controllers: list = []
        self.project_queue = deque([])
        # self.active_project_controllers = []
        # self.queue_project_controllers = []
        # self.archive_project_controllers = []
        # self.project_controller = Project_controller()
        # self.project_controllers.append(Project_controller())

        self.paramsQueue = deque([])

        # self.tasks_window = TasksWindow(self.plots_window, self.paramsQueue, self.active_project_controllers)

        queue_program_thread = QueueProgramThread(self.paramsQueue)
        queue_program_thread.start()

        self.show()

    def initWidgets(self):
        create_tab_list = ["Optimizing",
                           "Application",
                           "Custom"]
        modes_tab_list = ["Active projects",
                          "Archive projects",
                          "Queue",
                          "Create project",
                          "Predict"]
        output_tab_labels = ["Output 1",
                             "Output 2",
                             "Erroneous output"]
        for i in range(len(create_tab_list)):
            self.tabWidget.setTabText(i, create_tab_list[i])
        self.tabWidget.setCurrentIndex(0)

        for i in range(len(modes_tab_list)):
            self.modes_TW.setTabText(i, modes_tab_list[i])
        self.modes_TW.setCurrentIndex(0)

        for i in range(len(output_tab_labels)):
            self.output_TW.setTabText(i, output_tab_labels[i])
        self.output_TW.setCurrentIndex(0)

        # self.archive_projects_LW
        #####Test#####
        # self.test_pc = Project_controller(mode=Project_controller.C2D_IMG_CLF_GEN, plot_ui=self.plots_window)
        # self.item = QListWidgetItem(self.active_projects_LW)
        # self.active_projects_LW.addItem(self.item)
        # self.test_pc.name = "testteteteteteteteteteteteetet"
        # self.row = Project_Viewer(self.test_pc)
        # self.item.setSizeHint(self.row.minimumSizeHint())
        # self.active_projects_LW.setItemWidget(self.item, self.row)
        ##############

        self.opt_project_type_CB.addItems(["Convolutional 2D NN"])
        self.opt_method_CB.addItems(["Genetic optimize", "Immune optimize", "Custom"])
        self.app_model_CB.addItems(["ResNet50V2", "VGG19"])
        self.predict_problem_CB.addItems(["classification", "regression", "clasterization"])
        self.predict_datatype_CB.addItems(["2D (image)", "3D (video)", "1D (timesteps)", "text", "DataFrame"])

        self.opt_open_Btn.clicked.connect(self.open_Btn_Click)
        self.opt_create_Btn.clicked.connect(self.create_Btn_Click)
        self.pushButton_3.clicked.connect(self.task_Btn_Click)
        self.dataset_path_TB.clicked.connect(self.app_dataset_path_Btn_clicked)
        self.saveTo_TB.clicked.connect(self.app_saveTo_Bnt_Clicked)
        self.app_create_Btn.clicked.connect(self.app_create_Btn_Clicked)
        self.predict_letsgo_Btn.clicked.connect(self.predict_lets_go_Btn_Clicked)

    def loadSettings(self):
        self.app_dataset_path_LE.setText(self.settings.value("app_datasetPath", "C:/", type=str))
        self.saveTo_path_LE.setText(self.settings.value("custom_model_path", "C:/", type=str))

    def create_Btn_Click(self):
        if self.opt_project_type_CB.currentIndex() == 0:
            if self.opt_method_CB.currentIndex() == 0:
                self.create_project_controller(Project_controller.C2D_IMG_CLF_GEN, self.opt_project_name_LE.text())
                print("")
                # self.c2d_window = MainWindow(self.paramsQueue, self.active_project_controllers[-1])
                # self.c2d_window.show()
                pass
                # self.hide()

        pass

    def create_project_controller(self, mode, name):
        temp_project_controller = Project_controller(mode=mode,
                                                     project_name=name,
                                                     plot_ui=self.plots_window)
        temp_project_controller.is_shown = True
        temp_project_controller.socket_port = self.get_uniq_socket_port()
        self.project_controllers.append(temp_project_controller)
        self.update_projects_list()

    def get_uniq_socket_port(self):
        ports = []
        for i in self.project_controllers:
            ports.append(i.socket_port)
        max_port = max(ports)

        return max_port + 1

        pass

    def update_projects_list(self):
        # for index in self.project_controllers
        if len(self.project_controllers) == 0: return
        self.active_projects_LW.clear()
        self.archive_projects_LW.clear()
        self.queue_projects_LW.clear()
        for index in range(len(self.project_controllers)):
            row = Project_Viewer(self.project_controllers[index])

            if self.project_controllers[index].is_shown:
                item = QListWidgetItem(self.active_projects_LW)
                item.setSizeHint(row.minimumSizeHint())
                self.active_projects_LW.addItem(item)
                self.active_projects_LW.setItemWidget(item, row)
            else:
                item = QListWidgetItem(self.archive_projects_LW)
                item.setSizeHint(self.row.minimumSizeHint())
                self.archive_projects_LW.addItem(item)
                self.archive_projects_LW.setItemWidget(item, row)

            if self.project_controllers[index].is_in_queue:
                item = QListWidgetItem(self.queue_projects_LW)
                item.setSizeHint(self.row.minimumSizeHint())
                self.queue_projects_LW.addItem(item)
                self.queue_projects_LW.setItemWidget(item, row)
            # item = QListWidgetItem()
        # self.item = QListWidgetItem(self.active_projects_LW)
        # self.active_projects_LW.addItem(self.item)
        # self.test_pc.name = "testteteteteteteteteteteteetet"
        # self.row = Project_Viewer(self.test_pc)
        # self.item.setSizeHint(self.row.minimumSizeHint())
        # self.active_projects_LW.setItemWidget(self.item, self.row)
        pass

    def open_Btn_Click(self):
        pass

    def task_Btn_Click(self):
        self.tasks_window.show()
        pass

    def app_dataset_path_Btn_clicked(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get Dataset folder",
                                                   self.settings.value("app_datasetPath", "C:/", type=str))
        if dirlist == "":
            self.app_dataset_path_LE.setText(self.settings.value("app_datasetPath", "C:/", type=str))
        else:
            self.app_dataset_path_LE.setText(dirlist)
            self.settings.setValue("app_datasetPath", dirlist)
            self.settings.sync()

    def app_saveTo_Bnt_Clicked(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get folder to save model",
                                                   self.settings.value("custom_model_path", "C:/", type=str))
        if dirlist == "":
            self.saveTo_path_LE.setText(self.settings.value("custom_model_path", "C:/", type=str))
        else:
            self.saveTo_path_LE.setText(dirlist)
            self.settings.setValue("custom_model_path", dirlist)
            self.settings.sync()

    def app_create_Btn_Clicked(self):
        if self.app_model_CB.currentText() == 0:
            params = {"model": "ResNet50V2",
                      "datapath": self.app_dataset_path_LE.text(),
                      "save_to": self.saveTo_path_LE.text(),
                      "project_name": self.app_project_name_LE.text()}
            self.paramsQueue.append(params)

            pass

    def predict_lets_go_Btn_Clicked(self):
        self.predict_window = None
        # predict_mode = (self.predict_problem_CB.currentText() == 0) and (self.predict_datatype_CB.currentText() == 0)
        if (self.predict_problem_CB.currentIndex() == 0) and (self.predict_datatype_CB.currentIndex() == 0):
            self.predict_window = PredictC2DWindow()
        self.predict_window.show()

        pass

    def selected_item_Changed(self):
        pass


class QueueProgramThread(Thread):
    def __init__(self, params_queue: deque):
        super().__init__()
        self.params_queue = params_queue

    def run(self):
        # while len(self.chromosome_params_queue) > 0:
        #
        while True:
            if len(self.params_queue) != 0:
                prog = None
                params = self.params_queue.popleft()
                if params.__class__.__name__ == "C2D_ChromosomeParams":
                    prog = GeneticProgramProcess(params)
                elif type(params) == dict:
                    pass
                elif params == "custom":  # переделать под custom
                    pass

                prog.run()
                # процесс стопит поток или нет? Yes
            else:
                time.sleep(1)


class Project_Viewer(QWidget):
    def __init__(self, project_controller: Project_controller, parent: StartPageWindow=None):
        super(Project_Viewer, self).__init__(parent)
        self.parent_window = parent
        self.project_controller = project_controller

        if len(self.project_controller.name) > 15:
            self.hint = True
            self.shown_name = self.project_controller.name[:13] + "..."
        else:
            self.hint = False
            self.shown_name = self.project_controller.name
        self.name_wiget = QLabel(self.shown_name)
        if self.hint: self.name_wiget.setToolTip(self.project_controller.name)

        self.project_type = QLabel(str(self.project_controller.mode))
        self.progress_bar_widget = QProgressBar()
        self.progress_bar_widget.setValue(self.project_controller.progress_percent)

        self.play_pause_btn = QPushButton()
        self.play_pause_btn.setIcon(QtGui.QIcon('../Forms/resourses/play_btn.png'))
        self.play_pause_btn.clicked.connect(self.play_pause_btn_Click)

        self.stop_btn = QPushButton()
        self.stop_btn.setIcon(QtGui.QIcon('../Forms/resourses/stop_btn.png'))
        self.stop_btn.clicked.connect(self.stop_btn_Click)

        # self.settings_btn = QPushButton()
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(QtGui.QIcon('../Forms/resourses/settings_btn.png'))
        self.settings_btn.clicked.connect(self.setting_btn_Click)

        self.archive_btn = QPushButton()
        self.archive_btn.setIcon(QtGui.QIcon('../Forms/resourses/archive_btn.png'))
        self.archive_btn.clicked.connect(self.archive_btn_Click)

        self.row = QHBoxLayout()
        self.row.addWidget(self.name_wiget)
        # self.row.addStretch(10)
        self.row.addWidget(self.project_type)
        # self.row.addStretch(10)
        self.row.addWidget(self.progress_bar_widget)
        # self.row.addStretch(10)
        self.row.addWidget(self.settings_btn)
        # self.row.addStretch(1)
        self.row.addWidget(self.archive_btn)
        # self.row.addStretch(1)
        self.row.addWidget(self.stop_btn)
        # self.row.addStretch(1)
        self.row.addWidget(self.play_pause_btn)
        # self.row.addStretch(1)

        self.row.setStretch(0, 10)
        self.row.setStretch(1, 10)
        self.row.setStretch(2, 10)
        self.row.setStretch(3, 1)
        self.row.setStretch(4, 1)
        self.row.setStretch(5, 1)
        self.row.setStretch(6, 1)

        self.setLayout(self.row)

    def setting_btn_Click(self):
        if self.project_controller.mode == Project_controller.C2D_IMG_CLF_GEN:
            # поменять конструктор формы!
            # передавать динамическую ссылку!
            self.project_setting_window = MainWindow(paramsQueue=deque([]),  # какую очередь передавать и передавать ли?
                                                     project_controller=self.project_controller)
        self.project_setting_window.show()

    def stop_btn_Click(self):
        # убрать из очереди
        pass

    def play_pause_btn_Click(self):
        self.project_controller.is_run = not self.project_controller.is_run
        if self.project_controller.is_run:
            self.play_pause_btn.setIcon(QtGui.QIcon('../Forms/resourses/play_btn.png'))
            # сохранить состояние проекта, прекратить обучение

        else:
            self.play_pause_btn.setIcon(QtGui.QIcon('../Forms/resourses/pause_btn.png'))
            # добавить в очередь
            # возможно поменять местами строки

        pass

    def archive_btn_Click(self):
        self.project_controller.is_shown = False
        self.project_controller.is_run = False
        if self.project_controller.is_in_queue:
            self.project_controller.is_in_queue = False
            self.parent_window.project_controllers.remove(self)  # сомнительно


        pass




if __name__ == '__main__':
    # Новый экземпляр QApplication
    # app = QtWidgets.QApplication(sys.argv)
    QCoreApplication.setOrganizationName("QSoft")
    # QCoreApplication.setOrganizationDomain("Settings")
    QCoreApplication.setApplicationName("NN Family Creater")

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    # app.setSt
    # app.setStyle('windowsvista')
    # app.setStyle('Windows')
    # print(QStyleFactory.keys())
    # Сздание инстанса класса
    # graphviz = GraphvizOutput(output_file='graph.png')
    # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
    startWindow = StartPageWindow()
    # Запуск
    sys.exit(app.exec_())
