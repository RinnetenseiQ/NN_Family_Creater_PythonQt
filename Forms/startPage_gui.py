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
    QSizePolicy, QToolButton, QFrame, QListWidget

from MPL_Canvas import MyMplCanvas
from master.Algorithms.GeneticProgram import GeneticProgramProcess, GeneticProgram
from Forms.Parents.start_page_gui_parent import Ui_StartPageWindow
from Forms.c2d_gui import MainWindow
from Forms.plot_ui import PlotWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as Toolbar
from Forms.predict_c2d_gui import PredictC2DWindow
from Forms.task_manager_gui import TasksWindow
from Project_controller import Project_controller

from tensorboard import program



class StartPageWindow(QtWidgets.QMainWindow, Ui_StartPageWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()

        # self.plots_window = PlotWindow()
        self.setupUi(self)
        self.settings = QSettings()
        self.loadSettings()
        self.initWidgets()

        self.selected_pc: Project_controller = None

        self.project_controllers: list = []
        self.project_queue = deque([])
        # self.active_project_controllers = []
        # self.queue_project_controllers = []
        # self.archive_project_controllers = []
        # self.project_controller = Project_controller()
        # self.project_controllers.append(Project_controller())

        # self.paramsQueue = deque([])

        # self.tasks_window = TasksWindow(self.plots_window, self.paramsQueue, self.active_project_controllers)

        queue_program_thread = QueueProgramThread(self.project_queue)
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

        self.active_projects_LW.itemSelectionChanged.connect(self.list_widget_SelectionChanged)
        self.archive_projects_LW.itemSelectionChanged.connect(self.list_widget_SelectionChanged)
        self.queue_projects_LW.itemSelectionChanged.connect(self.list_widget_SelectionChanged)
        # self.active_projects_LW.itemClicked.connect(self.list_widget_SelectionChanged)

        self.init_plot()
        ####### Test #####
        self.opt_project_name_LE.setText("Genetic Project")

    def init_plot(self):
        self.figure = plt.figure()
        self.lineUpping = QtWidgets.QVBoxLayout(self.plot_W)
        self.canvas = MyMplCanvas(self.figure)
        self.lineUpping.addWidget(self.canvas)
        self.toolbar = Toolbar(self.canvas, self)
        self.lineUpping.addWidget(self.toolbar)

    def loadSettings(self):
        self.app_dataset_path_LE.setText(self.settings.value("app_datasetPath", "C:/", type=str))
        self.saveTo_path_LE.setText(self.settings.value("custom_model_path", "C:/", type=str))

    def create_Btn_Click(self):
        if self.opt_project_type_CB.currentIndex() == 0:
            if self.opt_method_CB.currentIndex() == 0:
                self.create_project_controller(Project_controller.C2D_IMG_CLF_GEN, self.opt_project_name_LE.text())
                self.c2d_window = MainWindow(self.project_queue, self.project_controllers[-1])
                self.c2d_window.show()
                pass
                # self.hide()

        pass

    # pyqtSlot
    def add_to_queue(self):
        self.project_queue.append(self)

    def list_widget_SelectionChanged(self):
        list_widget: QListWidget = self.sender()
        # if isinstance(list_widget, self.queue_projects_LW):
        select: QListWidgetItem = list_widget.selectedItems()[0]
        widget = list_widget.itemWidget(select)
        pc_instance = widget.project_controller
        self.selected_pc = pc_instance
        self.update_text()
        self.update_selected_plot()

    def update_output(self, pc_instance):
        if pc_instance is self.selected_pc:
            ###
            #self.update_plot(pc_instance)
            self.update_text()
        pass

    def update_text(self):
        self.output_1_TE.setText(self.selected_pc.optimising_search_output)
        pos_x = self.output_2_TE_2.cursor().pos().x()
        pos_y = self.output_2_TE_2.cursor().pos().y()
        len_old = len(self.output_2_TE_2.toPlainText())
        len_new = len(self.selected_pc.network_output)
        diff = self.selected_pc.network_output[len_old: len_new]
        self.output_2_TE_2.append(diff)
        # self.output_2_TE_2.setText(self.selected_pc.network_output)
        if self.output_2_TE_2.verticalScrollBar().value() != self.output_2_TE_2.verticalScrollBar().maximum():
            self.output_2_TE_2.cursor().pos().setX(pos_x)
            self.output_2_TE_2.cursor().pos().setY(pos_y)
        #TE_2_text = self.output_2_TE_2.toPlainText()
        # if TE_2_text != "":
        #     pos_x = self.output_2_TE_2.cursor().pos().x()
        #     pos_y = self.output_2_TE_2.cursor().pos().y()
        #     self.output_2_TE_2.append(self.selected_pc.network_output.split(TE_2_text)[0])
        #     self.output_2_TE_2.cursor().pos().setX(pos_x)
        #     self.output_2_TE_2.cursor().pos().setY(pos_y)
        # else:
        #     self.output_2_TE_2.append(self.selected_pc.network_output)

        self.erroneous_output_TE.setText(self.selected_pc.erroneus_output)

    def update_plot(self, pc_instance):
        project_controller: Project_controller = self.selected_pc
        if pc_instance is self.selected_pc:
            self.figure.clear()
            if len(project_controller.Assessments) == 0: return
            for i in project_controller.Assessments.columns:
                if i != "epoch":
                    plt.plot(project_controller.Assessments["epoch"].values,
                             project_controller.Assessments[i].values, label=i)
                    plt.scatter(project_controller.Assessments["epoch"].values,
                                project_controller.Assessments[i].values)
            self.canvas.draw()
        pass

    def update_selected_plot(self):
        project_controller: Project_controller = self.selected_pc
        self.figure.clear()
        if len(project_controller.Assessments) == 0: return
        for i in project_controller.Assessments.columns:
            if i != "epoch":
                plt.plot(project_controller.Assessments["epoch"].values,
                         project_controller.Assessments[i].values, label=i)
                plt.scatter(project_controller.Assessments["epoch"].values,
                            project_controller.Assessments[i].values)
        self.canvas.draw()
        pass

    def create_project_controller(self, mode, name):
        temp_project_controller = Project_controller(mode=mode,
                                                     project_name=name)
        temp_project_controller.is_shown = True
        temp_project_controller.communicator.pinok.connect(self.update_output)
        temp_project_controller.communicator.ui_pinok.connect(self.update_plot)
        # temp_project_controller.socket_port = self.get_uniq_socket_port()
        self.project_controllers.append(temp_project_controller)
        #self.update_projects_list()
        self.update_list_viewers("active")

    def get_uniq_socket_port(self):
        ports = []
        for i in self.project_controllers:
            ports.append(i.socket_port)
        max_port = max(ports)

        return max_port + 1

        pass

    def update_list_viewers(self, mode):
        if len(self.project_controllers) == 0: return
        if mode == "active":
            if len(self.active_projects_LW) == 0:
                for pc_instance in self.project_controllers:
                    if pc_instance.is_shown:
                        widget_list = ["name", "type", "plot", "sett", "archive", "toQueue"]
                        self.create_list_row(widget_list, self.active_projects_LW, pc_instance)
            else:
                active_pc = []
                items = []
                for index in range(self.active_projects_LW.count()):
                    items.append(self.active_projects_LW.item(index))

                for item in items:
                    active_pc.append(self.active_projects_LW.itemWidget(item).project_controller)

                for pc_instance in self.project_controllers:
                    if pc_instance in active_pc: continue
                    widget_list = ["name", "type", "plot", "sett", "archive", "toQueue"]
                    self.create_list_row(widget_list, self.active_projects_LW, pc_instance)
        elif mode == "archive":
            if len(self.archive_projects_LW) == 0:
                for pc_instance in self.project_controllers:
                    if not pc_instance.is_shown:
                        widget_list = ["name", "type"]
                        self.create_list_row(widget_list, self.archive_projects_LW, pc_instance)
            else:
                archive_pc = []
                items = []
                for index in range(self.active_projects_LW.count()):
                    items.append(self.active_projects_LW.item(index))

                for item in items:
                    archive_pc.append(self.archive_projects_LW.itemWidget(item).project_controller)

                for pc_instance in self.project_controllers:
                    if pc_instance in archive_pc: continue
                    widget_list = ["name", "type"]
                    self.create_list_row(widget_list, self.archive_projects_LW, pc_instance)
        elif mode == "queue":
            if len(self.queue_projects_LW) == 0:
                for pc_instance in self.project_controllers:
                    if pc_instance.is_in_queue:
                        widget_list = ["name", "type", "progbar", "plot", "sett", "play_pause", "stop"]
                        self.create_list_row(widget_list, self.queue_projects_LW, pc_instance)
            else:
                queue_pc = []
                items = []
                for index in range(self.queue_projects_LW.count()):
                    items.append(self.queue_projects_LW.item(index))

                for item in items:
                    queue_pc.append(self.queue_projects_LW.itemWidget(item).project_controller)

                for pc_instance in self.project_controllers:
                    if pc_instance in queue_pc: continue
                    widget_list = ["name", "type", "progbar", "plot", "sett", "play_pause", "stop"]
                    self.create_list_row(widget_list, self.queue_projects_LW, pc_instance)

    def create_list_row(self, widget_list, list_widget, pc_instance):
        row = Project_Viewer(pc_instance, parent=self, widget_list=widget_list)
        item = QListWidgetItem(list_widget)
        item.setSizeHint(row.minimumSizeHint())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, row)

    # widget_list = ["name", "type", "plot", "sett", "archive", "toQueue"]
    # row = Project_Viewer(self.project_controllers[index], parent=self, widget_list=widget_list)
    # item = QListWidgetItem(self.active_projects_LW)
    # item.setSizeHint(row.minimumSizeHint())
    # self.active_projects_LW.addItem(item)
    # self.active_projects_LW.setItemWidget(item, row)
    # list_widget: QListWidget = self.sender()
    # # if isinstance(list_widget, self.queue_projects_LW):
    # select: QListWidgetItem = list_widget.selectedItems()[0]
    # widget = list_widget.itemWidget(select)
    # pc_instance = widget.project_controller
    # self.selected_pc = pc_instance
    # self.update_text()
    # self.update_selected_plot()

    def update_projects_list(self):
        # for index in self.project_controllers
        if len(self.project_controllers) == 0: return
        self.active_projects_LW.clear()
        self.archive_projects_LW.clear()
        self.queue_projects_LW.clear()

        # for index in range(len(self.project_controllers)):

        for index in range(len(self.project_controllers)):
            # row = Project_Viewer(self.project_controllers[index])

            if self.project_controllers[index].is_shown:
                widget_list = ["name", "type", "plot", "sett", "archive", "toQueue"]
                row = Project_Viewer(self.project_controllers[index], parent=self, widget_list=widget_list)
                item = QListWidgetItem(self.active_projects_LW)
                item.setSizeHint(row.minimumSizeHint())
                self.active_projects_LW.addItem(item)
                self.active_projects_LW.setItemWidget(item, row)
            else:
                widget_list = ["name", "type", "toQueue"]
                row = Project_Viewer(self.project_controllers[index], parent=self, widget_list=widget_list)
                item = QListWidgetItem(self.archive_projects_LW)
                item.setSizeHint(row.minimumSizeHint())
                self.archive_projects_LW.addItem(item)
                self.archive_projects_LW.setItemWidget(item, row)

            if self.project_controllers[index].is_in_queue:
                widget_list = ["name", "type", "progbar", "plot", "sett", "play_pause", "stop"]
                row = Project_Viewer(self.project_controllers[index], parent=self, widget_list=widget_list)
                item = QListWidgetItem(self.queue_projects_LW)
                item.setSizeHint(row.minimumSizeHint())
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
            # self.paramsQueue.append(params)

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

    def __init__(self, project_queue: deque):
        super().__init__()
        self.project_queue = project_queue

    def run(self):
        # while len(self.chromosome_params_queue) > 0:
        #
        while True:
            if len(self.project_queue) != 0:
                project_controller = self.project_queue.popleft()
                project_controller.is_run = True
                # sock, port = project_controller.get_socket()
                net_sock, net_port, gen_sock, gen_port = project_controller.get_socket()
                # project_controller.listen(net_sock, gen_sock)
                project_controller.listen3(net_sock, gen_sock)

                # port = project_controller.
                print("start")
                genetic_program = GeneticProgram(project_controller, net_port, gen_port)
                genetic_program.run()
                print("end")
                # prog = GeneticProgramProcess(project_controller.params)
                # elif type(params) == dict:
                #     pass
                # elif params == "custom":  # переделать под custom
                #     pass
                # процесс стопит поток или нет? Yes

            else:
                time.sleep(1)


class Project_Viewer(QWidget):
    def __init__(self, project_controller: Project_controller, parent: StartPageWindow = None, widget_list=None):
        super(Project_Viewer, self).__init__(parent)
        self.widget_list = widget_list or ["name", "sett", "toQueue"]
        self.parent_window = parent
        self.project_controller = project_controller
        self.widgets_dict = {}  # following protocol

        # "name" - name of project: QLabel
        # "type" - type of project: QLabel
        # "play_pause" - play/pause button: QToolButton
        # "archive" - archive button: QToolButton
        # "sett" - settings of project button: QToolButton
        # "stop" - stop button: QToolButton
        # "progbar" - progress bar: QProgressBar
        # "toQueue" - toQueue button: QToolButton
        # "plot" - show plots button: QToolButton
        # ...

        if len(self.project_controller.project_name) > 15:
            self.hint = True
            self.shown_name = self.project_controller.project_name[:13] + "..."
        else:
            self.hint = False
            self.shown_name = self.project_controller.project_name
        self.name_wiget = QLabel(self.shown_name)
        if self.hint: self.name_wiget.setToolTip(self.project_controller.project_name)
        self.name_wiget.setFrameShape(QFrame.StyledPanel)
        self.widgets_dict["name"] = self.name_wiget

        self.project_type_widget = QLabel(str(self.project_controller.mode))
        self.project_type_widget.setToolTip("ID of project type")
        self.project_type_widget.setFrameShape(QFrame.StyledPanel)
        self.widgets_dict["type"] = self.project_type_widget

        self.progress_bar_widget = QProgressBar()
        self.progress_bar_widget.setValue(self.project_controller.progress_percent)
        self.widgets_dict["progbar"] = self.progress_bar_widget

        self.play_pause_btn = QToolButton()
        self.play_pause_btn.setIcon(QtGui.QIcon('../Forms/resourses/play_btn.png'))
        self.play_pause_btn.clicked.connect(self.play_pause_btn_Click)
        self.widgets_dict["play_pause"] = self.play_pause_btn

        self.stop_btn = QToolButton()
        self.stop_btn.setIcon(QtGui.QIcon('../Forms/resourses/stop_btn.png'))
        self.stop_btn.clicked.connect(self.stop_btn_Click)
        self.widgets_dict["stop"] = self.stop_btn

        # self.settings_btn = QPushButton()
        self.settings_btn = QToolButton()
        self.settings_btn.setIcon(QtGui.QIcon('../Forms/resourses/settings_btn.png'))
        self.settings_btn.clicked.connect(self.setting_btn_Click)
        self.widgets_dict["sett"] = self.settings_btn

        self.archive_btn = QToolButton()
        self.archive_btn.setIcon(QtGui.QIcon('../Forms/resourses/archive_btn.png'))
        self.archive_btn.clicked.connect(self.archive_btn_Click)
        self.widgets_dict["archive"] = self.archive_btn

        self.to_queue_btn = QToolButton()
        self.to_queue_btn.setIcon((QtGui.QIcon('../Forms/resourses/toQueue.png')))
        self.to_queue_btn.clicked.connect(self.toQueue_btn_Click)
        self.widgets_dict["toQueue"] = self.to_queue_btn

        self.plot_btn = QToolButton()
        self.plot_btn.setIcon((QtGui.QIcon('../Forms/resourses/plot.png')))
        self.plot_btn.clicked.connect(self.plot_btn_Clicked)
        self.widgets_dict["plot"] = self.plot_btn
        self.row = QHBoxLayout()

        for key in self.widget_list:
            self.row.addWidget(self.widgets_dict.get(key))
        self.setLayout(self.row)

    def plot_btn_Clicked(self):
        self.plot_window = PlotWindow(self.project_controller)
        self.project_controller.communicator.ui_pinok.connect(self.plot_window.refresh_figure)
        pass

    def toQueue_btn_Click(self):
        self.project_controller.is_in_queue = True
        #self.parent_window.update_projects_list()
        self.parent_window.update_list_viewers("queue")
        pass

    def setting_btn_Click(self):
        if self.project_controller.mode == Project_controller.C2D_IMG_CLF_GEN:
            # поменять конструктор формы!
            # передавать динамическую ссылку!
            self.project_setting_window = MainWindow(project_queue=deque([]),
                                                     # какую очередь передавать и передавать ли?
                                                     project_controller=self.project_controller)
        self.project_setting_window.show()

    def stop_btn_Click(self):
        # убрать из очереди
        pass

    def play_pause_btn_Click(self):
        self.project_controller.is_run = not self.project_controller.is_run
        if self.project_controller.is_run:
            self.play_pause_btn.setIcon(QtGui.QIcon('../Forms/resourses/pause_btn.png'))
            # добавить в очередь на обучение
            self.parent_window.project_queue.append(self.project_controller)
            # self.plot_window = PlotWindow(self.project_controller)
            # self.project_controller.communicator.ui_pinok.connect(self.plot_window.refresh)
            # self.plot_window.show()

            ##### Test Tensorboard #######
            # tb = program.TensorBoard()
            # tb.configure(argv=[None, '--logdir', "logs"])
            # url = tb.launch()

        else:
            self.play_pause_btn.setIcon(QtGui.QIcon('../Forms/resourses/play_btn.png'))
            # остановить обучение, сохранить состояние
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
    #app.setStyleSheet(qdarkstyle.load_stylesheet())
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
