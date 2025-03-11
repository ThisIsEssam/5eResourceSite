import random
from pprint import pprint

from Backend.NPC_Class.Hero import Hero
from Backend.NPC_Class.Commoner import Commoner
from Backend.API.APIHelper import ApiHelper
from Backend.API import getResource
import Fantasy_Names
import Fantasy_Names.human_diverse

# Fetch classes, lineages, and spells
classes = getResource.get_class()
lineages = getResource.get_lineage()
spells = getResource.get_spells()

class_results = classes['results']
lineage_results = lineages['results']
spell_results = spells['results']

class_list = []
lineage_list = []
spell_list = []

for i in class_results:
    class_list.append(i['name'])

for i in lineage_results:
    lineage_list.append(i['name'])

for i in spell_results:
    spell_list.append(i['name'])

heroes = []
commoners = []

for i in range(0, 1):
    ran_class = random.choice(class_list)
    ran_lin = random.choice(lineage_list)
    ran_spells = random.sample(spell_list, 3)  # Select 3 random spells for each hero

    if ran_lin.lower() == "dwarf":
        name = Fantasy_Names.dwarf()
    elif ran_lin.lower() == "dragonborn":
        name = Fantasy_Names.dragonborn()
    elif ran_lin.lower() == "elf":
        name = Fantasy_Names.elf()
    elif ran_lin.lower() == "gnome":
        name = Fantasy_Names.gnome()
    elif ran_lin.lower() == "half-elf":
        first_names = Fantasy_Names.human().split(" ")
        last_names = Fantasy_Names.elf().split(" ")
        name = random.choice(first_names) + " " + random.choice(last_names)
    elif ran_lin.lower() == "half-orc":
        first_names = Fantasy_Names.human().split(" ")
        last_names = Fantasy_Names.orc().split(" ")
        name = random.choice(first_names) + " " + random.choice(last_names)
    elif ran_lin.lower() == "orc":
        name = Fantasy_Names.orc()
    elif ran_lin.lower() == "halfling":
        name = Fantasy_Names.hobbit()
    elif ran_lin.lower() == "human":
        name = Fantasy_Names.human_diverse.human()
    elif ran_lin.lower() == "tiefling":
        name = Fantasy_Names.tiefling()

    hero_first_name = name.split(" ")[0]
    hero_last_name = name.split(" ")[1]

    new_hero = Hero(hero_first_name, hero_last_name, ran_lin, ran_class)
    if new_hero.class_name in ["Wizard", "Sorcerer", "Warlock", "Druid", "Cleric", "Bard", "Ranger", "Paladin"]:
        hero_profile = {
            "Name": new_hero.first_name + " " + new_hero.last_name,
            "Class: ": new_hero.class_name,
            "Lineage: ": new_hero.race,
            "Spells: ": ran_spells
        }
    else:
        hero_profile = {
            "Name": new_hero.first_name + " " + new_hero.last_name,
            "Class: ": new_hero.class_name,
            "Lineage: ": new_hero.race,
            "Spells: ": []
        }
        
    heroes.append(hero_profile)


    # Generate random name and race for commoner
    ran_commoner_lin = random.choice(lineage_list)
    if ran_commoner_lin.lower() == "dwarf":
        commoner_name = Fantasy_Names.dwarf()
    elif ran_commoner_lin.lower() == "dragonborn":
        commoner_name = Fantasy_Names.dragonborn()
    elif ran_commoner_lin.lower() == "elf":
        commoner_name = Fantasy_Names.elf()
    elif ran_commoner_lin.lower() == "gnome":
        commoner_name = Fantasy_Names.gnome()
    elif ran_commoner_lin.lower() == "half-elf":
        first_names = Fantasy_Names.human().split(" ")
        last_names = Fantasy_Names.elf().split(" ")
        commoner_name = random.choice(first_names) + " " + random.choice(last_names)
    elif ran_commoner_lin.lower() == "half-orc":
        first_names = Fantasy_Names.human().split(" ")
        last_names = Fantasy_Names.orc().split(" ")
        commoner_name = random.choice(first_names) + " " + random.choice(last_names)
    elif ran_commoner_lin.lower() == "orc":
        commoner_name = Fantasy_Names.orc()
    elif ran_commoner_lin.lower() == "halfling":
        commoner_name = Fantasy_Names.hobbit()
    elif ran_commoner_lin.lower() == "human":
        commoner_name = Fantasy_Names.human_diverse.human()
    elif ran_commoner_lin.lower() == "tiefling":
        commoner_name = Fantasy_Names.tiefling()

    commoner_first_name = commoner_name.split(" ")[0]
    commoner_last_name = commoner_name.split(" ")[1]

    new_commoner = Commoner(commoner_first_name, commoner_last_name, ran_commoner_lin)

    
    
    commoner_profile = {
        "Name": new_commoner.first_name + " " + new_commoner.last_name,
        "Race: ": new_commoner.race
    }

    
    commoners.append(commoner_profile)

print("Heroes:")
pprint(heroes)

print("\nCommoners:")
pprint(commoners)