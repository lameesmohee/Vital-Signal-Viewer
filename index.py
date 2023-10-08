import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
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
import pyqtgraph as pg


MainUI, _ = loadUiType(path.join(path.dirname(__file__), 'main.ui'))




class File:
    def __init__(self):
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
        self.fig = plt.figure(figsize=(898 / 80, 345/ 80), dpi=80)
        self.fig.set_facecolor('#222b2e')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#222b2e')
        self.fig2 = plt.figure(figsize=(898 / 80, 345 / 80), dpi=80)
        self.fig2.set_facecolor('#222b2e')
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_facecolor('#222b2e')
        # self.ax.grid(False)
        self.ax.grid(True, color='gray', linestyle='--', alpha=0.5)
        self.ax.xaxis.label.set_color('white')  # X-axis label
        self.ax.yaxis.label.set_color('white')

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax2.grid(True, color='gray', linestyle='--', alpha=0.5)
        self.ax2.xaxis.label.set_color('white')  # X-axis label
        self.ax2.yaxis.label.set_color('white')

        self.ax2.spines['bottom'].set_color('white')
        self.ax2.spines['left'].set_color('white')
        # self.ax.xaxis.set_tick_params(color='white')
        # self.ax.yaxis.set_tick_params(color='white')
        # self.ax.xaxis.get_major_ticks()[0].label.set_color('white')  # X-axis
        # self.ax.yaxis.get_major_ticks()[0].label.set_color('white')  # Y-axis
        # self.l_line = []
        # self.l_line2 = []
        self.handle_button_push()
        self.ax.set_xlabel('Time (s)')

        self.ax.set_ylabel("Vital Signal")



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
        # print("kckfdlk")
        global specific_row_2
        self.specific_row_2 += 1

        self.current_data_2 = i


        for kk in self.dic_channel2.items():
            if kk[0] != 0:
                print("ياللهووي")
                print(len(self.present_line2))
                for ll in self.present_line2.items():
                    print(f"l:{ll[kk[0]]}")
                    current_idx_2=ll[kk[0]]
                    self.x_fig2[kk[0]].append(kk[1][0][current_idx_2+3 - self.specific_row_2])
                    self.y_fig2[kk[0]].append(kk[1][1][current_idx_2+3 - self.specific_row_2])
                    print(f"line2:{self.x_fig2[kk[0]]}")
                    self.lines2[kk[0]].set_data(self.x_fig2[kk[0]], self.y_fig2[kk[0]])

            else:
                self.x_fig2[kk[0]].append(kk[1][0][self.specific_row_2])
                self.y_fig2[kk[0]].append(kk[1][1][self.specific_row_2])
                print(self.x_fig2[kk[0]])
                self.lines2[kk[0]].set_data(self.x_fig2[kk[0]], self.y_fig2[kk[0]])

            # print(self.current_data)
            if kk[0] == 0:
                if self.current_data_2 > 30:
                    self.ax2.set_xlim(kk[1][0][self.current_data_2 - 30], kk[1][0][self.current_data_2])


        return tuple(self.lines2)













    def animate_fig1(self,i):

        global specific_row
        self.specific_row += 1

        self.current_data = i
        print(f"i:{i}")
        print(f"s:{self.specific_row}")

        for k in self.dic_channel1.items():
            if k[0] != 0:
                print("ياللهووي")
                print(len(self.present_line1))
                for l in self.present_line1.items():
                    print(f"l:{l[k[0]]}")
                    current_idx=l[k[0]]
                    self.x_fig1[k[0]].append(k[1][0][current_idx+3 - self.specific_row])
                    self.y_fig1[k[0]].append(k[1][1][current_idx+3 - self.specific_row])
                    print(f"line2:{self.x_fig1[k[0]]}")
                    self.lines1[k[0]].set_data(self.x_fig1[k[0]], self.y_fig1[k[0]])

            else:
                self.x_fig1[k[0]].append(k[1][0][self.specific_row])
                self.y_fig1[k[0]].append(k[1][1][self.specific_row])
                print(self.x_fig1[k[0]])
                self.lines1[k[0]].set_data(self.x_fig1[k[0]], self.y_fig1[k[0]])

            # print(self.current_data)
            if k[0] == 0:
                if self.current_data > 30:
                    self.ax.set_xlim(k[1][0][self.current_data - 30], k[1][0][self.current_data])



        # previous_i=i
        return tuple(self.lines1)

        # self.x_fig1.append(self.time_list[self.specific_row])
        # self.y_fig1.append(self.signal_values_list[self.specific_row])
        # self.line_plot.set_data(self.x_fig1, self.y_fig1)
        # # print(f"y:{y}")
        #
        # if self.current_data > 30:
        #     plt.xlim(self.time_list[self.current_data - 30], self.time_list[self.current_data])
        #
        # print(self.line_plot)
        #
        # return self.line_plot,




        #
        # for k in self.dic_channel1.items():
        #      # print(self.k[1][1][self.specific_row])
        #      self.x_fig1.append(k[1][0][self.specific_row])
        #      self.y_fig1.append(k[1][1][self.specific_row])
        #
        #
        #      if self.current_data > 30:
        #          self.ax.set_xlim(k[1][0][self.current_data - 30], k[1][0][self.current_data])



        #
        # print(len(self.x_fig1))



        # print(f"y:{self.y}")
        # # print(self.current_data)
        # for ax_line in self.list_lines_channel1:
        #     ax_line.set_data(self.x_fig1, self.y_fig1)
        #     self.l_line.append(ax_line)
        #
        # # print(self.l_line)
        #
        # return self.l_line,

    # def init(self):
    #    self.name_line.set_data([], [])
    #    return self.name_line,


    def Plot(self):
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
       elif (channel1 == "None" and channel2 == "None") and (
               len(self.visited_channel1) == 0 or len(self.visited_channel2) == 0):
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

                   else:
                       self.visited_channel1.append(file_part)
                       self.visited_channel2.append(file_part)

           self.time_list, self.signal_values_list = self.read_ecg_data_from_csv(file_namee)


           for tick in self.ax.get_xticklabels():
               tick.set_color('white')
               # X-axis

           for tick in self.ax.get_yticklabels():
               tick.set_color('white')

           data_x, data_y = self.time_list, self.signal_values_list

           x_range = (floor(min(data_x)), ceil(max(data_x)))
           y_range = (floor(min(data_y)), ceil(max(data_y)))
           # print(x_range)

           print(file_part)
           print("dcjdkjdk")

           count_files_channel1 = Counter(self.visited_channel1)
           count_files_channel2 = Counter(self.visited_channel2)


            ## Channel 1
           if channel1 == "channel1":

               print('hi')


               for item in count_files_channel1.items():
                   if item[0] == file_part:
                       no_of_repeated = item[1]
                       break

               if no_of_repeated == 1:
                   self.previous_line1=self.no_of_line



                   self.no_of_line += 1
                   self.ax.set_xlim(x_range)
                   self.ax.set_ylim(y_range)
                   self.delay_interval = 200
                   colors={0:'b',1:'r'}

                   # self.line_plot,=self.ax.plot([],[] ,label=
                   for i in range(self.previous_line1,self.no_of_line):

                       self.lines1[i],=self.ax.plot([], [], label=file_part ,color=colors[i])
                       self.x_fig1[i] = []
                       self.y_fig1[i] = []

                   if self.no_of_line > 1:
                       print("halllo")
                       self.data_xline,self.data_yline =self.read_ecg_data_from_csv(file_namee)
                       self.present_line1[self.no_of_line-1]=self.current_data
                       for idx in range(len(self.data_xline)) :
                             # x=self.dic_channel1[0]

                           print(f"x:{self.dic_channel1[0][0][self.current_data]}")
                           if self.data_xline[idx] >= self.dic_channel1[0][0][self.current_data] :
                               print("حد يلجقنا")
                               print(f"idx:{idx}")

                               self.data_xline = self.data_xline[idx:]
                               self.data_yline = self.data_yline[idx:]
                               print(f"len_x:{len(self.data_xline)}")
                               break

                       self.dic_channel1[self.no_of_line - 1] =self.data_xline,self.data_yline
                   else:
                       self.dic_channel1[self.no_of_line - 1] = self.read_ecg_data_from_csv(file_namee)






                   if len(self.dic_channel1) == 1:
                       self.ani = FuncAnimation(self.fig, self.animate_fig1, interval=self.delay_interval,
                                                frames=397, repeat=False)


                   self.ax.legend()


                   if len(self.visited_channel1) == 1:
                      scene1 = QtWidgets.QGraphicsScene()
                      canvas1 = FigureCanvasQTAgg(self.fig)
                      self.Qwindow.graphicsView_channel1.setScene(scene1)
                      scene1.addWidget(canvas1)
                      toolbar_1 = NavigationToolbar(canvas1, self.Qwindow)
                      self.Qwindow.verticalLayout_toolbar1.addWidget(toolbar_1)



           if channel2 == "channel2":


               for item in count_files_channel2.items():
                   if item[0] == file_part:
                       no_of_repeated = item[1]

               if no_of_repeated == 1:
                   self.previous_line2 = self.no_of_line_2
                   # self.name_line2=file_part
                   self.no_of_line_2 += 1
                   self.ax2.set_xlim(x_range)
                   self.ax2.set_ylim(y_range)
                   self.delay_interval = 200
                   colors = {0: 'b', 1: 'r'}

                   for i in range(self.previous_line2,self.no_of_line_2 ):
                       self.lines2[i], = self.ax2.plot([], [], label=file_part ,color=colors[i])
                       self.x_fig2[i] = []
                       self.y_fig2[i] = []

                   if self.no_of_line_2 > 1:
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

                   if len(self.dic_channel2) == 1:
                       self.ani2 = FuncAnimation(self.fig2, self.animate_fig2, interval=self.delay_interval,
                                                 frames=397, repeat=False)

                       QCoreApplication.processEvents()
                       self.ax2.legend()

                       scene2 = QtWidgets.QGraphicsScene()
                       canvas2 = FigureCanvasQTAgg(self.fig2)
                       self.Qwindow.graphicsView_channel2.setScene(scene2)
                       scene2.addWidget(canvas2)
                       toolbar_2 = NavigationToolbar(canvas2, self.Qwindow)
                       self.Qwindow.verticalLayout_toolbar2.addWidget(toolbar_2)

    def current_file_and_channel(self):
           # channel1=self.Qwindow.checkBox_2.isChecked()
           # channel2=self.Qwindow.checkBox_3.isChecked()
           # if channel1:

           return str(self.Qwindow.signals_name.currentText())

    # else:
    #     return str(self.Qwindow.signals_name.Current_text()), channel2

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open File", "",
                                                   "CSV Files (*.csv)",
                                                   options=options)

        if file_name:
            print("Selected file:", file_name)
            self.files_name.append(file_name)
            file_name=str(file_name)
            self.line = file_name.split('/')[-1].split('_')[0]

            self.Qwindow.signals_name.addItem(self.line)

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


    def forward (self):
       print(self.line)
       return self.line


class MainApp(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Signal Real-Time Monitoring")
        # self.file = File()

        # self.open_file.triggered.connect(self.file.browse_file)
        # self.file.forward()
    # def call_line(self):
    #     self.line=self.file.forward()
    #     print(self.line)



    def hi(self):
        print("hello")

def main():
    app = QApplication(sys.argv)
    window =File()
    window.Qwindow.show()
    # window.show()
    app.exec_()


if __name__ == '__main__':
    main()
