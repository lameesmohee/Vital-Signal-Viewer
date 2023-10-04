print('hello')
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from os import path
import sys
import csv
import pandas as pd
import pyqtgraph as pg
MainUI,_ = loadUiType(path.join(path.dirname(__file__),'main.ui'))

class MainApp(QMainWindow , MainUI):
    def __init__(self , parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("ECG Real-Time Monitoring")
        # self.pushButton_2_button = QPushButton("File", self)
        # self.pushButton_2_button.clicked.connect(self.browse_file)
        self.open_file.triggered.connect(self.browse_file)

        self.time_list = []
        self.signal_values_list = []



    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "CSV Files (*.csv)",
                                                   options=options)

        if file_name:
            print("Selected file:", file_name)
            self.time_list, self.signal_values_list = self.read_ecg_data_from_csv(file_name)


    def read_ecg_data_from_csv(self, file_name):
        try:
            with open(file_name, 'r') as csv_file:
                # csv_reader = csv.DictReader(csv_file)
                csv_reader = pd.read_csv(csv_file)
                time_list = csv_reader.iloc[:, 0]
                signal_values_list = csv_reader.iloc[:, 1]
            return time_list, signal_values_list
        except Exception as e:
            print("Error reading CSV file")
            return [], []

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()