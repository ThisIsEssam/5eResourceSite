#!/usr/bin/env python
import datetime
import json
import os
import pprint
import random
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


class ErrorNameSave(QWidget):
    def __init__(self, parent=None):
        super(ErrorNameSave, self).__init__(parent)
        self.resize(200, 200)
        self.setWindowTitle("Save Failed")
        layout = QVBoxLayout()
        self.label = QLabel("Please pick a lineage.")
        layout.addWidget(self.label)
        self.setLayout(layout)


class DataDogGUIFailSaveWindow(QWidget):
    def __init__(self, parent=None):
        super(DataDogGUIFailSaveWindow, self).__init__(parent)
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

        # Hero Checkbox
        self.heroCheck = QCheckBox(self)
        self.heroCheck.setText("Hero")
        self.heroCheck.move(8, 20)
        self.heroCheck.clicked.connect(self.exclusive_checkboxes)

        # First Name Label
        firstNameLabel = QLabel(self)
        firstNameLabel.setText("First Name")
        firstNameLabel.setFont(font)
        firstNameLabel.move(10, 60)

        # First Name Entry
        self.firstNameEntry = QLineEdit(self)
        self.firstNameEntry.setFixedWidth(220)
        self.firstNameEntry.setPlaceholderText("Enter First Name here...")
        self.firstNameEntry.move(75, 55)
        self.firstNameEntry.setFocus()

        # Last Name Label
        lastNameLabel = QLabel(self)
        lastNameLabel.setText("Last Name")
        lastNameLabel.setFont(font)
        lastNameLabel.move(10, 87)

        # Last Name Entry
        self.lastNameEntry = QLineEdit(self)
        self.lastNameEntry.setFixedWidth(220)
        self.lastNameEntry.setPlaceholderText("Enter Last Name here...")
        self.lastNameEntry.move(75, 82)


        # lineage Label
        self.lineageLabel = QLabel(self)
        self.lineageLabel.setText("Lineage")
        self.lineageLabel.setFont(font)
        self.lineageLabel.move(10, 112)

        # lineage Combo
        self.lineageCombo = QComboBox(self)
        self.lineageCombo.resize(90, 20)
        for i in lineage_list:
            self.lineageCombo.addItem(i)
        self.lineageCombo.move(75, 110)
      

        # Class Label
        classLabel = QLabel(self)
        classLabel.setText("Class")
        classLabel.setFont(font)
        classLabel.move(350, 60)
  

        # Class List Combo
        self.classCombo = QComboBox(self)
        self.classCombo.setFixedWidth(80)
        for i in class_list:
            self.classCombo.addItem(i)
        self.classCombo.move(390, 55)
        self.classCombo.setDisabled(True)

        #Generate NPC Button
        self.generateButton = QPushButton(self)
        self.generateButton.setText("Generate NPC")
        self.generateButton.move(10, 200)
        self.generateButton.clicked.connect(self.generateNPC)

        
    def exclusive_checkboxes(self):
        if self.heroCheck.isChecked():
            self.classCombo.setDisabled(False)
        if self.heroCheck.isChecked() == False:
            self.classCombo.setDisabled(True)

    def generateNPC(self):
        first_name = self.firstNameEntry.text()
        last_name = self.lastNameEntry.text()
        if first_name == "" or last_name == "":
            self.firstNameEntry.setPlaceholderText("Error! Please enter a valid first name.")
            self.lastNameEntry.setPlaceholderText("Error! Please enter a valid last name.")
            return
        lineage = self.lineageCombo.currentText()
        if self.heroCheck.isChecked():
            class_name = self.classCombo.currentText()
            new_npc = Hero(first_name, last_name, lineage, class_name)
        else:
            new_npc = Commoner(first_name, last_name, lineage)
        
        hero_profile = {
            "Name": new_npc.first_name + " " + new_npc.last_name,
            "Lineage: ": new_npc.lineage}
        
        if new_npc.__class__ == Hero:
            hero_profile["Class"] = new_npc.class_name
            if new_npc.class_name in ["Wizard", "Sorcerer", "Warlock", "Druid", "Cleric", "Bard", "Ranger", "Paladin"]:
                spells = getResource.get_spells()
                spell_results = spells['results']
                spell_list = []
                for i in spell_results:
                    spell_list.append(i['index'])
                ran_spells = random.sample(spell_list, 3)
                list_of_spells = {}
                for i in ran_spells:
                    name = getResource.get_spells(i)['name']
                    description = getResource.get_spells(i)['desc']
                    list_of_spells["Name"] = name
                    list_of_spells["Description"] = description
                hero_profile["Spells"] = list_of_spells

        pprint.pprint(hero_profile)
    
            
        
    def check_list(self, item, list):
        if item not in list:
            list.append(item)
        elif item in list:
            list.remove(item)
    
    
   

def main():
    app = QApplication(sys.argv)
    ex = DataDogGUILogWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
