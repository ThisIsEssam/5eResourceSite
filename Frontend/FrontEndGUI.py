#!/usr/bin/env python
import datetime
import json
import os
import pprint
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytz
import requests
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
from Backend.NPC_Class.Hero import Hero
from Backend.NPC_Class.Commoner import Commoner
from Backend.API import getResource
import Fantasy_Names
import Fantasy_Names.human_diverse


class DataDogGUIFailSaveWindow(QWidget):
    def __init__(self, parent=None):
        super(DataDogGUIFailSaveWindow, self).__init__(parent)
        self.resize(200, 200)
        self.setWindowTitle("Save Failed")
        layout = QVBoxLayout()
        self.label = QLabel("An Error occurred when trying to export records")
        layout.addWidget(self.label)
        self.setLayout(layout)


class DataDogGUISuccessSaveWindow(QWidget):
    def __init__(self, parent=None):
        super(DataDogGUISuccessSaveWindow, self).__init__(parent)
        self.resize(200, 200)
        self.setWindowTitle("Successfully Saved!")
        layout = QVBoxLayout()
        self.label = QLabel("Successfully saved to /Users/USERNAME/Documents/DataDogLogs.txt")
        layout.addWidget(self.label)
        self.setLayout(layout)


class DataDogGUILogWindow(QWidget):
    def __init__(self, parent=None):
        classes = getResource.get_class()
        lineages = getResource.get_lineage()
        class_results = classes['results']
        lineage_results = lineages['results']
        class_list = []
        lineage_list = []
        for i in class_results:
            class_list.append(i['name'])

        for i in lineage_results:
            lineage_list.append(i['name'])
 
        super(DataDogGUILogWindow, self).__init__(parent)
        self.saveWindowSuccess = None
        self.saveWindowFail = None
        self.resize(700, 700)
        self.setFixedSize(700, 700)
        self.setWindowTitle("D&D Character Tool")

        # Font
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(9)

        # First Name Label
        firstNameLabel = QLabel(self)
        firstNameLabel.setText("First Name")
        firstNameLabel.setFont(font)
        firstNameLabel.move(10, 30)

        # First Name Entry
        self.firstNameEntry = QLineEdit(self)
        self.firstNameEntry.setFixedWidth(220)
        self.firstNameEntry.setPlaceholderText("Enter First Name here...")
        self.firstNameEntry.move(75, 25)
        self.firstNameEntry.setFocus()

        # Last Name Label
        lastNameLabel = QLabel(self)
        lastNameLabel.setText("Last Name")
        lastNameLabel.setFont(font)
        lastNameLabel.move(10, 55)

        # Last Name Entry
        self.firstNameEntry = QLineEdit(self)
        self.firstNameEntry.setFixedWidth(220)
        self.firstNameEntry.setPlaceholderText("Enter Last Name here...")
        self.firstNameEntry.move(75, 50)



        # Service Label
        serviceLabel = QLabel(self)
        serviceLabel.setText("Class")
        serviceLabel.setFont(font)
        serviceLabel.move(10, 80)

        # Class List Combo
        self.classListChosen = []
        classList = []
        self.classCombo = QListWidget(self)
        self.classCombo.setFixedWidth(220)
        self.classCombo.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.classCombo.resize(200, 70)
        for i in class_list:
            self.classCombo.addItem(i)
        self.classCombo.move(75, 80)

        # Max Records Label
        maxRecordsLabel = QLabel(self)
        maxRecordsLabel.setText("Max Records")
        maxRecordsLabel.setFont(font)
        maxRecordsLabel.move(350, 60)

        # Max Records Entry
        self.maxRecordsEntry = QLineEdit(self)
        self.maxRecordsEntry.setFixedWidth(220)
        self.maxRecordsEntry.setPlaceholderText("Enter max number of records here..")
        self.maxRecordsEntry.setText("10")
        self.maxRecordsEntry.move(435, 55)

        # Status Label
        self.statusLabel = QLabel(self)
        self.statusLabel.setText("Log Status")
        self.statusLabel.setFont(font)
        self.statusLabel.move(350, 90)

        # Status Combo
        self.statusChosen = []
        self.statusCombo = QListWidget(self)
        self.statusCombo.setFixedWidth(220)
        self.statusCombo.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.statusCombo.resize(100, 70)
        self.statusCombo.addItem("info")
        self.statusCombo.addItem("warn")
        self.statusCombo.addItem("error")
        self.statusCombo.addItem("debug")
        self.statusCombo.move(435, 90)

        # Query Checkbox
        self.queryCheck = QCheckBox(self)
        self.queryCheck.setText("Query")
        self.queryCheck.move(8, 210)

        # Disable Query Box

        # Query Multi-line
        self.queryEntry = QTextEdit(self)
        self.queryEntry.setFixedWidth(580)
        self.queryEntry.setFixedHeight(50)
        self.queryEntry.setDisabled(True)
        self.queryEntry.move(75, 210)

        # Environment Label
        envLabel = QLabel(self)
        envLabel.setText("Environment")
        envLabel.setFont(font)
        envLabel.move(350, 30)

        # Environment Combo Box
        self.envCombo = QComboBox(self)
        self.envCombo.setFixedWidth(232)
        self.envCombo.addItem("staging")
        self.envCombo.addItem("production")
        self.envCombo.addItem("dev")
        self.envCombo.move(430, 20)

        # Results Label
        self.resultsLabel = QLabel(self)
        self.resultsLabel.setText("Results")
        self.resultsLabel.setFont(font)
        self.resultsLabel.move(10, 270)

        # Results Table
        self.resultTable = QTableWidget(self)
        self.resultTable.move(75, 270)
        self.resultTable.resize(580, 350)
        self.resultTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # Submit Button
        submitButton = QPushButton(self)
        submitButton.setText("Submit Query")
        submitButton.move(420, 655)

        self.exportButton = QPushButton(self)
        self.exportButton.setText("Export to Txt")
        self.exportButton.setDisabled(True)
        self.exportButton.clicked.connect(lambda: self.export_to_txt())
        self.exportButton.move(547, 655)

        # Next Button
        self.nextButton = QPushButton(self)
        self.nextButton.setText("Next")
        self.nextButton.move(595, 620)
        self.nextButton.clicked.connect(lambda: self.submit_query())

        

        # Lat Long Label
        # self.latLongLabel = QLabel(self)
        # self.latLongLabel.setFont(font)
        # self.latLongLabel.setText("Lat/Long Table")
        # self.latLongLabel.move(10, 550)

        # Lat Long ComboBox
        # self.latLongCombo = QComboBox(self)
        # self.latLongCombo.addItem("Lat/Long in JSON")
        # self.latLongCombo.addItem("Comma Separated Or-Bar")
        # self.latLongCombo.move(100, 540)

        # Lat Long  Table
        # self.latLongTable = QTableWidget(self)
        # self.latLongTable.resize(740, 200)
        # self.latLongTable.move(10, 575)




 



   


def main():
    app = QApplication(sys.argv)
    ex = DataDogGUILogWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
