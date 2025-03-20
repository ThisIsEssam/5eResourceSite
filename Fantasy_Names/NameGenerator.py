import Fantasy_Names
import Fantasy_Names.human_diverse
import random

def get_random_name(ran_lin):
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
        elif ran_lin.lower() == "warforged":
            name = Fantasy_Names.warforged()
        
        hero_first_name = name.split(" ")[0]
        hero_last_name = name.split(" ")[1]
        
        return hero_first_name, hero_last_name