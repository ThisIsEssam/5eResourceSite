import random
from pprint import pprint

from Backend.NPC_Class.Hero import Hero
from Backend.API.APIHelper import ApiHelper
from Backend.API import getResource
import Fantasy_Names
import Fantasy_Names.human_diverse


classes = getResource.get_class()
lineages = getResource.get_lineage()

class_results = classes['results']
lineage_results = lineages['results']

class_list =[]
print(class_list)
lineage_list = []

for i in class_results:
    class_list.append(i['name'])

for i in lineage_results:
    lineage_list.append(i['name'])




new_team = []

for i in range(0,5):
    ran_class = random.choice(class_list)
    ran_lin = random.choice(lineage_list)
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

    first_name = name.split(" ")[0]
    last_name = name.split(" ")[1]

    new_hero = Hero(first_name, last_name, ran_lin, ran_class)

    hero_profile = {"First Name: ": new_hero.first_name,
                    "Last Name: ": new_hero.last_name,
                    "Class: ": new_hero.class_name,
                    "Lineage: ": new_hero.race}

    new_team.append(hero_profile)

pprint(new_team)

