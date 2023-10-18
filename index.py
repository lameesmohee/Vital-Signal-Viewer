import matplotlib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.units import inch
import glob
from reportlab.platypus.doctemplate import Spacer
from reportlab.lib import styles
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
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
import os

MainUI, _ = loadUiType(path.join(path.dirname(__file__), 'main.ui'))
DocumentWindowUI, _ = loadUiType(path.join(path.dirname(__file__), 'DocumentWindow.ui'))


class File:
    def __init__(self):
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
        self.frames_channel1 = 300
        self.frames_channel2 = 300
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
        self.fig = plt.figure(figsize=(1450 / 80, 345 / 80), dpi=80)
        self.fig2 = plt.figure(figsize=(1450 / 80, 345 / 80), dpi=80)
        self.previous_specific_row = 0
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
        self.pdf_filename = f"Medical Report {self.pdf_counter}.pdf"
        self.doc = SimpleDocTemplate(self.pdf_filename, pagesize=letter)
        self.Qwindow.tableWidget.hide()
        self.img_channel1_counter = 0
        self.img_channel2_counter = 0
        self.statistics_data = []

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
        self.Dwindow.save_button.clicked.connect(self.create_pdf_file)
        QCoreApplication.processEvents()
        self.Dwindow.save_button.clicked.connect(self.Dwindow.close)
        QCoreApplication.processEvents()
        self.Qwindow.Timer.timeout.connect(self.Pause_pan)
        self.Qwindow.Timer.start(10)

    def Ui_graph_channel2(self):   # Styling the UI of the 2nd graph
        self.fig2.set_facecolor('#F0F5F9')
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_facecolor('#F0F5F9')
        left_margin = 0.1  # Adjust this value as needed
        self.ax2.set_position([left_margin, 0.1, 0.78, 0.85])  # [left, bottom, width, height]
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
        left_margin = 0.1  # Adjust this value as needed
        self.ax.set_position([left_margin, 0.1, 0.78, 0.85])    # [left, bottom, width, height]
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
        self.Qwindow.pause_button.hide()
        self.Qwindow.pause_button_2.hide()
        self.Qwindow.rewind_button1.hide()
        self.Qwindow.rewind_button2.hide()
        self.Qwindow.pause_button.setStyleSheet("background-color: #849dad;"
                                                " color: white;"
                                                "font-size: 16px")
        self.Qwindow.pause_button_2.setStyleSheet("background-color: #849dad;"
                                                  " color: white;"
                                                  "font-size: 16px")
        self.Qwindow.setFixedSize(1400, 1000)
        rewind_icon = icon("fa.backward", color='white')
        plus_icon = icon("fa.plus", color='white')
        minus_icon = icon("fa.minus", color='white')
        self.Qwindow.plus_button.setIcon(plus_icon)
        self.Qwindow.minus_button.setIcon(minus_icon)
        self.Qwindow.rewind_button1.setIcon(rewind_icon)
        self.Qwindow.rewind_button2.setIcon(rewind_icon)
        self.Qwindow.rewind_button1.setStyleSheet("background-color: #849dad;")
        self.Qwindow.rewind_button2.setStyleSheet("background-color: #849dad;")
        self.Qwindow.menuFile.setStyleSheet("QMenu::item:selected {background:#708694;}");
        self.Qwindow.graphicsView_channel1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Qwindow.graphicsView_channel1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Qwindow.graphicsView_channel2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Qwindow.graphicsView_channel2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
                self.play_ch1= "None"
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

    def Pause_pan(self):
        if self.ax.get_navigate_mode() == "PAN" and not self.play_ch1 and not self.link:
            x_min, x_max = self.ax.get_xlim()
            for item in self.dic_channel1.items():
                print(f"ite:{item[0]}")
                if x_min < item[1][0][1] and item[0] == 0:
                    new_x_min = item[1][0][1]
                    print(x_min)
                    print(f"new:{new_x_min}")
                    self.ax.set_xlim(new_x_min, item[1][0][5])
                    break
        if self.ax.get_navigate_mode() == "PAN" and not self.play_ch1 and not self.link:
            for item in self.dic_channel1.items():
                if x_max > item[1][0][self.specific_row] and item[0] == 0:
                    new_x_max = item[1][0][self.specific_row]
                    self.ax.set_xlim(item[1][0][self.specific_row - 28], new_x_max)
                    break
        if self.ax.get_navigate_mode() == "PAN" and not self.play_ch1 and self.link:
            if x_min < self.data_x_limits[1]:
                new_x_min = self.data_x_limits[1]
                print(x_min)
                print(f"new:{new_x_min}")
                self.ax.set_xlim(new_x_min, self.data_x_limits[5])
            if x_max > self.data_x_limits[self.specific_row]:
                    new_x_max = self.data_x_limits[self.specific_row]
                    self.ax.set_xlim(self.data_x_limits[self.specific_row - 28], new_x_max)

        if not self.play_ch1 and self.rewind_ch1:
            for item in self.dic_channel1.items():
                print(self.last_value)
                print(self.begin_value)
                print(self.x_fig1[item[0]])
                self.ax.plot(self.x_fig1[item[0]], self.y_fig1[item[0]], color=self.colors_channel1[item[0]])
                self.ax.set_xlim(item[1][0][self.begin_value], item[1][0][self.last_value])
                self.fig.canvas.draw()
                break
        if self.ax2.get_navigate_mode() == "PAN" and not self.play_ch2:
            x_min, x_max = self.ax2.get_xlim()
            for item in self.dic_channel2.items():
                if x_min < item[1][0][1] and item[0] == 0:
                    new_x_min = item[1][0][1]
                    self.ax2.set_xlim(new_x_min, item[1][0][5])
                    break
            for item in self.dic_channel2.items():
                if x_max > item[1][0][self.specific_row_2] and item[0] == 0:
                    new_x_max = item[1][0][self.specific_row_2]
                    self.ax.set_xlim(item[1][0][self.specific_row_2 - 28], new_x_max)
                    break
        if not self.play_ch2 and self.rewind_ch2:
            for item in self.dic_channel2.items():
                print(self.last_value_2)
                print(self.begin_value_2)
                print(self.x_fig2[item[0]])
                self.ax2.plot(self.x_fig2[item[0]], self.y_fig2[item[0]], color=self.colors_channel2[item[0]])
                self.ax2.set_xlim(item[1][0][self.begin_value_2], item[1][0][self.last_value_2])
                self.fig2.canvas.draw()
                break

    def link_two_graphs(self):  # to link two graphs
        if self.Qwindow.link_button.isChecked():
            self.link = True
            # Normalize limits
            x_limits = (floor((min(self.data_x_limits)) - 0.05), ceil(max(self.data_x_limits) + 0.01))
            y_limits = (floor((min(self.data_y_limits)) - 0.05), ceil(max(self.data_y_limits) + 0.01))
            # same time frames
            self.ax.set_xlim(x_limits)
            self.ax2.set_xlim(x_limits)
            self.ax.set_ylim(y_limits)
            self.ax2.set_ylim(y_limits)
        else:
            self.link = False

    def animate_fig2(self, i):  # To animate graph 2
        if self.pause_ch2 or self.rewind_ch2:  # to Pausr or Rewind Graph1
            self.ani2.event_source.stop()
            self.ani2 = FuncAnimation(self.fig2, self.animate_fig2, interval=self.delay_interval,
                                      frames=self.frames_channel2, repeat=False)
            self.pause_ch2 = False
            self.rewind_ch2 = False
        self.specific_row_2 += 1     # update frame
        print(f"s2:{self.specific_row_2}")
        self.current_data_2 = self.specific_row_2
        found = True
        for idx_line_ch2 in self.dic_channel2.items():   # iterate on lines ,dic={line:data of line,...}
            print(len(self.dic_channel2.items()))
            print(len(self.present_line2))
            # present line => lines except first one to begin other lines from the last time which first line is drawn
            # check if line in present lines or not
            # present_line2 contains the signals that are in the second port
            if idx_line_ch2[0] != 0 and idx_line_ch2[0] in self.present_line2.keys():
                print(len(self.present_line2))
                for idx_line2 in self.present_line2.items():
                    if idx_line2[0] == idx_line_ch2[0]:
                        print(f"l:{idx_line2[1]}")
                        current_idx_2 = idx_line2[1]
                        # append data to update graph2
                        self.x_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][0][self.specific_row_2 -
                                                                               (current_idx_2 + 1)])
                        self.y_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][1][self.specific_row_2 -
                                                                               (current_idx_2 + 1)])
                        print(f"line2:{self.x_fig2[idx_line_ch2[0]]}")
                        self.lines2[idx_line_ch2[0]].set_data(self.x_fig2[idx_line_ch2[0]],
                                                              self.y_fig2[idx_line_ch2[0]])
                        self.current_data_2 = self.specific_row_2 - current_idx_2
            else:
                # append data to update graph2 to first line
                self.x_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][0][self.specific_row_2])
                self.y_fig2[idx_line_ch2[0]].append(idx_line_ch2[1][1][self.specific_row_2])
                print(self.x_fig2[idx_line_ch2[0]])
                self.lines2[idx_line_ch2[0]].set_data(self.x_fig2[idx_line_ch2[0]], self.y_fig2[idx_line_ch2[0]])
                if self.current_data_2 == 2:
                    self.ax2.set_xlim(idx_line_ch2[1][0][self.current_data_2 - 10],
                                      idx_line_ch2[1][0][self.current_data_2])
                    self.specific_row_2 = 31
                    self.current_data_2 = 31
            if self.link:  # check if two graphs liked or not
                if self.current_data_2 > 30 and found:  # update limits
                    # self.current_data = self.specific_row - current_idx
                    self.ax2.set_xlim(self.data_x_limits[self.current_data_2 - 30],
                                      self.data_x_limits[self.current_data_2])
                    found = False
                # check which button is clicked
                if self.ax.get_navigate_mode() == 'ZOOM' or self.ax.get_navigate_mode() == 'PAN':
                    print(self.ax.get_navigate_mode())
                    limx = self.ax.get_xlim()
                    limy = self.ax.get_ylim()
                    self.ax2.set_xlim(limx)
                    self.ax2.set_ylim(limy)
            else:
                if self.current_data_2 > 30 and found:   # update limits
                    #      self.current_data = self.specific_row - current_idx
                    self.ax2.set_xlim(idx_line_ch2[1][0][self.current_data_2 - 30],
                                      idx_line_ch2[1][0][self.current_data_2])
                    found = False
        return tuple(self.lines2)  # return lines to plot ,lines=[self.ax.plot(data_x,datay),...]

    def animate_fig1(self, i):  # to animate graph1
        if self.pause_ch1 or self.rewind_ch1:  # TO Pause or Rewind The Graph2
            self.ani.event_source.stop()
            self.ani = FuncAnimation(self.fig, self.animate_fig1, interval=self.delay_interval,
                                     frames=self.frames_channel1, repeat=False)
            self.pause_ch1 = False
            self.rewind_ch1 = False
        self.specific_row += 1     # update frame
        self.current_data = self.specific_row
        print(f"s1:{self.specific_row , i}")
        found1 = True
        # present line => lines except first one to begin other lines from the last time which first line is drawn
        for idx_line_ch1 in self.dic_channel1.items():    # iterate on lines ,dic={line:data of line,...}
            if idx_line_ch1[0] != 0 and idx_line_ch1[0] in self.present_line1.keys():
                for idx_line1 in self.present_line1.items():  # check if line in present lines or not
                    if idx_line1[0] == idx_line_ch1[0]:
                        print(f"l:{idx_line1 [1]}")
                        print(f"len:{len(idx_line_ch1[1][0])}")
                        current_idx = idx_line1[1]+1
                        # append data to update graph1
                        self.x_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][0][self.specific_row - current_idx])
                        self.y_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][1][self.specific_row - current_idx])
                        print(f"line2:{self.x_fig1[ idx_line_ch1 [0]]}")
                        self.lines1[idx_line_ch1[0]].set_data(self.x_fig1[idx_line_ch1[0]],
                                                              self.y_fig1[idx_line_ch1[0]])
                        self.current_data = self.specific_row - current_idx
            else:
                # append data to update graph2 to first line
                self.x_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][0][self.specific_row])
                self.y_fig1[idx_line_ch1[0]].append(idx_line_ch1[1][1][self.specific_row])
                print(self.x_fig1[idx_line_ch1[0]])
                self.lines1[idx_line_ch1[0]].set_data(self.x_fig1[idx_line_ch1[0]], self.y_fig1[idx_line_ch1[0]])
                if self.current_data == 2:
                    self.ax.set_xlim(idx_line_ch1[1][0][self.current_data - 10], idx_line_ch1[1][0][self.current_data])
                    self.specific_row = 31
                    self.current_data = 31

            if self.link:  # check if two graphs liked or not
                if self.current_data > 30 and found1:
                    # self.current_data = self.specific_row - current_idx
                    self.ax.set_xlim(self.data_x_limits[self.current_data_2 - 30],
                                     self.data_x_limits[self.current_data_2])
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
                    self.ax.set_xlim(idx_line_ch1[1][0][self.current_data - 30], idx_line_ch1[1][0][self.current_data])
                    found1 = False
        return tuple(self.lines1)  # return lines to plot

    def increase_speed(self):  # to increase speed
        if self.delay_interval is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please Upload A Signal")
            msg.show()
            msg.exec_()
        else:
            # global ani
            self.delay_interval = 40
            channel1, channel2 = self.Ischecked()
            if channel1 == "channel1" and channel2 == "None":  # check which channel selected
                print(f"Time:{self.delay_interval}")
                self.pause_ch1 = True
            elif channel2 == "channel2" and channel1 == "None":
                self.pause_ch2 = True
            elif channel2 == "channel2" and channel1 == "channel1":
                self.pause_ch2 = True
                self.pause_ch1 = True
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setInformativeText("Please Upload a Signal")
                msg.show()
                msg.exec_()

    def decrease_speed(self):  # decrease speed
        if self.delay_interval is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please Upload A Signal")
            msg.show()
            msg.exec_()
        else:
            # check which channel selected
            self.delay_interval = 200
            channel1, channel2 = self.Ischecked()
            if channel1 == "channel1" and channel2 == "None":
                self.pause_ch1 = True
            elif channel2 == "channel2" and channel1 == "None":
                self.pause_ch2 = True
            elif channel2 == "channel2" and channel1 == "channel1":
                self.pause_ch1 = True
                self.pause_ch2 = True
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setInformativeText("Please Upload a Signal")
                msg.show()
                msg.exec_()

    def rewind_channel1(self):  # rewind channels 30 points as 30 millisecond (ms) for channel1
        if self.specific_row >= 62:
            return_value = 31
            self.begin_value = self.specific_row - 2 * 31

        else:
            if self.specific_row >= 31:
                return_value = 31
                self.begin_value = 0

            else:
                return_value = self.specific_row
                self.begin_value = 0

        self.specific_row -= return_value  # return points 30 point
        self.last_value = self.specific_row
        listx_1 = []
        listy_1 = []
        listx_11 = []
        listy_11 = []
        # clear previous data
        self.x_fig1.clear()
        self.y_fig1.clear()
        for item in self.dic_channel1.items():
            print(item[0])
            self.x_fig1[item[0]] = []
            self.y_fig1[item[0]] = []
            # store previous data which I can see when I rewind
            if item[0] not in self.present_line1.keys():
                print("hallo")
                print(listx_11)
                print(item[1][0][self.begin_value])
                print(item[1][0][self.last_value])
                listx_11 = item[1][0][self.begin_value: self.last_value]
                listy_11 = item[1][1][self.begin_value: self.last_value]
                for idx in range(len(listx_11)):
                    self.x_fig1[item[0]].append(listx_11[idx])
                    self.y_fig1[item[0]].append(listy_11[idx])
            else:
                print(len(item[1][0]))
                for data in range(len(item[1][0])):
                    print(item[1][0][data])
                    if item[1][0][data] >= listx_11[0]:
                        listx_1 = item[1][0][data: data + 31]
                        listy_1 = item[1][1][data: data + 31]
                        break

                for idx in range(len(listx_1)):
                    self.x_fig1[item[0]].append(listx_1[idx])
                    self.y_fig1[item[0]].append(listy_1[idx])
                print(self.present_line1[item[0]])
                self.present_line1[item[0]] -= 31
        self.rewind_ch1 = True

    def rewind_channel2(self):
        if self.specific_row_2 >= 62:
            return_value_2 = 31
            self.begin_value_2 = self.specific_row_2 - 2 * 31
        else:
            if self.specific_row_2 >= 31:
                return_value_2 = 31
                self.begin_value_2 = 0
            else:
                return_value_2 = self.specific_row_2
                self.begin_value_2 = 0
        self.specific_row_2 -= return_value_2  # return points 30 point
        self.last_value_2 = self.specific_row_2
        listx_2 = []
        listy_2 = []
        listx_22 = []
        listy_22 = []
        self.x_fig2.clear()
        self.y_fig2.clear()
        for item in self.dic_channel2.items():
            print(item[0])
            self.x_fig2[item[0]] = []
            self.y_fig2[item[0]] = []

            if item[0] not in self.present_line2.keys():
                listx_22 = item[1][0][self.begin_value_2:self.last_value_2]
                listy_22 = item[1][1][self.begin_value_2:self.last_value_2]
                for idx in range(len(listx_22)):
                    self.x_fig2[item[0]].append(listx_22[idx])
                    self.y_fig2[item[0]].append(listy_22[idx])
            else:
                print(len(item[1][0]))
                for data in range(len(item[1][0])):
                    print(item[1][0][data])
                    if item[1][0][data] >= listx_22[0]:
                        listx_2 = item[1][0][data: data + 31]
                        listy_2 = item[1][1][data: data + 31]
                        break

                for idx in range(len(listx_2)):
                    self.x_fig2[item[0]].append(listx_2[idx])
                    self.y_fig2[item[0]].append(listy_2[idx])

                print("hallo")
                print(self.present_line2[item[0]])
                self.present_line2[item[0]] -= 31
        self.rewind_ch2 = True

    def Ischecked(self):
        channel1 = self.Qwindow.checkBox_2.isChecked()
        channel2 = self.Qwindow.checkBox_3.isChecked()
        if channel1 and channel2:
            return "channel1", "channel2"
        elif channel1:

            return ["channel1", "None"]
        elif channel2:
            return ["None", "channel2"]
        else:
            return ["None", "None"]

    def channels_checked(self):  # fun return which channel and path of file which selected
        check_list = self.Ischecked()
        file_namee, channel1, channel2 = self.current_file_and_channel(), check_list[0], check_list[1]
        file_part = file_namee.split('/')[-1].split('.')[0]
        if channel1 == "None" and channel2 == 'None' and file_part not in self.visited_channel1:
            channel1 = "channel1"
            self.Qwindow.checkBox_2.setChecked(True)
        print(file_namee)
        print(channel1)
        print(channel2)
        if len(file_namee) == 0:  # check if the file which is choosen or not
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
            print(self.files_name)  # get name of file
            for file in self.files_name:
                file_part = file.split('/')[-1].split('.')[0]
                if file_part == file_namee:
                    file_namee = file
                    # Add signal in visited list
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
                    elif channel1 == "channel1" and channel2 == "channel2":
                        self.visited_channel2.append(file_part)
                        self.visited_channel1.append(file_part)
                        break
                    break
            # default limits
            self.data_x_limits, self.data_y_limits = self.read_ecg_data_from_csv('Vital-Signals\EMG_Dataset.csv')
            self.time_list, self.signal_values_list = self.read_ecg_data_from_csv(file_namee)
            return file_part, file_namee, channel1, channel2

    def Plot(self):  # plot animation
        file_part, file_namee, channel1, channel2 = self.channels_checked()
        # get range of data of signal
        data_x, data_y = self.time_list, self.signal_values_list
        x_range = (floor(min(data_x)-0.05), ceil(max(data_x)+0.01))
        y_range = (floor(min(data_y)), ceil(max(data_y)))
        print(file_part)
        # count times which signal add
        count_files_channel1 = Counter(self.visited_channel1)
        count_files_channel2 = Counter(self.visited_channel2)
        # hide channels
        print(self.visited_channel1)
        if channel1 == "None" and file_part in self.visited_channel1:
            del count_files_channel1[file_part]
            print(self.visited_channel1)
            self.visited_channel1 = [file for idx, file in enumerate(self.visited_channel1) if file != file_part]
            print("hallo")
            print(len(self.visited_channel1))
            if len(self.visited_channel1) == 0:
                self.specific_row = 0
                self.frames_channel1 += 300
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
        # Channel 1 /graph 1
        if channel1 == "channel1":
            for item in count_files_channel1.items():  # get no of repeateed signal
                if item[0] == file_part:
                    no_of_repeated = item[1]
                    break
            print(len(self.present_line1))
            # to transfer signal from graph 1 to graph 2
            if file_part in self.visited_channel2 and len(self.visited_channel2) == 1:
                for key, value in self.files_index_ch1.items():
                    if file_part == value:
                        if key in self.present_line1.keys():
                            data_x = self.ax.get_xlim()
                            last_time = max(data_x)
                            for idx in range(len(self.dic_channel1[key][0])):
                                if last_time < self.dic_channel1[key][0][idx]:
                                    print(f"last:{self.dic_channel1[key][0][idx]}")
                                    self.specific_row_2 = idx + 5
                                    break
                        else:
                            self.specific_row_2 = self.specific_row - 1
                            break
            if no_of_repeated == 1:
                self.previous_line1 = self.no_of_line
                self.no_of_line += 1  # every line take number which is key to access line
                # put limits
                self.ax.set_xlim(x_range)
                self.ax.set_ylim(y_range)
                self.delay_interval = 200
                if self.no_of_line == 1:   # to call func animation once
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
                # to add another lines and begin  from last time of first line
                if self.no_of_line > 1 and len(self.visited_channel1) != 1:
                    self.data_xline, self.data_yline = self.read_ecg_data_from_csv(file_namee)
                    self.present_line1[self.no_of_line - 1] = self.current_data
                    for key in self.dic_channel1.items():
                        print(key[1][0][self.current_data])
                        begin_idx_ch1 = key[1][0][self.current_data]
                        break
                    for idx in range(len(self.data_xline)):  # get index of first line to start from it
                        if self.data_xline[idx] >= begin_idx_ch1:
                            self.line_idx_ch1[self.no_of_line - 1] = idx
                            self.data_xline = self.data_xline[idx:]
                            self.data_yline = self.data_yline[idx:]
                            print(f"len_x:{len(self.data_xline)}")
                            break
                    self.dic_channel1[self.no_of_line - 1] = self.data_xline, self.data_yline  # add data to line
                else:
                    self.dic_channel1[self.no_of_line - 1] = self.read_ecg_data_from_csv(file_namee)
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
                    unwanted_buttons = ['Customize', 'Home', 'Subplots']
                    for x in self.toolbar_1.actions():
                        if x.text() in unwanted_buttons:
                            self.toolbar_1.removeAction(x)
                    # Finding The Zoom In button and changing it's icon
                    actions = self.toolbar_1.actions()
                    fourth_action = actions[4]
                    zero_action = actions[0]
                    first_action = actions[1]
                    second_action = actions[3]
                    sixth_action = actions[6]
                    # Disconnecting the button from it's functionality
                    sixth_action.triggered.disconnect()
                    sixth_action.triggered.connect(self.custom_save_function)
                    zoom_in_icon = icon("fa.search-plus",
                                        color="white")
                    left_arrow_icon = icon("ei.arrow-left", color="white")
                    right_arrow_icon = icon("ei.arrow-right", color="white")
                    pan_icon = icon("fa.hand-paper-o", color="white")
                    screenshot_icon = icon("ri.screenshot-2-fill", color="white")
                    fourth_action.setIcon(zoom_in_icon)
                    zero_action.setIcon(left_arrow_icon)
                    first_action.setIcon(right_arrow_icon)
                    second_action.setIcon(pan_icon)
                    sixth_action.setIcon(screenshot_icon)
                    zoom_out_icon = icon("fa.search-minus", color="white")
                    self.zoom_out_button1 = QtWidgets.QAction(zoom_out_icon, "Zoom Out", self.Qwindow)
                    self.zoom_out_button1.triggered.connect(self.Zoom_out_channel1)
                    self.toolbar_1.insertAction(self.toolbar_1.actions()[4], self.zoom_out_button1)
                    for child in self.toolbar_1.findChildren(QtWidgets.QToolButton):
                        child.setStyleSheet("background-color: #849dad; ")
                    self.Qwindow.pause_button.show()
                    self.Qwindow.rewind_button1.show()
                    self.Qwindow.verticalLayout_toolbar1.addWidget(self.toolbar_1)

        # channel2 /graph 2
        if channel2 == "None" and file_part in self.visited_channel2:
            del count_files_channel2[file_part]
            print(self.visited_channel2)
            self.visited_channel2 = [file2 for idx2, file2 in enumerate(self.visited_channel2) if file2 != file_part]
            print(len(self.visited_channel2))

            if len(self.visited_channel2) == 0:
                self.specific_row_2 = 0
                self.frames_channel2 += 300

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
        if channel2 == "channel2":
            for item in count_files_channel2.items():
                if item[0] == file_part:
                    no_of_repeated = item[1]
            print(len(self.present_line2))
            if file_part in self.visited_channel1 and len(self.visited_channel1) == 1:
                for key, value in self.files_index_ch2.items():
                    if file_part == value:
                        if key in self.present_line2.keys():
                            data_x = self.ax2.get_xlim()
                            last_time = max(data_x)
                            for idx in range(len(self.dic_channel2[key][0])):
                                if last_time < self.dic_channel2[key][0][idx]:
                                    print(f"last:{self.dic_channel2[key][0][idx]}")
                                    self.specific_row = idx + 5
                                    break
                        else:
                            self.specific_row = self.specific_row_2 - 1
                            break
            if no_of_repeated == 1:
                self.previous_line2 = self.no_of_line_2
                self.no_of_line_2 += 1
                self.ax2.set_xlim(x_range)
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
                    self.data_xline_2, self.data_yline_2 = self.read_ecg_data_from_csv(file_namee)
                    self.present_line2[self.no_of_line_2 - 1] = self.current_data_2
                    for key in self.dic_channel2.items():
                        print(key[1][0][self.current_data_2])
                        begin_idx_ch2 = key[1][0][self.current_data_2]
                        break
                    for idx_2 in range(len(self.data_xline_2)):
                        print(len(self.dic_channel2))
                        print(self.dic_channel2.keys())
                        if self.data_xline_2[idx_2] >= begin_idx_ch2:
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
                    self.canvas2 = FigureCanvasQTAgg(self.fig2)
                    self.Qwindow.graphicsView_channel2.setScene(scene2)
                    scene2.addWidget(self.canvas2)
                    self.toolbar_2 = NavigationToolbar(self.canvas2, self.Qwindow)
                    # Remove the Home and Customize buttons from the toolbar
                    unwanted_buttons = ['Customize', 'Home', 'Subplots']
                    for x in self.toolbar_2.actions():
                        if x.text() in unwanted_buttons:
                            self.toolbar_2.removeAction(x)
                    # Finding The buttons in the toolbar and changing its icons using qtawesome icons
                    actions = self.toolbar_2.actions()
                    fourth_action = actions[4]
                    zero_action = actions[0]
                    first_action = actions[1]
                    second_action = actions[3]
                    sixth_action = actions[6]
                    sixth_action.triggered.disconnect()
                    # Connect it to a custom function that handles saving
                    sixth_action.triggered.connect(self.custom_save_function_channel2)
                    zoom_in_icon = icon("fa.search-plus",
                                        color="white")
                    left_arrow_icon = icon("ei.arrow-left", color="white")
                    right_arrow_icon = icon("ei.arrow-right", color="white")
                    pan_icon = icon("fa.hand-paper-o", color="white")
                    screenshot_icon = icon("ri.screenshot-2-fill", color="white")
                    fourth_action.setIcon(zoom_in_icon)
                    zero_action.setIcon(left_arrow_icon)
                    first_action.setIcon(right_arrow_icon)
                    second_action.setIcon(pan_icon)
                    sixth_action.setIcon(screenshot_icon)
                    # Creating an Icon for the Zoom Out button and Creating the button Itself
                    zoom_out_icon = icon("fa.search-minus", color="white")
                    self.zoom_out_button2 = QtWidgets.QAction(zoom_out_icon, "Zoom Out", self.Qwindow)
                    self.zoom_out_button2.triggered.connect(self.Zoom_out_channel2)
                    self.toolbar_2.insertAction(self.toolbar_2.actions()[4], self.zoom_out_button2)
                    for child in self.toolbar_2.findChildren(QtWidgets.QToolButton):
                        child.setStyleSheet("background-color: #849dad;")
                    self.Qwindow.pause_button_2.show()
                    self.Qwindow.rewind_button2.show()
                    self.Qwindow.verticalLayout_toolbar2.addWidget(self.toolbar_2)

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

    def current_file_and_channel(self):
        return str(self.Qwindow.signals_name.currentText())

    def show_color_dialog(self):  # Function to open a color picker dialog for the signal
        color = QColorDialog.getColor()
        self.Qwindow.color_picker_button.setStyleSheet(f"background-color: {color.name()}; color: white;")
        # Create a palette for the button text color and set it to the selected color
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, color)
        self.Qwindow.color_picker_button.setPalette(palette)
        # Store the selected color as a signal attribute
        self.signal_color = color.name()
        return color

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open File", "",
                                                   "CSV Files (*.csv)",
                                                   options=options)
        if file_name:
            self.files_name.append(file_name)
            file_name = str(file_name)
            self.line = file_name.split('/')[-1].split('.')[0]
            self.Qwindow.signals_name.addItem(self.line)
            self.time_list, self.signal_values_list = self.read_ecg_data_from_csv(file_name)
            self.row_counter = self.row_counter + 1
            self.Qwindow.tableWidget.setRowCount(self.row_counter)
            self.mean = self.Qwindow.calc_mean(self.signal_values_list)
            self.std = self.Qwindow.calc_std(self.signal_values_list)
            self.duration = self.Qwindow.calc_duration(self.time_list)
            self.min_value, self.max_value = self.Qwindow.calc_min_max_values(self.signal_values_list)
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 0, QTableWidgetItem(self.line))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 1, QTableWidgetItem(str(round(self.mean, 3))))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 2, QTableWidgetItem(str(round(self.std, 3))))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 3, QTableWidgetItem(str(round(self.duration, 3))))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 4, QTableWidgetItem(str(round(self.min_value, 3))))
            self.Qwindow.tableWidget.setItem(self.row_counter - 1, 5, QTableWidgetItem(str(round(self.max_value, 3))))

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
        # Browsing for the Image
        options = QFileDialog.Options()
        screenshots, _ = QFileDialog.getOpenFileName(self.Dwindow, "Open Image File", "",
                                                     "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)", options=options)
        # Check if the image was selected
        if screenshots:
            '''QPixmap is primarily used for handling images,
            including loading, displaying, and manipulating them in graphical applications.'''
            pixmap = QPixmap(screenshots)
            if not pixmap.isNull():
                # Get the dimensions of the screenshot section in the main window
                target_width = self.Dwindow.screenshot_section.width()
                target_height = self.Dwindow.screenshot_section.height()
                # Scale the loaded image to fit the screenshot section
                self.scaled_pixmap = pixmap.scaled(target_width, target_height)
                self.Dwindow.screenshot_section.setPixmap(self.scaled_pixmap)
        else:
            print("File dialog canceled or encountered an error.")

    def create_pdf_file(self):
        # Building the PDF
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
        table_header = ["Name", "Mean", "Std", "Duration", "Min Value", "Max Value"]
        self.statistics_data.append(table_header)
        # Add the table data for each row
        for i in range(self.row_counter):
            row_data = [
                self.Qwindow.tableWidget.item(i, 0).text(),
                self.Qwindow.tableWidget.item(i, 1).text(),
                self.Qwindow.tableWidget.item(i, 2).text(),
                self.Qwindow.tableWidget.item(i, 3).text(),
                self.Qwindow.tableWidget.item(i, 4).text(),
                self.Qwindow.tableWidget.item(i, 5).text()
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
        # dheader_text_style.alignment = 1  # 1 represents center alignment
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

    def add_new_pdf_page(self):
        # Adding a Header for the image section and styling it
        pass
       
    def forward(self):
        return self.line


class MainApp(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.Timer = QTimer(self)
        self.setupUi(self)
        self.setWindowTitle("Signal Real-Time Monitoring")

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
