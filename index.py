import os
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer, Paragraph, Table, TableStyle
from reportlab.lib import colors
import matplotlib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.units import inch
import glob
from PIL import Image as PILImage
from reportlab.platypus.doctemplate import Spacer
from reportlab.lib import styles
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets, QtCore
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
from qtawesome import icon
from reportlab.lib.pagesizes import letter

MainUI, _ = loadUiType(path.join(path.dirname(__file__), 'main.ui'))
DocumentWindowUI, _ = loadUiType(path.join(path.dirname(__file__), 'DocumentWindow.ui'))


class File:
    def __init__(self):
        # self.child_item = None
        self.add_new_signal = False
        self.x_min_ch2 = 0
        self.move_to_ch1 = False
        self.hide_action_ch1 = False
        self.hide_action_ch2 = True
        self.count_files_channel1 = {}
        self.splitted_names_ch1 = []
        self.splitted_names_ch2 = []
        self.menu = None
        self.ani_list = []
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
        self.pause_ch1 = False
        self.pause_ch2 = False
        self.play_ch1 = True
        self.play_ch2 = True
        self.present_line1 = {}
        self.present_line2 = {}
        self.files_index_ch1 = {}
        self.files_index_ch2 = {}
        self.line_idx_ch1 = {}
        self.line_idx_ch2 = {}
        self.dic_channel1 = {}
        self.dic_channel2 = {}
        self.name_files_ch2 = {}
        self.name_files_ch1 = {}
        self.visited_channel1 = []
        self.visited_channel2 = []
        self.hidden_line_ch1 = {}
        self.hidden_line_ch2 = {}
        self.hide_action = False
        self.frames_channel1 = 500
        self.frames_channel2 = 500
        self.colors_channel1 = {}
        self.colors_channel2 = {}
        self.rewind_ch1 = False
        self.rewind_ch2 = False
        self.set_speed = False
        self.found_ch1 = True
        self.found_ch2 = True
        self.link = False
        self.specific_row = 0
        self.specific_row_2 = 0
        self.no_of_line = 0
        self.no_of_line_2 = 0
        self.data_y_limits = []
        self.data_x_limits = []
        self.lines1 = [None] * 100
        self.lines2 = [None] * 100
        self.Qwindow = MainApp()
        self.Dwindow = DocumentWindow()
        self.fig = plt.figure(figsize=(1500 / 80, 345 / 80), dpi=80)
        self.fig2 = plt.figure(figsize=(1500 / 80, 345 / 80), dpi=80)
        self.mean = 0
        self.std = 0
        self.duration = 0
        self.min_value = 0
        self.max_value = 0
        self.Qwindow.tableWidget.hide()
        self.Ui_graph_channel1()
        self.Ui_graph_channel2()
        self.Qwindow = MainApp()
        self.Dwindow = DocumentWindow()
        self.handle_button_push()
        self.styles()
        self.row_counter = 0
        self.Qwindow.tableWidget.setColumnCount(6)
        self.Qwindow.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.signal_color = 'r'
        self.toolbar_1 = None
        self.toolbar_2 = None
        self.pdf_counter = 0
        self.margin = 0
        self.page_container = []
        self.Time = np.linspace(0, 2, 600)
        self.pdf_filename = f"Medical Report {self.pdf_counter}.pdf"
        self.doc = SimpleDocTemplate(self.pdf_filename, pagesize=letter)
        self.Qwindow.tableWidget.hide()
        self.img_channel1_counter = 0
        self.img_channel2_counter = 0
        self.statistics_data = []

    def handle_button_push(self):
        self.Qwindow.open_file.triggered.connect(self.browse_file)
        QCoreApplication.processEvents()
        QCoreApplication.processEvents()
        QCoreApplication.processEvents()
        self.Qwindow.color_picker_button.clicked.connect(self.show_color_dialog_ch1)
        self.Qwindow.color_picker_button_2.clicked.connect(self.show_color_dialog_ch2)
        self.Qwindow.rewind_button2.clicked.connect(self.rewind_channel2)
        QCoreApplication.processEvents()
        self.Qwindow.rewind_button1.clicked.connect(self.rewind_channel1)
        QCoreApplication.processEvents()
        self.Qwindow.pause_button.clicked.connect(lambda: self.toggle_channel_animation(self.ani))
        QCoreApplication.processEvents()
        self.Qwindow.pause_button_2.clicked.connect(lambda: self.toggle_channel_animation(self.ani2))
        QCoreApplication.processEvents()
        self.Qwindow.link_button.toggled.connect(self.link_two_graphs)
        QCoreApplication.processEvents()
        self.Qwindow.make_pdf.triggered.connect(self.open_window)
        QCoreApplication.processEvents()
        self.Dwindow.save_button.clicked.connect(self.Dwindow.close)
        QCoreApplication.processEvents()
        self.Dwindow.save_button.clicked.connect(self.add_new_pdf_page)
        self.Qwindow.Timer.timeout.connect(self.Pause_pan)
        self.Qwindow.Timer.start(40)
        shortcut2 = QShortcut(QKeySequence('Ctrl+P'), self.Qwindow)
        shortcut2.activated.connect(self.Qwindow.pause_button_2.click)
        shortcut1 = QShortcut(QKeySequence('Ctrl+S'), self.Qwindow)
        shortcut1.activated.connect(self.Qwindow.pause_button.click)
        self.Qwindow.hide_button1.clicked.connect(lambda: self.hide(self.Qwindow.hide_button1))
        QCoreApplication.processEvents()
        self.Qwindow.hide_button2.clicked.connect(lambda: self.hide(self.Qwindow.hide_button2))
        QCoreApplication.processEvents()
        self.Qwindow.move_button1.clicked.connect(lambda: self.move(self.Qwindow.move_button1))
        QCoreApplication.processEvents()
        self.Qwindow.move_button2.clicked.connect(lambda: self.move(self.Qwindow.move_button2))
        QCoreApplication.processEvents()
        self.Qwindow.speed_up_button1.clicked.connect(lambda: self.increase_speed(self.Qwindow.speed_up_button1))
        QCoreApplication.processEvents()
        self.Qwindow.speed_up_button2.clicked.connect(lambda: self.increase_speed(self.Qwindow.speed_up_button2))
        QCoreApplication.processEvents()
        self.Qwindow.speed_down_button1.clicked.connect(lambda: self.decrease_speed(self.Qwindow.speed_down_button1))
        QCoreApplication.processEvents()
        self.Qwindow.speed_down_button2.clicked.connect(lambda: self.decrease_speed(self.Qwindow.speed_down_button2))

    def Ui_graph_channel2(self):   # Styling the UI of the 2nd graph
        self.fig2.set_facecolor('#F0F5F9')
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_facecolor('#F0F5F9')
        left_margin = 0.05  # Adjust this value as needed
        self.ax2.set_position([left_margin, 0.1, 0.83, 0.85])  # [left, bottom, width, height]
        self.ax2.set_facecolor('#F0F5F9')
        self.ax2.grid(True, color='gray', linestyle='--', alpha=0.5)
        self.ax2.xaxis.label.set_color('#708694')  # X-axis label
        self.ax2.xaxis.label.set_weight('bold')
        self.ax2.yaxis.label.set_color('#708694')
        self.ax2.yaxis.label.set_weight('bold')
        self.ax2.spines['bottom'].set_color('#708694')
        self.ax2.spines['left'].set_color('#708694')
        for tick in self.ax2.get_xticklabels():
            tick.set_color('#708694')
            tick.set_weight('bold')
        for tick in self.ax2.get_yticklabels():
            tick.set_color('#708694')
            tick.set_weight('bold')
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel("Vital Signal")

    def Ui_graph_channel1(self):  # Styling the UI for the 1st Graph
        self.fig.set_facecolor('#F0F5F9')
        self.ax = self.fig.add_subplot(111)
        left_margin = 0.05  # Adjust this value as needed
        self.ax.set_position([left_margin, 0.1, 0.83, 0.85])  # [left, bottom, width, height]
        self.ax.set_facecolor('#F0F5F9')
        self.ax.grid(True, color='gray', linestyle='--', alpha=0.5)
        self.ax.xaxis.label.set_color('#708694')  # X-axis label
        self.ax.xaxis.label.set_weight('bold')
        self.ax.yaxis.label.set_color('#708694')
        self.ax.yaxis.label.set_weight('bold')
        self.ax.spines['bottom'].set_color('#708694')
        self.ax.spines['left'].set_color('#708694')
        for tick in self.ax.get_xticklabels():
            tick.set_color('#708694')
            tick.set_weight('bold')
        for tick in self.ax.get_yticklabels():
            tick.set_color('#708694')
            tick.set_weight('bold')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel("Vital Signal")
        return

    def styles(self):
        for column in range(self.Qwindow.tableWidget.columnCount()):
            self.Qwindow.tableWidget.setColumnWidth(column, 307)
        header = self.Qwindow.tableWidget.horizontalHeader()
        header.setMinimumHeight(40)
        header_style = """
                                QHeaderView::section {
                                    background-color: #849dad; /* Change this to your desired color */
                                    color: white; /* Text color */
                                    font-weight: bold;
                                    font-size: 16px
                                }
                            """
        self.Qwindow.tableWidget.setStyleSheet("QTableWidget { font-size: 15px; font-weight: bold}"
                                               "QTableWidget::item { text-align: center; }"
                                               "QTableWidget QHeaderView::section { text-align: center; }")
        self.Qwindow.tableWidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
        self.Qwindow.tableWidget.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter)
        self.Qwindow.tableWidget.horizontalHeader().setStyleSheet(header_style)
        self.Qwindow.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Qwindow.pause_button.hide()
        self.Qwindow.pause_button_2.hide()
        self.Qwindow.rewind_button1.hide()
        self.Qwindow.rewind_button2.hide()
        self.Qwindow.move_button1.hide()
        self.Qwindow.move_button2.hide()
        self.Qwindow.hide_button1.hide()
        self.Qwindow.hide_button2.hide()
        self.Qwindow.speed_up_button1.hide()
        self.Qwindow.speed_up_button2.hide()
        self.Qwindow.speed_down_button1.hide()
        self.Qwindow.speed_down_button2.hide()
        self.Qwindow.color_picker_button.hide()
        self.Qwindow.color_picker_button_2.hide()
        self.Qwindow.pause_button.setStyleSheet("background-color: #849dad;"
                                                " color: white;"
                                                "font-size: 16px")
        self.Qwindow.pause_button_2.setStyleSheet("background-color: #849dad;"
                                                  " color: white;"
                                                  "font-size: 16px")
        rewind_icon = icon("fa.backward", color='white')
        self.Qwindow.rewind_button1.setIcon(rewind_icon)
        self.Qwindow.rewind_button2.setIcon(rewind_icon)
        self.Qwindow.rewind_button1.setStyleSheet("background-color: #849dad;")
        self.Qwindow.rewind_button2.setStyleSheet("background-color: #849dad;")
        self.Qwindow.graphicsView_channel1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Qwindow.graphicsView_channel1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Qwindow.graphicsView_channel2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Qwindow.graphicsView_channel2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Qwindow.hide_button1.setStyleSheet("background-color: #849dad;"
                                                  "color: white;"
                                                  "font-size: 16px")
        self.Qwindow.hide_button2.setStyleSheet("background-color: #849dad;"
                                                "color: white;"
                                                "font-size: 16px")
        hide_icon = icon("ph.eye-slash-fill", color='white')
        self.Qwindow.hide_button1.setIcon(hide_icon)
        self.Qwindow.hide_button2.setIcon(hide_icon)
        self.Qwindow.move_button1.setStyleSheet("background-color: #849dad;"
                                                  "color: white;"
                                                  "font-size: 16px")
        self.Qwindow.move_button2.setStyleSheet("background-color: #849dad;"
                                                  "color: white;"
                                              "font-size: 16px;")
        move_icon = icon("mdi6.swap-vertical-variant", color='white')
        self.Qwindow.move_button1.setIcon(move_icon)
        self.Qwindow.move_button2.setIcon(move_icon)
        self.Qwindow.speed_up_button1.setStyleSheet("background-color: #849dad;"
                                                    "color: white;"
                                                    "font-size: 16px")
        self.Qwindow.speed_up_button2.setStyleSheet("background-color: #849dad;"
                                                    "color: white;"
                                                    "font-size: 16px;")
        speedup_icon = icon("ph.trend-up-bold", color='white')
        self.Qwindow.speed_up_button1.setIcon(speedup_icon)
        self.Qwindow.speed_up_button2.setIcon(speedup_icon)
        self.Qwindow.speed_down_button1.setStyleSheet("background-color: #849dad;"
                                                    "color: white;"
                                                    "font-size: 16px")
        self.Qwindow.speed_down_button2.setStyleSheet("background-color: #849dad;"
                                                    "color: white;"
                                                    "font-size: 16px;")
        speed_down_icon = icon("ph.trend-down-bold", color='white')
        self.Qwindow.speed_down_button1.setIcon(speed_down_icon)
        self.Qwindow.speed_down_button2.setIcon(speed_down_icon)

    def hide_channel2(self, file_name):
        file_part = file_name.split('/')[-1].split('.')[0]
        if file_part in self.visited_channel2:
            del self.count_files_channel2[file_part]
            print(self.visited_channel2)
            self.visited_channel2 = [file2 for idx2, file2 in enumerate(self.visited_channel2) if file2 != file_part]
            self.splitted_names_ch2 = [file for idx, file in enumerate(self.splitted_names_ch2) if file != file_part]
            print(len(self.visited_channel2))

            if len(self.visited_channel2) == 0:
                self.specific_row_2 = 0
                self.frames_channel2 += 300
                self.hide_action_ch2 = True

            for item2 in self.hidden_line_ch2.items():
                if item2[0] == file_part:
                    self.hidden_idx_2 = item2[1]
                else:
                    self.name_files_ch2[item2[1]] = item2[0]
            print(self.lines2)
            del self.dic_channel2[self.hidden_idx_2]
            self.lines2[self.hidden_idx_2] = "None"
            print(self.lines2)
            print(self.present_line2.keys())
            if self.hidden_idx_2 in self.present_line2.keys():
                del self.present_line2[self.hidden_idx_2]
            self.fig2.clf()
            self.Ui_graph_channel2()
            for idx_line_ch2 in self.dic_channel2.items():
                self.lines2[idx_line_ch2[0]], = self.ax2.plot([], [], label=self.name_files_ch2[idx_line_ch2[0]],
                                                              color=self.colors_channel2[idx_line_ch2[0]])
            self.ax2.legend()

    def hide_channel1(self, file_name):
        file_part = file_name.split('/')[-1].split('.')[0]
        if file_part in self.visited_channel1:   # filepart: name of signal
            print(self.visited_channel1)
            del self.count_files_channel1[file_part]
            self.visited_channel1 = [file for idx, file in enumerate(self.visited_channel1) if file != file_part]
            self.splitted_names_ch1 = [file for idx, file in enumerate(self.splitted_names_ch1) if file != file_part]
            print("hello")
            print(len(self.visited_channel1))
            for item in self.hidden_line_ch1.items():
                if item[0] == file_part:
                    self.hidden_idx_1 = item[1]
                else:
                    self.name_files_ch1[item[1]] = item[0]
            del self.dic_channel1[self.hidden_idx_1]

            self.lines1[self.hidden_idx_1] = "None"

            if self.hidden_idx_1 in self.present_line1.keys():
                del self.present_line1[self.hidden_idx_1]
            self.fig.clf()
            self.Ui_graph_channel1()
            for idx_line_ch1 in self.dic_channel1.items():
                self.lines1[idx_line_ch1[0]], = self.ax.plot([], [], label=self.name_files_ch1[idx_line_ch1[0]],
                                                             color=self.colors_channel1[idx_line_ch1[0]])
            self.ax.legend()
            if len(self.visited_channel1) == 0:
                self.hide_action_ch1 = True
                self.specific_row = 0
                self.frames_channel1 += 300

    def move_to_channel2(self, file_name):
        if self.hide_action_ch2:
            self.specific_row_2 = 0
            self.hide_action_ch2 = False
        for file in self.files_name:
            file_part = file.split('/')[-1].split('.')[0]
            if file_name == file_part:
                print(f"file:{file}")
                self.signal_values_list = self.read_ecg_data_from_csv(file)
                break
        self.visited_channel2.append(file_part)
        if file_part not in self.splitted_names_ch2:
            self.splitted_names_ch2.append(file_part)
        self.x_min_ch2 = self.Time[self.specific_row_2]
        self.ax2.set_xlim(self.Time[self.specific_row_2], 2)
        data_y = self.signal_values_list
        y_range = (floor(min(data_y)), ceil(max(data_y)))
        self.count_files_channel2 = Counter(self.visited_channel2)
        for item in self.count_files_channel2.items():  # get no of repeated signal
            if item[0] == file_part:
                no_of_repeated = item[1]
                break

        if no_of_repeated == 1:
            self.previous_line2 = self.no_of_line_2
            self.no_of_line_2 += 1
            self.ax2.set_xlim(self.Time[3], self.Time[30])

            self.ax2.set_ylim(y_range)
            self.delay_interval = 200
            if self.no_of_line_2 == 1:
                graph_ch2 = True
            else:
                graph_ch2 = False
            for index_2 in range(self.previous_line2, self.no_of_line_2):
                self.hidden_line_ch2[file_part] = index_2
                self.lines2[index_2], = self.ax2.plot([], [], label=file_part, color=self.signal_color)
                self.colors_channel2[index_2] = self.signal_color
                self.files_index_ch2[index_2] = file_part
                self.x_fig2[index_2] = []
                self.y_fig2[index_2] = []
            if self.no_of_line_2 > 1 and len(self.visited_channel2) != 1:
                self.present_line2[self.no_of_line_2 - 1] = self.current_data_2

            self.dic_channel2[self.no_of_line_2 - 1] = self.read_ecg_data_from_csv(file)
            if graph_ch2:
                self.x_min_ch2 = self.specific_row_2
                self.ani2 = FuncAnimation(self.fig2, self.animate_fig2, interval=self.delay_interval,
                                          frames=self.frames_channel2, repeat=False)
                QCoreApplication.processEvents()
            self.ax2.legend()
            if graph_ch2:
                scene2 = QtWidgets.QGraphicsScene()
                self.canvas2 = FigureCanvasQTAgg(self.fig2)
                self.Qwindow.graphicsView_channel2.setScene(scene2)
                scene2.addWidget(self.canvas2)
                self.toolbar_2 = NavigationToolbar(self.canvas2, self.Qwindow)
                # Remove the Home and Customize buttons from the toolbar
                unwanted_buttons = ['Customize', 'Home', 'Subplots', 'Back', 'Forward']
                for x in self.toolbar_2.actions():
                    if x.text() in unwanted_buttons:
                        self.toolbar_2.removeAction(x)
                # Finding The buttons in the toolbar and changing its icons using qtawesome icons
                actions = self.toolbar_2.actions()
                fourth_action = actions[2]
                # zero_action = actions[0]
                # first_action = actions[1]
                second_action = actions[1]
                sixth_action = actions[4]
                sixth_action.triggered.disconnect()
                # Connect it to a custom function that handles saving
                sixth_action.triggered.connect(self.custom_save_function_channel2)

                zoom_in_icon = icon("fa.search-plus",
                                    color="white")
                # left_arrow_icon = icon("ei.arrow-left", color="white")
                # right_arrow_icon = icon("ei.arrow-right", color="white")
                pan_icon = icon("fa.hand-paper-o", color="white")
                screenshot_icon = icon("ri.screenshot-2-fill", color="white")
                fourth_action.setIcon(zoom_in_icon)
                # zero_action.setIcon(left_arrow_icon)
                # first_action.setIcon(right_arrow_icon)
                second_action.setIcon(pan_icon)
                sixth_action.setIcon(screenshot_icon)
                # Creating an Icon for the Zoom Out button and Creating the button Itself
                zoom_out_icon = icon("fa.search-minus", color="white")
                zoom_out_button2 = QtWidgets.QAction(zoom_out_icon, "Zoom Out", self.Qwindow)
                zoom_out_button2.triggered.connect(self.Zoom_out_channel2)
                self.toolbar_2.insertAction(self.toolbar_2.actions()[4], zoom_out_button2)
                for child in self.toolbar_2.findChildren(QtWidgets.QToolButton):
                    child.setStyleSheet("background-color: #849dad;")
                self.Qwindow.tableWidget.show()
                self.Qwindow.pause_button_2.show()
                self.Qwindow.rewind_button2.show()
                self.Qwindow.move_button2.show()
                self.Qwindow.hide_button2.show()
                self.Qwindow.speed_up_button2.show()
                self.Qwindow.speed_down_button2.show()
                self.Qwindow.color_picker_button_2.show()
                self.Qwindow.verticalLayout_toolbar2.addWidget(self.toolbar_2)

    def move_to_channel1(self, file_name):
        for file in self.files_name:
            file_part = file.split('/')[-1].split('.')[0]
            if file_name == file_part:
                print(f"file:{file}")
                self.move_to_ch1 = True
                self.Plot_channel1(file)
                break

    def hide(self, button_name):
        if button_name == self.Qwindow.hide_button1:
            if len(self.splitted_names_ch1) > 1:
                self.menu = QMenu()
                file = self.menu.triggered.connect(self.actionClicked)
                for file_name in self.splitted_names_ch1:
                    self.menu.addAction(file_name)
                action = self.menu.exec_(self.Qwindow.hide_button1.mapToGlobal(
                    self.Qwindow.hide_button1.rect().bottomLeft()))
                print(f"ac:{action}")
                if action is not None:
                    print(f"act:{action.text()}")
                    file_name = action.text()
                    self.hide_channel1(file_name)
            else:
                self.hide_channel1(self.splitted_names_ch1[0])

        if button_name == self.Qwindow.hide_button2:
            if len(self.splitted_names_ch2) > 1:
                self.menu = QMenu()
                file = self.menu.triggered.connect(self.actionClicked)
                for file_name in self.splitted_names_ch2:
                    self.menu.addAction(file_name)
                action = self.menu.exec_(self.Qwindow.hide_button2.mapToGlobal(
                    self.Qwindow.hide_button2.rect().bottomLeft()))
                if action is not None:
                    file_name = action.text()
                    self.hide_channel2(file_name)
            else:
                self.hide_channel2(self.splitted_names_ch2[0])

    def actionClicked(self, action):
        print("hakkk")
        print('Action: ', action.text())
        return action.text()

    def move(self, button_name):
        if button_name == self.Qwindow.move_button1:
            if len(self.splitted_names_ch1) > 1:
                self.menu = QMenu()
                self.menu.triggered.connect(self.actionClicked)
                for file_name in self.splitted_names_ch1:
                    self.menu.addAction(file_name)
                action = self.menu.exec_(self.Qwindow.move_button1.mapToGlobal(
                    self.Qwindow.move_button1.rect().bottomLeft()))
                if action is not None:
                    file = action.text()
                    self.move_to_channel2(file)
            else:
                self.move_to_channel2(self.splitted_names_ch1[0])
        if button_name == self.Qwindow.move_button2:
            if len(self.splitted_names_ch2) > 1:
                self.menu = QMenu()
                self.menu.triggered.connect(self.actionClicked)
                for file_name in self.splitted_names_ch2:
                    self.menu.addAction(file_name)
                action = self.menu.exec_(self.Qwindow.move_button2.mapToGlobal(
                    self.Qwindow.move_button2.rect().bottomLeft()))
                if action is not None:
                    file = action.text()
                    self.move_to_channel1(file)
            else:
                self.move_to_channel1(self.splitted_names_ch2[0])

    def Pause_pan(self):
        if self.ax.get_navigate_mode() == "PAN" and self.play_ch1:
            y_min, y_max = self.ax.get_ylim()

            if y_min < -1 or y_max > 1:
                self.ax.set_ylim(-1, 1)
                self.fig.canvas.draw()

        if self.ax.get_navigate_mode() == "PAN" and not self.play_ch1:
            x_min, x_max = self.ax.get_xlim()
            y_min, y_max = self.ax.get_ylim()
            for item in self.dic_channel1.items():
                print(f"ite:{item[0]}")
                if x_min < self.Time[3] and item[0] == 0:
                    new_x_min = self.Time[3]
                    print(f"min:{x_min, self.Time[3]}")

                    print(f"new:{new_x_min}")
                    self.ax.set_xlim(new_x_min, self.Time[10])
                    self.fig.canvas.draw()

                if (y_min < -1 and item[0] == 0) or (y_max > 1 and item[0] == 0):
                    self.ax.set_ylim(-1, 1)
                    self.fig.canvas.draw()

                if x_max > self.Time[self.specific_row] and item[0] == 0:
                    new_x_max = self.Time[self.specific_row]
                    self.ax.set_xlim(self.Time[self.specific_row - 28], new_x_max)
                    self.fig.canvas.draw()
                    break

        if not self.play_ch1 and self.rewind_ch1:
            for item in self.dic_channel1.items():
                print(self.x_fig1[item[0]])
                self.ax.plot(self.x_fig1[item[0]], self.y_fig1[item[0]], color=self.colors_channel1[item[0]])
                self.ax.set_xlim(self.Time[self.begin_value], self.Time[self.specific_row])
                self.fig.canvas.draw()
                break

        # channel2
        if self.ax2.get_navigate_mode() == "PAN" and self.play_ch2:
            y_min, y_max = self.ax2.get_ylim()

            if y_min < -1 or y_max > 1:
                self.ax2.set_ylim(-1, 1)
                self.fig2.canvas.draw()
        if self.ax2.get_navigate_mode() == "PAN" and not self.play_ch2:
            x_min, x_max = self.ax2.get_xlim()
            y_min, y_max = self.ax2.get_ylim()
            for item in self.dic_channel2.items():
                print(f"ite:{item[0]}")
                if x_min < self.Time[3] and item[0] == 0:
                    new_x_min = self.Time[3]
                    print(x_min)
                    print(f"new:{new_x_min}")
                    self.ax2.set_xlim(new_x_min, self.Time[10])
                    self.fig2.canvas.draw()

                if (y_min < -1 and item[0] == 0) or (y_max > 1 and item[0] == 0):
                    self.ax2.set_ylim(-1, 1)
                    self.fig2.canvas.draw()

                if x_max > self.Time[self.specific_row_2] and item[0] == 0:
                    new_x_max = self.Time[self.specific_row_2]
                    self.ax2.set_xlim(self.Time[self.specific_row_2 - 28], new_x_max)
                    self.fig2.canvas.draw()
                    break

        if not self.play_ch2 and self.rewind_ch2:
            for item in self.dic_channel2.items():
                print(self.x_fig2[item[0]])
                self.ax2.plot(self.x_fig2[item[0]], self.y_fig2[item[0]], color=self.colors_channel2[item[0]])
                self.ax2.set_xlim(self.Time[self.begin_value_2], self.Time[self.specific_row_2])
                self.fig2.canvas.draw()
                break

    def toggle_channel_animation(self, ani_num):
        if ani_num is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("No animations to toggle.")
            msg.show()
            msg.exec_()
            return
        if ani_num == self.ani:
            if self.Qwindow.pause_button.text() == "►":
                self.Qwindow.pause_button.setText("❚❚")
                self.play_ch1 = True
                self.ani.event_source.start()
                shortcut1 = QShortcut(QKeySequence('Ctrl+P'), self.Qwindow)
                shortcut1.activated.connect(self.Qwindow.pause_button.click)
            else:
                self.Qwindow.pause_button.setText("►")
                self.play_ch1 = False
                self.ani.event_source.stop()
                shortcut1 = QShortcut(QKeySequence('Ctrl+P'), self.Qwindow)
                shortcut1.activated.connect(self.Qwindow.pause_button.click)
        else:
            if self.Qwindow.pause_button_2.text() == "►":
                self.Qwindow.pause_button_2.setText("❚❚")
                shortcut2 = QShortcut(QKeySequence('Ctrl+B'), self.Qwindow)
                shortcut2.activated.connect(self.Qwindow.pause_button_2.click)
                self.play_ch2 = True
                self.play_ch1 = "None"
                self.ani2.event_source.start()
            else:
                self.Qwindow.pause_button_2.setText("►")
                shortcut2 = QShortcut(QKeySequence('Ctrl+B'), self.Qwindow)
                shortcut2.activated.connect(self.Qwindow.pause_button_2.click)
                self.play_ch2 = False
                self.play_ch1 = "None"
                self.ani2.event_source.stop()
        if self.link:
            if self.play_ch1 and self.play_ch1 != "None":
                self.ani2.event_source.start()
                self.Qwindow.pause_button_2.setText("❚❚")
            elif not self.play_ch1 and self.play_ch1 != "None":
                self.ani2.event_source.stop()
                self.Qwindow.pause_button_2.setText("►")
            else:
                if self.play_ch2:
                    self.ani.event_source.start()
                    self.Qwindow.pause_button.setText("❚❚")
                else:
                    self.ani.event_source.stop()
                    self.Qwindow.pause_button.setText("►")

    def Zoom_out_channel1(self):

        y_min, y_max = self.ax.get_ylim()
        y_min -= 0.01
        y_max += 0.01
        self.ax.set_ylim(y_min, y_max)
        # canvas refers to the area where the figure and its subplots are drawn
        self.fig.canvas.draw()

    def Zoom_out_channel2(self):
        y_min, y_max = self.ax2.get_ylim()
        y_min -= 0.01
        y_max += 0.01
        self.ax2.set_ylim(y_min, y_max)
        self.fig2.canvas.draw()

    def link_two_graphs(self):  # to link two graphs
        if self.Qwindow.link_button.isChecked():
            self.link = True
        else:
            self.link = False

    def animate_fig2(self, i):  # To animate graph 2
        if self.pause_ch2 or self.rewind_ch2:  # to Pause or Rewind Graph1
            self.ani2.event_source.stop()
            self.ani2 = FuncAnimation(self.fig2, self.animate_fig2, interval=self.delay_interval,
                                      frames=self.frames_channel2, repeat=False)

            self.pause_ch2 = False
            self.rewind_ch2 = False
        self.specific_row_2 += 1  # update frame
        print(f"s2:{self.specific_row_2}")
        self.current_data_2 = self.specific_row_2
        found = True
        for idx_line_ch2 in self.dic_channel2.items():  # iterate on lines ,dic={line:data of line,...}
            print(len(self.dic_channel2.items()))
            print(len(self.present_line2))
            # present line => lines except first one to begin other lines from the last time which first line is drawn
            # check if line in present lines or not
            if idx_line_ch2[0] in self.present_line2.keys():  # presentline = {index_line: current data(index)}
                print(len(self.present_line2))
                for idx_line2 in self.present_line2.items():
                    if idx_line2[0] == idx_line_ch2[0]:
                        print(f"l:{idx_line2[1]}")
                        current_idx_2 = idx_line2[1]
                        # append data to update graph2
                        self.y_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][self.specific_row_2 -
                                                                            (current_idx_2 + 1)])
                        print(f"line2:{self.x_fig2[idx_line_ch2[0]]}")
                        self.lines2[idx_line_ch2[0]].set_data(self.x_fig2[idx_line_ch2[0]],
                                                              self.y_fig2[idx_line_ch2[0]])
                        self.current_data_2 = self.specific_row_2 - current_idx_2
            else:
                # append data to update graph2 to first line
                if self.link:
                    self.x_fig2[idx_line_ch2[0]].append(self.Time[self.specific_row])
                    self.y_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][self.specific_row_2])
                else:
                    self.x_fig2[idx_line_ch2[0]].append(self.Time[self.specific_row_2])
                    self.y_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][self.specific_row_2])

                print(self.x_fig2[idx_line_ch2[0]])
                self.lines2[idx_line_ch2[0]].set_data(self.x_fig2[idx_line_ch2[0]], self.y_fig2[idx_line_ch2[0]])

            if self.link:  # check if two graphs linked or not
                if self.specific_row > 30 and found:  # update limit
                    print("alllo")
                    # self.current_data = self.specific_row - current_idx
                    self.ax2.set_xlim(self.Time[self.specific_row - 30], self.Time[self.specific_row])
                    found = False
                # check which button is clicked
                if self.ax.get_navigate_mode() == 'ZOOM' or self.ax.get_navigate_mode() == 'PAN':
                    print(self.ax.get_navigate_mode())
                    limx = self.ax.get_xlim()
                    limy = self.ax.get_ylim()
                    self.ax2.set_xlim(limx)
                    self.ax2.set_ylim(limy)
            else:
                if self.current_data_2 > 30 and found:  # update limits and move it
                    #      self.current_data = self.specific_row - current_idx
                    self.ax2.set_xlim(self.Time[self.current_data_2 - 30], self.Time[self.current_data_2])
                    found = False
        return tuple(self.lines2)  # return lines to plot ,lines=[self.ax.plot(data_x,datay),...]

    def animate_fig1(self, i):  # to animate graph1
        if self.pause_ch1 or self.rewind_ch1:  # TO Pause or Rewind The Graph2
            self.ani.event_source.stop()
            self.ani = FuncAnimation(self.fig, self.animate_fig1, interval=self.delay_interval,
                                     frames=self.frames_channel1, repeat=False)

            self.pause_ch1 = False
            self.rewind_ch1 = False
        print(f"rew2:{self.rewind_ch1}")
        self.specific_row += 1  # update frame
        self.current_data = self.specific_row
        print(f"s1:{self.specific_row, i}")
        found1 = True
        # present line => lines except first one to begin other lines from the last time which first line is drawn
        for idx_line_ch1 in self.dic_channel1.items():  # iterate on lines ,dic={line:data of line,...}
            if idx_line_ch1[0] != 0 and idx_line_ch1[0] in self.present_line1.keys():
                for idx_line1 in self.present_line1.items():  # check if line in present lines or not
                    if idx_line1[0] == idx_line_ch1[0]:
                        print(f"l:{idx_line1[1]}")
                        # print(f"len:{len(idx_line_ch1[1][0])}")
                        current_idx = idx_line1[1] + 1
                        self.x_fig1[idx_line_ch1[0]].append(self.Time[self.specific_row])
                        # append data to update graph1
                        self.y_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][self.specific_row - current_idx])
                        print(f"line2:{self.x_fig1[idx_line_ch1[0]]}")
                        self.lines1[idx_line_ch1[0]].set_data(self.x_fig1[idx_line_ch1[0]],
                                                              self.y_fig1[idx_line_ch1[0]])
                        self.current_data = self.specific_row - current_idx
            else:
                # append data to update graph1 to first line
                self.y_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][self.specific_row])
                self.x_fig1[idx_line_ch1[0]].append(self.Time[self.specific_row])
                print(f"x_data:{self.x_fig1[idx_line_ch1[0]]}")
                print(f"time:{self.y_fig1[idx_line_ch1[0]]}")
                self.lines1[idx_line_ch1[0]].set_data(self.x_fig1[idx_line_ch1[0]], self.y_fig1[idx_line_ch1[0]])
            if self.link:  # check if two graphs linked or not
                if self.current_data > 30 and found1:
                    # self.current_data = self.specific_row - current_idx
                    self.ax.set_xlim(self.Time[self.current_data - 30], self.Time[self.current_data])
                    found1 = False

                # check which button is clicked
                if self.ax2.get_navigate_mode() == 'ZOOM' or self.ax2.get_navigate_mode() == 'PAN':
                    print(self.ax2.get_navigate_mode())
                    limx = self.ax2.get_xlim()
                    limy = self.ax2.get_ylim()
                    self.ax.set_xlim(limx)
                    self.ax.set_ylim(limy)
            else:
                if self.current_data > 30 and found1:  # update limits
                    self.ax.set_xlim(self.Time[self.current_data - 30], self.Time[self.current_data])
                    found1 = False

        return tuple(self.lines1)  # return lines to plot

    def increase_speed(self, button_name):  # to increase speed
        if self.delay_interval is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please Upload A Signal")
            msg.show()
            msg.exec_()

        else:
            if button_name == self.Qwindow.speed_up_button1:
                self.delay_interval = 40
                self.pause_ch1 = True
                self.pause_ch2 = False

            elif button_name == self.Qwindow.speed_up_button2:
                self.delay_interval = 40
                self.pause_ch2 = True
                self.pause_ch1 = False

            elif self.link:
                self.delay_interval = 40
                self.pause_ch1 = True
                self.pause_ch2 = True

    def decrease_speed(self, button_name):  # decrease speed
        if self.delay_interval is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please Upload A Signal")
            msg.show()
            msg.exec_()
        else:
            if button_name == self.Qwindow.speed_down_button1:
                self.delay_interval = 200
                self.pause_ch1 = True
                self.pause_ch2 = False
            elif button_name == self.Qwindow.speed_down_button2:
                self.delay_interval = 200
                self.pause_ch2 = True
                self.pause_ch1 = False

            elif self.link:
                self.delay_interval = 200
                self.pause_ch1 = True
                self.pause_ch2 = True

    def pan_channel1(self):
        self.fig.canvas.mpl_connect('button_press_event', self.buttonZemaphore)
        self.fig.canvas.mpl_connect('button_release_event', self.buttonZemaphore)
        self.fig.canvas.mpl_connect('motion_notify_event', self.pan_fun_ch1)

    def pan_channel2(self):
        self.fig2.canvas.mpl_connect('button_press_event', self.buttonZemaphore)
        self.fig2.canvas.mpl_connect('button_release_event', self.buttonZemaphore)
        self.fig2.canvas.mpl_connect('motion_notify_event', self.pan_fun_ch2)

    def buttonZemaphore(self, event):
        # changing the flags for panning
        if (event.name == 'button_press_event') and (event.button.numerator == 1):
            # left-mouse button press: activate pan
            self.oldxy = [event.xdata, event.ydata]
            self.panningflag = 1

        elif (event.name == 'button_release_event') and (event.button.numerator == 1):
            # left-mouse button release: deactivate pan
            self.panningflag = 0

    def pan_fun_ch1(self, event):
        # drag-panning the axis
        # This function has to be efficient, as it is polled often.
        if (self.panningflag == 1) and (event.inaxes is not None):
            self.pan_ch1 = True
            # do pan
            self.ax = event.inaxes  # set the axis to work on

            x, y = event.xdata, event.ydata
            print(self.oldxy[0], self.oldxy[1])
            print(f"x,y:{x, y}")
            print(f"limits:{self.ax.get_xlim()}")
            self.ax.set_xlim(self.ax.get_xlim() + self.oldxy[0] - x)  # set new axes limits
            self.ax.set_ylim(self.ax.get_ylim() + self.oldxy[1] - y)
            self.ax.figure.canvas.draw()  # force re-draw

    def pan_fun_ch2(self, event):
        # drag-panning the axis
        # This function has to be efficient, as it is polled often.
        if (self.panningflag == 1) and (event.inaxes is not None):
            self.pan_ch2 = True
            # do pan
            self.ax2 = event.inaxes  # set the axis to work on

            x, y = event.xdata, event.ydata
            print(self.oldxy[0], self.oldxy[1])
            print(f"x,y:{x, y}")
            print(f"limits:{self.ax.get_xlim()}")
            self.ax2.set_xlim(self.ax2.get_xlim() + self.oldxy[0] - x)  # set new axes limits
            self.ax2.set_ylim(self.ax2.get_ylim() + self.oldxy[1] - y)
            self.ax2.figure.canvas.draw()  # force re-draw

    def rewind_channel1(self):  # rewind channels 30 points as 30 milisecond (ms) for channel1
        x_min = self.ax.get_xlim()
        self.rewind_ch1 = True
        listx_1 = []
        listy_1 = []
        listx_11 = []
        listy_11 = []
        self.x_fig1.clear()
        self.y_fig1.clear()

        for item in self.dic_channel1.items():
            print(item[0])
            # store previous data which I can see when I rewind
            if item[0] not in self.present_line1.keys():  # first signal
                self.x_fig1[item[0]] = []
                self.y_fig1[item[0]] = []

                if self.specific_row > 60:
                    print("kskl")
                    self.begin_value = self.specific_row - 60
                    self.specific_row -= 30
                    print(f"sss:{self.specific_row}")
                else:
                    if self.specific_row > 30:
                        self.begin_value = 0
                        self.specific_row = 30
                    else:
                        self.begin_value = 0
                        self.specific_row = self.specific_row
                listx_11 = self.Time[self.begin_value: self.specific_row]
                print(f"list:{listx_11}")
                listy_11 = item[1][self.begin_value: self.specific_row]
                for idx in range(len(listx_11)):
                    self.x_fig1[item[0]].append(listx_11[idx])
                    self.y_fig1[item[0]].append(listy_11[idx])
            else:  # second signal
                self.x_fig1[item[0]] = []
                self.y_fig1[item[0]] = []
                for data in self.present_line1.items():
                    print(f"ii:{data[0]}")
                    print(f"ii:{data[1]}")

                    listx_1 = listx_11
                    print(data[1] - self.begin_value, data[1] - self.specific_row)
                    if data[1] - self.specific_row > 62:
                        begin_value = data[1] - self.specific_row - 30
                    else:
                        begin_value = 0

                    listy_1 = item[1][(begin_value):(data[1] - self.specific_row)]
                    print(f"len:{len(listx_11), len(listy_1)}")

                for idx in range(len(listx_1)):
                    self.x_fig1[item[0]].append(listx_1[idx])
                    self.y_fig1[item[0]].append(listy_1[idx])

                print("hallo")
                print(self.present_line1[item[0]])
                self.present_line1[item[0]] -= 31
        print(f"spe:{self.specific_row}")
        if self.rewind_ch1 and not self.rewind_ch2 and self.link:
            self.rewind_channel2()

    def rewind_channel2(self):
        self.rewind_ch2 = True
        listx_2 = []
        listy_2 = []
        listx_22 = []
        listy_22 = []
        self.x_fig2.clear()
        self.y_fig2.clear()

        for item in self.dic_channel2.items():
            print(item[0])
            # store previous data which I can see when I rewind
            if item[0] not in self.present_line2.keys():  # first signal
                self.x_fig2[item[0]] = []
                self.y_fig2[item[0]] = []
                if self.specific_row_2 > 60:
                    print("kskl")
                    self.begin_value_2 = self.specific_row_2 - 60
                    self.specific_row_2 -= 30
                    print(f"sss:{self.specific_row_2}")
                else:
                    if self.specific_row_2 > 30:
                        self.begin_value_2 = 0
                        self.specific_row_2 = 30
                    else:
                        self.begin_value_2 = 0
                        self.specific_row_2 = self.specific_row

                listx_22 = self.Time[self.begin_value_2: self.specific_row_2]
                print(f"list:{listx_22}")
                listy_22 = item[1][self.begin_value_2: self.specific_row_2]

                for idx in range(len(listx_22)):
                    self.x_fig2[item[0]].append(listx_22[idx])
                    self.y_fig2[item[0]].append(listy_22[idx])
            else:  # second signal
                self.x_fig2[item[0]] = []
                self.y_fig2[item[0]] = []

                for data in self.present_line2.items():
                    print(f"ii:{data[0]}")
                    print(f"ii:{data[1]}")

                    listx_2 = listx_22
                    print(data[1] - self.begin_value, data[1] - self.specific_row)
                    if data[1] - self.specific_row_2 > 62:
                        begin_value_2 = data[1] - self.specific_row_2 - 30
                    else:
                        begin_value_2 = 0

                    listy_1 = item[1][(begin_value_2):(data[1] - self.specific_row_2)]
                    print(f"len:{len(listx_22), len(listy_2)}")

                for idx in range(len(listx_2)):
                    self.x_fig2[item[0]].append(listx_2[idx])
                    self.y_fig2[item[0]].append(listy_2[idx])

                print("hallo")
                print(self.present_line2[item[0]])
                self.present_line2[item[0]] -= 31
        print(f"spe:{self.specific_row_2}")

        if self.rewind_ch2 and not self.rewind_ch1 and self.link:
            self.rewind_channel1()

    def show_color_dialog_ch1(self):  # Function to open a color picker dialog for the signal
        color = QColorDialog.getColor()
        self.Qwindow.color_picker_button.setStyleSheet(f"background-color: {color.name()}; color: white;"
                                                       f"border-radius:50%;")
        # Create a palette for the button text color and set it to the selected color
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, color)
        self.Qwindow.color_picker_button.setPalette(palette)
        # Store the selected color as a signal attribute
        self.signal_color = color.name()
        if not self.add_new_signal:
            if len(self.splitted_names_ch1) > 1:
                self.menu = QMenu()
                self.menu.triggered.connect(self.actionClicked)
                for file_name in self.splitted_names_ch1:
                    self.menu.addAction(file_name)
                action = self.menu.exec_(self.Qwindow.move_button1.mapToGlobal(
                    self.Qwindow.move_button1.rect().bottomLeft()))
                if action is not None:
                    file = action.text()
                    for item in self.files_index_ch1.items():
                        if item[1] == file:
                            self.lines1[item[0]], = self.ax.plot([], [], label=item[1], color=self.signal_color)
                            self.colors_channel1[item[0]] = self.signal_color
                            break

            else:

                for item in self.files_index_ch1.items():
                    if item[1] == self.splitted_names_ch1[0]:
                        print(item[0], self.signal_color)
                        self.colors_channel1[item[0]] = self.signal_color
                        self.lines1[item[0]], = self.ax.plot([], [], label=item[1], color=self.colors_channel1[item[0]])

                        break
        return color

    def show_color_dialog_ch2(self):  # Function to open a color picker dialog for the signal
        color = QColorDialog.getColor()
        self.Qwindow.color_picker_button_2.setStyleSheet(f"background-color: {color.name()}; color: white;"
                                                       f"border-radius:50%;")
        # Create a palette for the button text color and set it to the selected color
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, color)
        self.Qwindow.color_picker_button_2.setPalette(palette)
        # Store the selected color as a signal attribute
        self.signal_color = color.name()
        if len(self.splitted_names_ch2) > 1:
            self.menu = QMenu()
            self.menu.triggered.connect(self.actionClicked)
            for file_name in self.splitted_names_ch2:
                self.menu.addAction(file_name)
            action = self.menu.exec_(self.Qwindow.move_button2.mapToGlobal(
                self.Qwindow.move_button2.rect().bottomLeft()))
            if action is not None:
                file = action.text()
                for item in self.files_index_ch2.items():
                    if item[1] == file:
                        self.lines2[item[0]], = self.ax2.plot([], [], label=item[1], color=self.signal_color)
                        self.colors_channel2[item[0]] = self.signal_color
                        break
        else:
            for item in self.files_index_ch2.items():
                if item[1] == self.splitted_names_ch2[0]:
                    print(item[0], self.signal_color)
                    self.lines2[item[0]], = self.ax2.plot([], [], label=item[1], color=self.signal_color)
                    self.colors_channel2[item[0]] = self.signal_color
                    break
        return color

    def Plot_channel1(self, file_name):
        if self.hide_action_ch1:
            self.specific_row = 0
            self.hide_action_ch1 = False
        self.signal_values_list = self.read_ecg_data_from_csv(file_name)
        file_part = file_name.split('/')[-1].split('.')[0]
        self.visited_channel1.append(file_part)
        data_y = self.signal_values_list
        y_range = (floor(min(data_y)), ceil(max(data_y)))
        self.count_files_channel1 = Counter(self.visited_channel1)
        for item in self.count_files_channel1.items():  # get no of repeateed signal
            if item[0] == file_part:
                no_of_repeated = item[1]
                break
        print(len(self.present_line1))
        # show line
        if no_of_repeated == 1:
            if self.move_to_ch1:
                self.specific_row = 0
                self.move_to_ch1 = False
            self.splitted_names_ch1.append(file_part)
            self.previous_line1 = self.no_of_line
            self.no_of_line += 1  # every line take number which is key to access line
            # put limits
            self.ax.set_ylim(y_range)
            self.ax.set_xlim(self.Time[3], self.Time[30])
            self.delay_interval = 200
            if self.no_of_line == 1:  # to call func animation once
                graph_ch1 = True
            else:
                graph_ch1 = False
            for index in range(self.previous_line1, self.no_of_line):  # store lines of graph1
                self.hidden_line_ch1[file_part] = index
                self.files_index_ch1[index] = file_part
                self.lines1[index], = self.ax.plot([], [], label=file_part, color=self.signal_color)
                self.colors_channel1[index] = self.signal_color
                self.x_fig1[index] = []
                self.y_fig1[index] = []
            # to add another /signals and begin  from last time of first line
            if self.no_of_line > 1 and len(self.visited_channel1) != 1:
                self.present_line1[self.no_of_line - 1] = self.specific_row

            self.dic_channel1[self.no_of_line - 1] = self.read_ecg_data_from_csv(file_name)
            if graph_ch1:  # create animation
                self.ani = FuncAnimation(self.fig, self.animate_fig1, interval=200,
                                         frames=self.frames_channel1, repeat=False)
            self.ax.legend()  # set label to lines
            if graph_ch1:  # show graph on graphics view
                scene1 = QtWidgets.QGraphicsScene()
                self.canvas1 = FigureCanvasQTAgg(self.fig)
                self.Qwindow.graphicsView_channel1.setScene(scene1)
                scene1.addWidget(self.canvas1)
                self.toolbar_1 = NavigationToolbar(self.canvas1, self.Qwindow)
                # Remove the Home and Customize buttons from the toolbar
                unwanted_buttons = ['Customize', 'Home', 'Subplots', 'Back', 'Forward']
                for x in self.toolbar_1.actions():
                    if x.text() in unwanted_buttons:
                        self.toolbar_1.removeAction(x)
                # Finding The Zoom In button and changing it's icon
                for items in self.toolbar_1.toolitems:
                    print(items)

                actions = self.toolbar_1.actions()
                fourth_action = actions[2]
                second_action = actions[1]
                sixth_action = actions[4]
                sixth_action.triggered.disconnect()
                # Connect it to a custom function that handles saving
                sixth_action.triggered.connect(self.custom_save_function)
                zoom_in_icon = icon("fa.search-plus",
                                    color="white")
                pan_icon = icon("fa.hand-paper-o", color="white")
                screenshot_icon = icon("ri.screenshot-2-fill", color="white")
                fourth_action.setIcon(zoom_in_icon)
                second_action.setIcon(pan_icon)
                sixth_action.setIcon(screenshot_icon)
                zoom_out_icon = icon("fa.search-minus", color="white")
                zoom_out_button1 = QtWidgets.QAction(zoom_out_icon, "Zoom Out", self.Qwindow)
                zoom_out_button1.triggered.connect(self.Zoom_out_channel1)
                self.toolbar_1.insertAction(self.toolbar_1.actions()[4], zoom_out_button1)
                for child in self.toolbar_1.findChildren(QtWidgets.QToolButton):
                    child.setStyleSheet("background-color: #849dad; ")
                self.Qwindow.tableWidget.show()
                self.Qwindow.pause_button.show()
                self.Qwindow.rewind_button1.show()
                self.Qwindow.move_button1.show()
                self.Qwindow.hide_button1.show()
                self.Qwindow.speed_up_button1.show()
                self.Qwindow.speed_down_button1.show()
                self.Qwindow.color_picker_button.show()
                self.Qwindow.verticalLayout_toolbar1.addWidget(self.toolbar_1)

    def browse_file(self):
        options = QFileDialog.Options()
        # file_prev = file_name
        file_name, _ = QFileDialog.getOpenFileName(None, "Open File", "",
                                                   "CSV Files (*.csv)",
                                                   options=options)

        if file_name:
            self.files_name.append(file_name)
            file_name = str(file_name)
            file_part = file_name.split('/')[-1].split('.')[0]
            self.line = file_part
            self.Qwindow.signals_name.addItem(self.line)
            self.Plot_channel1(file_name)
            self.row_counter = self.row_counter + 1
            self.Qwindow.tableWidget.setRowCount(self.row_counter)
            self.mean = self.Qwindow.calc_mean(self.signal_values_list)
            self.std = self.Qwindow.calc_std(self.signal_values_list)
            # self.duration = self.Qwindow.calc_duration(self.time_list)
            self.min_value, self.max_value = self.Qwindow.calc_min_max_values(self.signal_values_list)
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 0, QTableWidgetItem(self.line))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 1, QTableWidgetItem(str(round(self.mean, 8))))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 2, QTableWidgetItem(str(round(self.std, 8))))
            # self.Qwindow.tableWidget.setItem(self.row_counter - 1, 3, QTableWidgetItem(str(self.duration)))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 3, QTableWidgetItem(str(self.min_value)))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 4, QTableWidgetItem(str(self.max_value)))

    def read_ecg_data_from_csv(self, file_name):
        with open(file_name, 'r') as csv_file:
            print(f"csv:{csv_file}")
            csv_reader = pd.read_csv(csv_file)
            signal_values_list = csv_reader.iloc[:, 1].tolist()
            print(f"sig:{signal_values_list[:10]}")
        return signal_values_list

    def open_window(self):
        self.Dwindow.show()

    def custom_save_function(self):
        # A function to choose a specific folder to save the image in
        file_path = f"screenshots/channel1no{self.img_channel1_counter}.png"
        # Specify the frmat, e.g., "png"
        format = "png"
        # Save the figure to the specified path and format
        self.canvas1.print_figure(file_path, format=format)
        self.img_channel1_counter += 1

    def custom_save_function_channel2(self):
        file_path = f"screenshots/channel2no{self.img_channel2_counter}.png"
        # Specify the frmat, e.g., "png"
        format = "png"
        # Save the figure to the specified path and format
        self.canvas2.print_figure(file_path, format=format)
        self.img_channel2_counter += 1

    def add_new_pdf_page(self):
        img_header = "Vital Signs Image"
        header_text_style = styles.getSampleStyleSheet()["Normal"]
        header_text_style.alignment = 1  # 1 represents center alignment
        header_text_style.fontSize = 16  # Set font size to 12px
        header_text_style.fontWeight = 'bold'  # Set font size to 12px
        paragraph = Paragraph(img_header, header_text_style)
        self.page_container.append(paragraph)
        self.page_container.append(Spacer(1, 0.5 * inch))
        folder_path = "screenshots"
        # List all files in the folder
        image_files = glob.glob(os.path.join(folder_path, '*.png'))
        file_names = [os.path.basename(path) for path in image_files]
        # Read and process each image
        for image_path in file_names:
            pdf_image = Image(f"screenshots/{image_path}", width=8 * inch, height=4 * inch)
            self.page_container.append(pdf_image)
            self.page_container.append(PageBreak())
            self.page_container.append(Spacer(1, 1 * inch))
        # Adding Header for the comment section and styling it
        table_header = "Signals Statistics Information: "
        theader_text_style = styles.getSampleStyleSheet()["Normal"]
        theader_text_style.alignment = 1  # 1 represents center alignment
        theader_text_style.fontSize = 16  # Set font size to 12px
        theader_text_style.fontWeight = 'bold'  # Set font size to 12px
        paragraph = Paragraph(table_header, theader_text_style)
        self.page_container.append(paragraph)
        self.page_container.append(Spacer(1, 0.5 * inch))
        # Adding Signals statistics
        table_header = ["Name", "Mean", "Std", "Min Value", "Max Value"]
        self.statistics_data.append(table_header)
        # Add the table data for each row
        for i in range(self.row_counter):
            row_data = [
                self.Qwindow.tableWidget.item(i, 0).text(),
                self.Qwindow.tableWidget.item(i, 1).text(),
                self.Qwindow.tableWidget.item(i, 2).text(),
                self.Qwindow.tableWidget.item(i, 3).text(),
                self.Qwindow.tableWidget.item(i, 4).text(),
                # self.Qwindow.tableWidget.item(i, 5).text()
            ]
            self.statistics_data.append(row_data)
        # Create the table and style
        table = Table(self.statistics_data, colWidths=[1.5 * inch] * 6)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        self.page_container.append(table)
        self.page_container.append(PageBreak())
        # Adding Header for the comment section and styling it
        doctor_header = "Doctor's Comments: "
        dheader_text_style = styles.getSampleStyleSheet()["Normal"]
        dheader_text_style.fontSize = 16  # Set font size to 12px
        dheader_text_style.fontWeight = 'bold'  # Set font size to 12px
        paragraph = Paragraph(doctor_header, dheader_text_style)
        self.page_container.append(paragraph)
        self.page_container.append(Spacer(1, 0.5 * inch))
        # Add text to the PDF
        text = self.Dwindow.comment_section.toPlainText()
        text_style = styles.getSampleStyleSheet()["Normal"]
        text_style.alignment = 1  # 1 represents center alignment
        text_style.fontSize = 14  # Set font size to 12px
        paragraph = Paragraph(text, text_style)
        self.page_container.append(paragraph)
        self.pdf_counter += 1
        self.Dwindow.comment_section.setText("")
        self.doc.build(self.page_container)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # List all files in the directory
            files = os.listdir(folder_path)
            # Loop through the files and delete only if they are image files (you can customize this check)
            for file in files:
                file_path = os.path.join(folder_path, file)
                # You can customize this condition to check for specific image file extensions
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
            else:
                print(f"The folder path {folder_path} does not exist or is not a directory.")


class MainApp(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Signal Real-Time Monitoring")
        self.Timer = QTimer(self)

    # Calculate the Mean of the signal
    def calc_mean(self, values):
        return np.mean(values)

    # Calculate the Standard Deviation of the signal
    def calc_std(self, values):
        return np.std(values)

    # Calculate the signal Duration
    def calc_duration(self, time):
        return np.max(time)

    # Calculate minimum and maximum values
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
