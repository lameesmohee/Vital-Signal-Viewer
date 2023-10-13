import matplotlib
# from bokeh.models import MultiLine
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
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
from reportlab.pdfgen import canvas
import io


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
        self.delay_interval = None
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
        self.specific_row = 0
        self.specific_row_2 = 0
        self.no_of_line = 0
        self.no_of_line_2 = 0
        self.lines1 =[None] * 100
        self.lines2 = [None] * 100
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
        self.story = []
        self.pdf_filename = f"Medical Report {self.pdf_counter}.pdf"
        self.doc = SimpleDocTemplate(self.pdf_filename, pagesize=letter)





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
        self.Dwindow.save_button.clicked.connect(self.create_pdf_file)
        self.Dwindow.save_button.clicked.connect(self.Dwindow.close)
        self.Dwindow.add_new_page_button.clicked.connect(self.add_new_pdf_page)



    def styles(self):
        self.fig = plt.figure(figsize=(980 / 80, 400 / 80), dpi=80)
        self.fig.set_facecolor('#F0F5F9')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#F0F5F9')
        left_margin = 0.075  # Adjust this value as needed
        self.ax.set_position([left_margin, 0.1, 0.8, 0.89])
        self.fig2 = plt.figure(figsize=(980 / 80, 400 / 80), dpi=80)
        self.fig2.set_facecolor('#F0F5F9')
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_facecolor('#F0F5F9')
        left_margin = 0.075  # Adjust this value as needed
        self.ax2.set_position([left_margin, 0.1, 0.8, 0.89])
        self.ax.grid(True, color='gray', linestyle='--', alpha=0.5)
        self.ax.xaxis.label.set_color('#708694')  # X-axis label
        self.ax.xaxis.label.set_weight('bold')
        self.ax.yaxis.label.set_color('#708694')
        self.ax.yaxis.label.set_weight('bold')
        self.ax.spines['bottom'].set_color('#708694')
        self.ax.spines['left'].set_color('#708694')
        self.ax2.grid(True, color='gray', linestyle='--', alpha=0.5)
        self.ax2.xaxis.label.set_color('#708694')  # X-axis label
        self.ax2.xaxis.label.set_weight('bold')
        self.ax2.yaxis.label.set_color('#708694')
        self.ax2.yaxis.label.set_weight('bold')
        self.ax2.spines['bottom'].set_color('#708694')
        self.ax2.spines['left'].set_color('#708694')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel("Vital Signal")
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel("Vital Signal")
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
        self.Qwindow.pause_button.setStyleSheet("background-color: #849dad;"
                                                " color: white;"
                                                "font-size: 16px")
        self.Qwindow.pause_button_2.setStyleSheet("background-color: #849dad;"
                                                  " color: white;"
                                                  "font-size: 16px")
        self.Qwindow.setFixedSize(1930,1000)
        rewind_icon = icon("fa.backward", color='white')
        self.Qwindow.rewind_button1.setIcon(rewind_icon)
        self.Qwindow.rewind_button2.setIcon(rewind_icon)
        self.Qwindow.rewind_button1.setStyleSheet("background-color: #849dad;")
        self.Qwindow.rewind_button2.setStyleSheet("background-color: #849dad;")
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

    def zoom_out(self):
        # Implement your custom button functionality here
        pass  # Replace with your code


    def increase_speed(self):
        if self.delay_interval == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please UPload A Signal")
            msg.show()
            msg.exec_()


    def decrease_speed(self):
        if self.delay_interval == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please UPload A Signal")
            msg.show()
            msg.exec_()

    def animate_fig2(self, i):
        global specific_row_2
        self.specific_row_2 += 1
        self.current_data_2 = i


        for kk in self.dic_channel2.items():
            if kk[0] != 0:
                for ll in self.present_line2.items():
                    current_idx_2=ll[kk[0]]
                    self.x_fig2[kk[0]].append(kk[1][0][current_idx_2+3 - self.specific_row_2])
                    self.y_fig2[kk[0]].append(kk[1][1][current_idx_2+3 - self.specific_row_2])
                    self.lines2[kk[0]].set_data(self.x_fig2[kk[0]], self.y_fig2[kk[0]])
            else:
                self.x_fig2[kk[0]].append(kk[1][0][self.specific_row_2])
                self.y_fig2[kk[0]].append(kk[1][1][self.specific_row_2])
                self.lines2[kk[0]].set_data(self.x_fig2[kk[0]], self.y_fig2[kk[0]])

            if kk[0] == 0:
                if self.current_data_2 > 30:
                    self.ax2.set_xlim(kk[1][0][self.current_data_2 - 30], kk[1][0][self.current_data_2])


        return tuple(self.lines2)

    def animate_fig1(self, i):

        global specific_row
        self.specific_row += 1
        self.current_data = i

        for k in self.dic_channel1.items():
            if k[0] != 0:
                for l in self.present_line1.items():
                    current_idx=l[k[0]]
                    self.x_fig1[k[0]].append(k[1][0][current_idx+3 - self.specific_row])
                    self.y_fig1[k[0]].append(k[1][1][current_idx+3 - self.specific_row])
                    self.lines1[k[0]].set_data(self.x_fig1[k[0]], self.y_fig1[k[0]])

            else:
                self.x_fig1[k[0]].append(k[1][0][self.specific_row])
                self.y_fig1[k[0]].append(k[1][1][self.specific_row])
                self.lines1[k[0]].set_data(self.x_fig1[k[0]], self.y_fig1[k[0]])

            if k[0] == 0:
                if self.current_data > 30:
                    self.ax.set_xlim(k[1][0][self.current_data - 30], k[1][0][self.current_data])

        return tuple(self.lines1)

    def Plot(self):


       check_list = self.Ischecked()
       file_namee, channel1, channel2 = self.current_file_and_channel(), check_list[0], check_list[1]
       if len(file_namee) == 0:
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Warning)
           msg.setInformativeText("Please UPload A Signal")
           msg.show()
           msg.exec_()
       elif (channel1 == "None" and channel2 == "None") and (
               len(self.visited_channel1) == 0 or len(self.visited_channel2) == 0):
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Warning)
           msg.setInformativeText("Please Enter A Channel")
           msg.show()
           msg.exec_()
       else:

           for file in self.files_name:
               file_part = file.split('/')[-1].split('.')[0]
               if file_part == file_namee:
                   file_namee = file

                   # self.line_applied=file_part
                   if channel1 == "channel1" and channel2 == "None":
                       self.visited_channel1.append(file_part)
                       break

                   elif channel2 == "channel2" and channel1 == "None":
                       self.visited_channel2.append(file_part)
                       break

                   else:
                       self.visited_channel1.append(file_part)
                       self.visited_channel2.append(file_part)

           self.time_list, self.signal_values_list = self.read_ecg_data_from_csv(file_namee)


           for tick in self.ax.get_xticklabels():
               tick.set_color('#708694')
               tick.set_weight('bold')
               # X-axis
           for tick in self.ax.get_yticklabels():
               tick.set_color('#708694')
               tick.set_weight('bold')

           for tick in self.ax2.get_xticklabels():
               tick.set_color('#708694')
               tick.set_weight('bold')
               # X-axis
           for tick in self.ax2.get_yticklabels():
               tick.set_color('#708694')
               tick.set_weight('bold')
           data_x, data_y = self.time_list, self.signal_values_list
           x_range = (floor(min(data_x)), ceil(max(data_x)))
           y_range = (floor(min(data_y)), ceil(max(data_y)))
           count_files_channel1 = Counter(self.visited_channel1)
           count_files_channel2 = Counter(self.visited_channel2)
            ## Channel 1
           if channel1 == "channel1":

               for item in count_files_channel1.items():
                   if item[0] == file_part:
                       no_of_repeated = item[1]
                       break

               if no_of_repeated == 1:
                   self.previous_line1 = self.no_of_line
                   self.no_of_line += 1
                   self.ax.set_xlim(x_range)
                   self.ax.set_ylim(y_range)
                   self.delay_interval = 200
                   # colors = {0: 'b', 1: 'r'}
                   for i in range(self.previous_line1, self.no_of_line):

                       self.lines1[i], = self.ax.plot([], [], label=file_part, color=self.signal_color)
                       self.x_fig1[i] = []
                       self.y_fig1[i] = []

                   if self.no_of_line > 1:
                       self.data_xline, self.data_yline = self.read_ecg_data_from_csv(file_namee)
                       self.present_line1[self.no_of_line-1] = self.current_data
                       for idx in range(len(self.data_xline)):

                           if self.data_xline[idx] >= self.dic_channel1[0][0][self.current_data]:
                               self.data_xline = self.data_xline[idx:]
                               self.data_yline = self.data_yline[idx:]
                               break

                       self.dic_channel1[self.no_of_line - 1] = self.data_xline, self.data_yline
                   else:
                       self.dic_channel1[self.no_of_line - 1] = self.read_ecg_data_from_csv(file_namee)


                   if len(self.dic_channel1) == 1:
                       self.ani = FuncAnimation(self.fig, self.animate_fig1, interval=self.delay_interval,
                                                frames=397, repeat=False)
                   self.ani_list.append(self.ani)

                   self.ax.legend()


                   if len(self.visited_channel1) == 1:
                      scene1 = QtWidgets.QGraphicsScene()
                      canvas1 = FigureCanvasQTAgg(self.fig)
                      self.Qwindow.graphicsView_channel1.setScene(scene1)
                      scene1.addWidget(canvas1)
                      self.toolbar_1 = NavigationToolbar(canvas1, self.Qwindow)

                      # Remove the Home and Customize buttons from the toolbar
                      unwanted_buttons = ['Customize', 'Home', 'Subplots']
                      for x in self.toolbar_1.actions():
                          if x.text() in unwanted_buttons:
                              self.toolbar_1.removeAction(x)

                      # Finding The Zoom In button and changing it's icon
                      actions = self.toolbar_1.actions()

                      fourth_action = actions[4]
                      Zero_action = actions[0]
                      first_action = actions[1]
                      second_action = actions[3]
                      sixth_action = actions[6]

                      zoom_in_icon = icon("fa.search-plus",
                                          color="white")
                      left_arrow_icon = icon("ei.arrow-left", color="white")
                      right_arrow_icon = icon("ei.arrow-right", color="white")
                      pan_icon = icon("fa.hand-paper-o", color="white")
                      screenshot_icon = icon("ri.screenshot-2-fill", color="white")

                      fourth_action.setIcon(zoom_in_icon)
                      Zero_action.setIcon(left_arrow_icon)
                      first_action.setIcon(right_arrow_icon)
                      second_action.setIcon(pan_icon)
                      sixth_action.setIcon(screenshot_icon)

                      zoom_out_icon = icon("fa.search-minus", color="white")
                      zoom_out_button1 = QtWidgets.QAction(zoom_out_icon, "Zoom Out", self.Qwindow)


                      def zoom_out_graph1():
                          pass  # Replace with your code

                      zoom_out_button1.triggered.connect(zoom_out_graph1)
                      self.toolbar_1.insertAction(self.toolbar_1.actions()[4], zoom_out_button1)
                      for child in self.toolbar_1.findChildren(QtWidgets.QToolButton):
                          child.setStyleSheet("background-color: #849dad; ")

                      self.Qwindow.pause_button.show()
                      self.Qwindow.rewind_button1.show()
                      self.Qwindow.verticalLayout_toolbar1.addWidget(self.toolbar_1)





           if channel2 == "channel2":


               for item in count_files_channel2.items():
                   if item[0] == file_part:
                       no_of_repeated = item[1]

               if no_of_repeated == 1:
                   self.previous_line2 = self.no_of_line_2
                   self.no_of_line_2 += 1
                   self.ax2.set_xlim(x_range)
                   self.ax2.set_ylim(y_range)
                   self.delay_interval = 200

                   for i in range(self.previous_line2, self.no_of_line_2):
                       self.lines2[i], = self.ax2.plot([], [], label=file_part, color=self.signal_color)
                       self.x_fig2[i] = []
                       self.y_fig2[i] = []

                   if self.no_of_line_2 > 1:
                       self.data_xline_2, self.data_yline_2 = self.read_ecg_data_from_csv(file_namee)
                       self.present_line2[self.no_of_line_2 - 1] = self.current_data_2
                       for idx_2 in range(len(self.data_xline_2)):

                           if self.data_xline_2[idx_2] >= self.dic_channel2[0][0][self.current_data_2]:

                               self.data_xline_2 = self.data_xline_2[idx_2:]
                               self.data_yline_2 = self.data_yline_2[idx_2:]
                               break

                       self.dic_channel2[self.no_of_line_2 - 1] = self.data_xline_2, self.data_yline_2
                   else:
                       self.dic_channel2[self.no_of_line_2 - 1] = self.read_ecg_data_from_csv(file_namee)

                   if len(self.dic_channel2) == 1:
                       self.ani2 = FuncAnimation(self.fig2, self.animate_fig2, interval=self.delay_interval,
                                                 frames=397, repeat=False)

                       QCoreApplication.processEvents()
                       self.ax2.legend()
                       self.ani_list.append(self.ani2)

                       scene2 = QtWidgets.QGraphicsScene()
                       canvas2 = FigureCanvasQTAgg(self.fig2)
                       self.Qwindow.graphicsView_channel2.setScene(scene2)
                       scene2.addWidget(canvas2)
                       self.toolbar_2 = NavigationToolbar(canvas2, self.Qwindow)

                       # Remove the Home and Customize buttons from the toolbar
                       unwanted_buttons = ['Customize', 'Home', 'Subplots']
                       for x in self.toolbar_2.actions():
                           if x.text() in unwanted_buttons:
                               self.toolbar_2.removeAction(x)

                       # Finding The Zoom In button and changing it's icon
                       actions = self.toolbar_2.actions()

                       fourth_action = actions[4]
                       Zero_action = actions[0]
                       first_action = actions[1]
                       second_action = actions[3]
                       sixth_action = actions[6]

                       zoom_in_icon = icon("fa.search-plus",
                                           color="white")
                       left_arrow_icon = icon("ei.arrow-left", color="white")
                       right_arrow_icon = icon("ei.arrow-right", color="white")
                       pan_icon = icon("fa.hand-paper-o", color="white")
                       screenshot_icon = icon("ri.screenshot-2-fill", color="white")

                       fourth_action.setIcon(zoom_in_icon)
                       Zero_action.setIcon(left_arrow_icon)
                       first_action.setIcon(right_arrow_icon)
                       second_action.setIcon(pan_icon)
                       sixth_action.setIcon(screenshot_icon)
                       # Creating an Icon for the Zoom Out button and Creating the button Itself
                       zoom_out_icon = icon("fa.search-minus", color="white")
                       zoom_out_button2 = QtWidgets.QAction(zoom_out_icon, "Zoom Out", self.Qwindow)

                       def zoom_out_graph2():
                           pass  # Replace with your code

                       zoom_out_button2.triggered.connect(zoom_out_graph2)
                       self.toolbar_2.insertAction(self.toolbar_2.actions()[4], zoom_out_button2)
                       for child in self.toolbar_2.findChildren(QtWidgets.QToolButton):
                           child.setStyleSheet("background-color: #849dad;")
                       self.Qwindow.pause_button_2.show()
                       self.Qwindow.rewind_button2.show()
                       self.Qwindow.verticalLayout_toolbar2.addWidget(self.toolbar_2)



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
            self.line = file_name.split('/')[-1].split('.')[0]
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
                self.scaled_pixmap = pixmap.scaled(target_width, target_height)

                self.Dwindow.screenshot_section.setPixmap(self.scaled_pixmap)
                # self.Dwindow.screenshot_section.setp(pixmap)
        else:
            print("File dialog canceled or encountered an error.")


    def create_pdf_file(self):
        self.add_new_pdf_page()
        self.doc.build(self.story)
        # self.pdf_counter_name+=1


    def add_new_pdf_page(self):
 

        # Add an image to the PDF
        pixmap = self.Dwindow.screenshot_section.pixmap()
        
        # Convert QPixmap to PIL Image
        image = QImage(pixmap)
        
        # Specify a unique filename for each image
        image_filename = f"temp_image_{self.pdf_counter}.png"
        image.save(image_filename)
        
        # Add the image to the PDF
        pdf_image = Image(image_filename, width=8 * inch, height=4 * inch)
        self.story.append(pdf_image)
        self.story.append(Spacer(1, 0.5 * inch))

        # Add text to the PDF
        text = self.Dwindow.comment_section.text()
        text_style = styles.getSampleStyleSheet()["Normal"]
        text_style.alignment = 1  # 1 represents center alignment
        text_style.fontSize = 14  # Set font size to 12px
        paragraph = Paragraph(text, text_style)
        self.story.append(paragraph)

        # Build the PDF document
        self.pdf_counter += 1
        self.story.append(PageBreak())

        empty_pixmap = QPixmap()  # Create an empty QPixmap
        self.Dwindow.screenshot_section.setPixmap(empty_pixmap)
        self.Dwindow.comment_section.setText("")






    def forward (self):
       return self.line


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
