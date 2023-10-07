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

plt.style.use('ggplot')
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT as NavigationToolbar
import pyqtgraph as pg


MainUI, _ = loadUiType(path.join(path.dirname(__file__), 'main.ui'))


# class MplCanvas(FigureCanvasQTAgg):
#
#     def __init__(self, parent=None, data_x=[], data_y=[]):
#         fig = plt.Figure()
#         # self.ax = fig.add_subplot(111)
#
#         super(MplCanvas, self).__init__(fig)
#         # print(data_x[10)
#         #  self.file = File()
#         data_x, data_y  = data_x, data_y
#
#         self.x_range = (floor(min(data_x)), ceil(max(data_x)))
#         self.y_range = (floor(min(data_y)), ceil(max(data_y)))
#         self.ax = plt.axes(xlim=self.x_range, ylim=self.y_range)




class File:
    def __init__(self):
        self.time_list = []
        self.signal_values_list = []
        self.line = None
        self.files_name=[]
        self.delay_interval = None
        self.x=[]
        self.y=[]
        self.visited=[]
        self.specific_row=0
        self.Qwindow=MainApp()
        self.fig = plt.figure(figsize=(898 / 80, 345/ 80), dpi=80)
        self.fig.set_facecolor('#222b2e')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#222b2e')
        # self.ax.grid(False)
        self.ax.grid(True, color='gray', linestyle='--', alpha=0.5)
        self.ax.xaxis.label.set_color('white')  # X-axis label
        self.ax.yaxis.label.set_color('white')

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.xaxis.set_tick_params(color='white')
        self.ax.yaxis.set_tick_params(color='white')
        self.ax.xaxis.get_major_ticks()[0].label.set_color('white')  # X-axis
        self.ax.yaxis.get_major_ticks()[0].label.set_color('white')  # Y-axis

        self.handle_button_push()



    def handle_button_push(self):
        self.Qwindow.open_file.triggered.connect(self.browse_file)

        self.Qwindow.pushButton_plot.clicked.connect(self.Plot)
        self.Qwindow.minus_button.clicked.connect(self.decrease_speed)
        self.Qwindow.plus_button.clicked.connect(self.increase_speed)
        self.Qwindow.checkBox_2.stateChanged.connect(self.Ischecked)
        self.Qwindow.checkBox_3.toggled.connect(self.Ischecked)
        self.Qwindow.checkBox_3.setCheckable(True)


    def Ischecked(self):
        channel1 = self.Qwindow.checkBox_2.isChecked()
        channel2 = self.Qwindow.checkBox_3.isChecked()
        if channel1:
            return channel1
        else:
            return  channel2







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

    def animate(self,i):
        # print("kckfdlk")
        global specific_row
        self.specific_row += 1

        self.current_data = i

        self.x.append(self.time_list[self.specific_row])
        self.y.append(self.signal_values_list[self.specific_row])

        self.line_plot .set_data(self.x, self.y)

        # print(f"y:{self.y}")
        # print(self.current_data)

        if self.current_data > 30:
            plt.xlim(self.time_list[self.current_data - 30], self.time_list[self.current_data])

        return self.line,

    def init(self):
        self.line_plot.set_data([], [])
        return self.line,

    def Plot(self):
        file_namee, channel = self.current_file_and_channel(), self.Ischecked()
        print(file_namee)
        if  len(file_namee) == 0:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please UPload A Signal")
            msg.show()
            msg.exec_()

        else:
            # file_namee,channel=self.cu rrent_file_and_channel(),self.Ischecked()
            print(self.files_name)
            for file in self.files_name:
                file_part = file.split('/')[6].split('_')[0]
                if  file_part == file_namee:
                    file_namee = file
                    self.line_applied=file_part
                    self.visited.append(file_part)

                    break
            self.time_list, self.signal_values_list = self.read_ecg_data_from_csv(file_namee)

            print(self.visited)
            if len(self.visited) < 2:
                # ax = fig.add_subplot(111)
                plt.xlabel('Time (s)')  # label x axis
                plt.ylabel(self.line_applied)  # label y axis
                plt.title(self.line_applied + 'Graph')
                # x_range = (0, 10)
                # y_range = (0, 1)
                # ax = plt.axes(xlim=(0,4), ylim=(0,40))
                for tick in self.ax.get_xticklabels():
                    tick.set_color('white')  # X-axis

                for tick in self.ax.get_yticklabels():
                    tick.set_color('white')

            data_x, data_y = self.time_list, self.signal_values_list

            # ax = plt.axes(xlim=x_range,
            #               ylim=y_range)

            x_range = (floor(min(data_x)), ceil(max(data_x)))
            y_range = (floor(min(data_y)), ceil(max(data_y)))
            # print(x_range)


            self.ax.set_xlim(x_range)
            self.ax.set_ylim(y_range)
            self.line_plot, = self.ax.plot([], [])

            print(self.line_plot)

            # plt.gcf (get current figure) will reload the plat based on the data saved in the 'data' DataFrame
            # animate argument will call the function defined above
            # interval = 2000 milli second. The frames will be updated every 2 seconds.
            # frames = 200. After plotting 200 frames, the animation will stop.

            self.ani = FuncAnimation(plt.gcf(), self.animate, init_func=self.init, interval=100, frames=len(self.time_list), repeat=False)
            # plt.show()

            scene = QtWidgets.QGraphicsScene()
            # view = QtWidgets.QGraphicsView(scene, self.Qwindow)

            # Removing the repeation of the toolbar
            # List of layouts to check
            layouts = [self.Qwindow.verticalLayout_channel1, self.Qwindow.verticalLayout_channel2]

            # Iterate through the layouts
            for layout in layouts:
                for i in reversed(range(layout.count())):
                    widget = layout.itemAt(i).widget()
                    if isinstance(widget, NavigationToolbar):
                        layout.removeWidget(widget)
                        widget.deleteLater()

            if self.Qwindow.checkBox_2.isChecked():
                self.Qwindow.graphicsView_channel1.setScene(scene)

                # Add a new instance of the toolbar when checkbox is checked
                canvas = FigureCanvasQTAgg(self.fig)
                scene.addWidget(canvas)
                toolbar_1 = NavigationToolbar(canvas, self.Qwindow)
                toolbar_1.setFixedSize(toolbar_1.sizeHint())
                self.Qwindow.verticalLayout_channel1.addWidget(toolbar_1)

            else:
                self.Qwindow.graphicsView_channel1.setScene(None)

            if self.Qwindow.checkBox_3.isChecked():
                self.Qwindow.graphicsView_channel2.setScene(scene)

                # Add a new instance of the toolbar when checkbox is checked
                canvas = FigureCanvasQTAgg(self.fig)
                scene.addWidget(canvas)
                toolbar_2 = NavigationToolbar(canvas, self.Qwindow)
                self.Qwindow.verticalLayout_channel2.addWidget(toolbar_2)
            else:
                self.Qwindow.graphicsView_channel2.setScene(None)

            # view.resize(200, 200)
            # view.setGeometry(70,410, 1039, 216)
            # view.show()

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
            self.line = file_name.split('/')[6].split('_')[0]

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
