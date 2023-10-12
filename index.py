import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QPixmap
from os import path
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil, floor
from collections import Counter
plt.style.use('ggplot')
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import numpy as np
# from qtawesome import icon
from DocumentWindow import Ui_documet_window
MainUI, _ = loadUiType(path.join(path.dirname(__file__), 'main.ui'))
DocumentWindowUI, _ = loadUiType(path.join(path.dirname(__file__), 'DocumentWindow.ui'))
class File:
    def __init__(self):
        self.ani_list=[]
        self.ani = None
        self.ani2 = None
        self.time_list = []
        self.signal_values_list = []
        self.line = None
        self.files_name = []
        self.delay_interval = 200
        self.x_fig1 = {}
        self.y_fig1 = {}
        self.x_fig2 = {}
        self.y_fig2 = {}
        self.present_line1 = {}
        self.present_line2 = {}
        self.dic_channel1 = {}
        self.dic_channel2 = {}
        self.visited_channel1 = []
        self.visited_channel2 = []
        self.hidden_line_ch1 = {}
        self.hidden_line_ch2 = {}
        self.hide_action = False
        self.frames_channel1 = 400
        self.frames_channel2 = 400
        self.rewind_ch1 = False
        self.rewind_ch2 = False
        self.specific_row = 0
        self.specific_row_2 = 0
        self.no_of_line = 0
        self.no_of_line_2 = 0
        self.lines1 =[None] * 100
        self.lines2 = [None] * 100
        self.Qwindow = MainApp()
        self.Dwindow = DocumentWindow()
        self.fig = plt.figure(figsize=(898 / 80, 345 / 80), dpi=80)
        self.fig2 = plt.figure(figsize=(898 / 80, 345 / 80), dpi=80)

        self.Ui_graph_channel1()
        self.Ui_graph_channel2()

        self.handle_button_push()

        self.styles()
        self.row_counter = 0
        self.Qwindow.tableWidget.setColumnCount(6)
        self.Qwindow.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.signal_color = 'r'
        self.toolbar_1 = None
        self.toolbar_2 = None




    def handle_button_push(self):
        self.Qwindow.open_file.triggered.connect(self.browse_file)
        QCoreApplication.processEvents()
        self.Qwindow.pushButton_plot.clicked.connect(self.Plot)
        QCoreApplication.processEvents()
        self.Qwindow.minus_button.clicked.connect(self.decrease_speed)
        QCoreApplication.processEvents()
        self.Qwindow.plus_button.clicked.connect(self.increase_speed)
        QCoreApplication.processEvents()
        self.Qwindow.checkBox_2.stateChanged.connect(self.Ischecked)
        QCoreApplication.processEvents()
        self.Qwindow.checkBox_3.toggled.connect(self.Ischecked)
        QCoreApplication.processEvents()
        self.Qwindow.checkBox_3.setCheckable(True)
        self.Qwindow.color_picker_button.clicked.connect(self.show_color_dialog)
        self.Qwindow.pause_button.clicked.connect(lambda: self.toggle_channel_animation(self.ani))
        self.Qwindow.pause_button_2.clicked.connect(lambda: self.toggle_channel_animation(self.ani2))
        self.Qwindow.make_pdf.triggered.connect(self.open_window)
        self.Dwindow.add_image_button.clicked.connect(self.load_image)

    def Ui_graph_channel2(self):

        self.fig2.set_facecolor('#222b2e')
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_facecolor('#222b2e')

        self.ax2.grid(True, color='gray', linestyle='--', alpha=0.5)
        self.ax2.xaxis.label.set_color('white')  # X-axis label
        self.ax2.yaxis.label.set_color('white')

        self.ax2.spines['bottom'].set_color('white')
        self.ax2.spines['left'].set_color('white')
        for tick in self.ax2.get_xticklabels():
            tick.set_color('white')
            # X-axis

        for tick in self.ax2.get_yticklabels():
            tick.set_color('white')
        self.ax2.set_xlabel('Time (s)')

        self.ax2.set_ylabel("Vital Signal")

    def Ui_graph_channel1(self):
        print("graph1")
        self.fig.set_facecolor('#222b2e')

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#222b2e')
        self.ax.grid(True, color='gray', linestyle='--', alpha=0.5)
        self.ax.xaxis.label.set_color('white')  # X-axis label
        self.ax.yaxis.label.set_color('white')

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        for tick in self.ax.get_xticklabels():
            tick.set_color('white')
            # X-axis

        for tick in self.ax.get_yticklabels():
            tick.set_color('white')
        self.ax.set_xlabel('Time (s)')

        self.ax.set_ylabel("Vital Signal")
        return

    def print_pdf(self):
        print("PDF Created")


    def styles(self):
        for column in range(self.Qwindow.tableWidget.columnCount()):
            self.Qwindow.tableWidget.setColumnWidth(column, 309)
        header = self.Qwindow.tableWidget.horizontalHeader()
        header.setMinimumHeight(50)
        header_style = """
                                QHeaderView::section {
                                    background-color: #4fa08b; /* Change this to your desired color */
                                    color: white; /* Text color */
                                    font-weight: bold;
                                    font-size: 16px
                                }
                            """
        self.Qwindow.tableWidget.horizontalHeader().setStyleSheet(header_style)
        self.Qwindow.pause_button.hide()
        self.Qwindow.pause_button_2.hide()
        self.Qwindow.rewind_button1.hide()
        self.Qwindow.rewind_button2.hide()
        self.Qwindow.pause_button.setStyleSheet("background-color: white;"
                                                " color: black;"
                                                "font-size: 16px")
        self.Qwindow.pause_button_2.setStyleSheet("background-color: white;"
                                                  " color: black;"
                                                  "font-size: 16px")
        self.Qwindow.setFixedSize(1930,1000)
        # You can choose a different color
        # self.Qwindow.rewind_button1.setIcon(rewind_icon)
        # self.Qwindow.rewind_button2.setIcon(rewind_icon)
        self.Qwindow.rewind_button1.setStyleSheet("background-color: white;")
        self.Qwindow.rewind_button2.setStyleSheet("background-color: white;")


    def toggle_channel_animation(self, ani_num):
        if ani_num == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("No animations to toggle.")
            msg.show()
            msg.exec_()
            return
        if (ani_num == self.ani):
            if self.Qwindow.pause_button.text() == "►":
                self.Qwindow.pause_button.setText("❚❚")
                self.ani.event_source.start()
            else:
                self.Qwindow.pause_button.setText("►")
                self.ani.event_source.stop()
        else:

            if self.Qwindow.pause_button_2.text() == "►":
                self.Qwindow.pause_button_2.setText("❚❚")
                self.ani2.event_source.start()
            else:
                self.Qwindow.pause_button_2.setText("►")
                self.ani2.event_source.stop()




    def Ischecked(self):
        channel1 = self.Qwindow.checkBox_2.isChecked()
        channel2 = self.Qwindow.checkBox_3.isChecked()
        if channel1 and channel2:
            return "channel1","channel2"
        elif channel1:

            return ["channel1","None"]
        elif channel2:
            return  ["None", "channel2"]
        else:
            return ["None" ,"None"]



    def increase_speed(self):

        if self.delay_interval == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please Upload A Signal")
            msg.show()
            msg.exec_()

        else:
            self.ani.event_source.stop()


            self.delay_interval= 10
            #
            # self.create_animation()
            self.ani.event_source.start()




    def decrease_speed(self):

        if self.delay_interval == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please UPload A Signal")
            msg.show()
            msg.exec_()

        else:
            print("decrease")
            self.ani.event_source.stop()

            self.delay_interval += 200






    def animate_fig2(self, i):
        # global specific_row_2
        self.specific_row_2 += 1
        print(f"s2:{self.specific_row_2}")

        self.current_data_2 = i

        for idx_line_ch2 in self.dic_channel2.items():
            if idx_line_ch2[0] != 0 and len(self.present_line1) != 0:
                print("ياللهووي")
                print(len(self.present_line2))
                for idx_line2 in self.present_line2.items():
                    if idx_line2[0] == idx_line_ch2[0]:
                        print(f"l:{idx_line2[1]}")
                        current_idx_2 = idx_line2[1]
                        self.x_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][0][current_idx_2 + 3 - self.specific_row_2])
                        self.y_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][1][current_idx_2 + 3 - self.specific_row_2])
                        print(f"line2:{self.x_fig2[idx_line_ch2[0]]}")
                        self.lines2[idx_line_ch2[0]].set_data(self.x_fig2[idx_line_ch2[0]],
                                                              self.y_fig2[idx_line_ch2[0]])





            else:
                self.x_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][0][self.specific_row_2])
                self.y_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][1][self.specific_row_2])
                print(self.x_fig2[idx_line_ch2[0]])
                self.lines2[idx_line_ch2[0]].set_data(self.x_fig2[idx_line_ch2[0]], self.y_fig2[idx_line_ch2[0]])

            # print

            if self.rewind_ch2:
                self.ax.set_xlim(idx_line_ch2[1][0][self.current_data_2 - 60],
                                 idx_line_ch2[1][0][self.current_data_2 - 30])
                self.rewind_ch2 = False
            else:
                if self.current_data_2 > 30:
                    self.ax2.set_xlim(idx_line_ch2[1][0][self.current_data_2 - 30],
                                      idx_line_ch2[1][0][self.current_data_2])

        return tuple(self.lines2)

    def animate_fig1(self, i):

        # global specific_row
        self.specific_row += 1

        self.current_data = i
        # print(f"i:{i}")
        print(f"time:{self.delay_interval}")
        print(f"s1:{self.specific_row}")

        for idx_line_ch1 in self.dic_channel1.items():
            if idx_line_ch1[0] != 0 and len(self.present_line1) != 0:
                # print("ياللهووي")
                # print(self.present_line1.items())
                for idx_line1 in self.present_line1.items():
                    if idx_line1[0] == idx_line_ch1[0]:
                        # print(f"k:{idx_line_ch1[0]}")
                        # print(f"l:{idx_line1 [1]}")
                        current_idx = idx_line1[1]
                        self.x_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][0][current_idx + 3 - self.specific_row])
                        self.y_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][1][current_idx + 3 - self.specific_row])
                        # print(f"line2:{self.x_fig1[ idx_line_ch1 [0]]}")
                        self.lines1[idx_line_ch1[0]].set_data(self.x_fig1[idx_line_ch1[0]],
                                                              self.y_fig1[idx_line_ch1[0]])


            else:
                self.x_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][0][self.specific_row])
                self.y_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][1][self.specific_row])
                # print(self.x_fig1[idx_line_ch1[0]])
                self.lines1[idx_line_ch1[0]].set_data(self.x_fig1[idx_line_ch1[0]], self.y_fig1[idx_line_ch1[0]])

            # print(self.current_data)
            # if  idx_line_ch1 [0] == 0:

            if self.rewind_ch1:
                self.ax.set_xlim(idx_line_ch1[1][0][self.current_data - 60], idx_line_ch1[1][0][self.current_data - 30])
                self.rewind_ch1 = False
            else:
                if self.current_data > 30:
                    self.ax.set_xlim(idx_line_ch1[1][0][self.current_data - 30], idx_line_ch1[1][0][self.current_data])

        # self.ani.event_source.interval = 0
        return tuple(self.lines1)
    def channels_checked(self):
        check_list = self.Ischecked()
        file_namee, channel1, channel2 = self.current_file_and_channel(), check_list[0], check_list[1]
        print(file_namee)
        print(channel1)
        print(channel2)
        if len(file_namee) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please UPload A Signal")
            msg.show()
            msg.exec_()
        elif (channel1 == "None" and len(self.visited_channel1) == 0) and (
                channel2 == "None" and len(self.visited_channel2) == 0):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please Enter A Channel")
            msg.show()
            msg.exec_()




        else:

            print(self.files_name)
            for file in self.files_name:
                file_part = file.split('/')[-1].split('_')[0]
                if file_part == file_namee:
                    file_namee = file

                    # self.line_applied=file_part
                    if channel1 == "channel1" and channel2 == "None":
                        self.visited_channel1.append(file_part)
                        break

                    elif channel2 == "channel2" and channel1 == "None":
                        self.visited_channel2.append(file_part)
                        break

                    elif channel2 == "channel2" and file_part in self.visited_channel1:
                        self.visited_channel2.append(file_part)
                        if channel1 == "channel1":
                            self.visited_channel1.append(file_part)

                        break
                    elif channel1 == "channel1" and file_part in self.visited_channel2:
                        self.visited_channel1.append(file_part)
                        if channel2 == "channel2":
                            self.visited_channel2.append(file_part)
                        break

                    elif  channel1 == "channel1" and channel2 == "channel2":
                        self.visited_channel2.append(file_part)
                        self.visited_channel1.append(file_part)
                        break

                    break

            self.time_list, self.signal_values_list = self.read_ecg_data_from_csv(file_namee)

            return file_part ,file_namee , channel1 ,channel2
    #

    # def create_animation(self):
    #     self.ani = FuncAnimation(self.fig, self.animate_fig1, interval=self.delay_interval,
    #                              frames=self.frames_channel1, repeat=False)


    def Plot(self):
        file_part, file_namee, channel1, channel2 = self.channels_checked()

        data_x, data_y = self.time_list, self.signal_values_list

        x_range = (floor(min(data_x)), ceil(max(data_x)))
        y_range = (floor(min(data_y)), ceil(max(data_y)))

        print(file_part)
        print("dcjdkjdk")

        count_files_channel1 = Counter(self.visited_channel1)
        count_files_channel2 = Counter(self.visited_channel2)

        ## hide channels
        print(self.visited_channel1)
        if channel1 == "None" and file_part in self.visited_channel1:
            print("laama1")
            del count_files_channel1[file_part]
            print(self.visited_channel1)

            self.visited_channel1 = [file for idx, file in enumerate(self.visited_channel1) if file != file_part]
            print(len(self.visited_channel1))

            name_files = {}

            for item in self.hidden_line_ch1.items():
                if item[0] == file_part:
                    self.hidden_idx_1 = item[1]

                else:
                    name_files[item[1]] = item[0]

            del self.dic_channel1[self.hidden_idx_1]
            self.lines1[self.hidden_idx_1] = "None"
            # a ,= self.lines1[self.hidden_idx_1]
            # self.ax.lines[self.hidden_idx_1].remove(lines[self.hidden_idx_1][0])
            print(self.lines1)

            if self.hidden_idx_1 != 0:
                del self.present_line1[self.hidden_idx_1]

            self.fig.clf()
            # self.ax = self.fig.add_subplot(111)
            self.Ui_graph_channel1()

            for idx_line_ch1 in self.dic_channel1.items():
                self.lines1[idx_line_ch1[0]], = self.ax.plot([], [], label=name_files[idx_line_ch1[0]])

            self.ax.legend()

        ## Channel 1
        if channel1 == "channel1":
            # self.ani.event_source.interval = self.delay_interval

            print('hi')
            print(self.visited_channel1)

            for item in count_files_channel1.items():
                if item[0] == file_part:
                    no_of_repeated = item[1]
                    break

            print(len(self.present_line1))
            if file_part in self.visited_channel2 and len(self.visited_channel2) == 1:
                print("hahahahaha")
                self.specific_row_2 = self.specific_row - 1

            if no_of_repeated == 1:
                print("ooooo")
                self.previous_line1 = self.no_of_line
                self.no_of_line += 1
                self.ax.set_xlim(x_range)
                self.ax.set_ylim(y_range)
                self.delay_interval = 200
                colors = {0: 'b', 1: 'r', 2: 'g'}
                print(f"no of line:{self.no_of_line}")

                if self.no_of_line == 1:
                    graph_ch1 = True

                else:
                    graph_ch1 = False

                # self.line_plot,=self.ax.plot([],[] ,label=
                for index in range(self.previous_line1, self.no_of_line):
                    self.hidden_line_ch1[file_part] = index

                    self.lines1[index], = self.ax.plot([], [], label=file_part, color=self.signal_color)
                    self.x_fig1[index] = []
                    self.y_fig1[index] = []

                if self.no_of_line > 1 and len(self.visited_channel1) != 1:
                    print("halllo")

                    self.data_xline, self.data_yline = self.read_ecg_data_from_csv(file_namee)
                    self.present_line1[self.no_of_line - 1] = self.current_data
                    for idx in range(len(self.data_xline)):
                        # x=self.dic_channel1[0]

                        # print(f"x:{self.dic_channel1[0][0][self.current_data]}")
                        if self.data_xline[idx] >= self.dic_channel1[0][0][self.current_data]:
                            print("حد يلجقنا")
                            print(f"idx:{idx}")

                            self.data_xline = self.data_xline[idx:]
                            self.data_yline = self.data_yline[idx:]
                            print(f"len_x:{len(self.data_xline)}")
                            break

                    self.dic_channel1[self.no_of_line - 1] = self.data_xline, self.data_yline
                else:
                    self.dic_channel1[self.no_of_line - 1] = self.read_ecg_data_from_csv(file_namee)

                if graph_ch1:
                    # self.create_animation()

                    self.ani = FuncAnimation(self.fig, self.animate_fig1 ,interval=200,
                                             frames=self.frames_channel1, repeat=False  )

                    # self.ani.event_source.interval = 0

                self.ax.legend()

                if graph_ch1:
                    scene1 = QtWidgets.QGraphicsScene()
                    canvas1 = FigureCanvasQTAgg(self.fig)
                    self.Qwindow.graphicsView_channel1.setScene(scene1)
                    scene1.addWidget(canvas1)
                    toolbar_1 = NavigationToolbar(canvas1, self.Qwindow)
                    self.Qwindow.verticalLayout_toolbar1.addWidget(toolbar_1)

        print(self.visited_channel2)
        if channel2 == "None" and file_part in self.visited_channel2:
            print("laama")
            del count_files_channel2[file_part]
            print(self.visited_channel2)

            self.visited_channel2 = [file2 for idx2, file2 in enumerate(self.visited_channel2) if file2 != file_part]
            print(len(self.visited_channel2))

            name_files2 = {}

            for item2 in self.hidden_line_ch2.items():
                if item2[0] == file_part:
                    self.hidden_idx_2 = item2[1]

                else:
                    name_files2[item2[1]] = item2[0]

            del self.dic_channel2[self.hidden_idx_2]
            self.lines2[self.hidden_idx_2] = "None"

            print(self.lines2)

            if self.hidden_idx_2 != 0:
                del self.present_line1[self.hidden_idx_2]

            self.fig2.clf()
            # self.ax = self.fig.add_subplot(111)
            self.Ui_graph_channel2()

            for idx_line_ch2 in self.dic_channel2.items():
                self.lines2[idx_line_ch2[0]], = self.ax2.plot([], [], label=name_files[idx_line_ch2[0]] ,color=self.signal_color)

            self.ax2.legend()

        if channel2 == "channel2":

            for item in count_files_channel2.items():
                if item[0] == file_part:
                    no_of_repeated = item[1]

            print(len(self.present_line2))
            if file_part in self.visited_channel1 and len(self.visited_channel1) == 1:
                print("hahahahaha")
                self.specific_row = self.specific_row_2 - 1

            if no_of_repeated == 1:
                self.previous_line2 = self.no_of_line_2
                # self.name_line2=file_part
                self.no_of_line_2 += 1
                self.ax2.set_xlim(x_range)
                self.ax2.set_ylim(y_range)
                self.delay_interval = 200
                colors = {0: 'b', 1: 'r', 2: 'g'}

                if self.no_of_line_2 == 1:
                    graph_ch2 = True
                else:
                    graph_ch2 = False

                for index_2 in range(self.previous_line2, self.no_of_line_2):
                    self.hidden_line_ch2[file_part] = index_2
                    self.lines2[index_2], = self.ax2.plot([], [], label=file_part, color=self.signal_color)
                    self.x_fig2[index_2] = []
                    self.y_fig2[index_2] = []

                if self.no_of_line_2 > 1 and len(self.visited_channel2) != 1:
                    print("halllo2")
                    self.data_xline_2, self.data_yline_2 = self.read_ecg_data_from_csv(file_namee)
                    self.present_line2[self.no_of_line_2 - 1] = self.current_data_2
                    for idx_2 in range(len(self.data_xline_2)):
                        # x=self.dic_channel1[0]

                        print(f"x:{self.dic_channel2[0][0][self.current_data_2]}")
                        if self.data_xline_2[idx_2] >= self.dic_channel2[0][0][self.current_data_2]:
                            print("حد يلجقنا2")
                            print(f"idx2:{idx_2}")

                            self.data_xline_2 = self.data_xline_2[idx_2:]
                            self.data_yline_2 = self.data_yline_2[idx_2:]
                            print(f"len_x2:{len(self.data_xline_2)}")
                            break

                    self.dic_channel2[self.no_of_line_2 - 1] = self.data_xline_2, self.data_yline_2
                else:
                    self.dic_channel2[self.no_of_line_2 - 1] = self.read_ecg_data_from_csv(file_namee)

                if graph_ch2:
                    self.ani2 = FuncAnimation(self.fig2, self.animate_fig2, interval=self.delay_interval,
                                              frames=self.frames_channel2, repeat=False)

                    QCoreApplication.processEvents()
                self.ax2.legend()
                if graph_ch2:
                    scene2 = QtWidgets.QGraphicsScene()
                    canvas2 = FigureCanvasQTAgg(self.fig2)
                    self.Qwindow.graphicsView_channel2.setScene(scene2)
                    scene2.addWidget(canvas2)
                    toolbar_2 = NavigationToolbar(canvas2, self.Qwindow)
                    self.Qwindow.verticalLayout_toolbar2.addWidget(toolbar_2)


    def current_file_and_channel(self):
        return str(self.Qwindow.signals_name.currentText())

    def show_color_dialog(self):
        color = QColorDialog.getColor()
        self.Qwindow.color_picker_button.setStyleSheet(f"background-color: {color.name()}; color: white;")
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, color)
        self.Qwindow.color_picker_button.setPalette(palette)
        self.signal_color = color.name()
        print(self.signal_color)

        return color

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open File", "",
                                                   "CSV Files (*.csv)",
                                                   options=options)

        if file_name:
            self.files_name.append(file_name)
            file_name = str(file_name)

            self.line = file_name.split('/')[-1].split('_')[0]
            self.Qwindow.signals_name.addItem(self.line)
            self.time_list, self.signal_values_list = self.read_ecg_data_from_csv(file_name)
            self.row_counter = self.row_counter + 1
            self.Qwindow.tableWidget.setRowCount(self.row_counter)
            mean = self.Qwindow.calc_mean(self.signal_values_list)
            std = self.Qwindow.calc_std(self.signal_values_list)
            duration = self.Qwindow.calc_duration(self.time_list)
            min_value, max_value = self.Qwindow.calc_min_max_values(self.signal_values_list)
            print(mean)
            print(std)
            print(duration)
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 0, QTableWidgetItem(self.line))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 1, QTableWidgetItem(str(round(mean, 8))))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 2, QTableWidgetItem(str(round(std, 8))))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 3, QTableWidgetItem(str(duration)))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 4, QTableWidgetItem(str(min_value)))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 5, QTableWidgetItem(str(max_value)))



    def read_ecg_data_from_csv(self, file_name):
       try:
           with open(file_name, 'r') as csv_file:
               # csv_reader = csv.DictReader(csv_file)
               csv_reader = pd.read_csv(csv_file)
               time_list = csv_reader.iloc[:, 0].tolist()
               signal_values_list = csv_reader.iloc[:, 1].tolist()
           return time_list, signal_values_list
       except Exception as e:
           print("Error reading CSV file")
           return [], []
       
    def open_window(self):
        self.Dwindow.show()

    def load_image(self):
        options = QFileDialog.Options()
        screenshots, _ = QFileDialog.getOpenFileName(self.Dwindow, "Open Image File", "",
                                                     "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)",
                                                     options=options)
        if screenshots:
            pixmap = QPixmap(screenshots)
            if not pixmap.isNull():
                target_width = self.Dwindow.screenshot_section.width()
                target_height = self.Dwindow.screenshot_section.height()
                scaled_pixmap = pixmap.scaled(target_width, target_height)

                self.Dwindow.screenshot_section.setPixmap(scaled_pixmap)
                # self.Dwindow.screenshot_section.setp(pixmap)
        else:
            print("File dialog canceled or encountered an error.")





class MainApp(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Signal Real-Time Monitoring")

    def hi(self):
        print("hello")

    def calc_mean(self, values):
        return np.mean(values)

    def calc_std(self, values):
        return np.std(values)

    def calc_duration(self, time):
        return np.max(time)

    def calc_min_max_values(self, values):
        return np.min(values), np.max(values)

class DocumentWindow(QMainWindow, DocumentWindowUI):
    def __init__(self, parent=None):
        super(DocumentWindow, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Create A PDF")

def main():
    app = QApplication(sys.argv)
    window = File()
    window.Qwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
