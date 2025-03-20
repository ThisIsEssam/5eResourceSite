#!/usr/bin/env python
import datetime
import json
import os
from pathlib import Path
import random
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytz
import requests
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QMovie
from Backend.NPC_Class.Hero import Hero
from Backend.NPC_Class.Commoner import Commoner
from Backend.API import getResource
from Backend.LLM.LLM_Worker import LLMWorker
import Fantasy_Names.human_diverse
from Backend.LLM.LLM_Class import get_llm_response  
from Fantasy_Names.NameGenerator import get_random_name


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


class NPCCreatorWindow(QWidget):
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
 
        super(NPCCreatorWindow, self).__init__(parent)
        self.saveWindowSuccess = None
        self.saveWindowFail = None
        self.resize(700, 700)
        self.setFixedSize(700, 650)
        self.setWindowTitle("D&D Character Tool")

        # Font
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(9)

        # Hero Checkbox
        self.heroCheck = QCheckBox(self)
        self.heroCheck.setText("Hero")
        self.heroCheck.move(350, 25)
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

        self.firstNameLock = QCheckBox(self)
        self.firstNameLock.move(300, 55)
        self.firstNameLock.setChecked(True)

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
        
        self.lastNameLock = QCheckBox(self)
        self.lastNameLock.move(300, 82)
        self.lastNameLock.setChecked(True)


        # lineage Label
        self.lineageLabel = QLabel(self)
        self.lineageLabel.setText("Lineage")
        self.lineageLabel.setFont(font)
        self.lineageLabel.move(10, 112)

        self.lineageLock = QCheckBox(self)
        self.lineageLock.move(300, 110)
        self.lineageLock.setChecked(True)

        # lineage Combo
        self.lineageCombo = QComboBox(self)
        self.lineageCombo.resize(90, 22)
        for i in lineage_list:
            self.lineageCombo.addItem(i)
        self.lineageCombo.addItem("Warforged")
        self.lineageCombo.move(75, 110)
      

        # Class Label
        classLabel = QLabel(self)
        classLabel.setText("Class")
        classLabel.setFont(font)
        classLabel.move(350, 60)

        self.classLock = QCheckBox(self)
        self.classLock.move(570, 55)
        self.classLock.setChecked(True)
        self.classLock.setDisabled(True)

  

        # Class List Combo
        self.classCombo = QComboBox(self)
        self.classCombo.setFixedWidth(80)
        for i in class_list:
            self.classCombo.addItem(i)
        self.classCombo.move(420, 55)
        self.classCombo.setDisabled(True)

        #Level combo
        self.levelCombo = QComboBox(self)
        for i in range (1, 21):
            self.levelCombo.addItem(str(i))
        self.levelCombo.move(420, 82)
        self.levelCombo.setDisabled(True)

        #Level Label
        self.levelLabel = QLabel(self)
        self.levelLabel.setText("Level")
        self.levelLabel.setFont(font)
        self.levelLabel.move(350, 87)
        
        self.levelLock = QCheckBox(self)
        self.levelLock.move(570, 82)
        self.levelLock.setChecked(True)
        self.levelLock.setDisabled(True)




        #Background combo
        self.backGroundCombo = QComboBox(self)
        backgrounds = getResource.get_backgrounds()
        background_results = backgrounds['results']
        self.backGroundCombo.resize(135, 22)
        background_list = []
        for i in background_results:
            background_list.append(i['name'])   
        for i in background_list:
            self.backGroundCombo.addItem(i)
        self.backGroundCombo.move(420, 110)
        self.backGroundCombo.setDisabled(True)

        self.backgroundLock = QCheckBox(self)
        self.backgroundLock.move(570, 110)
        self.backgroundLock.setChecked(True)
        self.backgroundLock.setDisabled(True)
        


        #background label
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setText("Background")
        self.backgroundLabel.setFont(font)
        self.backgroundLabel.move(350, 115)


        #Generate NPC Button
        self.generateButton = QPushButton(self)
        self.generateButton.setText("Generate NPC")
        self.generateButton.move(10, 155)
        self.generateButton.clicked.connect(self.generateNPC)

        #Randomize NPC Button
        self.randomButton = QPushButton(self)
        self.randomButton.setText("Randomize NPC")
        self.randomButton.move(100, 155)
        self.randomButton.clicked.connect(self.randomizeNPC)
    
        self.backgroundLock.clicked.connect(self.lock_element)
        self.levelLock.clicked.connect(self.lock_element)
        self.classLock.clicked.connect(self.lock_element)
        self.lastNameLock.clicked.connect(self.lock_element)
        self.lineageLock.clicked.connect(self.lock_element)
        self.firstNameLock.clicked.connect(self.lock_element)

        self.loadingLabel = QLabel(self)
        loading_gif_path = os.path.join(Path(__file__).parent.parent, "Images", "loading.gif")
        self.loadingMovie = QMovie(loading_gif_path)

        # Set the size of the label to match the GIF size
        self.loadingMovie.start()
        gif_size = self.loadingMovie.currentPixmap().size()
        self.loadingLabel.setFixedSize(gif_size)
        self.loadingLabel.setMovie(self.loadingMovie)
        self.loadingLabel.setVisible(False)  # Initially hidden

        # Center the loading label
        self.center_loading_label()

        # Connect the resize event to re-center the loading label
        self.resizeEvent = self.on_resize
        

        self.lineEdit = QTextEdit(self)
        self.lineEdit.move(10, 200)
        self.lineEdit.setFixedSize(680 ,400)
        self.lineEdit.setReadOnly(True)

        # Create a mapping between checkboxes and their associated elements
        self.lock_mapping = {
            self.firstNameLock: self.firstNameEntry,
            self.lastNameLock: self.lastNameEntry,
            self.lineageLock: self.lineageCombo,
            self.classLock: self.classCombo,
            self.levelLock: self.levelCombo,
            self.backgroundLock: self.backGroundCombo,
        }

        # Connect all checkboxes to the lock_element method
        for checkbox in self.lock_mapping.keys():
            checkbox.clicked.connect(self.lock_element)
    
    def center_loading_label(self):
       
        x = (self.width() - self.loadingLabel.width()) // 2
        y = (self.height() - self.loadingLabel.height()) // 2
        self.loadingLabel.move(x, y)

    def on_resize(self, event):
        self.center_loading_label()
        super().resizeEvent(event)        

    def exclusive_checkboxes(self):
        if self.heroCheck.isChecked():
            self.classCombo.setDisabled(False)
            self.levelCombo.setDisabled(False)
            self.backGroundCombo.setDisabled(False)
            self.classLock.setDisabled(False)
            self.levelLock.setDisabled(False)
            self.backgroundLock.setDisabled(False)
        if self.heroCheck.isChecked() == False:
            self.classCombo.setDisabled(True)
            self.levelCombo.setDisabled(True)
            self.backGroundCombo.setDisabled(True)
            self.classLock.setDisabled(True)
            self.levelLock.setDisabled(True)
            self.backgroundLock.setDisabled(True)   

    def generateNPC(self):
        first_name = self.firstNameEntry.text()
        last_name = self.lastNameEntry.text()
        level = self.levelCombo.currentText()
        background = self.backGroundCombo.currentText()
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
            "Lineage": new_npc.lineage}
        
        if new_npc.__class__== Hero:
            hero_profile["Class"] = new_npc.class_name
            hero_profile["Level"] = level
            hero_background = {"Background": background, "Description": ""} 
            background_description = getResource.get_backgrounds(background.lower().replace(" ", "-"))
            hero_background["Description"] = background_description['desc']
            hero_profile["Background"] = hero_background
            if new_npc.class_name in ["Wizard", "Sorcerer", "Warlock", "Druid", "Cleric", "Bard", "Ranger", "Paladin"]:
                hero_profile["Spells"] = []
                highest_spell_level = self.highest_spell_slot(new_npc.class_name, int(level))
                if highest_spell_level == 0:
                    hero_profile["Spells"] = []
                spells = getResource.get_class(new_npc.class_name.lower() + "/spells")
                spell_results = spells['results']
                levelled_spells = []
                for i in spell_results:
                    if i['level'] <= highest_spell_level:
                        levelled_spells.append(i)
                spell_list = []
                if levelled_spells:
                    for i in range(0, 3):
                        spell_list.append(random.choice(levelled_spells)['index'])
                for i in spell_list:
                    list_of_spells = {"Name": "", "Description": "", "Level": ""}
                    name = getResource.get_spells(i)['name']
                    description = getResource.get_spells(i)['desc'][0]
                    level = getResource.get_spells(i)['level']
                    list_of_spells["Level"] = level
                    list_of_spells["Name"] = name
                    list_of_spells["Description"] = description
                    hero_profile["Spells"].append(list_of_spells)
        prompt = "Role play in the first person as a D&D "+ new_npc.lineage+" NPC named "+new_npc.first_name+" "+new_npc.last_name+"."
        if new_npc.__class__ == Hero:
           prompt += " You are a level "+ hero_profile["Level"]+" "+hero_profile["Class"]+" with a "+hero_profile["Background"]["Background"]+" background. "+ hero_profile["Background"]["Description"]+" Start with a very brief and unique description of what you look like (no more than 20 words) before going into first-person dialogue (no more than 50-80 words). Add verbal quirks based on your lineage."
        
        self.loadingLabel.raise_()
        self.loadingLabel.setVisible(True)
        self.loadingMovie.start()
        self.worker = LLMWorker(prompt)
        self.worker.finished.connect(self.on_llm_response)
        self.worker.error.connect(self.on_llm_error)
        self.worker.start()
        
    
    def highest_spell_slot(self, character_class, level):
    # Define spell slot progression based on class type
        full_casters = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5,
                        10: 5, 11: 6, 12: 6, 13: 7, 14: 7, 15: 8, 16: 8, 17: 9, 18: 9, 19: 9, 20: 9}
        half_casters = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 3,
                        10: 3, 11: 3, 12: 3, 13: 4, 14: 4, 15: 4, 16: 4, 17: 5, 18: 5, 19: 5, 20: 5}
        third_casters = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2,
                        10: 2, 11: 3, 12: 3, 13: 3, 14: 3, 15: 3, 16: 3, 17: 4, 18: 4, 19: 4, 20: 4}
        warlock_pact_magic = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5,
                            10: 5, 11: 5, 12: 5, 13: 5, 14: 5, 15: 5, 16: 5, 17: 5, 18: 5, 19: 5, 20: 5}
        
        # Normalize class name input
        class_type = character_class.lower()
        
        if class_type in ["wizard", "sorcerer", "cleric", "druid", "bard"]:
            return full_casters.get(level, 0)
        elif class_type in ["paladin", "ranger", "artificer"]:
            return half_casters.get(level, 0)
        elif class_type in ["eldritch knight", "arcane trickster"]:
            return third_casters.get(level, 0)
        elif class_type == "warlock":
            return warlock_pact_magic.get(level, 0)
        else:
            raise ValueError("Invalid class name. Please enter a valid spellcasting class.")
                
    
    def check_list(self, item, list):
        if item not in list:
            list.append(item)
        elif item in list:
            list.remove(item)
    
    def on_llm_response(self, response):
    # Hide the loading indicator
        self.loadingMovie.stop()
        self.loadingLabel.setVisible(False)

    # Display the response in the QTextEdit widget
        self.lineEdit.setPlainText(response)

    def on_llm_error(self, error_message):
    # Hide the loading indicator
        self.loadingMovie.stop()
        self.loadingLabel.setVisible(False)

    # Display the error message
        self.lineEdit.setPlainText(f"Error: {error_message}")
    
    def randomizeNPC(self):
       if self.heroCheck.isChecked():
           if self.classCombo.isEnabled():
            self.classCombo.setCurrentIndex(random.randint(0, self.classCombo.count() - 1))
           if self.levelCombo.isEnabled():
            self.levelCombo.setCurrentIndex(random.randint(0, self.levelCombo.count() - 1))
           if self.backGroundCombo.isEnabled():
            self.backGroundCombo.setCurrentIndex(random.randint(0, self.backGroundCombo.count() - 1))
       if self.lineageCombo.isEnabled():
        self.lineageCombo.setCurrentIndex(random.randint(0, self.lineageCombo.count() - 1))
       lineage = self.lineageCombo.currentText()
       first_name, last_name = get_random_name(lineage)
       if self.firstNameEntry.isEnabled():
        self.firstNameEntry.setText(first_name)
       if self.lastNameEntry.isEnabled():
        self.lastNameEntry.setText(last_name)    
       
    
    def lock_element(self):
        # Iterate through the mapping and enable/disable elements based on the checkbox state
        for checkbox, element in self.lock_mapping.items():
            if checkbox in [self.classLock, self.levelLock, self.backgroundLock]:
                # Only update class, level, and background if the hero checkbox is enabled
                element.setEnabled(self.heroCheck.isChecked() and checkbox.isChecked())
            else:
                element.setEnabled(checkbox.isChecked())
       
     


def main():
    app = QApplication(sys.argv)
    ex = NPCCreatorWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
